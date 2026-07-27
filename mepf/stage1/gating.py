"""Reliability gating for Stage I early exit."""

from __future__ import annotations

from ..schema import ForensicsResult, SemanticResult, StageOneResult


class ReliabilityGate:
    """Apply the paper's pre-verification decision policy."""

    def __init__(self, semantic_threshold_tau: float, forensics_threshold: float) -> None:
        self.semantic_threshold_tau = semantic_threshold_tau
        self.forensics_threshold = forensics_threshold

    def decide(
        self,
        semantic: SemanticResult,
        forensics: ForensicsResult,
    ) -> StageOneResult:
        if semantic.p_inconsistent >= self.semantic_threshold_tau:
            return StageOneResult(
                semantic=semantic,
                forensics=forensics,
                should_intercept=True,
                reason="image-text semantic inconsistency",
            )

        if forensics.p_forged >= self.forensics_threshold:
            return StageOneResult(
                semantic=semantic,
                forensics=forensics,
                should_intercept=True,
                reason="visual source appears forged",
            )

        return StageOneResult(
            semantic=semantic,
            forensics=forensics,
            should_intercept=False,
            reason="passed semantic and visual reliability checks",
        )
