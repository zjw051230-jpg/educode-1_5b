# Attention Shapes

Attention code often fails because shapes are easy to confuse.
A useful habit is to write down the expected dimensions first.

Example symbols:
- `B` = batch size
- `T` = sequence length
- `D` = model width
- `H` = number of heads
- `Hd` = head dimension

Typical flow:
- input hidden states: `(B, T, D)`
- query/key/value after projection: `(B, T, D)`
- split heads: `(B, H, T, Hd)`
- attention scores: `(B, H, T, T)`
- merged output: `(B, T, D)`

When training at larger scale, shape correctness is still the first gate.
A huge GPU does not fix a shape bug.
That is why small smoke tests and large profiling runs both matter.
