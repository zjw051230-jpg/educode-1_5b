# EduCode-1.5B

A CS336-inspired modular LLM training system, built from scratch and staged from local CUDA smoke tests toward larger-scale dense Transformer experiments.

## Current Status
- Resume MVP is complete.
- Formal training preparation has started.
- Tiny BPE tokenizer artifact created for tokenizer path validation.
- Tiny BPE tokenizer has passed dataset/model/loss integration smoke.
- Tokenizer configs have been split into byte smoke, toy BPE smoke, and formal BPE placeholder.
- Toy BPE tokenizer config path validation is now covered by a dedicated smoke config.
- Formal `educode_bpe_8k` tokenizer artifact has been created from the current synthetic seed corpus.
- The formal BPE config is linked to the observed tokenizer vocab size `1174`.
- BPE processed-data model/loss smoke has passed.
- One-batch train/val validation-loop smoke has passed.
- A bounded 50-step synthetic-seed small training run has completed with periodic validation, checkpoint reload, generation output, and structured logs.
- Expanded synthetic corpus intake and the expanded BPE tokenizer path have been validated on the current 15-document synthetic corpus, with observed tokenizer vocab size `1846`.
- The approved `synthetic_expanded` source has now been expanded to 45 project-authored corpus files across five categories.
- A bounded 50-step expanded BPE small training run has completed with periodic validation, checkpoint reload, and structured logs.
- The approved `mixed_domain_external` processed corpus has been created from the project-authored domain corpus plus the controlled external supplement, with provenance preserved.
- Mixed/domain BPE tokenizer path has been validated on the approved mixed corpus, reaching observed vocab size `8192`.
- Mixed/domain BPE processed-data model/loss smoke has passed on the approved mixed corpus, with `external_general_text` remaining supplement only.
- A bounded 50-step mixed/domain BPE small training run has completed with periodic validation, checkpoint reload, and structured logs.
- A bounded 100-step mixed/domain BPE small training run has completed with periodic validation, checkpoint reload, and structured logs.
- Mixed/domain local training shows overfitting signal; next step is controlled A100 mixed/domain scale validation, not more local step stacking.
- An A100 100M draft config has been created and passes read-only config inspection against the current validator.
- This A100 draft still uses the current observed tokenizer vocab size `1174` from the current `educode_bpe_8k` tokenizer artifact trained on the synthetic seed corpus.
- An A100 first-session command checklist has been prepared for the selected single `A100 80GB` provider path.
- A100 80GB single-GPU smoke path validated up to 2.15B-scale optimizer profiling.
- A local dry-run of the FineWeb-Edu `300M` A100 smoke script now validates config, tokenizer, bounded public-corpus batch formation, and exact parameter counting at `319329280` parameters without entering A100.
- A draft-only corpus worker framework now exists under `data/real_corpus/draft_queue/domain_synthetic_batch_03/` with a 120-topic reservation registry and review-only templates.
- Batch_04 draft aggregation, structural validation, and automated quality review have completed across `6000` review-only files from six worker deliveries.
- Batch_04 passed structural validation and passed quality review with concentrated notes in `CC-2`, `CC-3`, markdown-heavy `CC-5`, and markdown-heavy `CC-6`; the next step is targeted human sampling, not promotion.
- Batch_05 repair-aware draft validation and automated quality review have completed across `600` review-only files, with structural validation clean and concentrated residual notes in `CC-2`, `CC-5`, and `CC-6`.
- Batch_05 targeted sampling review has completed across a `120`-file bounded review pack, yielding `92` strong candidates, `17` keep candidates, and `11` rewrite cases; the result supports a small future promotion-candidate discussion but not promotion in this step.
- An E1 research paper assistant corpus framework now exists with inbox, metadata, derived, draft-queue, and RAG-library boundaries; raw paper files remain source-library only by default and do not enter the formal training corpus in this step.
- E1.R1 aligned the research paper metadata schema, source policy, and paper-to-corpus taxonomy around standardized fields and task names without introducing any real paper data.
- MVP-2 selected FineWeb-Edu `sample-10BT` as the first bounded public corpus source for the A100 MVP without downloading a real slice in this step.
- MVP-3.R hardened the FineWeb-Edu dry-run path and confirmed a tiny preview-only dry-run could succeed without generating `raw.jsonl`.
- MVP-17 added a host-RAM-efficient streaming batch iterator for public16k A800/A100 configs and validated it locally with unit tests, memory inspection, streaming data/model/loss smoke, and dry-runs.
- MVP-20 prepared a bounded FineWeb-Edu `sample-10BT` 2GB public corpus slice locally/CPU-side, with raw validation, intake validation, and a local prepared split package for future GPU transfer.
- MVP-21.Q prepared a 2GB public16k 5000-step follow-up config and readiness evidence, completing a 2GB 1000/3000/5000-step local queue for future GPU execution.
- MVP-22.P prepared a bounded FineWeb-Edu `sample-10BT` 5GB public corpus slice locally/CPU-side, with raw validation, intake validation, local prepared split package, and 5GB 1000/3000-step readiness evidence.
- MVP-26.P prepared a Modal backend adapter plan, Modal Volume data policy, runner skeleton, remote runbook, and preflight receipt template for future A100/A100-40GB execution.
- MVP-23.J added seed-controlled `shuffle_buffer` sampling for future prepared-data streaming runs, replacing the prior train-prefix-only sampling caveat for 2GB/5GB execution configs.
- Current result is engineering/scaling validation, not full pretraining.
- After A100 scaling validation, the next bottleneck is permitted corpus scale and tokenizer quality.
- Since no existing local notes are available, the main project backbone remains project-authored synthetic educational data rather than a general external-language backbone.
- The controlled `external_general_text` supplement has been processed and approved for tokenizer retraining plus bounded mixed-corpus experiments only.
- Raw provenance is preserved and `external_general_text` remains separate from `synthetic_expanded`.
- ByteTokenizer remains a legacy smoke/debug tokenizer path.
- Core pipeline validated: config, data, tokenizer, model, loss, optimizer step, checkpoint, generation, logging, and periodic validation.
- Not yet real pretraining, not yet 1.5B, not yet external real dataset.

