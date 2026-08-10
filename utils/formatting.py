"""
utils/formatting.py

Generic terminal / text formatting helpers. No business logic.
"""

from __future__ import annotations

LINE = "=" * 60
THIN_LINE = "-" * 60


def section(title: str) -> str:
    return f"\n{THIN_LINE}\n{title}\n{THIN_LINE}"


def banner(title: str) -> str:
    return f"\n{LINE}\n{title.center(60)}\n{LINE}"


def check(message: str) -> str:
    return f"  \u2713 {message}"


def currency(value: float) -> str:
    return f"${value:,.2f}"


def percent(value: float) -> str:
    return f"{value:.2f}%"


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"  - {item}" for item in items)
