from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List
import csv
import json
import math
import statistics

from .experiment import EXPERIMENTS


@dataclass
class MetricSummary:
    n: int
    mean: float
    stdev: float
    minimum: float
    maximum: float

    def as_dict(self) -> Dict[str, float]:
        return {
            "n": self.n,
            "mean": round(self.mean, 6),
            "stdev": round(self.stdev, 6),
            "min": round(self.minimum, 6),
            "max": round(self.maximum, 6),
        }


def _flatten(prefix: str, value: Any, out: Dict[str, Any]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else key
            _flatten(next_prefix, child, out)
    else:
        out[prefix] = value


def flatten_result(result: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    _flatten("", result, out)
    return out


def _numeric(values: Iterable[Any]) -> List[float]:
    out: List[float] = []
    for value in values:
        if isinstance(value, bool):
            out.append(float(value))
        elif isinstance(value, (int, float)) and math.isfinite(float(value)):
            out.append(float(value))
    return out


def summarize_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {}

    flattened = [flatten_result(row) for row in rows]
    keys = sorted({key for row in flattened for key in row})
    summary: Dict[str, Any] = {}

    for key in keys:
        values = _numeric(row.get(key) for row in flattened)
        if len(values) != len(rows):
            continue
        summary[key] = MetricSummary(
            n=len(values),
            mean=statistics.mean(values),
            stdev=statistics.stdev(values) if len(values) > 1 else 0.0,
            minimum=min(values),
            maximum=max(values),
        ).as_dict()

    return summary


def run_repeated_experiment(
    experiment_name: str,
    seeds: Iterable[int],
    baseline_kind: str = "strong",
    **kwargs: Any,
) -> Dict[str, Any]:
    if experiment_name not in EXPERIMENTS:
        raise KeyError(f"unknown experiment: {experiment_name}")

    runner = EXPERIMENTS[experiment_name]
    runs: List[Dict[str, Any]] = []

    for seed in seeds:
        result = runner(seed=int(seed), baseline_kind=baseline_kind, **kwargs)
        result["seed"] = int(seed)
        runs.append(result)

    return {
        "experiment": experiment_name,
        "baseline_kind": baseline_kind,
        "seeds": [int(x) for x in seeds],
        "runs": runs,
        "summary": summarize_rows(runs),
    }


def run_experiment_matrix(
    seeds: Iterable[int] = range(10),
    baseline_kinds: Iterable[str] = ("naive", "strong"),
) -> Dict[str, Any]:
    seed_list = [int(x) for x in seeds]
    results: Dict[str, Any] = {
        "version": "MAO Experiment v0.3",
        "seeds": seed_list,
        "comparisons": {},
    }

    for baseline_kind in baseline_kinds:
        baseline_block: Dict[str, Any] = {}
        for experiment_name in EXPERIMENTS:
            baseline_block[experiment_name] = run_repeated_experiment(
                experiment_name,
                seeds=seed_list,
                baseline_kind=baseline_kind,
            )
        results["comparisons"][baseline_kind] = baseline_block

    return results


def export_json(result: Dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def export_csv(result: Dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows: List[Dict[str, Any]] = []
    for baseline_kind, experiments in result["comparisons"].items():
        for experiment_name, block in experiments.items():
            for run in block["runs"]:
                row = flatten_result(run)
                row["matrix.baseline_kind"] = baseline_kind
                row["matrix.experiment"] = experiment_name
                rows.append(row)

    fieldnames = sorted({key for row in rows for key in row})

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return path


def build_comparison_table(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return a compact table for human review.

    The table intentionally focuses on a few interpretable metrics instead of
    every exported field.
    """
    rows: List[Dict[str, Any]] = []

    metric_map = {
        "context_obesity": [
            "baseline.duplicate_ratio",
            "mao.duplicate_ratio",
            "mao.context_saturation",
            "mao.homeostatic_debt",
        ],
        "memory_contamination": [
            "baseline.duplicate_ratio",
            "mao.memory_integrity",
            "mao.homeostatic_debt",
        ],
        "tool_deterioration": [
            "baseline.failures",
            "mao.tool_reliability",
            "mao.recovery_reserve",
        ],
        "resource_pressure": [
            "mao.resource_pressure",
            "mao.regulation_events",
        ],
        "malicious_payload": [
            "baseline.memory_size",
            "mao.blood.quarantined",
        ],
        "chronic_degradation": [
            "baseline.duplicate_ratio",
            "mao.homeostatic_debt",
            "mao.recovery_reserve",
        ],
    }

    for baseline_kind, experiments in result["comparisons"].items():
        for experiment_name, block in experiments.items():
            row: Dict[str, Any] = {
                "baseline_kind": baseline_kind,
                "experiment": experiment_name,
            }
            for metric in metric_map[experiment_name]:
                stat = block["summary"].get(metric)
                row[metric] = None if not stat else stat["mean"]
            rows.append(row)

    return rows
