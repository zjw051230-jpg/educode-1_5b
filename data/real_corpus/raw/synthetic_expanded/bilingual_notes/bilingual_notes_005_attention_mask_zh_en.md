# Attention Mask Notes / 注意力掩码说明

Project-authored synthetic educational example for controlled corpus expansion.

## English
An attention mask controls which token positions are allowed to interact.
In autoregressive training, a causal mask prevents a token from seeing future tokens.

## 中文
注意力掩码用于控制哪些 token 位置可以彼此交互。
在自回归训练中，因果掩码会阻止当前位置看到未来 token。

## Why it matters / 为什么重要
A wrong mask can silently leak future information and make the loss misleading.
错误的掩码可能会悄悄泄露未来信息，从而让损失值失去解释意义。

## Summary / 总结
Masking is a structural correctness rule, not just a convenience detail.
掩码属于结构正确性要求，而不只是实现细节。