"""Configuration helpers for the MEPF framework."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class MEPFConfig:
    semantic_threshold_tau: float = 0.55
    forensics_threshold: float = 0.50
    max_planning_steps: int = 3
    semantic_model: dict[str, Any] | None = None
    forensics_model: dict[str, Any] | None = None
    retrieval: dict[str, Any] | None = None
    reasoner: dict[str, Any] | None = None

    @classmethod
    def from_json(cls, path: str | Path) -> "MEPFConfig":
        with Path(path).open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)
