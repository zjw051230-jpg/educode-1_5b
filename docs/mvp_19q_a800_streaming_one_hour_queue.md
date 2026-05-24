# MVP-19.Q A800 Streaming One-Hour Queue

## 1. Purpose

MVP-19.Q prepares the next A800/A100 one-hour session so the rented GPU time does not sit idle after the primary run finishes.

This is queue preparation only. It does not run training, enter A100/A800, download data, train tokenizer/model artifacts, modify model architecture, or commit checkpoints, raw corpus files, processed data, split files, or result tarballs.

## 2. Queue

Primary:

- MVP-19 streaming 3000-step public16k run.

Follow-up if time remains:

- MVP-20.S streaming 5000-step public16k run.

The 5000-step run is optional and must not start unless the primary 3000-step run passes the execution conditions below.

## 3. Execution Conditions

Run the 3000-step job first.

Run the 5000-step follow-up only if all conditions are true:

- 3000-step `success=true`;
- `checkpoint_reload_match=true`;
- post-run artifact validation passed;
- no OOM occurred;
- no non-finite loss occurred;
- remaining rental/session time is at least `30` minutes.

## 4. Do Not Run 5000-step If

Do not run the 5000-step follow-up if any of these occur:

- the 3000-step run fails;
- validation fails;
- `checkpoint_reload_match=false`;
- remaining time is insufficient;
- GPU or host behavior is unstable;
- readiness reports blockers;
- the prepared data package layout does not match the config;
- the run would require Hugging Face fetch on the GPU host.

## 5. Resource

Recommended resources:

- 1 x A800/A100 40GB-class GPU;
- container/host RAM `>=48GiB`;
- disk `>=50GB` available;
- prepared data uploaded from local/CPU-side package;
- no Hugging Face fetch on the GPU host.

The queue remains bounded training-systems validation. It is not a model-quality claim.

## 6. Copyback Policy

For each run, download only the small result package containing:

- `summary.json`;
- `summary.md`;
- `metrics.jsonl`;
- `validation_metrics.jsonl`;
- `run_config.json`;
- `run_metadata.json`;
- `post_run_artifact_validation_summary.json`.

Do not download:

- checkpoint files;
- raw corpus files;
- processed corpus files;
- split files;
- prepared data packages.

## 7. Queue Commands Summary

Primary config:

```text
configs/a100/fineweb_edu_500mb_300m_3000step_public16k_execute.json
```

Follow-up config:

```text
configs/a100/fineweb_edu_500mb_300m_5000step_public16k_execute.json
```

Both configs use:

- `data_loading_mode=streaming`;
- `batch_size=8`;
- `gradient_accumulation_steps=4`;
- `sequence_length=512`;
- `tokenizer_vocab_size=16384`;
- prepared 500MB train/validation splits.

## 8. Local Follow-up

After the future GPU session, import and validate the result packages separately:

- MVP-19.R for the 3000-step package;
- MVP-20.S.R for the 5000-step package if the follow-up ran.

Keep result tarballs local-only unless a later step explicitly changes the artifact policy.
