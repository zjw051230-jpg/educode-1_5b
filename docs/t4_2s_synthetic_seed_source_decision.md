# T4.2S Synthetic Seed Corpus Source Decision

## 1. Purpose
At the current stage, the user does not have an existing local notes/code corpus ready for intake.

To keep the formal data pipeline moving forward, the first approved source is changed to a synthetic educational seed corpus.

This future corpus:
- will be project-generated rather than externally downloaded
- is intended to validate tokenizer behavior, data pipeline flow, train/validation split handling, and small training setup
- must not be described as real internet text or large-scale pretraining data

## 2. Source Decision
Current source decision:
- `source_id`: `source_synthetic_seed_000001`
- `source_category`: `synthetic_examples`
- `approval_status`: `approved_for_training`
- `license_or_ownership`: `project_authored`
- `privacy_risk`: `none`
- `expected_file_types`: `[".md", ".txt", ".py"]`
- `allowed_for_training`: `true`
- `allowed_to_commit`: `true`
- `local_path`: `data/real_corpus/raw/synthetic_seed/`
- `data_added`: `false`
- `external_download`: `false`

## 3. Why Synthetic Seed Corpus
Why this is a good first approved source:
- no external copyright dependency
- no private user data
- easy to commit
- aligned with the EduCode CS/ML/code theme
- useful for validating the data pipeline before a real corpus exists
- can be expanded gradually

## 4. Limitations
Current limitations:
- synthetic seed corpus is not real-world data
- it is not enough to claim real pretraining
- it may be stylistically narrow
- it may overfit templates
- later stages still need permissive real educational or code data

## 5. Planned Content Categories
A later T4.3 step may create:
- transformer explanations
- tokenizer explanations
- next-token prediction notes
- PyTorch training loop notes
- loss/logits/cross-entropy examples
- checkpointing examples
- generation examples
- Python snippets
- algorithm notes
- math-like technical text
- Chinese-English mixed technical notes

## 6. What T4.2S Does Not Do
This step does not:
- create corpus content
- train a tokenizer
- train a model
- write a data pipeline
- download data
- execute `git push`

## 7. Next Step
Recommended next step:
- T4.3: create synthetic seed corpus

T4.3 may create:
- `data/real_corpus/raw/synthetic_seed/README.md`
- several small `.md` / `.txt` / `.py` synthetic examples
- an updated source manifest

T4.3 still does not need to run training.
