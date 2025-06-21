import json
import re
import logging
from difflib import SequenceMatcher

# Set up logging to append to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('q2/run.log', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_knowledge_base():
    """Load the knowledge base from kb.json"""
    with open('q2/kb.json', 'r') as f:
        return json.load(f)

def normalize_text(text):
    """Normalize text for comparison (lowercase, remove extra spaces, punctuation)"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove common punctuation that might affect matching
    text = re.sub(r'[.,!?;:]', '', text)
    
    return text

def string_similarity(str1, str2):
    """Calculate similarity between two strings using SequenceMatcher"""
    return SequenceMatcher(None, str1, str2).ratio()

def find_kb_answer(question, kb_data):
    """Find the corresponding answer in the knowledge base"""
    normalized_question = normalize_text(question)
    
    for item in kb_data['knowledge_base']:
        if normalize_text(item['question']) == normalized_question:
            return item['answer']
    
    return None

def validate_response(question, response, kb_data, similarity_threshold=0.8):
    """Validate a response against the knowledge base"""
    
    # Check if question exists in KB
    kb_answer = find_kb_answer(question, kb_data)
    
    if kb_answer is None:
        # Question not in KB - out of domain
        return {
            "status": "RETRY",
            "reason": "out-of-domain",
            "message": "RETRY: out-of-domain",
            "kb_answer": None,
            "model_response": response,
            "similarity": None
        }
    
    # Question is in KB - check if answer matches
    normalized_response = normalize_text(response)
    normalized_kb_answer = normalize_text(kb_answer)
    
    # Calculate similarity
    similarity = string_similarity(normalized_response, normalized_kb_answer)
    
    if similarity >= similarity_threshold:
        # Answer matches KB
        return {
            "status": "OK",
            "reason": "matches-kb",
            "message": "OK: answer matches KB",
            "kb_answer": kb_answer,
            "model_response": response,
            "similarity": similarity
        }
    else:
        # Answer differs from KB - potential hallucination
        return {
            "status": "RETRY",
            "reason": "answer-differs",
            "message": "RETRY: answer differs from KB",
            "kb_answer": kb_answer,
            "model_response": response,
            "similarity": similarity
        }

def validate_all_responses():
    """Validate all responses in model_responses.json"""
    
    # Load data
    kb_data = load_knowledge_base()
    
    try:
        with open('q2/model_responses.json', 'r') as f:
            responses = json.load(f)
    except FileNotFoundError:
        logger.error("model_responses.json not found. Run ask_model.py first.")
        return []
    
    # Validate each response
    validation_results = []
    
    for response_data in responses:
        question = response_data['question']
        response = response_data['response']
        question_id = response_data['question_id']
        is_kb_question = response_data['is_kb_question']
        
        logger.info(f"Validating question {question_id}: {question}")
        
        validation_result = validate_response(question, response, kb_data)
        validation_result['question_id'] = question_id
        validation_result['question'] = question
        validation_result['is_kb_question'] = is_kb_question
        
        validation_results.append(validation_result)
        
        logger.info(f"Result: {validation_result['message']}")
        if validation_result['kb_answer']:
            logger.info(f"KB Answer: {validation_result['kb_answer']}")
        logger.info(f"Model Response: {validation_result['model_response']}")
        if validation_result['similarity']:
            logger.info(f"Similarity: {validation_result['similarity']:.3f}")
        logger.info("-" * 50)
    
    # Save validation results
    with open('q2/validation_results.json', 'w') as f:
        json.dump(validation_results, f, indent=2)
    
    logger.info("Validation results saved to q2/validation_results.json")
    return validation_results

def generate_summary(validation_results):
    """Generate a summary of validation results"""
    
    total_questions = len(validation_results)
    kb_questions = sum(1 for r in validation_results if r['is_kb_question'])
    edge_questions = total_questions - kb_questions
    
    # Count by status
    ok_count = sum(1 for r in validation_results if r['status'] == 'OK')
    retry_count = sum(1 for r in validation_results if r['status'] == 'RETRY')
    
    # Count by reason
    out_of_domain = sum(1 for r in validation_results if r['reason'] == 'out-of-domain')
    answer_differs = sum(1 for r in validation_results if r['reason'] == 'answer-differs')
    matches_kb = sum(1 for r in validation_results if r['reason'] == 'matches-kb')
    
    # Calculate average similarity for KB questions
    kb_similarities = [r['similarity'] for r in validation_results if r['is_kb_question'] and r['similarity'] is not None]
    avg_similarity = sum(kb_similarities) / len(kb_similarities) if kb_similarities else 0
    
    summary = {
        "total_questions": total_questions,
        "kb_questions": kb_questions,
        "edge_questions": edge_questions,
        "ok_responses": ok_count,
        "retry_responses": retry_count,
        "out_of_domain": out_of_domain,
        "answer_differs": answer_differs,
        "matches_kb": matches_kb,
        "average_similarity_kb": round(avg_similarity, 3),
        "hallucination_rate": round(retry_count / total_questions * 100, 2)
    }
    
    return summary

if __name__ == "__main__":
    logger.info("Starting validation process")
    
    validation_results = validate_all_responses()
    
    if validation_results:
        summary = generate_summary(validation_results)
        
        logger.info("=== VALIDATION SUMMARY ===")
        logger.info(f"Total questions: {summary['total_questions']}")
        logger.info(f"KB questions: {summary['kb_questions']}")
        logger.info(f"Edge questions: {summary['edge_questions']}")
        logger.info(f"OK responses: {summary['ok_responses']}")
        logger.info(f"RETRY responses: {summary['retry_responses']}")
        logger.info(f"Out of domain: {summary['out_of_domain']}")
        logger.info(f"Answer differs: {summary['answer_differs']}")
        logger.info(f"Matches KB: {summary['matches_kb']}")
        logger.info(f"Average similarity (KB): {summary['average_similarity_kb']}")
        logger.info(f"Hallucination rate: {summary['hallucination_rate']}%")
        
        # Save summary
        with open('q2/validation_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info("Summary saved to q2/validation_summary.json") 