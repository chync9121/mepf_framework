"""Serialized fact-checking via a planning agent.

This mirrors Algorithm 1 in the paper:

InitState -> GenerateSubProblem -> SelectTool -> Execute -> Analyze
-> UpdateState -> SynthesizeVerdict
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..schema import EvidenceItem, NewsSample, Verdict
from .prompts import FACT_CHECKING_SYSTEM_PROMPT
from .tools import RetrievalToolbox, SearchResult


@dataclass
class CognitiveState:
    sample: NewsSample
    step: int = 0
    checked_questions: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


class PlanningAgent:
    """A thin interface for planned retrieval and evidence-grounded judgment."""

    def __init__(
        self,
        max_steps: int,
        retrieval_config: dict,
        reasoner_config: dict,
        toolbox: RetrievalToolbox | None = None,
    ) -> None:
        self.max_steps = max_steps
        self.reasoner_config = reasoner_config
        self.system_prompt = reasoner_config.get(
            "system_prompt", FACT_CHECKING_SYSTEM_PROMPT
        )
        self.toolbox = toolbox or RetrievalToolbox(retrieval_config)

    def verify(self, sample: NewsSample) -> tuple[Verdict, list[EvidenceItem], str]:
        state = CognitiveState(sample=sample)
        evidence_chain: list[EvidenceItem] = []

        while state.step < self.max_steps and not self.should_terminate(state):
            subproblem = self.generate_subproblem(state)
            tool_name, query, observations = self.select_and_execute(state, subproblem)
            conclusion = self.analyze(subproblem, observations)
            evidence_chain.append(
                EvidenceItem(
                    subproblem=subproblem,
                    tool=tool_name,
                    query=query,
                    observations=[item.snippet for item in observations],
                    conclusion=conclusion,
                )
            )
            self.update_state(state, subproblem, conclusion)

        return self.synthesize_verdict(state, evidence_chain)

    def should_terminate(self, state: CognitiveState) -> bool:
        return bool(state.notes and "enough evidence" in state.notes[-1].lower())

    def generate_subproblem(self, state: CognitiveState) -> str:
        plan = [
            "Verify whether the image provenance matches the claimed event.",
            "Verify whether the named event actually happened as described.",
            "Verify whether entities, time, and location are supported by independent sources.",
        ]
        return plan[min(state.step, len(plan) - 1)]

    def select_and_execute(
        self,
        state: CognitiveState,
        subproblem: str,
    ) -> tuple[str, str, list[SearchResult]]:
        if "image provenance" in subproblem:
            results = self.toolbox.reverse_image_search(state.sample.image_path)
            return "reverse_image_search", state.sample.image_path, results

        query = f"{state.sample.text} {subproblem}"
        results = self.toolbox.keyword_search(query)
        return "keyword_search", query, results

    def analyze(self, subproblem: str, observations: list[SearchResult]) -> str:
        # TODO: Replace with GPT-4o/Qwen/LLaVA evidence analysis from `3_news`.
        if not observations:
            return "No supporting evidence found."
        return f"Placeholder analysis for: {subproblem}"

    def update_state(self, state: CognitiveState, subproblem: str, conclusion: str) -> None:
        state.checked_questions.append(subproblem)
        state.notes.append(conclusion)
        state.step += 1

    def synthesize_verdict(
        self,
        state: CognitiveState,
        evidence_chain: list[EvidenceItem],
    ) -> tuple[Verdict, list[EvidenceItem], str]:
        # TODO: Implement entailment-style final synthesis:
        # Real only if image, event, entities, time, and location are all verified.
        explanation = "Stage II completed with placeholder planned evidence analysis."
        return Verdict.UNCERTAIN, evidence_chain, explanation
