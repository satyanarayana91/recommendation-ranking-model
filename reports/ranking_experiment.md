# Ranking Experiment

This is an educational offline experiment, not a production recommendation claim. Each user's earliest 80% of interactions is history, the next 10% forms supervised training candidates, and the latest 10% is the held-out test period. Candidate sets include held-out rated movies plus 50 deterministically sampled, unseen movies per user. Sampled unobserved movies are treated as zero-label evaluation negatives for this experiment; this is a limitation, not evidence of dislike.

- Seed: `42`; relevance: rating >= 4; features: training-history user/item aggregates only.
- Raw interaction splits: train **80,808**, validation-as-training-examples **9,596**, test **9,596**.
- Candidate rows: ranker training **51,906**, test **50,420**; test users with a relevant item: **829**.

| Method | NDCG@10 | MRR@10 | MAP@10 |
| --- | ---: | ---: | ---: |
| Training-history popularity baseline | 0.6158 | 0.4844 | 0.4297 |
| XGBoost `rank:ndcg` | 0.6161 | 0.5028 | 0.4442 |

Metrics are computed per user and averaged only over users with at least one relevant held-out rated item. NDCG uses the raw 1–5 rating for observed held-out movies and zero for sampled candidates; MRR/MAP use the fixed binary relevance policy. Both methods use exactly the same test candidate rows and seen-item exclusion.
