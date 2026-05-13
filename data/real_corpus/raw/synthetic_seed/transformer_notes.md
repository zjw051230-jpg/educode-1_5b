# Decoder-only transformer notes

A decoder-only language model reads tokens from left to right.
Each position can attend to earlier positions but not future positions.
This masking rule turns sequence modeling into next-token prediction.

A small synthetic example:
- input: "machine learning is"
- target: predict the next token
- model output: a probability distribution over the vocabulary

Key ideas:
- token embeddings map ids to vectors
- attention mixes contextual information
- feed-forward layers reshape the representation
- logits are produced before softmax

Why this matters for EduCode:
- it connects math, code, and training behavior
- it gives short technical text for tokenizer and cleaning checks
- it is safe to commit because it is project-authored synthetic content
