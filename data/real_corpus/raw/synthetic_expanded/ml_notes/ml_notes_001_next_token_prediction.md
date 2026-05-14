# Next Token Prediction

Next token prediction is a simple training goal for a decoder-only language model.
The model reads a prefix and learns to score the next token.
A token can be a byte, subword, or wordpiece depending on the tokenizer.
In this project the current tokenizer path uses BPE artifacts.

Example sequence:
- input tokens: `deep learning uses`
- target next token: `gradients`

Training does not require the model to know a whole sentence at once.
It only needs many local prediction examples.
That is why document count and corpus diversity matter.
A very small corpus can still reduce loss during smoke tests.
A very small corpus cannot support meaningful generalization.

Why this matters for EduCode:
- smoke training can validate tensor shapes and loss flow
- repeated phrases can make loss look good too quickly
- a larger corpus gives more varied next-token targets
- tokenizer quality affects which prediction units exist

A practical warning:
If the corpus is tiny, the model may memorize short patterns.
That is useful for engineering validation.
That is not evidence of broad capability.
