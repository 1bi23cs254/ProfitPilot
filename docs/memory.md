# memory.md

# ProfitPilot Development Memory

---

# 1. Current Status

Current Phase: Phase 4 — Integration, Reporting & Terminal Experience

Current Task: None (Version 1 complete)

Status: Complete

Last Updated: See repository commit history / generation date

---

# 2. Completed Work

## Documentation

- [x] PRD, architecture, rules, phases carried over into docs/
- [x] README.md with setup, architecture, and extension guide

## Implementation

- [x] Project foundation and folder structure (matches architecture.md Section 10)
- [x] Workflow state schema (core/workflow/state.py)
- [x] LangGraph orchestrator wiring all 7 stages (core/orchestrator/graph.py)
- [x] Planning stage (core/planning/planner.py)
- [x] Data Collector Agent (agents/collector)
- [x] Data Processing Agent (agents/processor)
- [x] Analysis Agent — trend, forecast, anomaly, product performance (agents/analysis)
- [x] RAG Retrieval Layer with pluggable vector store, TF-IDF default (knowledge_base/)
- [x] Autonomous Reasoning Engine — pluggable backends: rule_based (default), anthropic, huggingface_local (llm/)
- [x] Business Tactics Agent — reasoning + explainable recommendations (agents/business_tactics)
- [x] Report Generation Agent — terminal + file report (agents/report)
- [x] SQLite persistence layer (database/db.py)
- [x] Terminal entrypoint (main.py)
- [x] Seed knowledge base (5 documents in knowledge_base/documents/)
- [x] Sample dataset for demonstration (data/raw/sample_sales.csv)

## Testing

- [x] Unit tests: validation, cleaning, forecasting, anomaly detection, RAG retrieval, reasoning engine
- [x] End-to-end workflow test (tests/test_workflow.py::test_end_to_end_workflow)
- [x] Manual terminal run verified against phases.md "Expected Terminal Execution"

---

# 3. Current Work

Currently Working On: N/A — Version 1 scope complete

Status: Idle

Notes: Ready for extension (real LLM backend, ChromaDB, additional datasets)
or progression toward the documented future roadmap (React UI, FastAPI,
PostgreSQL, Docker).

---

# 4. Next Tasks

Immediate Next Task

- [ ] Validate against additional real-world Kaggle business datasets

Upcoming Tasks

- [ ] Optional: enable ANTHROPIC_API_KEY / REASONING_ENGINE_BACKEND=anthropic for richer reasoning narratives
- [ ] Optional: enable VECTOR_STORE_BACKEND=chromadb in an environment with model-download access
- [ ] Expand knowledge_base/documents/ with domain-specific strategy documents

Future Tasks

- [ ] React frontend (post-Version 1, per architecture.md Future Technology Roadmap)
- [ ] FastAPI service layer
- [ ] PostgreSQL migration
- [ ] Docker packaging / cloud deployment

---

# 5. Development Log

## Version 1 Implementation

Completed

- Full four-agent architecture implemented and wired through a LangGraph StateGraph
- RAG layer, reasoning engine, and vector store built as replaceable interfaces per Loose Coupling principle
- End-to-end terminal execution verified against a synthetic sample dataset

Current Work

- None — Version 1 complete

Notes

- Default reasoning engine is rule-based (zero external dependencies) so the
  system is deployable without an API key or GPU; DeepAnalyze-8B and
  Anthropic-backed alternatives are wired but opt-in.

---

# 6. Decisions Made

## Reasoning engine default

Decision: Ship a deterministic rule_based reasoning engine as the default backend instead of requiring DeepAnalyze-8B at first run.

Reason: An 8B-parameter model requires GPU infrastructure and multi-gigabyte downloads that would prevent the project from running out of the box in most environments. The rule-based engine implements the same two responsibilities (planning + business reasoning) deterministically and remains fully explainable; DeepAnalyze-8B (or any HF model) can be enabled via `REASONING_ENGINE_BACKEND=huggingface_local` with no changes to any other module.

## Vector store default

Decision: Ship a TF-IDF vector store as the default instead of ChromaDB.

Reason: ChromaDB's default embedding function downloads a model on first use, which is not guaranteed in every deployment environment. TF-IDF requires no downloads and no network access. ChromaDB remains available via `VECTOR_STORE_BACKEND=chromadb`.

---

# 7. Blockers

Current Blockers

- None

Resolution

- N/A

---

# 8. Notes

- All configuration is environment-driven (config/settings.py); nothing is hardcoded.
- Column detection (utils/column_mapper.py) makes the pipeline schema-agnostic across different business datasets.
- Every recommendation includes an explanation, evidence, confidence score, and expected impact (FR-6 compliance).
