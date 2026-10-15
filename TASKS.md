# Project 1 — Recommendation Ranking Model

## Project Status

- Current phase: Planning and documentation
- Implementation status: Not started
- Goal: Build a reproducible recommendation-ranking pipeline and demonstrate its quality using real evaluation results.

## 1. Problem & Data

- [ ] Define the recommendation-ranking problem
- [ ] Select a suitable public dataset
- [ ] Understand users, items, interactions, and labels
- [ ] Perform exploratory data analysis (EDA) and data-quality checks
- [ ] Check for data leakage

## 2. Candidate & Ranking Pipeline

- [ ] Define the candidate-generation and retrieval setup
- [ ] Prepare ranking candidates
- [ ] Create user-level features
- [ ] Create item-level features
- [ ] Create user-item interaction features

## 3. Baseline

- [ ] Define a simple baseline ranking approach
- [ ] Establish the evaluation methodology
- [ ] Measure baseline performance

## 4. Ranking Model

- [ ] Prepare the ranking dataset
- [ ] Train an XGBoost ranking model
- [ ] Tune important model parameters
- [ ] Compare the model with the baseline

## 5. Evaluation

- [ ] Evaluate using NDCG
- [ ] Evaluate using MRR
- [ ] Analyze ranking errors
- [ ] Document limitations

## 6. Explainability

- [ ] Apply SHAP to the ranking model
- [ ] Analyze important features
- [ ] Document limitations of feature importance and explainability

## 7. Experiment Tracking

- [ ] Track experiments with MLflow
- [ ] Log important parameters
- [ ] Log evaluation metrics
- [ ] Store relevant artifacts

## 8. API

- [ ] Implement a FastAPI `/rank` endpoint
- [ ] Define request and response schemas
- [ ] Add API tests

## 9. Documentation & Evidence

- [ ] Update README with methodology
- [x] Add architecture diagram
- [ ] Document experiments and results
- [ ] Add relevant screenshots
- [ ] Document setup and usage
- [ ] Prepare an end-to-end demo

## 10. Final Review

- [ ] Verify that every feature has a clear purpose
- [ ] Remove unnecessary features
- [ ] Verify that all reported results are reproducible
- [ ] Ensure no proprietary or company data/code is included
- [ ] Ensure the project can be explained clearly in an interview

## Core Workflow

Candidate Generation → Retrieval → Feature Engineering → Ranking → Evaluation → Reranking/API

## Scope Boundaries

The project will focus on a clear, testable ranking pipeline.

Out of scope unless a demonstrated need arises:

- Deep learning
- LLM/RAG integration
- Kubernetes
- Complex microservices
- Multiple databases
- A frontend without meaningful demo value
- Implementing every possible ranking algorithm

## Completion Principle

Only mark a task complete after its implementation or documentation has been verified. Report real metrics, preserve reproducibility, and document limitations honestly.
