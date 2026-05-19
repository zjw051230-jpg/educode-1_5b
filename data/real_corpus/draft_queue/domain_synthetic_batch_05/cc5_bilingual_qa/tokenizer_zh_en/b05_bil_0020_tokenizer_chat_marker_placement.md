---
draft_status: candidate
topic_id: B05-BIL-0020
source_category: synthetic_examples
project_backbone: cs_ml_python_transformer_training_systems
worker_id: CC-5
approved_for_training: false
contains_external_text: false
contains_private_data: false
target_use: draft_review_only
batch_id: domain_synthetic_batch_05
---

# Tokenizer Boundaries and Mixed Scripts 20: Chat Marker Placement

## Learning objective
- ZH: 识别 `chat_marker_placement` 如何改变中英混排中的切分边界。
- EN: See how `chat_marker_placement` shifts boundary decisions in mixed Chinese-English text.

## Scene
A reviewer compares two prompts that differ only by one delimiter choice and gets different token counts.

## Before / after strings
- before: `请总结GPU memory, keep fp16.`
- after: `请总结 GPU memory，keep fp16。`

## Boundary sketch
- before tokens: `[请总结][GPU][memory][,][keep][fp16][.]`
- after tokens: `[请总结][GPU][memory][，][keep][fp][16][。]`

## Why it matters
The visible sentence still looks equivalent, but the tokenizer now spends capacity on punctuation and split numerals differently. That changes sequence length, padding pressure, and sometimes the exact location where a glossary term gets fragmented.

## Concrete anchor: small pseudo-run log
- Watch whether `fp16` stays whole or breaks into `fp` + `16`.
- If the split happens only on one side of a bilingual pair, alignment can drift even when wording looks natural.

## Tiny bilingual repair
- ZH rewrite: `请总结 GPU memory，并保持 fp16 写法一致。`
- EN rewrite: `Summarize GPU memory and keep the fp16 spelling stable.`

## Takeaway
A token count is not just a length number; it is a trace of boundary decisions.
