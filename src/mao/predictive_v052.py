from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List
import csv
import json
import math
import random
import statistics

SHAPES = ("healthy", "linear", "stepwise", "relapse", "single_organ", "cross_variable")
MONITORS = ("adaptive", "debt_only", "reserve_only", "debt_reserve")
FPR_BUDGETS = (0.05, 0.10, 0.20)


def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


@dataclass
class Trace:
    seed: int
    shape: str
    memory_integrity: List[float]
    tool_reliability: List[float]
    resource_pressure: List[float]
    context_saturation: List[float]
    error_rate: List[float]
    shock_cycle: int
    future_failure: bool


def make_trace(seed: int, shape: str, cycles: int = 240) -> Trace:
    rng = random.Random(19_000_003 + seed * 100_003 + SHAPES.index(shape) * 97_409)
    mi, tr, rp, cs, er = [], [], [], [], []
    latent = 0.0

    for i in range(cycles):
        p = i / max(1, cycles - 1)
        memory, tool, resource, context, errors = 0.982, 0.982, 0.33, 0.44, 0.018

        if shape == "healthy":
            memory += rng.uniform(-0.007, 0.007)
            tool += rng.uniform(-0.007, 0.007)
            resource += rng.uniform(-0.035, 0.035)
            context += rng.uniform(-0.040, 0.040)
            errors += rng.uniform(-0.007, 0.007)

        elif shape == "linear":
            latent += 0.0012 + rng.uniform(-0.0002, 0.0002)
            memory -= 0.050 * p + 0.035 * latent
            tool -= 0.045 * p + 0.025 * latent
            resource += 0.22 * p + 0.08 * latent
            context += 0.20 * p + 0.06 * latent
            errors += 0.035 * p + 0.018 * latent

        elif shape == "stepwise":
            stage = 0 if p < 0.35 else (1 if p < 0.70 else 2)
            step = (0.0, 0.35, 0.80)[stage]
            latent += 0.0006 + 0.00035 * stage + rng.uniform(-0.00015, 0.00015)
            memory -= 0.032 * step + 0.030 * latent
            tool -= 0.028 * step + 0.020 * latent
            resource += 0.15 * step + 0.060 * latent
            context += 0.14 * step + 0.050 * latent
            errors += 0.025 * step + 0.015 * latent

        elif shape == "relapse":
            if p < 0.40:
                d = p / 0.40
            elif p < 0.65:
                d = 1.0 - ((p - 0.40) / 0.25) * 0.65
            else:
                d = 0.35 + ((p - 0.65) / 0.35) * 0.90
            latent = max(0.0, latent + 0.0008 * d + rng.uniform(-0.00015, 0.00015))
            memory -= 0.050 * d + 0.025 * latent
            tool -= 0.040 * d + 0.020 * latent
            resource += 0.18 * d + 0.060 * latent
            context += 0.17 * d + 0.050 * latent
            errors += 0.032 * d + 0.015 * latent

        elif shape == "single_organ":
            latent += 0.0013 + rng.uniform(-0.0002, 0.0002)
            memory -= 0.075 * p + 0.055 * latent
            tool -= 0.010 * p
            resource += 0.045 * p
            context += 0.060 * p
            errors += 0.018 * p

        elif shape == "cross_variable":
            latent += 0.0010 + rng.uniform(-0.00018, 0.00018)
            memory -= 0.030 * p + 0.020 * latent
            tool -= 0.028 * p + 0.018 * latent
            resource += 0.14 * p + 0.050 * latent
            context += 0.12 * p + 0.040 * latent
            errors += 0.025 * p + 0.012 * latent

        else:
            raise KeyError(shape)

        mi.append(clamp(memory + rng.uniform(-0.004, 0.004)))
        tr.append(clamp(tool + rng.uniform(-0.004, 0.004)))
        rp.append(clamp(resource + rng.uniform(-0.009, 0.009)))
        cs.append(clamp(context + rng.uniform(-0.009, 0.009)))
        er.append(clamp(errors + rng.uniform(-0.0035, 0.0035)))

    shock_cycle = int(cycles * 0.88)
    tail = slice(-36, None)
    burden = (
        (1.0 - statistics.mean(mi[tail])) * 1.7
        + (1.0 - statistics.mean(tr[tail])) * 1.5
        + statistics.mean(rp[tail]) * 0.7
        + statistics.mean(cs[tail]) * 0.55
        + statistics.mean(er[tail]) * 2.1
    )
    susceptibility = {
        "healthy": -0.22,
        "linear": 0.10,
        "stepwise": 0.12,
        "relapse": 0.18,
        "single_organ": 0.06,
        "cross_variable": 0.15,
    }[shape]
    failure_probability = clamp((burden + susceptibility - 0.68) / 0.90)
    future_failure = rng.random() < failure_probability

    return Trace(seed, shape, mi, tr, rp, cs, er, shock_cycle, future_failure)


