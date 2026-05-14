# Checkpoint Notes / 检查点说明

Project-authored synthetic educational example for controlled corpus expansion.

## English
A training checkpoint stores enough state to resume or inspect a run later.
Common contents include model weights, optimizer state, step number, and metadata.

## 中文
训练检查点会保存足够的状态，以便之后恢复或检查一次运行。
常见内容包括模型权重、优化器状态、步数以及元数据。

## Practical value / 实际价值
If a checkpoint cannot be reloaded correctly, the saved artifact is much less useful.
如果检查点无法被正确重新加载，那么保存下来的产物价值会大幅下降。

## Summary / 总结
A checkpoint is only trustworthy when save and reload both work.
只有保存和重载都能正常工作时，检查点才值得信任。