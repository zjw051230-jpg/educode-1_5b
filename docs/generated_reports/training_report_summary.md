# Training Report Summary

This generated report summarizes committed imported artifact metadata only. It does not read root-level result tarballs, checkpoints, raw data, or prepared data.

## Runs

| Run | Status | Rows | Loss | Throughput | Memory |
| --- | --- | --- | --- | --- | --- |
| seq512 batch8 3000step | success | metrics 3000, val 10 | train 3.029707, val 8.341638 | summary 47973.371610, step mean 48013.581977 tokens/sec | alloc 2.645120 GiB, reserved 8.416016 GiB |
| seq512 batch8 50step | success | metrics 50, val 1 | train 4.328258, val 8.897261 | summary 44100.712407, step mean 46732.188322 tokens/sec | alloc 2.645120 GiB, reserved 8.416016 GiB |
| seq1024 batch4 10step | success | metrics 10, val 1 | train 2.392136, val 9.044042 | summary 27151.115060, step mean 40433.276612 tokens/sec | alloc 2.649026 GiB, reserved 8.412109 GiB |
| seq1024 batch4 50step | success | metrics 50, val 1 | train 1.450320, val 9.930368 | summary 41430.475003, step mean 44774.595547 tokens/sec | alloc 2.649026 GiB, reserved 8.412109 GiB |

## Comparability Notes

- seq512 and seq1024 profiling rows are systems evidence for throughput, step time, and memory.
- Short 10-step and 50-step runs are not model-quality evidence.
- 3000-step training loss is useful for trend sanity checks only when paired with validation coverage notes.

## Quality Caveat

Loss values from short profiling or memory preflight runs are sanity signals. They should not be described as quality training results.
