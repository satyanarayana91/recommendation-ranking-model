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


### Project Explanation and Interview Preparation

- [ ] Prepare a two-minute project explanation.
- [ ] Explain the problem and motivation.
- [ ] Describe the planned architecture.
- [ ] Explain the role of the XGBoost ranking model.
- [ ] Explain the popularity baseline.
- [ ] Describe NDCG and MRR.
- [ ] Explain the planned MLflow, SHAP, and FastAPI components.
- [ ] Clearly state the current implementation status.
- [ ] Practice answering the six follow-up questions.
- [ ] Update the explanation as genuine implementation evidence becomes available.

### Project Review and Publication Readiness

- [ ] Review README structure and accuracy.# Project 1 — Recommendation Ranking Model

## Project Status

- **Current phase:** Planning and documentation
- **Implementation status:** Not started
- **Goal:** Build a reproducible recommendation-ranking pipeline and demonstrate its quality using real evaluation results.
- **Current priority:** Finalize documentation, select a suitable dataset, and establish the ranking problem before implementation.

## 1. Problem Definition and Dataset Selection

- [ ] Define the recommendation-ranking problem and intended use case.
- [ ] Identify suitable public recommendation datasets.
- [ ] Compare datasets based on interaction types, available features, size, documentation, and suitability for ranking.
- [ ] Select a dataset appropriate for the project objective.
- [ ] Document the dataset source, license, and applicable usage restrictions.
- [ ] Understand the available users, items, interactions, and relevance labels.
- [ ] Inspect the dataset schema and data types.
- [ ] Perform exploratory data analysis (EDA).
- [ ] Check missing values, duplicate records, invalid values, and data-quality issues.
- [ ] Investigate interaction sparsity, popularity bias, and potential cold-start limitations.
- [ ] Define the relevance-labeling strategy.
- [ ] Identify potential sources of data leakage.
- [ ] Choose an appropriate train-validation-test split strategy.
- [ ] Document confirmed dataset limitations after inspection.
- [ ] Update the README with verified dataset information.

## 2. Candidate Preparation and Feature Engineering

- [ ] Define the recommendation request and the items to be ranked.
- [ ] Determine whether separate candidate generation or retrieval is necessary for the selected dataset.
- [ ] Document the candidate-generation or retrieval approach if required.
- [ ] Prepare ranking examples with clearly defined relevance labels.
- [ ] Create relevant user-level features, where supported by the dataset.
- [ ] Create relevant item-level features.
- [ ] Create user-item interaction features.
- [ ] Validate feature data types, missing values, and distributions.
- [ ] Ensure features use only information available at prediction time.
- [ ] Check that feature construction does not introduce data leakage.
- [ ] Document feature definitions and preprocessing decisions.

## 3. Baseline Development

- [ ] Define a simple baseline ranking approach.
- [ ] Implement a popularity-based baseline if suitable for the dataset.
- [ ] Calculate popularity statistics using training data only.
- [ ] Define the recommendation request and candidate-item evaluation setup.
- [ ] Select the evaluation cutoff, such as K = 5 or K = 10.
- [ ] Implement the baseline evaluation procedure.
- [ ] Verify baseline metric calculations using manually checked examples.
- [ ] Evaluate the baseline on the validation set during development.
- [ ] Record baseline configuration and evaluation results.
- [ ] Evaluate the final baseline on the test set after model selection.

## 4. Ranking Model Development

- [ ] Finalize the ranking formulation based on the dataset and relevance labels.
- [ ] Prepare the ranking dataset and any required query or group identifiers.
- [ ] Select an appropriate XGBoost ranking objective.
- [ ] Implement the training pipeline.
- [ ] Establish a reproducible training configuration.
- [ ] Train the initial ranking model.
- [ ] Tune important model parameters using the validation set.
- [ ] Compare model performance with the baseline using the same evaluation setup.
- [ ] Check for overfitting and unexpected performance differences.
- [ ] Save the required model artifacts and configuration.
- [ ] Document the training procedure and implementation decisions.

## 5. Evaluation Methodology

### Metric Implementation and Validation

