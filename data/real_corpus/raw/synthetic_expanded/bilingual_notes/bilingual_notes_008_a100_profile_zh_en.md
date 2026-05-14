# A100 Profile Notes / A100 配置说明

Project-authored synthetic educational example for controlled corpus expansion.

## English
An A100-focused profile usually changes scale assumptions such as batch size, model size, and runtime expectations.
It belongs to a different execution regime than a tiny local smoke run.

## 中文
面向 A100 的配置通常会改变批大小、模型规模和运行时间等规模假设。
它与本地的小型 smoke run 属于不同的执行阶段。

## Why stage separation matters / 为什么要区分阶段
Mixing local validation goals with large-scale hardware goals can make experiment interpretation confusing.
如果把本地验证目标与大规模硬件目标混在一起，实验结论会变得难以解释。

## Summary / 总结
Hardware profiles should match the stage and purpose of the experiment.
硬件配置应当与实验阶段和目标保持一致。