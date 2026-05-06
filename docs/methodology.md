# Methodology & Impartiality Notes

This document captures the methodological choices that keep
BrokerBench scores meaningful and comparable across models.  Read
this before publishing absolute scores or running any cross-model
comparison.

## 1. Answer-Position Shuffling

### Why

The hand-curated MCQ datasets in `brokerbench/resources/datasets/*.jsonl`
were originally written without enforcing a balanced distribution of
gold-label letters.  Before the v0.2 release, the raw dataset looked
like this:

| Letter | Count | Share |
|--------|------:|------:|
| A      |    13 |  8.0% |
| B      |   118 | 72.4% |
| C      |    30 | 18.4% |
| D      |     2 |  1.2% |

A model that did nothing but emit `B` for every question would have
scored ~72% — completely undermining cross-model comparisons and
absolute publishable numbers.

### How

`brokerbench.harness.shuffle.shuffle_instance_choices` permutes each
MCQ instance's choices using a deterministic seed derived from the
`instance_id`.  The seed is stable across runs (so reports are
reproducible) but uncorrelated with the original position (so the new
gold-letter distribution is approximately uniform).

After shuffling, the same dataset looks like:

| Letter | Count | Share |
|--------|------:|------:|
| A      |    33 | 20.2% |
| B      |    44 | 27.0% |
| C      |    46 | 28.2% |
| D      |    40 | 24.5% |

Shuffling is applied at **load** time inside both
`brokerbench.inference.load_instances` and
`brokerbench.harness.run_evaluation.load_instances`, so the model and
the grader always see the same shuffled choices.

To opt out (for debugging or to reproduce pre-v0.2 scores), set
`BROKERBENCH_SHUFFLE_CHOICES=0`.

## 2. Naive Baselines

Every published BrokerBench report should be accompanied by the naive
baselines.  If a model cannot beat `most-common-letter` or
`uniform-random` on a given domain, that domain's results should be
treated with skepticism — either the dataset is too small, the
question content is degenerate, or the model is broken.

```
python -m brokerbench.inference.run_baseline \
    --strategy all \
    --dataset all \
    --output_file predictions/_naive
```

The naive strategies are:

| Strategy        | Behaviour                                                 |
|-----------------|-----------------------------------------------------------|
| `always-a/b/c/d`| Always emits the same letter.                             |
| `uniform-random`| Picks a letter uniformly at random per instance.          |
| `most-common`   | Picks the empirical most-common letter in the dataset.    |

On the post-shuffle v0.2 dataset, a real model should comfortably
clear the 30% naive ceiling.

## 3. Reasoning-Model Token Budget

The default `max_tokens` for API calls is **4096** to accommodate
deep-reasoning models (Claude 4.x thinking, GPT-5 thinking, Grok 4
deep think, Kimi K2 thinking, Gemini 2.5 Pro thinking).  Override
with the `BROKERBENCH_MAX_TOKENS` environment variable.

```
BROKERBENCH_MAX_TOKENS=8192 python -m brokerbench.inference.run_api ...
```

## 4. Provider Routing

Models with a `/` in the identifier are routed through OpenRouter
(`https://openrouter.ai/api/v1`).  This keeps the model matrix simple
to extend: a single `OPENROUTER_API_KEY` secret unlocks every
non-anchor frontier model in the matrix workflow.

The "anchor" baseline models (Claude Sonnet 4, Claude Opus 4, Gemini
2.5 Pro, GPT-4o, GPT-5) are still hit through their native SDKs so
that any drift versus published vendor scores is attributable to
prompting / scoring rather than to a third-party gateway.

## 5. Open Caveats

The current dataset contains **163 MCQ instances across 6 domains**
(plus state supplements).  This is enough to surface clear
differences between models and naive baselines, but it is not yet
enough to publish per-domain scores with tight confidence intervals.
Treat per-domain scores as directional until the dataset crosses
~50 questions per domain.

The `legal` and `marketing` domains in `brokerbench/collect/` are
placeholders and currently ship no instances.  They are NOT included
in any composite score yet, but their domain weights are reserved in
`brokerbench/harness/constants.py::DEFAULT_DOMAIN_WEIGHTS` for when
data lands.
