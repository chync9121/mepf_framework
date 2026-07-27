"""Efficiency and cost analysis for the computational funnel."""

from __future__ import annotations


def expected_retrieval_calls(
    stage1_interception_rate: float,
    avg_stage2_subqueries: float,
) -> float:
    """Compute C_MEPF from the paper's efficiency analysis."""
    return (1.0 - stage1_interception_rate) * avg_stage2_subqueries


def retrieval_reduction(
    stage1_interception_rate: float,
    avg_stage2_subqueries: float,
    standard_rag_calls: float,
) -> float:
    """Return relative reduction compared with unconditional Standard RAG."""
    mepf_calls = expected_retrieval_calls(stage1_interception_rate, avg_stage2_subqueries)
    if standard_rag_calls <= 0:
        return 0.0
    return 1.0 - (mepf_calls / standard_rag_calls)
