import json
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

# Set up logging to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('q2/run.log', mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_knowledge_base():
    """Load the knowledge base from kb.json"""
    with open('q2/kb.json', 'r') as f:
        return json.load(f)

def get_questions():
    """Get all questions: 10 from KB + 5 edge cases"""
    kb_data = load_knowledge_base()
    kb_questions = [item['question'] for item in kb_data['knowledge_base']]
    
    # 5 additional edge-case questions
    edge_questions = [
        "What is the capital of Atlantis?",
        "How many moons does planet X-47 have?",
        "What is the favorite color of unicorns?",
        "What year will humans first contact aliens?",
        "What is the molecular formula of dragon breath?"
    ]
    
    return kb_questions + edge_questions

def setup_model():
    """Setup a smaller language model for text generation"""
    try:
        # Use a smaller model that works well on most machines
        model_name = "microsoft/DialoGPT-medium"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        # Add padding token if not present
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        return tokenizer, model
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None, None

def ask_model(question, tokenizer, model, max_length=100):
    """Ask a question to the model and get response"""
    try:
        # Format the question for the model
        input_text = f"Question: {question}\nAnswer:"
        
        # Tokenize input
        inputs = tokenizer.encode(input_text, return_tensors='pt', truncation=True, max_length=512)
        
        # Generate response
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode response
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the answer part (after "Answer:")
        if "Answer:" in response:
            answer = response.split("Answer:")[-1].strip()
        else:
            answer = response.strip()
            
        return answer
        
    except Exception as e:
        logger.error(f"Error asking question '{question}': {e}")
        return f"Error: {str(e)}"

def main():
    """Main function to run the question-asking process"""
    logger.info("Starting hallucination detection system")
    
    # Load questions
    questions = get_questions()
    logger.info(f"Loaded {len(questions)} questions (10 KB + 5 edge cases)")
    
    # Setup model
    logger.info("Setting up language model...")
    tokenizer, model = setup_model()
    
    if tokenizer is None or model is None:
        logger.error("Failed to setup model. Exiting.")
        return
    
    # Ask questions and collect responses
    responses = []
    
    for i, question in enumerate(questions, 1):
        logger.info(f"Question {i}/{len(questions)}: {question}")
        
        response = ask_model(question, tokenizer, model)
        logger.info(f"Response: {response}")
        
        responses.append({
            "question_id": i,
            "question": question,
            "response": response,
            "is_kb_question": i <= 10  # First 10 are KB questions
        })
        
        logger.info("-" * 50)
    
    # Save responses
    with open('q2/model_responses.json', 'w') as f:
        json.dump(responses, f, indent=2)
    
    logger.info("All responses saved to q2/model_responses.json")

if __name__ == "__main__":
    main() 