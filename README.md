# ProfitPilot — Autonomous AI System for Profit Management

ProfitPilot is an autonomous, multi-agent business intelligence system that analyzes business data from a single natural-language objective.

The system accepts a business dataset and a user objective, then automatically:

- Understands the business objective.
- Creates an execution plan.
- Loads and validates the dataset.
- Cleans the data in memory.
- Detects important business columns automatically.
- Calculates business KPIs.
- Performs trend analysis.
- Generates a revenue forecast.
- Detects anomalous transactions.
- Identifies top-performing and low-margin products.
- Retrieves relevant business knowledge using RAG.
- Uses a locally running DeepAnalyze-8B model for business reasoning.
- Generates evidence-grounded business recommendations using the LLM.
- Produces a complete business report.
- Stores run information, KPIs, and recommendations in SQLite.

The entire Version 1 workflow runs from the terminal with a single command.

---

# Table of Contents

- [Project Overview](#project-overview)
- [Current Version](#current-version)
- [System Architecture](#system-architecture)
- [Workflow](#workflow)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Running the DeepAnalyze Server](#running-the-deepanalyze-server)
- [Kaggle Dataset Integration](#kaggle-dataset-integration)
- [Running ProfitPilot](#running-profitpilot)
- [Example Objective](#example-objective)
- [Understanding the Output](#understanding-the-output)
- [Dataset Requirements](#dataset-requirements)
- [RAG Knowledge Base](#rag-knowledge-base)
- [Reasoning and Recommendation Generation](#reasoning-and-recommendation-generation)
- [Configuration](#configuration)
- [Database and Generated Files](#database-and-generated-files)
- [Testing](#testing)

---

# Project Overview

Traditional business intelligence tools usually require users to manually:

- Upload data.
- Select metrics.
- Create dashboards.
- Interpret charts.
- Identify problems.
- Decide what actions to take.

ProfitPilot aims to automate this workflow.

The user provides:

1. A business dataset.
2. A natural-language business objective.

For example:

> Analyze the business data and identify the main profitability issues and opportunities for improvement.

ProfitPilot then executes the complete analysis pipeline automatically.

The current Version 1 implementation uses:

- A LangGraph-based workflow orchestrator.
- Multiple specialized agents.
- Deterministic Python-based KPI and analytical calculations.
- TF-IDF based Retrieval-Augmented Generation.
- A locally running DeepAnalyze-8B model.
- LLM-generated business reasoning.
- LLM-generated recommendations.
- SQLite persistence.
- Terminal-based reporting.

The design separates deterministic data analysis from LLM reasoning.

This means:

- Python is responsible for calculating KPIs and analytical results.
- The anomaly model identifies unusual transactions.
- Forecasting models generate future estimates.
- The RAG system retrieves relevant business knowledge.
- DeepAnalyze interprets the available evidence.
- DeepAnalyze generates recommendations based on that evidence.

The LLM does not directly load or calculate the raw dataset.

---

# Current Version

The current implementation is **ProfitPilot Version 1**.

The primary execution flow is:

```text
User Objective
      │
      ▼
Planning
      │
      ▼
Data Collection
      │
      ▼
Data Validation and Cleaning
      │
      ▼
KPI Computation
      │
      ▼
Business Analysis
      │
      ├── Trend Detection
      ├── Forecasting
      ├── Anomaly Detection
      └── Product Performance Analysis
      │
      ▼
RAG Knowledge Retrieval
      │
      ▼
DeepAnalyze Business Reasoning
      │
      ▼
DeepAnalyze Recommendation Generation
      │
      ▼
Report Generation
      │
      ▼
Terminal Report + SQLite Persistence
```

The current project uses the Superstore dataset from Kaggle for development and testing.

Dataset source:

```text
kaggle://vivek468/superstore-dataset-final
```

---

# System Architecture

ProfitPilot follows a multi-agent architecture.

```text
                         ┌─────────────────────┐
                         │    User Objective   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Planning Component  │
                         │    DeepAnalyze      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                 ┌────────────────────────────────┐
                 │       LangGraph Orchestrator    │
                 └──────────┬─────────────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Data Collector Agent│
                 │                     │
                 │ • Load dataset      │
                 │ • Validate data     │
                 │ • Clean data        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Data Processing     │
                 │ Agent               │
                 │                     │
                 │ • Detect columns    │
                 │ • Compute KPIs      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Analysis Agent      │
                 │                     │
                 │ • Trends            │
                 │ • Forecasting       │
                 │ • Anomalies         │
                 │ • Product analysis  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ RAG Retrieval Layer │
                 │                     │
                 │ • TF-IDF retrieval  │
                 │ • Business knowledge│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Business Tactics    │
                 │ Agent               │
                 │                     │
                 │ • Business reasoning│
                 │ • Recommendations   │
                 │   via DeepAnalyze   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Report Generation   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Terminal Report     │
                 │ SQLite Persistence  │
                 └─────────────────────┘
```

All workflow stages communicate through a shared `WorkflowState`.

Agents do not directly call one another.

The LangGraph orchestrator controls the workflow.

---

# Features

## 1. Single-Prompt Execution

The user provides a single business objective.

Example:

```text
Analyze the business data and identify the main profitability issues and opportunities for improvement.
```

The system automatically performs the remaining workflow.

---

## 2. Kaggle Dataset Integration

ProfitPilot can load datasets directly from Kaggle using the format:

```text
kaggle://owner/dataset-slug
```

Example:

```text
kaggle://vivek468/superstore-dataset-final
```

The dataset is downloaded through the Kaggle API and loaded directly into memory.

The dataset is not required to be permanently stored as a local CSV before analysis.

---

## 3. Automatic Dataset Validation

The Data Collector Agent validates the dataset before analysis.

The validation process checks information such as:

- Number of rows.
- Number of columns.
- Missing values.
- Duplicate rows.
- General dataset structure.

The validation summary is included in the final output.

---

## 4. Data Cleaning

The dataset is cleaned before downstream processing.

The workflow keeps the cleaned dataset in memory.

No intermediate cleaned CSV is required for the current pipeline.

The cleaned data is passed through the shared workflow state.

---

## 5. Automatic Business Column Detection

ProfitPilot attempts to detect important business columns automatically.

Examples include:

- Revenue / Sales.
- Cost.
- Profit.
- Quantity.
- Product.
- Customer.
- Date.
- Region.
- Category.
- Sub-category.

This allows the analysis pipeline to adapt to different business datasets without manually rewriting the analysis code for every schema.

---

## 6. KPI Computation

The Data Processing Agent calculates core business KPIs.

Depending on the available dataset columns, this includes:

- Total Revenue.
- Total Cost.
- Gross Profit.
- Net Profit.
- Net Profit Margin.
- Return on Investment.
- Record Count.

For datasets that contain a profit column, the system uses the provided profit values.

If a dataset contains cost information but no profit column, profit is derived from:

```text
Profit = Revenue - Cost
```

---

## 7. Trend Analysis

The Analysis Agent analyzes revenue trends.

When a date column is available, transaction-level revenue is aggregated into a time series before analysis.

The system identifies trends such as:

- Increasing.
- Decreasing.
- Flat.
- Insufficient data.

---

## 8. Revenue Forecasting

ProfitPilot forecasts future revenue periods.

The forecast horizon is configurable.

The default configuration is:

```text
FORECAST_PERIODS=6
```

Example output:

```text
Forecast (next 6 periods):
[69957.54, 70859.54, 71761.55, 72663.56, 73565.57, 74467.57]
```

---

## 9. Anomaly Detection

ProfitPilot uses `IsolationForest` to identify unusual business transactions.

The anomaly analysis can consider available numeric business features such as:

- Revenue / Sales.
- Profit.
- Quantity.
- Discount.

The anomaly detection process also enriches detected anomalies with business context when available.

Examples may include:

- Product.
- Customer.
- Sales.
- Profit.
- Quantity.
- Discount.
- Region.
- Category.
- Sub-category.

The anomaly contamination level is configurable.

Default:

```text
ANOMALY_CONTAMINATION=0.08
```

---

## 10. Product Performance Analysis

The system identifies:

### Top-Contributing Products

Products are ranked according to their contribution value.

When profit information is available, profit contribution is used.

Otherwise, revenue contribution is used.

### Low-Margin Products

The system calculates product-level margins and identifies products below the configured margin threshold.

Default threshold:

```text
LOW_MARGIN_THRESHOLD_PCT=10.0
```

Example:

```text
Eureka Disposable Bags
Margin: -275%
```

These analytical results are passed to the DeepAnalyze reasoning engine.

---

# Technology Stack

| Component                 | Technology                   |
| ------------------------- | ---------------------------- |
| Programming Language      | Python                       |
| Workflow Orchestration    | LangGraph                    |
| Data Processing           | Pandas                       |
| Numerical Computing       | NumPy                        |
| Anomaly Detection         | Scikit-learn IsolationForest |
| Forecasting               | Linear Trend Forecasting     |
| Environment Configuration | python-dotenv                |
| Dataset Download          | Kaggle API via HTTP requests |
| RAG Retrieval             | TF-IDF                       |
| Reasoning Engine          | DeepAnalyze-8B               |
| Local Model Server        | llama.cpp `llama-server`     |
| Database                  | SQLite                       |
| Report Output             | Terminal + `.txt` reports    |

---

# Project Structure

```text
ProfitPilot/
│
├── agents/
│   ├── collector/
│   │   └── agent.py
│   │
│   ├── processor/
│   │   └── agent.py
│   │
│   ├── analysis/
│   │   └── agent.py
│   │
│   ├── business_tactics/
│   │   └── agent.py
│   │
│   └── report/
│       └── agent.py
│
├── config/
│   └── settings.py
│
├── core/
│   ├── orchestrator/
│   │   └── graph.py
│   │
│   ├── planning/
│   │   └── planner.py
│   │
│   └── workflow/
│       └── state.py
│
├── database/
│   ├── db.py
│   └── profitpilot.db
│
├── knowledge_base/
│   │
│   ├── documents/
│   │   ├── cost_optimization.md
│   │   ├── inventory_optimization.md
│   │   ├── marketing_and_customer_strategy.md
│   │   ├── pricing_strategy.md
│   │   └── profitability_fundamentals.md
│   │
│   ├── rag/
│   │   └── retriever.py
│   │
│   └── vector_store/
│       ├── base.py
│       ├── factory.py
│       ├── tfidf_store.py
│       └── chromadb_store.py
│
├── llm/
│   └── reasoning_engine/
│       ├── base.py
│       ├── factory.py
│       ├── deepanalyze_backend.py
│       ├── rule_based.py
│       ├── anthropic_backend.py
│       └── huggingface_local.py
│
├── models/
│   ├── anomaly.py
│   └── forecasting.py
│
├── reports/
│   └── generated business reports
│
├── tests/
│   └── test_workflow.py
│
├── utils/
│   ├── column_mapper.py
│   ├── dataset_loader.py
│   ├── formatting.py
│   ├── logger.py
│   └── validation.py
│
├── docs/
│   ├── architecture.md
│   ├── phases.md
│   ├── prd.md
│   ├── rules.md
│   └── memory.md
│
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── main.py
```

---

# Prerequisites

Before running ProfitPilot, make sure the following are available:

- Python 3.
- `pip`.
- Git.
- A Kaggle account.
- Kaggle API credentials.
- `llama.cpp` with `llama-server`.
- Internet access for downloading the Kaggle dataset and DeepAnalyze model if it is not already available locally.

The current project has been developed using a local DeepAnalyze model served through `llama-server`.

---

# Installation

## 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Move into the project directory:

```bash
cd ProfitPilot
```

---

## 2. Create a Virtual Environment

On macOS or Linux:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies include:

```text
langgraph
pandas
numpy
scikit-learn
python-dotenv
requests
```

---

# Environment Configuration

Create your `.env` file.

You can start from:

```bash
cp .env.example .env
```

For the current DeepAnalyze implementation, configure the important values as follows:

```env
# -----------------------------------
# Reasoning Engine
# -----------------------------------

REASONING_ENGINE_BACKEND=deepanalyze

REASONING_ENGINE_MODEL=mattritchey/DeepAnalyze-8B-Q4_K_M-GGUF:Q4_K_M

DEEPANALYZE_BASE_URL=http://127.0.0.1:8080/v1

REASONING_MAX_TOKENS=1200

REASONING_TEMPERATURE=0.2


# -----------------------------------
# RAG
# -----------------------------------

VECTOR_STORE_BACKEND=tfidf

RAG_TOP_K=4


# -----------------------------------
# Analysis
# -----------------------------------

ANOMALY_CONTAMINATION=0.08

FORECAST_PERIODS=6

LOW_MARGIN_THRESHOLD_PCT=10.0

SLOW_MOVING_STOCK_DAYS=60


# -----------------------------------
# General
# -----------------------------------

LOG_LEVEL=INFO

VERBOSE_TERMINAL=true


# -----------------------------------
# Kaggle API
# -----------------------------------

KAGGLE_USERNAME=your_kaggle_username

KAGGLE_KEY=your_kaggle_api_key
```

Do not commit your `.env` file to Git because it contains credentials.

The `.env` file should remain ignored by Git.

---

# Running the DeepAnalyze Server

ProfitPilot does not load DeepAnalyze directly inside the Python process.

Instead, the local model is served through `llama-server`.

ProfitPilot communicates with the server using its OpenAI-compatible API.

The default configured API address is:

```text
http://127.0.0.1:8080/v1
```

ProfitPilot sends requests to:

```text
http://127.0.0.1:8080/v1/chat/completions
```

---

## 1. Install or Build llama.cpp

You need a version of `llama.cpp` that provides:

```text
llama-server
```

After installation, verify:

```bash
llama-server --help
```

If this command works, the server is available.

---

## 2. Start the DeepAnalyze Server

The current project configuration uses:

```text
mattritchey/DeepAnalyze-8B-Q4_K_M-GGUF:Q4_K_M
```

Start the server with:

```bash
llama-server \
  -hf mattritchey/DeepAnalyze-8B-Q4_K_M-GGUF:Q4_K_M \
  -c 4096 \
  --port 8080
```

Explanation:

```text
-hf
```

Downloads or loads the specified Hugging Face model.

```text
mattritchey/DeepAnalyze-8B-Q4_K_M-GGUF:Q4_K_M
```

The DeepAnalyze GGUF model used by the current project configuration.

```text
-c 4096
```

Sets the model context size to 4096 tokens.

This is important because the reasoning and recommendation prompts contain:

- KPIs.
- Analytical insights.
- Retrieved business knowledge.
- The user's objective.
- Business reasoning.

A context size that is too small can produce an error such as:

```text
request exceeds the available context size
```

```text
--port 8080
```

Runs the server on port `8080`.

---

## 3. Keep the Server Running

The DeepAnalyze server must remain running while ProfitPilot executes.

Use a separate terminal.

### Terminal 1

Run:

```bash
llama-server \
  -hf mattritchey/DeepAnalyze-8B-Q4_K_M-GGUF:Q4_K_M \
  -c 4096 \
  --port 8080
```

Leave this terminal running.

### Terminal 2

Activate the ProfitPilot environment:

```bash
cd ProfitPilot
source venv/bin/activate
```

Then run ProfitPilot.

---

# Kaggle Dataset Integration

The current project supports Kaggle datasets through a custom dataset loader.

The dataset source uses this format:

```text
kaggle://owner/dataset-slug
```

For the current Superstore dataset:

```text
kaggle://vivek468/superstore-dataset-final
```

ProfitPilot internally:

1. Detects the `kaggle://` prefix.
2. Extracts the dataset owner and dataset slug.
3. Sends a request to the Kaggle API.
4. Downloads the dataset archive into memory.
5. Locates the CSV file inside the ZIP archive.
6. Loads the CSV into a Pandas DataFrame.
7. Passes the DataFrame into the workflow.

The dataset does not need to be manually downloaded before running the application.

---

## Kaggle Credentials

ProfitPilot requires:

```text
KAGGLE_USERNAME
```

and:

```text
KAGGLE_KEY
```

Add them to your `.env` file:

```env
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_api_key
```

The dataset loader reads these values from the environment.

If the credentials are missing, the application will stop with an error indicating that Kaggle credentials are required.

---

# Running ProfitPilot

Make sure:

1. Your Python virtual environment is activated.
2. Your `.env` file is configured.
3. Kaggle credentials are available.
4. The DeepAnalyze `llama-server` is running.

Then run:

```bash
python main.py \
  --dataset "kaggle://vivek468/superstore-dataset-final" \
  --objective "Analyze the business data and identify the main profitability issues and opportunities for improvement."
```

This command starts the complete workflow.

---

# Example Objective

A simple objective:

```bash
python main.py \
  --dataset "kaggle://vivek468/superstore-dataset-final" \
  --objective "Analyze the business data and identify the main profitability issues and opportunities for improvement."
```

Another example:

```bash
python main.py \
  --dataset "kaggle://vivek468/superstore-dataset-final" \
  --objective "Analyze sales performance, identify weak products, unusual transactions, and opportunities to improve profitability."
```

Another example:

```bash
python main.py \
  --dataset "kaggle://vivek468/superstore-dataset-final" \
  --objective "Identify the major business risks and the most important opportunities for improving profit."
```

---

# Interactive Objective Input

The objective argument is optional.

You can run:

```bash
python main.py \
  --dataset "kaggle://vivek468/superstore-dataset-final"
```

ProfitPilot will then ask:

```text
Enter your business objective:
```

You can enter your objective directly in the terminal.

---

# Workflow Stages

A typical execution includes the following stages.

## Stage 1 — Planning

The reasoning engine receives the user's objective.

Example:

```text
Analyze the business data and identify the main profitability issues and opportunities for improvement.
```

The planning component creates a structured execution plan containing:

- Objective.
- Relevant focus areas.
- Analysis steps.

---

## Stage 2 — Data Collector Agent

The Data Collector Agent:

- Loads the Kaggle dataset.
- Validates the dataset.
- Generates a validation summary.
- Cleans the data.

The raw and cleaned DataFrames remain available in the workflow state.

---

## Stage 3 — Data Processing Agent

The Data Processing Agent:

- Detects relevant business columns.
- Computes KPIs.
- Prepares the dataset for analysis.

Example KPIs:

```text
Total Revenue
Total Cost
Gross Profit
Net Profit
Net Profit Margin
ROI
```

---

## Stage 4 — Analysis Agent

The Analysis Agent performs:

### Trend Analysis

Determines whether revenue is:

```text
Increasing
Decreasing
Flat
```

### Forecasting

Predicts future revenue periods.

### Anomaly Detection

Uses IsolationForest to identify unusual transactions.

### Product Analysis

Identifies:

- Top-contributing products.
- Low-margin products.

---

## Stage 5 — RAG Retrieval

The RAG layer retrieves relevant business knowledge.

The current knowledge base contains documents related to:

- Profitability fundamentals.
- Cost optimization.
- Inventory optimization.
- Marketing and customer strategy.
- Pricing strategy.

The retriever selects the most relevant documents based on the analysis context.

The current default vector store is:

```text
TF-IDF
```

---

## Stage 6 — Business Tactics Agent

The Business Tactics Agent does not contain hardcoded business recommendations.

Instead, it sends the available evidence to the reasoning engine.

The evidence includes:

- User objective.
- Deterministically calculated KPIs.
- Analytical insights.
- Retrieved business knowledge.

DeepAnalyze then performs business reasoning.

After reasoning is generated, DeepAnalyze is called again to generate structured business recommendations.

The recommendation generation is separate from the deterministic analysis logic.

---

# Reasoning and Recommendation Generation

ProfitPilot separates three LLM responsibilities.

## 1. Planning

Input:

```text
User Objective
```

Output:

```json
{
  "objective": "original objective",
  "focus_areas": ["pricing", "inventory", "marketing"],
  "steps": ["collect_and_validate_data", "compute_kpis"]
}
```

---

## 2. Business Reasoning

The DeepAnalyze model receives:

- User objective.
- KPIs.
- Analytical insights.
- Retrieved business knowledge.

It produces an evidence-grounded business reasoning narrative.

The model is instructed not to:

- Invent numbers.
- Recalculate already calculated metrics.
- Treat unsupported assumptions as facts.
- Generate conclusions unrelated to the provided evidence.

---

## 3. Recommendation Generation

The recommendation component receives:

- User objective.
- KPIs.
- Analytical insights.
- Retrieved business knowledge.
- Previously generated business reasoning.

The model returns a JSON array.

Example structure:

```json
[
  {
    "category": "pricing",
    "recommendation": "Review the pricing of products with strongly negative margins.",
    "evidence": "Multiple products were identified with negative profit margins.",
    "confidence_score": 0.85,
    "expected_impact": "Reducing loss-making sales could improve overall profitability."
  }
]
```

The recommendation prompt instructs the model to:

- Generate up to 3 recommendations.
- Use only the provided evidence.
- Avoid inventing numbers.
- Avoid unsupported business facts.
- Return fewer recommendations if the evidence does not support three recommendations.

This prevents the Python application from generating fixed or hardcoded business advice.

---

# Understanding the Output

A successful run produces a report containing several sections.

## Validation Summary

Example:

```text
Validation Summary

Rows: 9994
Columns: 21
No missing values detected
Duplicate rows: 0
```

---

## Business KPIs

Example:

```text
Business KPIs

Total Revenue:      $2,297,200.86
Total Cost:         $2,010,803.84
Gross Profit:       $286,397.02
Net Profit:         $286,397.02
Net Profit Margin:  12.47%
ROI:                14.24%
```

---

## Analytical Findings

This section can contain:

```text
Revenue Trend
Forecast
Anomalies Detected
Top Contributing Products
Low-Margin Products
```

Example:

```text
Revenue Trend: increasing

Forecast (next 6 periods):
[...]

Anomalies Detected: 799
```

---

## Retrieved Business Knowledge

ProfitPilot displays the knowledge documents retrieved by the RAG system.

Example:

```text
[pricing_strategy.md]
[profitability_fundamentals.md]
[cost_optimization.md]
```

Each retrieved document includes a relevance score and snippet.

---

## Business Reasoning

This section contains the DeepAnalyze-generated interpretation of:

- Overall performance.
- Growth trends.
- Profitability risks.
- Product performance.
- Anomalies.
- Business opportunities.

---

## Recommendations

Recommendations are generated by the LLM rather than predefined Python rules.

Each recommendation contains:

```text
Category
Recommendation
Evidence
Confidence Score
Expected Impact
```

Example:

```text
[PRICING]

Review the pricing of products with strongly negative margins.

Evidence:
Multiple products have negative profit margins.

Confidence:
0.85

Expected Impact:
Reducing loss-making sales may improve overall profitability.
```

---

# Dataset Requirements

ProfitPilot is designed for business datasets containing relevant columns such as:

```text
Sales / Revenue
Profit
Cost
Quantity
Product
Order Date
Customer
Region
Category
Sub-Category
Discount
```

The column mapper attempts to automatically identify these fields based on column names.

The current Superstore dataset provides a suitable structure for:

- KPI analysis.
- Product analysis.
- Trend detection.
- Forecasting.
- Anomaly detection.
- Margin analysis.

---

# RAG Knowledge Base

Business knowledge documents are stored in:

```text
knowledge_base/documents/
```

Current documents include:

```text
cost_optimization.md

inventory_optimization.md

marketing_and_customer_strategy.md

pricing_strategy.md

profitability_fundamentals.md
```

To extend the business knowledge base, add additional `.md` or `.txt` files to:

```text
knowledge_base/documents/
```

The retriever prepares the available documents when the application starts.

---

# Configuration

All main configuration values are centralized in:

```text
config/settings.py
```

Environment variables can override the defaults.

## Reasoning Engine

```env
REASONING_ENGINE_BACKEND=deepanalyze
```

Current backend:

```text
deepanalyze
```

---

## DeepAnalyze Model

```env
REASONING_ENGINE_MODEL=mattritchey/DeepAnalyze-8B-Q4_K_M-GGUF:Q4_K_M
```

---

## DeepAnalyze Server

```env
DEEPANALYZE_BASE_URL=http://127.0.0.1:8080/v1
```

---

## Maximum Generated Tokens

```env
REASONING_MAX_TOKENS=1200
```

---

## Temperature

```env
REASONING_TEMPERATURE=0.2
```

---

## RAG Retrieval

```env
VECTOR_STORE_BACKEND=tfidf

RAG_TOP_K=4
```

---

## Anomaly Detection Sensitivity

```env
ANOMALY_CONTAMINATION=0.08
```

Increasing this value generally causes more records to be treated as anomalous.

---

## Forecast Horizon

```env
FORECAST_PERIODS=6
```

---

## Low Margin Threshold

```env
LOW_MARGIN_THRESHOLD_PCT=10.0
```

Products below this margin threshold are considered low-margin products.

---

# Database and Generated Files

ProfitPilot uses SQLite for persistence.

The database file is:

```text
database/profitpilot.db
```

The system stores information such as:

- Workflow runs.
- Business objectives.
- Dataset sources.
- KPIs.
- Recommendations.
- Run status.

Generated reports are stored in:

```text
reports/
```

Each run creates a report with a unique run ID.

Example:

```text
reports/ee2bb3531ca2_report.txt
```

Logs are stored in:

```text
logs/
```

---

# Testing

The project contains workflow tests in:

```text
tests/test_workflow.py
```

Run:

```bash
pytest -q
```

Note: the current test file still contains references to the previously used:

```text
data/raw/sample_sales.csv
```

If that dataset has been removed from the project, the tests should be updated to use an available test dataset or a generated fixture before relying on the test suite as a validation step.

---

# Example Complete Execution

## Terminal 1 — Start DeepAnalyze

```bash
llama-server \
  -hf mattritchey/DeepAnalyze-8B-Q4_K_M-GGUF:Q4_K_M \
  -c 4096 \
  --port 8080
```

Keep this terminal running.

---

## Terminal 2 — Run ProfitPilot

```bash
cd ProfitPilot

source venv/bin/activate
```

Then execute:

```bash
python main.py \
  --dataset "kaggle://vivek468/superstore-dataset-final" \
  --objective "Analyze the business data and identify the main profitability issues and opportunities for improvement."
```

ProfitPilot will then:

```text
1. Start the workflow.
2. Generate a plan from the business objective.
3. Download the Superstore dataset from Kaggle.
4. Validate the dataset.
5. Clean the dataset.
6. Detect business columns.
7. Calculate KPIs.
8. Analyze revenue trends.
9. Generate a forecast.
10. Detect anomalies.
11. Identify top products.
12. Identify low-margin products.
13. Retrieve relevant business knowledge.
14. Generate business reasoning using DeepAnalyze.
15. Generate evidence-grounded recommendations using DeepAnalyze.
16. Generate a business report.
17. Save the report.
18. Store run information in SQLite.
```

---

# Example Final Output Structure

```text
============================================================
                   ProfitPilot Version 1
============================================================

User Objective Received:
Analyze the business data and identify the main profitability
issues and opportunities for improvement.

Validation Summary

Business KPIs

Analytical Findings

Retrieved Business Knowledge

Business Reasoning

Recommendations

Workflow Summary

============================================================
        ProfitPilot Version 1 Completed Successfully
============================================================

Report saved to:
reports/<run_id>_report.txt
```

---

# Core Design Principle

ProfitPilot separates:

```text
Data Analysis
```

from:

```text
Business Reasoning
```

The deterministic components calculate facts.

For example:

```text
Revenue
Profit
Margins
Trends
Forecasts
Anomalies
Product Performance
```

The RAG system provides relevant business knowledge.

DeepAnalyze then interprets this evidence.

The recommendation engine also receives the same evidence and produces structured recommendations.

The result is an architecture where the LLM is used for:

```text
Planning
Reasoning
Business Interpretation
Recommendation Generation
```

while deterministic Python components remain responsible for:

```text
Data Loading
Validation
Cleaning
KPI Calculation
Trend Analysis
Forecasting
Anomaly Detection
Product Analysis
```

This separation is intended to make ProfitPilot more explainable and easier to extend.

---

# Version 1 Scope

ProfitPilot Version 1 focuses on building a complete autonomous business intelligence pipeline.

The current core system provides:

- Single-objective execution.
- Kaggle dataset integration.
- Data validation.
- Data cleaning.
- Automatic column detection.
- KPI computation.
- Trend analysis.
- Forecasting.
- Anomaly detection.
- Product performance analysis.
- RAG-based knowledge retrieval.
- DeepAnalyze-based planning.
- DeepAnalyze-based business reasoning.
- DeepAnalyze-generated recommendations.
- Terminal reporting.
- SQLite persistence.

Frontend development, dashboards, cloud deployment, and real-time data integrations can be added in future versions after the core autonomous analysis system is fully developed.

---

# License

Add your preferred license here.

For example:

```text
MIT License
```

or another license appropriate for the project.

---

# Author

**ProfitPilot**

Autonomous AI System for Profit Management.
