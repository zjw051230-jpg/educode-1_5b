# A100 Smoke Testing

A100 smoke testing is useful when local engineering validation already works.
The goal is not to jump directly into long training.
The goal is to prove that larger shapes and higher memory loads behave as expected.

A good smoke ladder can include:
- forward-loss only
- short optimizer run
- checkpoint smoke
- longer no-checkpoint profile

Why the ladder matters:
- each step isolates a smaller failure surface
- memory issues are easier to diagnose
- infrastructure bugs appear before long-run cost accumulates

A successful A100 smoke result is a systems milestone.
It shows that the path to larger runs is plausible.
It does not mean the current corpus is sufficient for meaningful pretraining.
