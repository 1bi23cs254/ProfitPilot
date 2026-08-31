"""
ProfitPilot Streamlit Frontend

A light, editorial "business ledger" interface for the ProfitPilot AI
business analysis system. The backend workflow (agents, orchestration,
reasoning engine) is unchanged — this file only handles presentation.

Run with:

    streamlit run app.py
"""

from __future__ import annotations

import html
import re
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st

from config.settings import settings
from core.orchestrator.graph import build_workflow
from core.workflow.state import new_state
from database.db import Database
from knowledge_base.rag.retriever import KnowledgeRetriever
from knowledge_base.vector_store.factory import build_vector_store
from llm.reasoning_engine.factory import build_reasoning_engine
from utils.logger import get_logger


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ProfitPilot",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DATASET_SOURCE = "kaggle://vivek468/superstore-dataset-final"

WORKFLOW_STAGES = [
    "Planning",
    "Data Collector Agent",
    "Data Processing Agent",
    "Analysis Agent",
    "RAG Retrieval",
    "Business Tactics Agent",
]


# ============================================================
# HTML RENDERING — fixes raw "<div>", "<p>" tags leaking as text
# ============================================================
#
# Streamlit's markdown renderer treats any line that starts with four
# or more spaces as an indented code block, and prints it verbatim
# instead of rendering it as HTML. Python's normal function-body
# indentation means every multi-line HTML string in a file like this
# ends up with that leading whitespace, so tags show up literally on
# the page. render_html() strips leading whitespace from every line
# before handing it to st.markdown, so the source can stay readable
# while the browser always gets clean, flush-left markup.

