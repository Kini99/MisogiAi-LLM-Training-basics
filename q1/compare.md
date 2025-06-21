# Tokenization Comparison

## Sentence
> The cat sat on the mat because it was tired.

---

## BPE (roberta-base)
- **Tokens:** `['The', 'Ġcat', 'Ġsat', 'Ġon', 'Ġthe', 'Ġmat', 'Ġbecause', 'Ġit', 'Ġwas', 'Ġtired', '.']`
- **Token IDs:** `[133, 4758, 4005, 15, 5, 7821, 142, 24, 21, 7428, 4]`
- **Token Count:** 11

## WordPiece (bert-base-uncased)
- **Tokens:** `['the', 'cat', 'sat', 'on', 'the', 'mat', 'because', 'it', 'was', 'tired', '.']`
- **Token IDs:** `[1996, 4937, 2938, 2006, 1996, 13523, 2138, 2009, 2001, 5458, 1012]`
- **Token Count:** 11

## SentencePiece (albert-base-v2)
- **Tokens:** `[' the', ' cat', ' sat', ' on', ' the', ' mat', ' because', ' it', ' was', ' tired', '.']`
- **Token IDs:** `[14, 2008, 847, 27, 14, 4277, 185, 32, 23, 4117, 9]`
- **Token Count:** 11

---

### Why do the splits differ?
> Each tokenization algorithm uses a different approach: BPE merges frequent character pairs, WordPiece splits words into subwords based on frequency, and SentencePiece (Unigram) probabilistically selects subword units. This leads to different splits, especially for rare or compound words. BPE and WordPiece are deterministic and vocabulary-driven, while SentencePiece can handle out-of-vocabulary words more flexibly. The choice of algorithm affects how efficiently the model can represent and process language, impacting both performance and generalization.

---

# Mask & Predict Analysis

The script masked the tokens "cat" and "tired" and used `bert-base-uncased` to predict the replacements.

## Masked Token: "cat"
- **Top Predictions:** `dog`, `cat`, `horse`
- **Plausibility:** All predictions are highly plausible, as "dog" and "horse" are common animals that can sit on a mat, just like a "cat". This shows the model has a good understanding of the context.

## Masked Token: "tired"
- **Top Predictions:** `.` , `;` , `!`
- **Plausibility:** The model overwhelmingly predicted the period `.` with a score of 0.98. This is because the token at that position was the period. The other predictions, a semicolon and an exclamation mark, are also grammatically plausible sentence terminators, but much less likely. This demonstrates the model's strong grasp of sentence structure. 