# GPU Memory Notes

GPU memory pressure depends on more than parameter count.
Important factors include:
- batch size
- sequence length
- optimizer state
- activation storage
- temporary attention buffers

A useful fallback order for a smoke run is:
1. reduce batch size
2. reduce sequence length
3. reduce model size

That order preserves more of the intended model shape.
It can help isolate whether the problem is activations or core capacity.

Memory metrics are also worth recording separately:
- allocated memory
- reserved memory
- step time

Those numbers make later scaling choices less guess-based.
