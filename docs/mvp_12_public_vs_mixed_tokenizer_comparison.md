# MVP-12 Public 16k vs Mixed-domain 8k Tokenizer Comparison

## 1. Public 16k Tokenizer

Artifact:

```text
tokenizers/fineweb_edu_public_bpe_16k/tokenizer.json
```

Properties:

- trained on FineWeb-Edu 500MB train split;
- target vocab size: `16384`;
- observed vocab size: `16384`;
- special tokens: `<|endoftext|>`, `<|pad|>`, `<|unk|>`;
- intended for public FineWeb-Edu experiments.

Validation result:

- train samples checked: `20`;
- validation samples checked: `20`;
- round-trip pass count: `40`;
- round-trip fail count: `0`;
- unknown token count on samples: `0`.

## 2. Mixed-domain 8k Tokenizer

Artifact:

```text
tokenizers/educode_bpe_mixed_domain_8k/tokenizer.json
```

Properties:

- trained on the approved mixed-domain corpus;
- observed vocab size: `8192`;
- used by prior mixed-domain and FineWeb-Edu smoke paths;
- preserved unchanged in MVP-12.

## 3. Expected Benefits

The public 16k tokenizer should better fit FineWeb-Edu public English text because it is trained on the same public corpus family used by the next planned training path.

Observed sampled comparison:

| metric | public 16k | mixed-domain 8k |
|---|---:|---:|
| vocab size | 16384 | 8192 |
| sampled token count | 15302 | 21615 |

The public tokenizer produced fewer tokens on the sampled FineWeb-Edu text:

```text
token_count_ratio_public_vs_mixed = 0.707934
```

This suggests improved compression on the target public corpus sample.

## 4. Known Limitations

- The comparison is sample-based, not full-corpus token accounting.
- Lower token count does not automatically imply better model quality.
- Special token conventions differ from the older mixed-domain tokenizer.
- The public 16k tokenizer has not yet been used in a data/model/loss smoke.
- The 500MB corpus is still bounded and small relative to serious pretraining corpora.

## 5. When to Use Each

Use the public 16k tokenizer when:

- the experiment uses the FineWeb-Edu 500MB public corpus path;
- the goal is to test public-corpus tokenizer fit;
- MVP-13 explicitly chooses the new public tokenizer after review.

Use the mixed-domain 8k tokenizer when:

- reproducing or comparing against MVP-8/MVP-9 behavior;
- maintaining continuity with previous mixed-domain experiments;
- running a controlled A/B smoke where only tokenizer choice should differ.

## 6. Recommendation

MVP-13 should decide whether to run the 300M 1000-step bounded experiment with the public 16k tokenizer directly or first compare both tokenizers with a short smoke.

Recommended cautious path:

1. create the MVP-13 plan around the 500MB corpus;
2. run a small data/model/loss smoke with the public 16k tokenizer;
3. optionally run the same smoke with the mixed-domain 8k tokenizer for A/B comparison;
4. choose the tokenizer for the 300M 1000-step bounded run based on smoke compatibility and review goals.