- [ ] Finalize the relevance-labeling strategy.
- [ ] Define the train-validation-test split and document its rationale.
- [ ] Confirm that the split and feature construction prevent data leakage.
- [ ] Implement NDCG@K.
- [ ] Implement Mean Reciprocal Rank (MRR).
- [ ] Validate NDCG and MRR using manually calculated examples.
- [ ] Confirm that metric calculations handle the selected relevance-label format correctly.
- [ ] Document the evaluation cutoff and metric definitions.

### Model Evaluation and Analysis

- [ ] Evaluate the baseline on the validation set.
- [ ] Evaluate the ranking model on the validation set.
- [ ] Use validation results for model selection and tuning.
- [ ] Evaluate the selected baseline and model on the same held-out test setup.
- [ ] Compare baseline and model results using NDCG and MRR.
- [ ] Analyze ranking errors and representative examples.
- [ ] Investigate cases where the model performs worse than the baseline.
- [ ] Document evaluation limitations and possible sources of bias.
- [ ] Record actual results, configuration, and evaluation details.
- [ ] Update the README only with verified experimental results.

**Important:** Do not report illustrative numbers as actual results. Do not use test-set results to repeatedly tune the model.

## 6. Explainability

- [ ] Determine which trained model and features are suitable for explainability analysis.
- [ ] Apply SHAP to the implemented ranking model, if appropriate.
- [ ] Analyze important features and their contributions.
- [ ] Inspect explanations for representative ranking examples.
- [ ] Document the limitations of feature importance and explainability.
- [ ] Add genuine explanation outputs to the project evidence when available.

## 7. Experiment Tracking and Model Artifacts

- [ ] Configure MLflow experiment tracking.
- [ ] Define the experiment naming and organization approach.
- [ ] Log important model parameters.
- [ ] Log training and evaluation metrics.
- [ ] Store relevant model artifacts and configuration.
- [ ] Record dataset and evaluation setup details needed to interpret experiments.
- [ ] Verify that experiments can be reproduced from documented settings.
- [ ] Document how to inspect the recorded experiments.

## 8. API Development

- [ ] Define the intended ranking API behavior.
- [ ] Design request and response schemas.
- [ ] Implement the FastAPI `/rank` endpoint.
- [ ] Load the trained model or required ranking artifacts.
- [ ] Implement input validation and useful error responses.
- [ ] Ensure the endpoint returns candidates in the expected ranked order.
- [ ] Add API tests for valid requests.
- [ ] Add API tests for invalid or incomplete inputs.
- [ ] Test the endpoint with a real model and representative inputs.
- [ ] Document the API request and response format.
- [ ] Document how to start the API server.
- [ ] Verify the endpoint and interactive API documentation before publishing usage instructions.

## 9. Reproducibility and Setup

- [ ] Select a compatible Python version.
- [ ] Create and document the virtual environment.
- [ ] Establish the project dependency list.
- [ ] Create `requirements.txt` with compatible dependency versions.
- [ ] Document dataset download and preparation instructions.
- [ ] Implement the training entry point.
- [ ] Document training configuration and output artifacts.
- [ ] Document model evaluation commands.
- [ ] Document MLflow setup and experiment access.
- [ ] Document API startup and usage instructions.
- [ ] Validate installation and execution commands.
- [ ] Test the setup in a clean environment.
- [ ] Confirm that required files and artifacts are available or reproducibly generated.
- [ ] Add troubleshooting guidance for verified setup issues.
- [ ] Update the README to reflect the actual repository structure and tested commands.

## 10. Documentation and Evidence

### README and Repository Documentation

- [x] Add architecture diagram.
- [ ] Keep the README consistent with the actual project status.
- [ ] Document the problem statement and dataset.
- [ ] Document the ranking methodology and feature definitions.
- [ ] Document the baseline and evaluation methodology.
- [ ] Document actual model results after evaluation is complete.
- [ ] Document setup, training, evaluation, and API usage.
- [ ] Document known limitations and future improvements.
- [ ] Ensure planned functionality is not described as completed.

### Screenshot and Evidence Collection

