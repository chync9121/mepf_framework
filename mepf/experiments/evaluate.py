"""Evaluation skeleton for NewsCLIPpings and MMFakeBench."""

from __future__ import annotations

from collections.abc import Iterable

from ..pipeline import MEPFPipeline
from ..schema import MEPFResult, NewsSample


def evaluate_dataset(pipeline: MEPFPipeline, samples: Iterable[NewsSample]) -> list[MEPFResult]:
    """Run full MEPF inference and return per-sample results."""
    return [pipeline.run(sample) for sample in samples]


def compute_metrics(results: list[MEPFResult], labels: list[int]) -> dict[str, float]:
    """Placeholder for Accuracy, F1, class-wise F1, and confusion matrix."""
    # TODO: Map Verdict to label and call sklearn.metrics.
    return {"accuracy": 0.0, "f1": 0.0}
