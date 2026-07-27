"""MEPF: Multi-Expert Pre-verification and Planned Fact-retrieval."""

from .pipeline import MEPFPipeline
from .schema import EvidenceItem, MEPFResult, NewsSample, StageOneResult, Verdict

__all__ = [
    "EvidenceItem",
    "MEPFPipeline",
    "MEPFResult",
    "NewsSample",
    "StageOneResult",
    "Verdict",
]
