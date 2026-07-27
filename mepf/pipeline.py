"""Top-level MEPF pipeline.

This file mirrors the paper workflow:

Input Validation -> Retrieval Decision -> Evidence Verification -> Final Judgment
"""

from __future__ import annotations

from .config import MEPFConfig
from .schema import MEPFResult, NewsSample, Verdict
from .stage1.gating import ReliabilityGate
from .stage1.semantic import CrossModalSemanticEvaluator
from .stage1.forensics import VisualForensicsAnalyzer
from .stage2.planning_agent import PlanningAgent


class MEPFPipeline:
    """Coordinate Stage I pre-verification and Stage II planned retrieval."""

    def __init__(
        self,
        config: MEPFConfig,
        semantic_evaluator: CrossModalSemanticEvaluator | None = None,
        forensics_analyzer: VisualForensicsAnalyzer | None = None,
        planning_agent: PlanningAgent | None = None,
    ) -> None:
        self.config = config
        self.semantic_evaluator = semantic_evaluator or CrossModalSemanticEvaluator(
            config.semantic_model or {}
        )
        self.forensics_analyzer = forensics_analyzer or VisualForensicsAnalyzer(
            config.forensics_model or {}
        )
        self.gate = ReliabilityGate(
            semantic_threshold_tau=config.semantic_threshold_tau,
            forensics_threshold=config.forensics_threshold,
        )
        self.planning_agent = planning_agent or PlanningAgent(
            max_steps=config.max_planning_steps,
            retrieval_config=config.retrieval or {},
            reasoner_config=config.reasoner or {},
        )

    def run(self, sample: NewsSample) -> MEPFResult:
        stage_one = self._run_stage_one(sample)

        if stage_one.should_intercept:
            return MEPFResult(
                sample_id=sample.id,
                verdict=Verdict.FAKE,
                stage_one=stage_one,
                explanation=f"Intercepted at Stage I: {stage_one.reason}",
            )

        verdict, evidence_chain, explanation = self.planning_agent.verify(sample)
        return MEPFResult(
            sample_id=sample.id,
            verdict=verdict,
            stage_one=stage_one,
            evidence_chain=evidence_chain,
            explanation=explanation,
        )

    def _run_stage_one(self, sample: NewsSample):
        semantic = self.semantic_evaluator.predict(sample)
        forensics = self.forensics_analyzer.predict(sample)
        return self.gate.decide(semantic, forensics)
