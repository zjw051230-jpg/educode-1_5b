# MVP-10 Next-Scale Decision Matrix

| option | goal | benefit | risk | cost | prerequisite | recommended_order | decision |
|---|---|---|---|---|---|---:|---|
| `300M` `1000-step` on `50MB` | test longer-run stability on the current reviewed setup | fastest path to another GPU training result | likely overfits tiny corpus; does not improve data or tokenizer quality | medium GPU cost, low prep cost | current MVP-8 / MVP-9 path only | 3 | not recommended first |
| `500MB` public corpus expansion | improve public-corpus scale before longer runs | better substrate for training and tokenizer work while staying bounded | requires additional fetch/intake review work | low GPU cost, medium data-prep cost | approved fetch/intake plan for larger slice | 1 | recommended next |
| public `16k` tokenizer | align tokenizer to the public English corpus path | stronger tokenizer match for later public-corpus pretraining | extra step before next GPU run; weaker if corpus remains too small | low GPU cost, medium tokenizer-prep cost | larger reviewed public slice, preferably `500MB` | 2 | recommended after corpus expansion |
| `1B` `10-step` smoke | test larger-model materialization and short-run memory behavior | useful scaling signal beyond `319M` | amplifies architecture/config caveats if run too early | medium-to-high GPU cost | config/model caveat review and preferred tokenizer/corpus decision | 4 | secondary recommendation |
| `2B+` profile | measure upper-bound memory/throughput behavior | useful hardware envelope signal | little value before data/tokenizer/config cleanup; not a training-quality step | high GPU cost | larger-model config review and stronger scaling justification | 5 | defer |
| H200/B200 | move toward target-class hardware | future path for larger or longer runs | premature before public-corpus, tokenizer, and caveat cleanup | highest infra cost | stronger data substrate, logging cleanup, and architecture review | 6 | not recommended now |
