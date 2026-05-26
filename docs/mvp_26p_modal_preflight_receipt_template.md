# MVP-26.P Modal Preflight Receipt Template

## Modal Preflight Receipt

| field | value |
|---|---|
| 是否完成 |  |
| Modal CLI installed |  |
| Modal authenticated |  |
| Volume name | `educode-data` |
| Prepared package uploaded |  |
| GPU requested |  |
| mode |  |
| repo commit |  |
| config path |  |
| data_loading_mode |  |
| batch_size |  |
| grad_accum |  |
| max_steps |  |
| tokenizer_vocab_size |  |
| parameter_count |  |
| memory plan status |  |
| dry-run status |  |
| readiness status |  |
| blockers |  |
| output files in volume |  |
| 是否运行训练 |  |
| 是否产生 checkpoint |  |
| 下一步建议 |  |

## Expected Preflight Output Files

For `preflight_2gb_1000`, expected Modal Volume output directory:

```text
/results/modal_preflight_2gb_1000/
```

Expected files:

- `batch_memory_plan_summary.json`
- `dry_run_summary.json`
- `execution_readiness_summary.json`
- `modal_preflight_receipt.json`

## Policy Notes

- Preflight must not run training.
- Preflight must not produce checkpoints.
- Modal credentials must not be written into this receipt.
- Prepared packages remain in `/prepared/` and must not be committed.
- Checkpoints are not downloaded by default.
