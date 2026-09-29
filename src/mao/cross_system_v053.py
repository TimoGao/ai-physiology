from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List
import csv
import json
import math
import random
import statistics

MONITORS = ("adaptive", "debt_only", "reserve_only", "debt_reserve")
FPR_BUDGETS = (0.05, 0.10, 0.20)


def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


@dataclass
class CrossSystemTrace:
    seed: int
    memory_integrity: List[float]
    tool_reliability: List[float]
    resource_pressure: List[float]
    context_saturation: List[float]
    error_rate: List[float]
    shock_cycle: int
    future_failure: bool
    latent_severity: float
    latent_recovery_capacity: float


def make_trace(seed: int, cycles: int = 240) -> CrossSystemTrace:
    rng = random.Random(53_000_003 + seed * 1_000_003)

    severity = rng.betavariate(2.2, 2.6)
    recovery_capacity = rng.betavariate(2.5, 2.0)
    coupling = 0.65 + 0.35 * rng.random()

    mi, tr, rp, cs, er = [], [], [], [], []
    latent = 0.0

    for i in range(cycles):
        p = i / max(1, cycles - 1)
        latent += 0.00055 + 0.00100 * severity + rng.uniform(-0.00010, 0.00010)

        memory = 0.985 - (0.018 + 0.036 * severity) * p - 0.030 * latent * coupling
        tool = 0.985 - (0.015 + 0.032 * severity) * p - 0.022 * latent * coupling
        resource = 0.30 + (0.085 + 0.145 * severity) * p + 0.055 * latent * coupling
        context = 0.42 + (0.075 + 0.135 * severity) * p + 0.045 * latent * coupling
        errors = 0.015 + (0.010 + 0.026 * severity) * p + 0.012 * latent * coupling

        recovery_wave = recovery_capacity * 0.012 * max(
            0.0, math.sin((i / cycles) * math.pi * 4)
        )
        memory += recovery_wave * 0.55
        tool += recovery_wave * 0.45
        resource -= recovery_wave * 0.75
        context -= recovery_wave * 0.55
        errors -= recovery_wave * 0.40

        mi.append(clamp(memory + rng.uniform(-0.004, 0.004)))
        tr.append(clamp(tool + rng.uniform(-0.004, 0.004)))
        rp.append(clamp(resource + rng.uniform(-0.009, 0.009)))
        cs.append(clamp(context + rng.uniform(-0.009, 0.009)))
        er.append(clamp(errors + rng.uniform(-0.0035, 0.0035)))

    shock_cycle = int(cycles * 0.88)
    tail = slice(shock_cycle - 36, shock_cycle)

    recent_burden = (
        (1.0 - statistics.mean(mi[tail])) * 1.45
        + (1.0 - statistics.mean(tr[tail])) * 1.25
        + statistics.mean(rp[tail]) * 0.62
        + statistics.mean(cs[tail]) * 0.48
        + statistics.mean(er[tail]) * 1.75
    )
    latent_risk = (
        0.80 * severity
        + 0.45 * (1.0 - recovery_capacity)
        + 0.20 * coupling
    )
    failure_probability = clamp((recent_burden + latent_risk - 1.18) / 1.05)
    future_failure = rng.random() < failure_probability

    return CrossSystemTrace(
        seed=seed,
        memory_integrity=mi,
        tool_reliability=tr,
        resource_pressure=rp,
        context_saturation=cs,
        error_rate=er,
        shock_cycle=shock_cycle,
        future_failure=future_failure,
        latent_severity=severity,
        latent_recovery_capacity=recovery_capacity,
    )


