# Q2: Hallucination Detection System

## Overview
This system detects hallucinations in language model responses by verifying answers against a knowledge base using string matching.

## Setup
The required packages are already installed from Q1. If needed:
```bash
pip install transformers torch
```

## Files
- `kb.json`: Knowledge base with 10 factual Q-A pairs
- `ask_model.py`: Script to ask questions to the language model
- `validator.py`: Script to validate responses against KB
- `run.log`: Execution logs (populated when running scripts)
- `summary.md`: Detailed system explanation
- `README.md`: This file

## Usage

### Step 1: Ask Questions to Model
```bash
python q2/ask_model.py
```
This will:
- Load the knowledge base
- Ask 10 KB questions + 5 edge cases to the model
- Save responses to `model_responses.json`

### Step 2: Validate Responses
```bash
python q2/validator.py
```
This will:
- Compare model responses against KB
- Classify responses as OK or RETRY
- Generate summary statistics
- Save results to `validation_results.json` and `validation_summary.json`

## Validation Logic

### For Knowledge Base Questions:
- **OK**: Answer matches KB (similarity ≥ 0.8)
- **RETRY**: Answer differs from KB (similarity < 0.8)

### For Edge Cases (fictional topics):
- **RETRY**: Always marked as out-of-domain

## Expected Output Files
- `model_responses.json`: Raw model responses
- `validation_results.json`: Detailed validation results
- `validation_summary.json`: Summary statistics with metrics

## Model Used
- **microsoft/DialoGPT-medium**: Smaller model suitable for most machines
- Alternative: Can be modified to use other models in `ask_model.py`

## Notes
- The system uses string similarity (SequenceMatcher) for comparison
- Similarity threshold is set to 0.8 (configurable in validator.py)
- Edge cases test the model's ability to recognize unknown topics
- All logs are saved to console and can be redirected to run.log 