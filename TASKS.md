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

### Evaluation Methodology

- [ ] Define the recommendation request and candidate-item evaluation setup.
- [ ] Select the relevance-labeling strategy.
- [ ] Define the train-validation-test split.
- [ ] Check for data leakage.
- [ ] Implement the popularity baseline.
- [ ] Choose the evaluation cutoff, such as K = 5 or K = 10.
- [ ] Implement NDCG@K.
- [ ] Implement MRR.
- [ ] Validate metric calculations using manually checked examples.
- [ ] Evaluate the baseline on the test set.
- [ ] Evaluate the trained ranking model on the same test setup.
- [ ] Compare baseline and model results.
- [ ] Analyze ranking errors and dataset limitations.
- [ ] Document actual results only after evaluation is complete.

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


## Dataset Selection and Data Limitations

- [ ] Identify suitable public recommendation datasets.
- [ ] Compare datasets based on interaction types, features, size, and documentation.
- [ ] Select a dataset appropriate for the project objective.
- [ ] Document the dataset source and applicable license or usage terms.
- [ ] Understand the users, items, interactions, and relevance labels.
- [ ] Inspect the dataset schema and data types.
- [ ] Identify missing values, duplicate records, and data-quality issues.
- [ ] Investigate interaction sparsity, popularity bias, and cold-start limitations.
- [ ] Define the relevance-labeling strategy.
- [ ] Identify potential sources of data leakage.
- [ ] Plan the train-validation-test split.
- [ ] Document confirmed dataset limitations after inspection.
### Reproducibility and Setup

- [ ] Select a compatible Python version.
- [ ] Create and document the virtual environment.
- [ ] Establish the project dependency list.
- [ ] Create `requirements.txt` with compatible package versions.
- [ ] Document dataset download and preparation instructions.
- [ ] Implement the training script.
- [ ] Document training configuration and output artifacts.
- [ ] Configure MLflow experiment tracking.
- [ ] Implement the FastAPI `/rank` endpoint.
- [ ] Document API request and response schemas.
- [ ] Add instructions for starting the API server.
- [ ] Validate all installation and execution commands.
- [ ] Test the setup in a clean environment.
- [ ] Update the README with verified results and troubleshooting guidance.


### Screenshot and Evidence Collection

- [ ] Create a location for project screenshots when implementation begins.
- [ ] Capture genuine baseline evaluation results.
- [ ] Capture XGBoost ranking evaluation results.
- [ ] Capture the baseline-versus-model comparison.
- [ ] Capture MLflow experiment tracking.
- [ ] Capture a successful API request and response.
- [ ] Add dashboard screenshots if a dashboard is implemented.
- [ ] Check screenshots for sensitive information.
- [ ] Add captions and explanations to the README.
- [ ] Verify that screenshots match the actual implementation and recorded results.
