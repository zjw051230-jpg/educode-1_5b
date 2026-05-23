# MVP-12 Public 16k Tokenizer Preview

## 1. Timing

MVP-12 should begin only after the FineWeb-Edu 500MB slice has been fetched, validated, intaked, and reviewed.

The project should not train a public 16k tokenizer directly on the current 50MB slice. The 50MB corpus was sufficient to prove the public-corpus training loop, but it is still too small to justify treating a new public tokenizer as representative.

## 2. Goal

The MVP-12 tokenizer goal is to train a public-corpus 16k tokenizer that better fits the reviewed FineWeb-Edu English corpus path.

Expected benefits:

- better public English corpus fit;
- cleaner comparison against the current mixed-domain 8k tokenizer;
- less reliance on a tokenizer trained for a different corpus mixture;
- preservation of the existing tokenizer as an unchanged baseline.

## 3. Comparison Target

MVP-12 should compare the new public 16k tokenizer against the current mixed-domain 8k tokenizer without overwriting the existing tokenizer artifact or changing prior run interpretation.

The comparison should focus on tokenization statistics, config compatibility, and a bounded data/model/loss smoke before any longer model training.

## 4. Why Not 32k Yet

A 32k tokenizer should wait for a larger reviewed public corpus. At the 500MB stage, 16k is the better bounded target because it improves public-corpus fit without prematurely increasing vocabulary size beyond the available corpus scale.

## 5. Next Step

After MVP-11.1 completes, write the full MVP-12 public 16k tokenizer training plan.