## Quick Demo
Run either of these commands:

```text
python scripts/run_resume_demo.py
```

or

```text
python scripts/run_50_step_toy_training.py
```

## Current Result

| Metric | Value |
|---|---|
| max_steps | 100 |
| eval_interval | 10 |
| first_train_loss | 9.161793 |
| final_train_loss | 3.796839 |
| final_val_loss | 7.833482 |
| checkpoint reload match | True |
| tokens/sec | 27905.04 |
| generation preview | `N/A for D16.4 (no generation step)` |

## Architecture / Pipeline

`config → tokenizer → dataset → model → loss → optimizer → checkpoint → generation → logging`

Current implementation note:
- the current demo uses toy data and a tiny decoder-only model
- the same modular structure is intended to later support tokenizer, data, scale, and hardware upgrades

## Technical Highlights
- Built a modular decoder-only Transformer training pipeline in PyTorch.
- Implemented config loading and validation, byte-level tokenization, x/y sequence batching, model forward, next-token loss, optimizer step, checkpoint save/load, autoregressive generation, and run logging.
- Validated the end-to-end pipeline on an RTX 4060 Ti with one-step smoke, 10-step minimal loop, and bounded 50-step toy training milestones.
- Validated 100M/300M training smoke and 2.15B-scale optimizer profiling on a single A100 80GB.
- Produced reproducible run artifacts including `run_config.json`, `run_metadata.json`, `metrics.jsonl`, `generation_samples.jsonl`, checkpoint manifest files, and markdown summaries.
- Added guardrails so generated artifacts remain Git-ignored and bounded runs do not silently turn into larger experiments.