class AdaptiveMonitor:
    def __init__(self):
        self.history = {k: [] for k in ("mi", "tr", "rp", "cs", "er")}
        self.ewma = {k: None for k in self.history}
        self.scores: List[float] = []

    def observe(self, sample: Dict[str, float]) -> float:
        for k, v in sample.items():
            self.ewma[k] = v if self.ewma[k] is None else 0.18 * v + 0.82 * self.ewma[k]
            self.history[k].append(self.ewma[k])

        def trend(k: str) -> float:
            arr = self.history[k]
            return 0.0 if len(arr) < 25 else (arr[-1] - arr[-25]) / 24.0

        s = 0.0
        s += max(0.0, -trend("mi")) * 55
        s += max(0.0, -trend("tr")) * 50
        s += max(0.0, trend("rp")) * 35
        s += max(0.0, trend("cs")) * 30
        s += max(0.0, trend("er")) * 55
        s += max(0.0, 0.94 - self.ewma["mi"]) * 4.0
        s += max(0.0, 0.94 - self.ewma["tr"]) * 3.0
        s += max(0.0, self.ewma["rp"] - 0.58) * 2.2
        s += max(0.0, self.ewma["cs"] - 0.68) * 1.8
        s += max(0.0, self.ewma["er"] - 0.055) * 4.0
        self.scores.append(clamp(s))
        return self.scores[-1]


class PhysiologyMonitor:
    def __init__(self, mode: str):
        self.mode = mode
        self.debt = 0.0
        self.reserve = 1.0
        self.debt_history: List[float] = []
        self.reserve_history: List[float] = []
        self.scores: List[float] = []

    def observe(self, s: Dict[str, float]) -> float:
        burden = (
            max(0.0, 0.975 - s["mi"]) * 1.5
            + max(0.0, 0.975 - s["tr"]) * 1.2
            + max(0.0, s["rp"] - 0.34) * 0.38
            + max(0.0, s["cs"] - 0.46) * 0.34
            + max(0.0, s["er"] - 0.020) * 1.4
        )
        self.debt = clamp(self.debt * 0.989 + burden * 0.047)
        self.reserve = clamp(
            self.reserve
            + (0.003 if self.debt < 0.08 else 0.0)
            - 0.018 * self.debt
            - 0.0055 * max(0.0, s["rp"] - 0.50)
        )
        self.debt_history.append(self.debt)
        self.reserve_history.append(self.reserve)

        debt_trend = 0.0 if len(self.debt_history) < 30 else max(
            0.0, (self.debt_history[-1] - self.debt_history[-30]) / 29.0
        )
        reserve_trend = 0.0 if len(self.reserve_history) < 30 else max(
            0.0, (self.reserve_history[-30] - self.reserve_history[-1]) / 29.0
        )

        if self.mode == "debt_only":
            score = 0.82 * self.debt + 10.0 * debt_trend
        elif self.mode == "reserve_only":
            score = 0.90 * (1.0 - self.reserve) + 8.0 * reserve_trend
        else:
            score = (
                0.52 * self.debt
                + 0.48 * (1.0 - self.reserve)
                + 7.0 * debt_trend
                + 5.0 * reserve_trend
            )

        self.scores.append(clamp(score))
        return self.scores[-1]


def score_trace(trace: Trace, monitor_name: str) -> List[float]:
    monitor: Any = AdaptiveMonitor() if monitor_name == "adaptive" else PhysiologyMonitor(monitor_name)
    for i in range(len(trace.memory_integrity)):
        monitor.observe({
            "mi": trace.memory_integrity[i],
            "tr": trace.tool_reliability[i],
            "rp": trace.resource_pressure[i],
            "cs": trace.context_saturation[i],
            "er": trace.error_rate[i],
        })
    return monitor.scores


def roc_auc(labels: List[int], scores: List[float]) -> float:
    positives = [s for y, s in zip(labels, scores) if y]
    negatives = [s for y, s in zip(labels, scores) if not y]
    if not positives or not negatives:
        return 0.5
    wins = 0.0
    for p in positives:
        for n in negatives:
            wins += 1.0 if p > n else (0.5 if p == n else 0.0)
    return wins / (len(positives) * len(negatives))


