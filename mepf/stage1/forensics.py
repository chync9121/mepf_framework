"""Visual media forensics analysis.

Replace the placeholder with the NPR/ResNet detector from `2_ai/resnet.py`
and any additional image forensics tools used in the experiments.
"""

from __future__ import annotations

from ..schema import ForensicsResult, NewsSample


class VisualForensicsAnalyzer:
    """Estimate whether an image is generated or manipulated."""

    def __init__(self, model_config: dict) -> None:
        self.model_config = model_config
        self.detectors = {}

    def load(self) -> None:
        """Load NPR detector and optional forensics models."""
        # TODO:
        # 1. from 2_ai.resnet import resnet50
        # 2. load NPR.pth
        # 3. add other detectors if needed: TruFor, Sniffer, etc.
        pass

    def predict(self, sample: NewsSample) -> ForensicsResult:
        """Return p_forged for reliability gating."""
        score = float(sample.metadata.get("p_forged", 0.10))
        return ForensicsResult(
            p_forged=score,
            detector_scores={"npr": score},
            details={"source": "placeholder"},
        )