## Limitations
- small synthetic data only
- ByteTokenizer remains a legacy smoke/debug path
- expanded BPE observed vocab is `1846`, still far below the target `8192`
- learned position embeddings, not RoPE
- PyTorch SDPA only, not FlashAttention-2
- tiny model only, not 1.5B
- only tiny synthetic validation splits
- no meaningful generation quality
- no B200 experiments yet

## Roadmap
- T1 formal training roadmap
- T2 BPE tokenizer plan
- BPE tokenizer integration
- RoPE integration
- real dataset pipeline
- validation loop
- learning-rate scheduler
- resume training test
- A100 100M profiling
- B200 1.5B pretraining experiment

## Current Direction
- add a reviewable research-paper assistant corpus line that keeps raw papers inbox-only by default while allowing later metadata, RAG, note-taking, and non-replicative derived-artifact workflows
- E line now uses standardized paper metadata fields and standardized paper-to-corpus task names.
- First A100 MVP public corpus selected as FineWeb-Edu sample-10BT bounded slice.
- MVP-7 implemented the A100 FineWeb-Edu 300M 10-step smoke script with local dry-run validation, exact parameter counting, and explicit declared-vs-core feature compatibility reporting.
- A100/A800 MVP training loop validated with 319M model on FineWeb-Edu 50MB public corpus.
- After successful A800 10-step and 100-step runs, the next recommended route is 500MB public corpus expansion, public 16k tokenizer, then a 300M 1000-step bounded run.
- FineWeb-Edu public corpus has been expanded from 50MB to 500MB for public tokenizer and longer 300M training experiments.
- Public 16k tokenizer is now available for 500MB FineWeb-Edu experiments, while mixed-domain 8k remains unchanged.
- MVP-13 selected the public 16k tokenizer as the intended next 300M public-corpus tokenizer, gated by a local public16k data/model/loss smoke before any 1000-step GPU execution.
- Public 16k tokenizer has passed local data/model/loss smoke and is eligible for the next 300M 1000-step bounded run plan.
- Before the next A800 run, logging/path validation has been added for validation_metrics.jsonl, checkpoint_path, run_id, and output_dir correctness.
- Next A800 rental should run public16k 1000-step first, then 3000-step if the first run succeeds and time remains.
- Low-RAM A800 runs completed; next experiments should use 32GB+ host/container RAM or improve streaming batch preparation before larger batch runs.
- MVP-17 implemented host-RAM-efficient streaming batch preparation for the public16k 1000/3000-step A800 configs, with local unit tests, memory inspection, streaming data/model/loss smoke, and dry-runs passing.
- Streaming batch iterator successfully restored `batch_size=8` / `gradient_accumulation_steps=4` A800 training under `48GiB` host RAM.
- Streaming batch iterator is now the baseline for future public16k A800 runs; data should be prepared locally/CPU-side and transferred to GPU hosts.
- Next GPU run should use prepared local/CPU-side data package and run streaming 3000-step without Hugging Face fetch on the GPU host.
- Next GPU session can run streaming 3000-step first, then streaming 5000-step only if 3000-step succeeds and time remains.
- FineWeb-Edu 2GB prepared splits are now available locally for future 300M public16k streaming experiments without Hugging Face fetch on the GPU host.
- 2GB prepared corpus is ready for A800/A100 streaming runs; future GPU hosts should receive prepared data packages and start with 2GB 1000-step before longer runs.
- The 2GB public16k queue now includes 1000/3000/5000-step configs; the next GPU session should still execute them in order and stop on any failed validation.
- FineWeb-Edu 5GB prepared splits are now available locally for future 300M public16k streaming experiments without Hugging Face fetch on the GPU host.
- 5GB public16k 1000/3000-step configs passed local memory inspection, dry-run, and readiness, but should run only after the 2GB queue supports moving up in data scale.
- Modal can be used as an alternate A100/A100-40GB execution backend; prepared data packages should be uploaded to Modal Volume and GPU functions should not fetch Hugging Face data.
- Modal A100 can be used as an alternate execution backend for prepared-data streaming runs; future Modal jobs should keep using Volume prepared packages and avoid Hugging Face fetch on GPU workers.
- Modal A100 backend is validated for 2GB prepared-data streaming runs; next recommended path is scheduler/sampling cleanup or 5GB 1000-step preflight rather than blindly extending 2GB step count.
- Before further longer or larger-corpus training, scheduler behavior and streaming sampling policy should be made explicit to improve run interpretability.
- Fixed learning-rate training is now represented as explicit `scheduler_policy=constant` rather than an accidental scheduler caveat.
- Streaming train data now supports seed-controlled `shuffle_buffer` sampling; future 2GB/5GB runs should use shuffled streaming rather than prefix-only sampling.
- 5GB Modal preflight has passed; `train_5gb_1000` should only run after explicit cost approval and should download only the small result package.
- 5GB prepared-data streaming run on Modal A100 is now validated with `shuffle_buffer` sampling and constant scheduler metadata; future longer 5GB runs require separate cost approval.
- Validation streaming configs now support deterministic multi-document coverage through validation-side `shuffle_buffer` sampling plus a per-document block cap before any longer 5GB run.
- Real 5GB validation coverage preflight now passes without GPU or training, with `validation_unique_doc_count=15` and `validation_prefix_only_risk=false`; next 5GB work should be a 3000-step training plan with cost approval, not a direct 10000-step jump.
- MVP-26.P prepares the 5GB 3000-step Modal A100 training plan and cost gate; `train_5gb_3000` still needs a runner mode before any approved training execution.
- MVP-26.I adds and locally validates the `train_5gb_3000` Modal runner mode; actual Modal A100 training still requires a separate cost gate.
- Modal A100 5GB 3000-step streaming run completed with corrected validation coverage: `final_train_loss=3.029707`, `final_validation_loss=8.341638`, `validation_unique_doc_count=15`, and `validation_prefix_only_risk=false`.
- MVP-27.A analysis finds the 5GB 3000-step run improved both final train loss and corrected validation loss versus 5GB 1000-step; next step is route selection, not a direct 10000-step jump.
- MVP-27.B selects the next route: MVP-28 should prepare SDPA / FlashAttention profiling before longer training, followed by context-length preflight and then a 5000-step-vs-optimizer decision.
- MVP-28.P audits the current attention path: runtime uses causal PyTorch SDPA; FlashAttention is not implemented yet, so the next step is a bounded profiling harness/config plan before any GPU run.
- MVP-28.I prepares a bounded `profile_5gb_50step_sdpa` Modal runner mode and 50-step SDPA profiling config; actual A100 profiling still requires a separate cost gate.
- MVP-18 completed the A800 1000-step public16k streaming run with finite losses, standalone validation metrics, checkpoint reload match, and post-run artifact validation.
- Imported A800 bounded-run results remain training-systems evidence only, with architecture-parity caveats explicit and no model-quality claims.

