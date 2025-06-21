import json
from transformers import AutoTokenizer, pipeline

# Sentence to tokenize
sentence = "The cat sat on the mat because it was tired."

# Tokenizers
bpe_tokenizer = AutoTokenizer.from_pretrained("roberta-base")
wordpiece_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
sentencepiece_tokenizer = AutoTokenizer.from_pretrained("albert-base-v2")

results = {}

# BPE (Roberta)
bpe_tokens = bpe_tokenizer.tokenize(sentence)
bpe_ids = bpe_tokenizer.convert_tokens_to_ids(bpe_tokens)
results['BPE'] = {
    'tokens': bpe_tokens,
    'ids': bpe_ids,
    'count': len(bpe_tokens)
}

# WordPiece (BERT)
wp_tokens = wordpiece_tokenizer.tokenize(sentence)
wp_ids = wordpiece_tokenizer.convert_tokens_to_ids(wp_tokens)
results['WordPiece'] = {
    'tokens': wp_tokens,
    'ids': wp_ids,
    'count': len(wp_tokens)
}

# SentencePiece (ALBERT)
sp_tokens = sentencepiece_tokenizer.tokenize(sentence)
sp_ids = sentencepiece_tokenizer.convert_tokens_to_ids(sp_tokens)
results['SentencePiece'] = {
    'tokens': sp_tokens,
    'ids': sp_ids,
    'count': len(sp_tokens)
}

# Save tokenization results for reporting
with open("q1/tokenization_results.json", "w") as f:
    json.dump(results, f, indent=2)

# Mask & Predict (using BERT)
# Pick two tokens to mask (e.g., 'cat' and 'tired')
wp_mask_token = wordpiece_tokenizer.mask_token
wp_tokens_masked = wp_tokens.copy()
mask_indices = [1, 10]  # 'cat' and 'tired' positions in token list
for idx in mask_indices:
    wp_tokens_masked[idx] = wp_mask_token

# Reconstruct masked sentence
masked_sentence = wordpiece_tokenizer.convert_tokens_to_string(wp_tokens_masked)

# Fill-mask pipeline
fill_mask = pipeline("fill-mask", model="bert-base-uncased")
predictions = []
for i, idx in enumerate(mask_indices):
    # For each mask, replace only that mask in the sentence
    temp_tokens = wp_tokens.copy()
    temp_tokens[idx] = wp_mask_token
    temp_sentence = wordpiece_tokenizer.convert_tokens_to_string(temp_tokens)
    preds = fill_mask(temp_sentence)
    top_preds = [{
        'sequence': p['sequence'],
        'token_str': p['token_str'],
        'score': p['score']
    } for p in preds[:3]]
    predictions.append({
        'masked_index': idx,
        'masked_token': wp_tokens[idx],
        'top_predictions': top_preds
    })

# Save predictions
with open("q1/predictions.json", "w") as f:
    json.dump(predictions, f, indent=2) 