class AdaptiveMonitor:
    def __init__(self):
        self.ewma = {k: None for k in ("mi", "tr", "rp", "cs", "er")}
        self.history = {k: [] for k in self.ewma}
        self.scores: List[float] = []

    def observe(self, s: Dict[str, float]) -> float:
        for k, v in s.items():
            self.ewma[k] = v if self.ewma[k] is None else 0.18 * v + 0.82 * self.ewma[k]
            self.history[k].append(self.ewma[k])

        def trend(k: str) -> float:
            arr = self.history[k]
            if len(arr) < 25:
                return 0.0
            return (arr[-1] - arr[-25]) / 24.0

        score = 0.0
        score += max(0.0, -trend("mi")) * 55
        score += max(0.0, -trend("tr")) * 50
        score += max(0.0, trend("rp")) * 35
        score += max(0.0, trend("cs")) * 30
        score += max(0.0, trend("er")) * 55
        score += max(0.0, 0.94 - self.ewma["mi"]) * 4.0
        score += max(0.0, 0.94 - self.ewma["tr"]) * 3.0
        score += max(0.0, self.ewma["rp"] - 0.58) * 2.2
        score += max(0.0, self.ewma["cs"] - 0.68) * 1.8
        score += max(0.0, self.ewma["er"] - 0.055) * 4.0

        self.scores.append(clamp(score))
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
            max(0.0, 0.975 - s["mi"]) * 1.45
            + max(0.0, 0.975 - s["tr"]) * 1.20
            + max(0.0, s["rp"] - 0.34) * 0.38
            + max(0.0, s["cs"] - 0.46) * 0.34
            + max(0.0, s["er"] - 0.020) * 1.35
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

        debt_trend = 0.0
        reserve_trend = 0.0
        if len(self.debt_history) >= 30:
            debt_trend = max(
                0.0,
                (self.debt_history[-1] - self.debt_history[-30]) / 29.0,
            )
            reserve_trend = max(
                0.0,
                (self.reserve_history[-30] - self.reserve_history[-1]) / 29.0,
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


def score_trace(trace: CrossSystemTrace, monitor_name: str) -> List[float]:
    monitor: Any = (
        AdaptiveMonitor()
        if monitor_name == "adaptive"
        else PhysiologyMonitor(monitor_name)
    )

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
    if total_pos == 0:
        return 0.0
    paired = sorted(zip(scores, labels), reverse=True)
    tp = fp = 0
    prev_recall = ap = 0.0
    for score, label in paired:
        if label:
            tp += 1
        else:
            fp += 1
        recall = tp / total_pos
        precision = tp / max(1, tp + fp)
        ap += (recall - prev_recall) * precision
        prev_recall = recall
    return ap


def build_rows(seeds: Iterable[int], cycles: int = 240) -> List[Dict[str, Any]]:
    rows = []
    for seed in seeds:
        trace = make_trace(int(seed), cycles)
        for monitor in MONITORS:
            scores = score_trace(trace, monitor)
            rows.append({
                "seed": int(seed),
                "monitor": monitor,
                "future_failure": trace.future_failure,
                "shock_cycle": trace.shock_cycle,
                "final_score": scores[trace.shock_cycle - 1],
                "score_history": scores,
                "latent_severity": trace.latent_severity,
                "latent_recovery_capacity": trace.latent_recovery_capacity,
            })
    return rows


def threshold_for_fpr(rows: List[Dict[str, Any]], monitor: str, budget: float) -> float:
    negatives = sorted(
        r["final_score"]
        for r in rows
        if r["monitor"] == monitor and not r["future_failure"]
    )
    if not negatives:
        return 1.0
    idx = max(
        0,
        min(
            len(negatives) - 1,
            math.ceil((1.0 - budget) * len(negatives)) - 1,
        ),
    )
    return negatives[idx]


def evaluate_threshold(
    rows: List[Dict[str, Any]],
    monitor: str,
    threshold: float,
) -> Dict[str, float]:
    group = [r for r in rows if r["monitor"] == monitor]
    tp = fp = tn = fn = 0
    leads = []

    for r in group:
        pred = r["final_score"] >= threshold
        actual = bool(r["future_failure"])
        if pred and actual:
            tp += 1
        elif pred and not actual:
            fp += 1
        elif not pred and actual:
            fn += 1
        else:
            tn += 1

        if actual:
            warning = next(
                (
                    i
                    for i, score in enumerate(r["score_history"][: r["shock_cycle"]])
                    if score >= threshold
                ),
                None,
            )
            if warning is not None:
                leads.append(r["shock_cycle"] - warning)

    return {
        "threshold": threshold,
        "recall": tp / max(1, tp + fn),
        "precision": tp / max(1, tp + fp),
        "fpr": fp / max(1, fp + tn),
        "mean_lead_time": statistics.mean(leads) if leads else 0.0,
    }


def run_benchmark(
    calibration_seeds: Iterable[int] = range(500),
    evaluation_seeds: Iterable[int] = range(500, 1000),
    cycles: int = 240,
) -> Dict[str, Any]:
    calibration = build_rows(calibration_seeds, cycles)
    evaluation = build_rows(evaluation_seeds, cycles)

    summary = []
    for monitor in MONITORS:
        group = [r for r in evaluation if r["monitor"] == monitor]
        labels = [1 if r["future_failure"] else 0 for r in group]
        scores = [float(r["final_score"]) for r in group]
        row: Dict[str, Any] = {
            "monitor": monitor,
            "n": len(group),
            "failures": sum(labels),
            "roc_auc": roc_auc(labels, scores),
            "pr_auc": average_precision(labels, scores),
        }

        for budget in FPR_BUDGETS:
            threshold = threshold_for_fpr(calibration, monitor, budget)
            metrics = evaluate_threshold(evaluation, monitor, threshold)
            tag = f"fpr{int(budget * 100)}"
            for k, v in metrics.items():
                row[f"{tag}_{k}"] = v

        summary.append(row)

    return {
        "version": "MAO v0.5.3 - Cross-System Degradation Validation",
        "calibration_seeds": list(calibration_seeds),
        "evaluation_seeds": list(evaluation_seeds),
        "cycles": cycles,
        "summary": summary,
    }


def export_results(result: Dict[str, Any], output_dir: str | Path) -> Dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "results.json"
    summary_path = out / "summary.csv"

    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    fields = sorted({k for row in result["summary"] for k in row})
    with summary_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result["summary"])

    return {"json": str(json_path), "summary": str(summary_path)}