## Resume Resources
- [Resume Bullets](docs/resume_bullets.md)
- [Resume Project Report](docs/resume_project_report.md)
- [Quickstart](docs/quickstart.md)
- [Reproducibility Checklist](docs/reproducibility_checklist.md)
- [Public Showcase Checklist](docs/public_showcase_checklist.md)

## Current Milestones
- W1 project skeleton
- W2 CUDA environment check
- W3 config schema draft
- W4 smoke test plan
- W5 run logging format
- W6 config validation checklist
- W7 minimal run manifest templates
- W8 experiment index
- W9 Windows 10M smoke preflight checklist
- W10 Windows 10M smoke implementation plan
- W10.1 config loader only
- W10.2 config validator only
- W10.3 run setup only
- W10.4 toy data + ByteTokenizer only
- W10.5 sequence dataset x/y only
- W10.6 tiny model forward only
- W10.7 loss only
- W10.8 backward + optimizer step only
- W10.9 checkpoint save/load only
- W10.10 generation only
- W10.11 logging integration only
- W10.12 one-step smoke run
- W10.13 one-step smoke review
- W11 minimal training loop plan
- W11.1 minimal training loop script
- W11.2 minimal training loop review
- W11.3 bounded 50-step toy training plan
- W11.4 bounded 50-step toy training
- W11.5 bounded 50-step toy training review
- R1 resume MVP pack
- T1 formal training roadmap
- T2 BPE tokenizer plan
- T2.1 tokenizer environment check
- T2.2 tiny BPE tokenizer artifact
- T2.3 BPE tokenizer integration smoke
- T2.4 tokenizer config schema update
- T2.5 tokenizer config migration
- T3 small real dataset plan
- T4 real corpus intake structure
- T4.1 first corpus source decision
- T4.2S synthetic seed corpus source decision
- T4.3 synthetic seed corpus
- T5 real data intake cleaning script plan
- T5.1 synthetic seed intake cleaning script
- T5.2 BPE 8k tokenizer training plan
- T5.3 BPE 8k tokenizer artifact
- T5.4 BPE 8k config linkage validation
- T5.5 BPE data/model/loss smoke
- T6 validation loop plan
- T6.1 validation loop smoke
- T7 small real-data training plan
- T7.1 bounded 50-step small real-data training
- T7.2 50-step small training review
- T7.3 bounded 100-step small training plan
- T7.4 bounded 100-step small training run
- T7.5 100-step small training review
- T7.6 50-step vs 100-step comparison
- T8 A100 100M scaling plan
- T8.1 A100 100M config draft
- T8.2 A100 environment preflight checklist
- T8.3 A100 100M forward/loss smoke plan
- T8.4 A100 execution runbook
- T8.5 A100 access decision checklist
- T8.6 A100 provider selection record
- T8.7 A100 first-session command checklist
- T8.8 A100 first-session report template
- A1 A100 smoke milestone report
- D1 expand permitted corpus plan
- D2 expanded synthetic educational corpus plan
- D2.1 expanded synthetic corpus source decision and skeleton
- D2.2 first expanded synthetic corpus batch
- D3 synthetic expanded corpus intake
- D4 expanded BPE tokenizer
- D5 expanded BPE data/model/loss smoke
- D6 expanded corpus small training plan
- D6.1 50-step expanded BPE training run
- D6.2 50-step expanded BPE training review
- D6.3 100-step expanded BPE training plan
- D6.4 100-step expanded BPE training
- D6.5 100-step expanded BPE training review
- D6.6 50-step vs 100-step expanded BPE comparison
- D7 expanded synthetic corpus batch 2
- D8 45-file expanded synthetic corpus intake
- D9 domain BPE tokenizer on 45-file corpus
- D10 domain BPE data/model/loss smoke
- D11 domain BPE small training plan
- D11.1 50-step domain BPE training
- D11.2 50-step domain BPE training review
- D11.3 100-step domain BPE training plan
- D11.4 100-step domain BPE training
- D11.5 100-step domain BPE training review
- D11.6 50-step vs 100-step domain BPE comparison
- D12 external/general text supplement plan
- D12.1 Project Gutenberg source decision record
- D12.2 external general text skeleton and manifest placeholder
- D12.3 Project Gutenberg file-level review plan
- D12.4 Project Gutenberg candidate terms record
- D12.5 Gutenberg single candidate selection
- D12.6 Gutenberg controlled download plan
- D12.7 Gutenberg controlled download inspection
- D12.8 external general text intake / cleaning plan
- D12.9 external general text intake
- D12.10 external general text intake review
- D13 mixed corpus integration strategy
- D13.1 mixed domain/external corpus build
- D14 mixed/domain BPE tokenizer retraining plan
- D14.1 mixed/domain BPE tokenizer
- D15 mixed/domain BPE data/model/loss smoke
- D16 mixed/domain BPE small training plan
- D16.1 50-step mixed/domain BPE training
- D16.2 50-step mixed/domain BPE training review
- D16.3 100-step mixed/domain BPE training plan
- D16.4 100-step mixed/domain BPE training
- D16.5 100-step mixed/domain BPE training review
- D16.6 50-step vs 100-step mixed/domain BPE comparison
- A2 A100 mixed/domain training plan
- D17.0 draft corpus taxonomy and worker framework
- D17.1 draft corpus generation validation
- D17.2 draft corpus review gate
- D18 batch_04 draft corpus validation and quality review
- D18.1 targeted sampling review pack
- D18.3 batch 04 sampling review aggregate
- D19.2 batch_05 repair-aware validation and quality review
- D19.3 batch_05 sampling review plan
- D19.3 batch_05 targeted sampling review
- D20 promotion subset plan
- D20.1 batch 05 promotion subset candidate selection
- E1 research paper assistant corpus framework
- E1.R1 research paper schema and taxonomy alignment
- MVP-2 FineWeb-Edu public corpus source decision
- MVP-3.R FineWeb-Edu dry-run troubleshooting
- MVP-3.1 FineWeb-Edu 50MB slice fetch and validation
- MVP-4 FineWeb-Edu public corpus intake and tokenizer decision
- MVP-5 FineWeb-Edu data/model/loss smoke
- MVP-6 A100 300M 10-step smoke plan
- MVP-7 A100 FineWeb-Edu 300M 10-step training script
- MVP-8.P A100 execution preflight gate
- MVP-8 A800 300M 10-step training smoke completed
- MVP-9 A800 300M 100-step bounded run completed
- MVP-10 post-A800 review and next-scale decision
- MVP-11 FineWeb-Edu 500MB public corpus expansion plan
- MVP-11.1 FineWeb-Edu 500MB fetch and intake
- MVP-12 public FineWeb-Edu 16k tokenizer trained
- MVP-13 300M 1000-step public tokenizer decision and run plan
- MVP-13.1 public 16k data/model/loss smoke
- MVP-14.P A800 1000-step public16k preflight gate
- MVP-14.Q A800 one-hour utilization queue prepared
- MVP-14 A800 1000-step public16k low-RAM fallback completed
- MVP-15 A800 3000-step public16k low-RAM fallback completed
- MVP-16 host-RAM and batching fix plan
- MVP-17 streaming batch iterator implemented
- MVP-18 A800 1000-step public16k streaming run completed
- MVP-18.S streaming breakthrough summary and next-scale decision
- MVP-19.P A800 streaming 3000-step execution plan
- MVP-19.Q A800 one-hour streaming queue prepared
- MVP-20 FineWeb-Edu 2GB prepared corpus
- MVP-21.P A800 2GB streaming preflight gate
- MVP-21.Q A800 2GB streaming one-hour queue
- MVP-22.P FineWeb-Edu 5GB prepared corpus and readiness
- MVP-23 A800 5GB streaming training plan
- MVP-26.P Modal backend adapter planned
- MVP-21 Modal A100 2GB 1000-step streaming run completed
- MVP-22 Modal A100 2GB 3000-step streaming run completed
- MVP-22.S Modal 2GB streaming stage summary
- MVP-23.P scheduler and sampling cleanup plan
- MVP-23.I scheduler metadata cleanup
- MVP-23.J streaming shuffle buffer
- MVP-24.P Modal 5GB 1000-step training mode prepared
- MVP-24 Modal A100 5GB 1000-step streaming run completed
- MVP-25.B validation coverage fix prepared
- MVP-25.C real 5GB validation coverage preflight passed
- MVP-26.P 5GB 3000-step training plan and cost gate prepared
- MVP-26.I 5GB 3000-step Modal runner mode prepared
- MVP-26 Modal A100 5GB 3000-step streaming run completed
- MVP-27.A 5GB 3000-step result analysis completed
- MVP-27.B next-stage route selection completed
- MVP-28.P attention backend profiling plan completed
- MVP-28.I SDPA attention profiling mode prepared
