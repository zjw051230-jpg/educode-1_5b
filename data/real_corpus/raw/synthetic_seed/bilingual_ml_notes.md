# Bilingual ML notes

Transformer 模型可以处理技术文本、代码片段、以及中英混合说明。
A small corpus does not need scale first; it needs structure first.

示例主题：
- tokenization 决定文本如何切分
- attention 决定上下文如何混合
- loss 反映预测与目标之间的差距
- checkpoint 让实验可以恢复

Safe engineering idea:
- 先验证 pipeline，再扩大数据规模
- 先记录 source policy，再引入真实语料
- 先保证无隐私风险，再考虑公开仓库
