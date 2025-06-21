# Hallucination Detection System Summary

## Overview
This system detects hallucinations in language model responses by comparing answers against a knowledge base (KB) using string matching.

## Components

### 1. Knowledge Base (`kb.json`)
- Contains 10 factual Q-A pairs covering various topics
- Topics: Geography, Science, History, Literature, Mathematics
- Serves as the ground truth for validation

### 2. Question Set
- **10 KB Questions**: Questions that exist in the knowledge base
- **5 Edge Cases**: Questions about fictional/non-existent topics (e.g., Atlantis, unicorns)
- Total: 15 questions to test the model

### 3. Model Interface (`ask_model.py`)
- Uses `microsoft/DialoGPT-medium` for text generation
- Asks all 15 questions to the model
- Saves responses to `model_responses.json`
- Logs all activities to `run.log`

### 4. Validator (`validator.py`)
- Implements string matching against KB
- Uses similarity threshold (0.8) for matching
- Classifies responses as:
  - **OK**: Answer matches KB
  - **RETRY**: Answer differs from KB or out-of-domain
- Logs validation results to `run.log`

## Validation Logic

### For KB Questions:
- If similarity ≥ 0.8: **OK**
- If similarity < 0.8: **RETRY: answer differs from KB**

### For Edge Cases:
- Always **RETRY: out-of-domain**

## Results Summary

### Overall Statistics:
- **Total Questions**: 15
- **KB Questions**: 10
- **Edge Questions**: 5
- **OK Responses**: 1
- **RETRY Responses**: 14
- **Hallucination Rate**: 93.33%

### Breakdown:
- **Out of Domain**: 5 (all edge cases correctly identified)
- **Answer Differs**: 9 (9 out of 10 KB questions had incorrect answers)
- **Matches KB**: 1
- **Average Similarity (KB)**: 0.212

## Key Findings

### 1. Performance
The model showed a 93.33% hallucination rate. One KB question was answered correctly.

### 2. KB Questions Performance
**Correct Answer (1/10):**
- **Largest ocean**: Model said "The Pacific Ocean" (correct: Pacific Ocean) - Similarity: 0.867

**Incorrect Answers (9/10):**
- **Capital of France**: Model said "The capital of France..." (correct: Paris) - Similarity: 0.154
- **Chemical symbol for gold**: Model said "It's not as easy as that" (correct: Au) - Similarity: 0.077
- **Romeo and Juliet author**: Model said "The bible" (correct: William Shakespeare) - Similarity: 0.214
- **Largest planet**: Model said "The sun" (correct: Jupiter) - Similarity: 0.286
- **WWII end year**: Model gave irrelevant response (correct: 1945) - Similarity: N/A
- **Sun's main component**: Model said "I think it's the same way a lot of things are" (correct: Hydrogen) - Similarity: 0.075
- **Square root of 144**: Model said "A square root of 144" (correct: 12) - Similarity: 0.091
- **Mona Lisa painter**: Model said "Probably the artist was not given a choice" (correct: Leonardo da Vinci) - Similarity: 0.271
- **Water boiling point**: Model said "1.21 joules per second" (correct: 100) - Similarity: 0.083

### 3. Edge Case Detection
All 5 edge cases were correctly identified as out-of-domain:
- Capital of Atlantis
- Moons of planet X-47
- Unicorn's favorite color
- Year of alien contact
- Dragon breath molecular formula

### 4. Similarity Analysis
The average similarity score of 0.212 for KB questions indicates that most of the model's responses were quite different from the expected answers, though one answer (Pacific Ocean) was close enough to be considered correct.

## System Effectiveness

### Strengths:
- Successfully identified all out-of-domain questions
- Provided detailed similarity scores for analysis
- Generated comprehensive validation reports
- Proper logging to `run.log` file
- One correct answer demonstrates the system can work

### Limitations:
- The chosen model (DialoGPT-medium) still struggles with most factual Q&A
- String matching may be too strict for some variations in correct answers
- The model's conversational nature influences its responses

## Files Generated
- `model_responses.json`: Raw model responses
- `validation_results.json`: Detailed validation results
- `validation_summary.json`: Summary statistics
- `run.log`: Complete execution logs from both scripts

## Usage
1. Run `python q2/ask_model.py` to get model responses
2. Run `python q2/validator.py` to validate responses
3. Check generated files for results
4. Review `run.log` for detailed execution logs

## Metrics
- **Hallucination Rate**: 93.33%
- **Average Similarity**: 0.212 (KB questions only)
- **Out-of-Domain Detection**: 100% (5/5 edge cases)
- **Correct Answer Rate**: 10% (1/10 KB questions) 