# Validation Notes / 验证说明

Project-authored synthetic educational example for controlled corpus expansion.

## English
Validation uses held-out data to check whether improvements on the training set also appear outside the seen examples.
It is one of the main defenses against over-interpreting train loss.

## 中文
验证会使用留出的数据来检查：训练集上的改进是否也能在未见样本上出现。
它是防止过度解读训练损失的重要方法之一。

## Caution / 注意
A tiny validation split can be noisy, so trends matter more than one isolated number.
如果验证集很小，波动会比较大，因此趋势通常比单个数字更重要。

## Summary / 总结
Validation is a boundary check on training claims.
验证是对训练结论进行边界约束的一种检查。