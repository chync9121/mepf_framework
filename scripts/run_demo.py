#!/usr/bin/env python
"""Run one sample through the lightweight MEPF framework."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mepf.config import MEPFConfig
from mepf.pipeline import MEPFPipeline
from mepf.schema import NewsSample


def load_sample(path: Path) -> NewsSample:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return NewsSample(
        id=data["id"],
        text=data["text"],
        image_path=data["image_path"],
        metadata=data.get("metadata", {}),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to a sample JSON file.")
    parser.add_argument(
        "--config",
        default=str(ROOT / "configs" / "default.json"),
        help="Path to the MEPF config JSON file.",
    )
    args = parser.parse_args()

    config = MEPFConfig.from_json(args.config)
    sample = load_sample(Path(args.input))
    result = MEPFPipeline(config).run(sample)

    print(json.dumps(result, default=lambda obj: getattr(obj, "value", obj.__dict__), indent=2))


if __name__ == "__main__":
    main()
