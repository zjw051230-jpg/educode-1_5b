# Tokenizer Notes / 分词器笔记

English:
A tokenizer turns raw text into units that a model can process.
Better corpus coverage usually leads to a more useful observed vocabulary.
A tiny corpus often yields a much smaller observed vocab than the nominal target.

中文：
分词器会把原始文本转换成模型可以处理的离散单元。
如果语料规模太小，观察到的词表通常会明显小于目标词表。
这不一定说明实现错误，更可能说明语料覆盖面不足。

Shared lesson:
corpus scale and tokenizer quality must be planned together.
