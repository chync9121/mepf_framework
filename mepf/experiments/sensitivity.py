"""Threshold sensitivity analysis for semantic decision threshold tau."""

from __future__ import annotations

from collections.abc import Iterable

from ..schema import SemanticResult


def sweep_tau(
    semantic_results: Iterable[SemanticResult],
    tau_values: Iterable[float],
) -> list[dict[str, float]]:
    """Compute interception rate for each tau value."""
    scores = [item.p_inconsistent for item in semantic_results]
    total = len(scores)
    rows = []
    for tau in tau_values:
        intercepted = sum(score >= tau for score in scores)
        rows.append(
            {
                "tau": tau,
                "interception_rate": intercepted / total if total else 0.0,
            }
        )
    return rows