def average_precision(labels: List[int], scores: List[float]) -> float:
    total_pos = sum(labels)
    if not total_pos:
        return 0.0
    groups: Dict[float, List[int]] = {}
    for score, label in zip(scores, labels):
        slot = groups.setdefault(score, [0, 0])
        slot[0 if label else 1] += 1
    tp = fp = 0
    previous_recall = ap = 0.0
    for threshold in sorted(groups, reverse=True):
        p, n = groups[threshold]
        tp += p
        fp += n
        recall = tp / total_pos
        precision = tp / max(1, tp + fp)
        ap += (recall - previous_recall) * precision
        previous_recall = recall
    return ap


def threshold_for_fpr(rows: List[Dict[str, Any]], monitor: str, budget: float) -> float:
    negatives = sorted(r["final_score"] for r in rows if r["monitor"] == monitor and not r["future_failure"])
    index = max(0, min(len(negatives) - 1, math.ceil((1.0 - budget) * len(negatives)) - 1))
    return negatives[index]


def threshold_metrics(rows: List[Dict[str, Any]], monitor: str, threshold: float) -> Dict[str, float]:
    group = [r for r in rows if r["monitor"] == monitor]
    tp = fp = tn = fn = 0
    leads: List[int] = []

    for r in group:
        pred = r["final_score"] >= threshold
        if pred and r["future_failure"]:
            tp += 1
        elif pred:
            fp += 1
        elif r["future_failure"]:
            fn += 1
        else:
            tn += 1

        if r["future_failure"]:
            warning = next((i for i, score in enumerate(r["score_history"][:r["shock_cycle"]]) if score >= threshold), None)
            if warning is not None:
                leads.append(r["shock_cycle"] - warning)

    return {
        "threshold": threshold,
        "recall": tp / max(1, tp + fn),
        "precision": tp / max(1, tp + fp),
        "fpr": fp / max(1, fp + tn),
        "mean_lead_time": statistics.mean(leads) if leads else 0.0,
    }


def build_rows(seeds: Iterable[int], cycles: int = 240) -> List[Dict[str, Any]]:
    rows = []
    for seed in seeds:
        for shape in SHAPES:
            trace = make_trace(int(seed), shape, cycles)
            for monitor in MONITORS:
                scores = score_trace(trace, monitor)
                rows.append({
                    "seed": int(seed),
                    "shape": shape,
                    "future_failure": trace.future_failure,
                    "monitor": monitor,
                    "shock_cycle": trace.shock_cycle,
                    "final_score": scores[trace.shock_cycle - 1],
                    "score_history": scores,
                })
    return rows


def run_benchmark(
    calibration_seeds: Iterable[int] = range(200),
    evaluation_seeds: Iterable[int] = range(200, 400),
    cycles: int = 240,
) -> Dict[str, Any]:
    calibration = build_rows(calibration_seeds, cycles)
    evaluation = build_rows(evaluation_seeds, cycles)

    summary = []
    per_shape = []

    for monitor in MONITORS:
        group = [r for r in evaluation if r["monitor"] == monitor]
        labels = [1 if r["future_failure"] else 0 for r in group]
        scores = [float(r["final_score"]) for r in group]
        item: Dict[str, Any] = {
            "monitor": monitor,
            "roc_auc": roc_auc(labels, scores),
            "pr_auc": average_precision(labels, scores),
        }
        for budget in FPR_BUDGETS:
            threshold = threshold_for_fpr(calibration, monitor, budget)
            metrics = threshold_metrics(evaluation, monitor, threshold)
            tag = f"fpr{int(budget * 100)}"
            for k, v in metrics.items():
                item[f"{tag}_{k}"] = v
        summary.append(item)

        for shape in SHAPES[1:]:
            shaped = [r for r in group if r["shape"] == shape]
            y = [1 if r["future_failure"] else 0 for r in shaped]
            s = [float(r["final_score"]) for r in shaped]
            per_shape.append({
                "shape": shape,
                "monitor": monitor,
                "roc_auc": roc_auc(y, s),
                "pr_auc": average_precision(y, s),
                "failures": sum(y),
                "n": len(y),
            })

    return {
        "version": "MAO v0.5.2 - Predictive Validity & Calibration",
        "calibration_seeds": list(calibration_seeds),
        "evaluation_seeds": list(evaluation_seeds),
        "cycles": cycles,
        "shapes": list(SHAPES),
        "summary": summary,
        "per_shape": per_shape,
    }


def export_results(result: Dict[str, Any], output_dir: str | Path) -> Dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "results.json"
    summary_path = out / "summary.csv"
    shape_path = out / "per_shape.csv"

    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_csv(summary_path, result["summary"])
    _write_csv(shape_path, result["per_shape"])
    return {"json": str(json_path), "summary": str(summary_path), "per_shape": str(shape_path)}


def _write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    fields = sorted({k for row in rows for k in row}) if rows else []
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
