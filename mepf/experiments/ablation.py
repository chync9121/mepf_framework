"""Ablation switches matching Table 2 in the paper."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AblationSetting:
    name: str
    use_dynamic_gating: bool
    use_visual_forensics: bool
    use_planned_retrieval: bool


ABLATION_SETTINGS = [
    AblationSetting("vanilla_clip", False, False, False),
    AblationSetting("preverify_without_vf", True, False, False),
    AblationSetting("preverify_with_vf", True, True, False),
    AblationSetting("standard_rag", False, False, False),
    AblationSetting("full_mepf", True, True, True),
]
