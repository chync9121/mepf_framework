"""Shared data structures used across the MEPF pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Verdict(str, Enum):
    REAL = "real"
    FAKE = "fake"
    UNCERTAIN = "uncertain"


@dataclass
class NewsSample:
    id: str
    text: str
    image_path: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SemanticResult:
    p_inconsistent: float
    s_pre: float | None = None
    s_fused: float | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ForensicsResult:
    p_forged: float
    detector_scores: dict[str, float] = field(default_factory=dict)
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class StageOneResult:
    semantic: SemanticResult
    forensics: ForensicsResult
    should_intercept: bool
    reason: str


@dataclass
class EvidenceItem:
    subproblem: str
    tool: str
    query: str
    observations: list[str]
    conclusion: str


@dataclass
class MEPFResult:
    sample_id: str
    verdict: Verdict
    stage_one: StageOneResult
    evidence_chain: list[EvidenceItem] = field(default_factory=list)
    explanation: str = ""
