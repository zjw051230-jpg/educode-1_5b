# Training Loop / 训练循环

English:
A training loop repeats batch loading, forward pass, loss computation, backward pass, and optimizer update.
For smoke testing, a short bounded loop is often enough to validate the path.

中文：
训练循环会重复执行：读取 batch、前向计算、loss 计算、反向传播、优化器更新。
对于 smoke test，短而有边界的循环通常已经足够验证工程路径。

Shared reminder:
short successful loops validate engineering plumbing, not model quality.
