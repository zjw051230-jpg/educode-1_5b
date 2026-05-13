# Split Policy

- Default split: 90% train / 10% validation.
- Prefer document-level split.
- Keep validation set fixed once created.
- Record split seed.
- Avoid train/validation leakage.
- Do not use validation-only documents to tune tokenizer if avoidable.
- For tiny early experiments, if corpus is too small, explicitly document limitations.