def render_html(content: str) -> None:
    lines = [line.lstrip() for line in content.strip("\n").splitlines()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


# ============================================================
# THEME
# ============================================================

def apply_theme() -> None:
    render_html(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap"
            rel="stylesheet"
        >
        """
    )

    render_html(
        """
        <style>
        :root {
            --paper: #FAFAF7;
            --ink: #1E2A32;
            --body-text: #47535F;
            --muted: #8A93A0;
            --accent: #2F6F5E;
            --accent-soft: #E8F0EC;
            --risk: #B4602E;
            --risk-soft: #FBEEE2;
            --line: #E4E1D7;
            --card: #FFFFFF;
        }

        .stApp {
            background: var(--paper);
            color: var(--body-text);
            font-family: "Inter", -apple-system, sans-serif;
        }

        .block-container {
            max-width: 980px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }

        #MainMenu, footer { visibility: hidden; }
        header { background: transparent !important; }

        h1, h2, h3 { font-family: "Source Serif 4", Georgia, serif; }

        /* ---------- Hero ---------- */
        .pp-hero {
            padding-bottom: 2rem;
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--line);
        }
        .pp-hero-title {
            font-family: "Source Serif 4", Georgia, serif;
            font-size: 3.1rem;
            font-weight: 700;
            color: var(--ink);
            line-height: 1.1;
            margin: 0 0 0.6rem 0;
        }
        .pp-hero-lede {
            font-size: 1.08rem;
            max-width: 620px;
            line-height: 1.7;
            color: var(--body-text);
            margin-bottom: 1.1rem;
        }
        .pp-hero-meta {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.88rem;
            color: var(--muted);
        }
        .pp-hero-meta .dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--accent);
            display: inline-block;
        }

        /* ---------- Section headings ---------- */
        .pp-section-title {
            font-family: "Source Serif 4", Georgia, serif;
            font-size: 1.55rem;
            font-weight: 700;
            color: var(--ink);
            margin-top: 2.6rem;
            margin-bottom: 0.3rem;
        }
        .pp-section-desc {
            font-size: 0.95rem;
            color: var(--muted);
            margin-bottom: 1.2rem;
        }

        /* ---------- Workflow stepper ---------- */
        .pp-stage {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            padding: 0.55rem 0;
            border-bottom: 1px solid var(--line);
            font-size: 0.95rem;
            color: var(--muted);
        }
        .pp-stage:last-child { border-bottom: none; }
        .pp-stage-num {
            width: 22px;
            height: 22px;
            flex-shrink: 0;
            border-radius: 50%;
            border: 1px solid var(--line);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            color: var(--muted);
        }
        .pp-stage.is-done { color: var(--ink); }
        .pp-stage.is-done .pp-stage-num {
            background: var(--accent);
            border-color: var(--accent);
            color: white;
        }

        /* ---------- Objective recap ---------- */
        .pp-objective {
            background: var(--accent-soft);
            border-left: 3px solid var(--accent);
            border-radius: 4px;
            padding: 1rem 1.3rem;
            margin-bottom: 0.5rem;
        }
        .pp-objective-label {
            font-size: 0.82rem;
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 0.35rem;
        }
        .pp-objective-text {
            font-size: 1.02rem;
            color: var(--ink);
            line-height: 1.6;
        }

        /* ---------- KPI ledger ---------- */
        .pp-kpi-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            border-top: 1px solid var(--line);
            border-left: 1px solid var(--line);
        }
        .pp-kpi-cell {
            border-right: 1px solid var(--line);
            border-bottom: 1px solid var(--line);
            padding: 1.2rem 1.4rem;
            background: var(--card);
        }
        .pp-kpi-label {
            font-size: 0.85rem;
            color: var(--muted);
            margin-bottom: 0.4rem;
        }
        .pp-kpi-value {
            font-family: "Source Serif 4", Georgia, serif;
            font-size: 1.6rem;
            font-weight: 700;
            color: var(--ink);
        }

        /* ---------- Findings ---------- */
        .pp-finding {
            background: var(--card);
            border: 1px solid var(--line);
            border-left: 3px solid var(--accent);
            border-radius: 4px;
            padding: 1rem 1.3rem;
            margin-bottom: 0.7rem;
        }
        .pp-finding.risk { border-left-color: var(--risk); }
        .pp-finding-title {
            font-weight: 600;
            color: var(--ink);
            margin-bottom: 0.3rem;
            font-size: 0.98rem;
        }
        .pp-finding-body {
            font-size: 0.96rem;
            line-height: 1.6;
            color: var(--body-text);
        }
        .pp-finding-body strong { color: var(--ink); }

        /* ---------- Insight panel ---------- */
        .pp-insight {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 1.6rem 1.8rem;
            font-family: "Source Serif 4", Georgia, serif;
            font-size: 1.04rem;
            line-height: 1.85;
            color: var(--ink);
        }
        .pp-insight p { margin: 0 0 1rem 0; }
        .pp-insight p:last-child { margin-bottom: 0; }

        /* ---------- Recommendations ---------- */
        .pp-rec {
            background: var(--card);
            border: 1px solid var(--line);
            border-radius: 6px;
            padding: 1.3rem 1.5rem;
            margin-bottom: 1rem;
        }
        .pp-rec-head {
            display: flex;
            align-items: baseline;
            gap: 0.6rem;
            margin-bottom: 0.7rem;
        }
        .pp-rec-num {
            font-family: "Source Serif 4", Georgia, serif;
            font-weight: 700;
            color: var(--accent);
            font-size: 1.05rem;
        }
        .pp-rec-tag {
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--accent);
            background: var(--accent-soft);
            border-radius: 3px;
            padding: 0.15rem 0.5rem;
        }
        .pp-rec-title {
            font-size: 1.02rem;
            font-weight: 600;
            color: var(--ink);
        }
        .pp-rec-evidence {
            background: var(--paper);
            border-radius: 4px;
            padding: 0.8rem 1rem;
            font-size: 0.92rem;
            color: var(--body-text);
            line-height: 1.6;
            margin-bottom: 0.8rem;
        }
        .pp-rec-evidence b { color: var(--ink); }
        .pp-rec-meta {
            display: flex;
            gap: 1.6rem;
            font-size: 0.85rem;
            color: var(--muted);
        }
        .pp-rec-meta b { color: var(--ink); }

        /* ---------- Success banner ---------- */
        .pp-success {
            background: var(--accent-soft);
            border-radius: 4px;
            padding: 0.9rem 1.2rem;
            color: var(--accent);
            font-weight: 600;
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
        }

        /* ---------- Widgets ---------- */
        .stButton > button {
            background: var(--ink);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
        }
        .stButton > button:hover { background: var(--accent); color: white; }

        .stTextArea label { color: var(--ink) !important; font-weight: 600; }
        .stTextArea textarea {
            color: #F4F3EE !important;
            font-size: 1.02rem !important;
            line-height: 1.65 !important;
            caret-color: #F4F3EE !important;
        }
        .stTextArea textarea::placeholder { color: #B8BCC4 !important; opacity: 1 !important; }

        hr { border: none; border-top: 1px solid var(--line); margin: 2rem 0; }
        .stDownloadButton > button {
            background: var(--card);
            border: 1px solid var(--line);
            color: var(--ink);
            border-radius: 6px;
            font-weight: 600;
        }

        @media (max-width: 700px) {
            .pp-hero-title { font-size: 2.2rem; }
            .pp-kpi-grid { grid-template-columns: repeat(2, 1fr); }
        }
        </style>
        """
    )


# ============================================================
# FORMATTING HELPERS
# ============================================================

def safe_text(value) -> str:
    if value is None:
        return ""
    return html.escape(str(value))


def format_currency(value) -> str:
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return "$0.00"


def format_percentage(value) -> str:
    try:
        return f"{float(value):.2f}%"
    except (ValueError, TypeError):
        return "0.00%"


# ============================================================
# CLEAN + CONVERT BUSINESS REASONING (DeepAnalyze output)
# ============================================================

def clean_business_reasoning(reasoning: str) -> str:
    """Strip DeepAnalyze's <Analyze>/<Answer> scaffolding, keeping only
    the final answer text that should be shown to the user."""

    if not reasoning:
        return "No business insights were generated."

    text = str(reasoning)

    answer_match = re.search(
        r"<Answer>(.*?)</Answer>", text, flags=re.DOTALL | re.IGNORECASE
    )

    if answer_match:
        text = answer_match.group(1)
    else:
        text = re.sub(
            r"<Analyze>.*?</Analyze>", "", text, flags=re.DOTALL | re.IGNORECASE
        )
        text = text.replace("<Answer>", "").replace("</Answer>", "")

    text = re.sub(r"</?Analyze>", "", text, flags=re.IGNORECASE)
    text = re.sub(r"</?Answer>", "", text, flags=re.IGNORECASE)

    text = re.sub(
        r"^Hmm,.*?(?=\*\*|Based on|Business Reasoning|Observed Facts)",
        "",
        text,
        flags=re.DOTALL,
    )

    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def reasoning_to_html(reasoning: str) -> str:
    reasoning = clean_business_reasoning(reasoning)
    escaped = safe_text(reasoning)

    paragraphs = escaped.split("\n\n")
    parts = []

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        paragraph = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", paragraph)
        paragraph = paragraph.replace("\n", "<br>")
        parts.append(f"<p>{paragraph}</p>")

    return "".join(parts) if parts else "<p>No business insights were generated.</p>"


# ============================================================
# BUILD FINDINGS  (mapped to the real WorkflowState insight keys)
# ============================================================

def build_findings(insights: dict) -> list[dict]:
    """Turn the analysis agent's `insights` dict into plain-language
    findings. Keys mirror agents/analysis/agent.py exactly:
    trend, anomalies, top_products, low_margin_products."""

    findings: list[dict] = []

    # -- Revenue trend --------------------------------------------------
    trend = insights.get("trend") or {}
    direction = trend.get("direction")

    if direction and direction not in ("insufficient_data", "unknown"):
        change_pct = trend.get("change_pct", 0.0)
        arrow = "▲" if direction == "increasing" else "▼" if direction == "decreasing" else "→"
        findings.append(
            {
                "title": f"Revenue trend {arrow}",
                "tone": "risk" if direction == "decreasing" else "positive",
                "body": (
                    f"Revenue is <strong>{safe_text(direction)}</strong>, "
                    f"a change of approximately "
                    f"<strong>{safe_text(f'{change_pct:.2f}')}%</strong> "
                    f"across the observed period."
                ),
            }
        )

    # -- Anomalies --------------------------------------------------------
    anomalies = insights.get("anomalies") or {}
    anomaly_count = anomalies.get("count", 0)

    if anomaly_count:
        findings.append(
            {
                "title": "Unusual transactions",
                "tone": "risk",
                "body": (
                    f"<strong>{safe_text(anomaly_count)}</strong> transactions "
                    "showed unusual patterns and may be worth a closer look."
                ),
            }
        )

    # -- Top contributing product ----------------------------------------
    top_products = insights.get("top_products") or []
    if top_products:
        top = top_products[0]
        findings.append(
            {
                "title": "Strongest contributor",
                "tone": "positive",
                "body": (
                    f"<strong>{safe_text(top.get('name'))}</strong> is the leading "
                    f"contributor to revenue, at approximately "
                    f"<strong>{format_currency(top.get('value'))}</strong>."
                ),
            }
        )

    # -- Lowest-margin product ---------------------------------------------
    low_margin = insights.get("low_margin_products") or []
    if low_margin:
        low = low_margin[0]
        findings.append(
            {
                "title": "Profitability risk",
                "tone": "risk",
                "body": (
                    f"<strong>{safe_text(low.get('name'))}</strong> is operating "
                    f"at roughly <strong>{format_percentage(low.get('margin_pct'))}</strong> "
                    "margin, well below a healthy threshold."
                ),
            }
        )

    if not findings:
        findings.append(
            {
                "title": "Analysis complete",
                "tone": "positive",
                "body": (
                    "The business data was processed successfully. Review the "
                    "AI insights and recommended actions below for details."
                ),
            }
        )

    return findings


# ============================================================
# RENDER HELPERS
# ============================================================

def render_kpi_ledger(kpis: dict) -> None:
    rows = [
        ("Total Revenue", format_currency(kpis.get("total_revenue"))),
        ("Total Cost", format_currency(kpis.get("total_cost"))),
        ("Gross Profit", format_currency(kpis.get("gross_profit"))),
        ("Net Profit", format_currency(kpis.get("total_net_profit"))),
        ("Net Profit Margin", format_percentage(
            kpis.get("net_profit_margin_pct"))),
        ("Return on Investment", format_percentage(kpis.get("roi_pct"))),
    ]

    cells = "".join(
        f"""
        <div class="pp-kpi-cell">
            <div class="pp-kpi-label">{safe_text(label)}</div>
            <div class="pp-kpi-value">{safe_text(value)}</div>
        </div>
        """
        for label, value in rows
    )

    render_html(f'<div class="pp-kpi-grid">{cells}</div>')

    note = kpis.get("note")
    if note:
        st.caption(f"ⓘ {note}")

    detected = kpis.get("detected_columns") or {}
    if detected:
        mapping = ", ".join(f"{k} → {v}" for k, v in detected.items())
        st.caption(f"Columns used: {mapping}")


def render_finding(finding: dict) -> None:
    tone_class = "risk" if finding.get("tone") == "risk" else ""
    render_html(
        f"""
        <div class="pp-finding {tone_class}">
            <div class="pp-finding-title">{safe_text(finding['title'])}</div>
            <div class="pp-finding-body">{finding['body']}</div>
        </div>
        """
    )


def render_recommendations(recommendations: list) -> None:
    if not recommendations:
        st.info("No recommendations were generated.")
        return

    for index, rec in enumerate(recommendations, start=1):
        if not isinstance(rec, dict):
            continue

        category = rec.get("category", "business")
        text = rec.get("recommendation", "Review this business opportunity.")
        evidence = rec.get("evidence", "No additional evidence available.")
        expected_impact = rec.get(
            "expected_impact", "Potential improvement in performance.")

        try:
            confidence_pct = f"{float(rec.get('confidence_score', 0)) * 100:.0f}%"
        except (ValueError, TypeError):
            confidence_pct = str(rec.get("confidence_score", "—"))

        render_html(
            f"""
            <div class="pp-rec">
                <div class="pp-rec-head">
                    <span class="pp-rec-num">{index:02d}</span>
                    <span class="pp-rec-tag">{safe_text(str(category).lower())}</span>
                </div>
                <div class="pp-rec-title">{safe_text(text)}</div>
                <div class="pp-rec-evidence"><b>Why this matters</b><br>{safe_text(evidence)}</div>
                <div class="pp-rec-meta">
                    <div>Confidence <b>{safe_text(confidence_pct)}</b></div>
                    <div>Expected impact <b>{safe_text(expected_impact)}</b></div>
                </div>
            </div>
            """
        )


def render_forecast(insights: dict) -> None:
    forecast = insights.get("forecast") or {}
    values = forecast.get("values") or []

    if not values:
        return

    st.markdown('<div class="pp-section-title">Revenue Outlook</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="pp-section-desc">Projected revenue for the upcoming periods, '
        "based on the trend observed in your data.</div>",
        unsafe_allow_html=True,
    )

    chart_df = pd.DataFrame(
        {"Projected revenue": values},
        index=[f"Period {i}" for i in range(1, len(values) + 1)],
    )
    st.bar_chart(chart_df, color="#2F6F5E")


def render_workflow(completed: bool) -> None:
    render_html('<div class="pp-section-title">Workflow</div>')

    items = "".join(
        f"""
        <div class="pp-stage {'is-done' if completed else ''}">
            <span class="pp-stage-num">{'✓' if completed else i}</span>
            <span>{safe_text(stage)}</span>
        </div>
        """
        for i, stage in enumerate(WORKFLOW_STAGES, start=1)
    )

    render_html(items)


# ============================================================
# RUN PROFITPILOT WORKFLOW  (unchanged backend wiring)
# ============================================================

def run_profitpilot_analysis(objective: str):
    settings.paths.ensure()

    logger = get_logger("streamlit_app", settings.log_level,
                        settings.paths.logs_dir)

    run_id = uuid.uuid4().hex[:12]

    db = Database(settings.paths.database_file)
    db.start_run(
        run_id, objective, DATASET_SOURCE, datetime.now().isoformat(timespec="seconds")
    )

    try:
        reasoning_engine = build_reasoning_engine(settings.reasoning)
        vector_store = build_vector_store(
            settings.rag, str(settings.paths.vector_store))
        retriever = KnowledgeRetriever(
            vector_store, settings.paths.knowledge_documents)

        doc_count = retriever.prepare()
        logger.info(f"Knowledge base prepared with {doc_count} documents")

        workflow = build_workflow(settings, reasoning_engine, retriever)
        state = new_state(objective, DATASET_SOURCE, run_id)

        final_state = workflow.invoke(state)

        db.save_kpis(run_id, final_state.get("kpis", {}))
        db.save_recommendations(run_id, final_state.get("recommendations", []))

        status = "completed_with_warnings" if final_state.get(
            "errors") else "success"
        db.complete_run(run_id, datetime.now().isoformat(
            timespec="seconds"), status)

        return final_state

    except Exception as exc:
        logger.error(f"Workflow failed: {exc}")
        try:
            db.complete_run(run_id, datetime.now().isoformat(
                timespec="seconds"), "failed")
        except Exception:
            pass
        raise exc


# ============================================================
# MAIN APP
# ============================================================

def main() -> None:
    apply_theme()

    # -------------------------------------------------------- HERO
    render_html(
        """
        <div class="pp-hero">
            <div class="pp-hero-title">ProfitPilot</div>
            <div class="pp-hero-lede">
                Autonomous AI System for Profit Management — it reads your business data, 
                runs its own analysis, and shows you where profit is being made or lost.
            </div>
            <div class="pp-hero-meta">
                <span class="dot"></span>
                Dataset: Superstore Dataset (Kaggle)
            </div>
        </div>
        """
    )

    # -------------------------------------------------------- OBJECTIVE INPUT
    render_html(
        '<div class="pp-section-title">What would you like to analyze?</div>')
    render_html(
        '<div class="pp-section-desc">Describe what you would like to know, in plain language.'
        "  ProfitPilot plans its analysis around it.</div>"
    )

    objective = st.text_area(
        "Business objective",
        value=(
            "Analyze the business data and identify the main profitability "
            "issues and opportunities for improvement."
        ),
        height=100,
        label_visibility="collapsed",
        placeholder="Example: Identify why margins dropped in the Furniture category last quarter.",
    )
    st.caption(
        "Edit the text above, or run it as-is for a general profitability review.")

    run_analysis = st.button("Run ProfitPilot Analysis")

    # -------------------------------------------------------- RUN
    if run_analysis:
        objective = objective.strip()

        if not objective:
            st.warning(
                "Please enter a business objective before starting the analysis.")
            return

        st.session_state["objective"] = objective

        workflow_placeholder = st.empty()
        with workflow_placeholder.container():
            render_workflow(completed=False)

        with st.status("ProfitPilot is analyzing your business data…", expanded=True) as status:
            status.write("Planning the analysis")
            status.write("Collecting and validating data")
            status.write("Calculating business KPIs")
            status.write("Running trend, forecast and anomaly analysis")
            status.write("Retrieving relevant business knowledge")
            status.write("Generating AI insights and recommendations")

            try:
                final_state = run_profitpilot_analysis(objective)
                status.update(label="Analysis complete",
                              state="complete", expanded=False)
                st.session_state["final_state"] = final_state
                st.session_state["analysis_completed"] = True
            except Exception as exc:
                status.update(label="Analysis failed", state="error")
                st.error(f"ProfitPilot encountered an error: {exc}")
                return

        workflow_placeholder.empty()
        with workflow_placeholder.container():
            render_workflow(completed=True)

    # -------------------------------------------------------- RESULTS
    if st.session_state.get("analysis_completed") and st.session_state.get("final_state"):
        final_state = st.session_state["final_state"]
        user_objective = st.session_state.get("objective", "")

        kpis = final_state.get("kpis", {})
        insights = final_state.get("insights", {})
        business_reasoning = final_state.get("business_reasoning", "")
        recommendations = final_state.get("recommendations", [])
        report_text = final_state.get("report_text", "")

        render_html(
            '<div class="pp-success">Analysis completed successfully</div>')

        render_html('<div class="pp-section-title">Business Report</div>')
        render_html(
            '<div class="pp-section-desc">A summary of performance, key risks '
            "and recommended actions.</div>"
        )

        render_html(
            f"""
            <div class="pp-objective">
                <div class="pp-objective-label">Your objective</div>
                <div class="pp-objective-text">{safe_text(user_objective)}</div>
            </div>
            """
        )

        # KPIs
        render_html(
            '<div class="pp-section-title">Performance at a Glance</div>')
        render_kpi_ledger(kpis)

        # Findings
        render_html('<div class="pp-section-title">What We Found</div>')
        for finding in build_findings(insights):
            render_finding(finding)

        anomaly_examples = (insights.get("anomalies")
                            or {}).get("examples") or []
        if anomaly_examples:
            with st.expander(f"View {len(anomaly_examples)} unusual transactions"):
                st.dataframe(pd.DataFrame(anomaly_examples),
                             use_container_width=True)

        # Forecast
        render_forecast(insights)

        # AI insights
        render_html('<div class="pp-section-title">AI Business Insights</div>')
        render_html(
            '<div class="pp-section-desc">A deeper read on what is affecting '
            "profitability and where the opportunities are.</div>"
        )
        render_html(
            f'<div class="pp-insight">{reasoning_to_html(business_reasoning)}</div>')

        # Recommendations
        render_html('<div class="pp-section-title">Recommended Actions</div>')
        render_html(
            '<div class="pp-section-desc">Practical next steps based on the '
            "analysis above.</div>"
        )
        render_recommendations(recommendations)

        # Download
        if report_text:
            st.markdown("<hr>", unsafe_allow_html=True)
            st.download_button(
                label="Download Full Report",
                data=report_text,
                file_name="profitpilot_business_report.txt",
                mime="text/plain",
                use_container_width=True,
            )


if __name__ == "__main__":
    main()
