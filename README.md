# ProfitPilot — Autonomous AI System for Profit Management

An autonomous, multi-agent business-intelligence system. Give it one
natural-language objective and a CSV dataset; it plans, collects and cleans
the data, computes KPIs, runs trend/forecast/anomaly analysis, retrieves
relevant business knowledge (RAG), reasons over all of it, and produces
explainable, evidence-backed recommendations — with no further user
interaction, end to end in the terminal.

This implementation follows `docs/architecture.md`, `docs/rules.md`, and
`docs/phases.md` exactly: single-prompt execution, a LangGraph orchestrator,
a fixed four-agent architecture (+ RAG layer + reasoning engine + report
agent), and a terminal-first Version 1 scope.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # optional — defaults already work

python main.py --dataset data/raw/sample_sales.csv \
  --objective "Analyze my sales data and tell me how to maximize profit."
```

No API key, GPU, or network access is required. The default configuration
uses a deterministic, evidence-grounded reasoning engine and an offline
TF-IDF knowledge retriever, so the full autonomous workflow runs immediately.

Run the test suite:

```bash
pytest -q
```

## Using your own dataset

Any business CSV with a revenue-like column works out of the box —
`utils/column_mapper.py` detects revenue, cost, profit, quantity, product,
date, region, and category columns by keyword, so the pipeline adapts to
different schemas (Kaggle retail/sales datasets, custom exports, etc.)
without code changes. Point `--dataset` at it:

```bash
python main.py --dataset data/raw/your_data.csv --objective "Your objective here"
```

## Architecture

```
User Prompt
    │
    ▼
Planning (Reasoning Engine)
    │
    ▼
Data Collector Agent      → validate, clean
    │
    ▼
Data Processing Agent     → compute KPIs
    │
    ▼
Analysis Agent            → trend, forecast, anomalies, product performance
    │
    ▼
RAG Retrieval Layer       → relevant business knowledge
    │
    ▼
Business Tactics Agent    → reasoning + explainable recommendations
    │
    ▼
Report Generation Agent   → terminal report
```

Every stage runs as a node in a `langgraph.graph.StateGraph`
(`core/orchestrator/graph.py`); agents never call each other directly — all
communication flows through the shared `WorkflowState`
(`core/workflow/state.py`), and only the orchestrator invokes agents.

```
ProfitPilot/
├── agents/            # collector, processor, analysis, business_tactics, report
├── core/               # orchestrator (LangGraph), planning, workflow state
├── llm/                # Autonomous Reasoning Engine (pluggable backends)
├── knowledge_base/     # RAG retriever + pluggable vector store + seed docs
├── models/             # forecasting (linear trend) + anomaly detection (IsolationForest)
├── database/           # SQLite persistence (run history, KPIs, recommendations)
├── data/               # raw / cleaned / processed / outputs
├── reports/            # generated terminal reports (.txt)
├── utils/               # logging, validation, formatting, column detection
├── config/             # all configuration, environment-driven
├── tests/              # unit + end-to-end tests
└── main.py
```

## Swapping components (they're all replaceable by design)

| Component | Default | Swap to | How |
|---|---|---|---|
| Reasoning Engine | `rule_based` (deterministic, zero-dependency) | `anthropic` (real LLM via Anthropic API) or `huggingface_local` (e.g. DeepAnalyze-8B or any local model) | Set `REASONING_ENGINE_BACKEND` in `.env` |
| Vector Store | `tfidf` (offline, no downloads) | `chromadb` (architecturally-specified production backend) | Set `VECTOR_STORE_BACKEND=chromadb`, `pip install chromadb` |
| Database | SQLite | PostgreSQL | `database/db.py` is the only file that needs a new implementation |

Each backend implements a small abstract interface
(`llm/reasoning_engine/base.py`, `knowledge_base/vector_store/base.py`), so
no agent, orchestrator, or report code changes when you swap one out.

## Extending the knowledge base

Drop additional `.md` or `.txt` files into `knowledge_base/documents/`; they
are picked up automatically on the next run.

## Configuration

All configuration lives in `config/settings.py` and is overridable via
environment variables — see `.env.example` for the full list (reasoning
engine, RAG top-k, anomaly sensitivity, forecast horizon, margin thresholds,
logging).

## Notes on the reasoning engine

The PRD specifies **DeepAnalyze-8B** as the initial reasoning engine. Running
an 8B-parameter model needs a GPU and multi-gigabyte weights, which would
make this project fail to run in most environments out of the box. The
default `rule_based` backend implements the *same two responsibilities*
(planning + business reasoning) deterministically and is fully explainable —
every sentence it produces is traced to a concrete KPI, insight, or
retrieved document. `llm/reasoning_engine/huggingface_local.py` is the exact
wiring point for DeepAnalyze-8B (or any other local model) once GPU
infrastructure is available; `llm/reasoning_engine/anthropic_backend.py` is a
ready-to-use real-LLM alternative that needs only an API key.

## Out of scope (Version 1)

Per `docs/phases.md`: GUI, authentication, cloud deployment, REST API,
multi-user support, and enterprise integrations. `docs/architecture.md`
documents the intended future path (React UI, FastAPI, PostgreSQL, Docker,
cloud deployment) without requiring changes to this core workflow.
