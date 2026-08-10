"""
database/db.py

Local persistence layer (architecture.md Section 12 - Data Persistence
Architecture). SQLite is used for Version 1; the schema and access pattern
are isolated behind this module so a future PostgreSQL migration requires no
changes to any agent or core module (architecturally required database
independence).
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    user_objective TEXT NOT NULL,
    dataset_path TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL DEFAULT 'running'
);

CREATE TABLE IF NOT EXISTS kpis (
    run_id TEXT NOT NULL,
    kpi_json TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs (run_id)
);

CREATE TABLE IF NOT EXISTS recommendations (
    run_id TEXT NOT NULL,
    category TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    expected_impact TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs (run_id)
);
"""


class Database:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def start_run(self, run_id: str, user_objective: str, dataset_path: str, started_at: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO runs (run_id, user_objective, dataset_path, started_at, status) "
                "VALUES (?, ?, ?, ?, 'running')",
                (run_id, user_objective, dataset_path, started_at),
            )

    def complete_run(self, run_id: str, completed_at: str, status: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "UPDATE runs SET completed_at = ?, status = ? WHERE run_id = ?",
                (completed_at, status, run_id),
            )

    def save_kpis(self, run_id: str, kpis: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO kpis (run_id, kpi_json) VALUES (?, ?)",
                (run_id, json.dumps(kpis, default=str)),
            )

    def save_recommendations(self, run_id: str, recommendations: list[dict[str, Any]]) -> None:
        with self._connect() as conn:
            conn.executemany(
                "INSERT INTO recommendations (run_id, category, recommendation, confidence_score, expected_impact) "
                "VALUES (?, ?, ?, ?, ?)",
                [
                    (
                        run_id,
                        rec["category"],
                        rec["recommendation"],
                        rec["confidence_score"],
                        rec["expected_impact"],
                    )
                    for rec in recommendations
                ],
            )

    def fetch_run_history(self, limit: int = 10) -> list[dict[str, Any]]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT run_id, user_objective, started_at, completed_at, status "
                "FROM runs ORDER BY started_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]