- [ ] Create a suitable location for project evidence when implementation begins.
- [ ] Capture genuine data exploration or validation evidence.
- [ ] Capture baseline evaluation results.
- [ ] Capture ranking-model evaluation results.
- [ ] Capture the baseline-versus-model comparison.
- [ ] Capture MLflow experiment tracking.
- [ ] Capture SHAP outputs if explainability is implemented.
- [ ] Capture a successful API request and response.
- [ ] Add dashboard evidence only if a dashboard is implemented and adds meaningful value.
- [ ] Check screenshots for secrets, sensitive information, and restricted data.
- [ ] Add accurate captions and explanations to the README.
- [ ] Verify that every screenshot matches the actual implementation and recorded results.

**Evidence rule:** Never present mockups, illustrative outputs, or unverified screenshots as real project results.

## 11. Project Explanation and Interview Preparation

- [ ] Prepare a two-minute project explanation.
- [ ] Explain the problem and motivation.
- [ ] Describe the architecture and end-to-end workflow.
- [ ] Explain how the dataset determines the ranking formulation.
- [ ] Explain the purpose and limitations of the popularity baseline.
- [ ] Explain how the ranking model works at a practical level.
- [ ] Explain NDCG and MRR using a simple example.
- [ ] Explain the train-validation-test strategy and leakage prevention.
- [ ] Explain the purpose of MLflow and experiment tracking.
- [ ] Explain the role and limitations of SHAP.
- [ ] Explain the purpose of the FastAPI endpoint.
- [ ] Clearly distinguish planned work from implemented and evaluated functionality.
- [ ] Practice answering the six project follow-up questions.
- [ ] Update the explanation as genuine implementation evidence becomes available.

## 12. Final Review and Publication Readiness

### Scope and Technical Quality

- [ ] Verify that every feature has a clear purpose.
- [ ] Remove unnecessary features and complexity.
- [ ] Confirm that the selected ranking approach fits the dataset.
- [ ] Review code quality after implementation.
- [ ] Review tests, preprocessing, and evaluation logic.
- [ ] Verify that reported metrics are reproducible.
- [ ] Confirm that the baseline and model use a consistent evaluation setup.
- [ ] Verify that documentation and actual outputs agree.

### Security and Public Repository

- [ ] Ensure no proprietary or company data or code is included.
- [ ] Check for credentials, tokens, secrets, and sensitive information.
- [ ] Verify dataset licensing and usage restrictions.
- [ ] Review `.gitignore` and ensure inappropriate local files or generated artifacts are excluded.
- [ ] Verify screenshots and demo outputs are authentic.
- [ ] Review repository structure and documentation for accidental content.
- [ ] Inspect the final Git diff before committing.
- [ ] Decide whether the repository is ready for public access.
- [ ] Document remaining gaps if publication readiness has not been achieved.
- [ ] Confirm that the project can be explained clearly in an interview.

## Core Workflow

**Dataset Selection → Data Validation → Candidate Preparation (if required) → Feature Engineering → Baseline → Ranking Model → Evaluation → Explainability and Experiment Tracking → API → Documentation and Demo**

## Scope Boundaries

The project will focus on a clear, testable recommendation-ranking pipeline.

Out of scope unless a demonstrated need arises:

- Deep learning
- LLM or RAG integration
- Kubernetes
- Complex microservices
- Multiple databases
- A frontend without meaningful demo value
- Separate candidate-generation or retrieval infrastructure without a clear project need
- Implementing every possible ranking algorithm

## Completion Principle

Only mark a task complete after its implementation or documentation has been verified.

Report real metrics, preserve reproducibility, distinguish planned work from completed work, and document limitations honestly.
- [ ] Verify that planned and implemented features are distinguished.
- [ ] Review Python code quality after implementation.
- [ ] Review tests and evaluation logic after implementation.
- [ ] Verify screenshot authenticity and accuracy.
- [ ] Review demo functionality after implementation.
- [ ] Check repository files for secrets and sensitive information.
- [ ] Verify applicable dataset licensing and usage restrictions.
- [ ] Confirm that project documentation matches actual outputs.
- [ ] Decide whether the repository is ready for public access.
- [ ] Document any remaining gaps before publication.
