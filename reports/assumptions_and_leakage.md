# Assumptions and Leakage Audit

This register separates observed evidence from proposed design. It does not claim that a learned model has been trained, that evaluation is leakage-free, or that ranking performance has improved.

## Assumptions Register

| Assumption | Why it matters | Verification method and evidence | Status | Next action |
| --- | --- | --- | --- | --- |
| Dataset source and permitted use are known | Data can be used and reproduced responsibly | Official GroupLens README retrieved locally; source and terms recorded in `reports/dataset_eda.md` | Verified | Recheck terms before publication or redistribution |
| User and movie identifiers are usable grouping/candidate keys | Ranking requires consistent groups and items | EDA: 0 missing IDs; 943 users; 1,682 movies; source documentation defines both IDs | Verified | Retain identifiers as IDs, not continuous model features |
| Ratings represent a valid relevance signal | Labels determine what “better ranking” means | Raw range 1–5 verified; graded and `rating >= 4` policies documented | Partially verified | Validate whether binary threshold suits the selected candidate policy |
| Duplicate interactions are intentionally handled | Duplicate records can distort counts and evaluation | EDA and SQLite validation found 0 exact duplicates and 0 repeated user–movie pairs | Verified | Repeat validation after any ingestion change |
| Historical aggregates exclude future information | Future data would inflate evaluation | `run_ranking_experiment.py` builds validation features from train and test features from train + validation; helper test confirms explicit-history behavior | Verified for the initial experiment | Maintain this order for future feature additions |
| Popularity uses training history only | Full-period popularity leaks future activity | Test popularity is calculated from train + validation, never test interactions | Verified for the initial experiment | Preserve this rule for later baselines |
| Candidate filtering is consistent | Baseline/model comparison must be fair | Baseline filters a supplied user seen-item set | Partially verified | Apply identical filtering in future evaluator/model paths |
| Test data is separate from tuning | Test reuse makes final metrics unreliable | Fixed model parameters are declared before scoring; no tuning loop uses test metrics | Partially verified | Use validation-only tuning if hyperparameters are changed |
| Ranking metrics are correct | Incorrect metrics invalidate comparisons | NDCG@K, MRR, and MAP@K have known-answer unit tests | Verified | Add more edge cases when metric conventions change |
| Results are reproducible | Claims require repeatable evidence | Download and report scripts run locally; no split/model configuration exists | Partially verified | Version split configuration and random seeds |

## Leakage Checklist

| Audit check | Current evidence | Status |
| --- | --- | --- |
| Target-derived features | Helpers create historical aggregates only; model feature selection does not yet exist | Partially verified |
| Feature availability | Historical-only helper interface is present | Partially verified |
| Split before fitted transforms | Per-user chronological split precedes feature creation | Verified for the initial experiment |
| Historical user/item aggregates | Validation uses train; test uses train + validation history | Verified for the initial experiment |
| Popularity baseline | Test popularity uses train + validation history only | Verified for the initial experiment |
| Temporal validity | Test interactions are not used to create historical features or popularity | Verified for the initial experiment |
| User/item split policy | Known-user future-recommendation scenario is documented | Partially verified |
| Duplicate records | No exact duplicates or repeated user–movie pairs observed | Verified |
| Negative sampling | Missing ratings are documented as ambiguous | Unverified |
| Test-set reuse | No model selection/evaluation workflow yet | Unverified |
| Candidate/relevance evaluation | Relevance policy exists; candidate policy is not implemented | Unverified |

## Short Project Review

### Verified findings

- MovieLens 100K was downloaded from the official source and documented with its usage restrictions.
- The ratings table has 100,000 rows, 943 users, 1,682 movies, no missing values, no exact duplicates, no repeated user–movie pairs, and a 6.3047% interaction density.
- Binary relevance (`rating >= 4`) and graded-rating alternatives are documented.
- Local Python tests validate training-input-only aggregate features and seen-item filtering in the popularity baseline.

### Incomplete work

- Chronological train/validation/test split and candidate generation.
- Explicit negative-sampling policy.
- Candidate design with richer or exposure-aware negatives, and sensitivity analysis for the current sampled-negative assumption.
- API, model-versioning, and error analysis beyond aggregate metrics.

## Next Actions

1. Compare candidate-generation and negative-sampling policies without treating all missing ratings as true dislikes.
2. Use validation-only tuning and preserve the test period for final confirmation.
3. Add user-segment error analysis and cold-start reporting.
4. Build an API only after the experiment design is stable.
