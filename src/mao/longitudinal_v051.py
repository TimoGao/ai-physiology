from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List
import csv
import json
import random
import statistics


def clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def slope(values: List[float], window: int = 24) -> float:
    vals = values[-window:]
    if len(vals) < 3:
        return 0.0
    n = len(vals)
    xm = (n - 1) / 2
    ym = statistics.mean(vals)
    num = sum((i - xm) * (y - ym) for i, y in enumerate(vals))
    den = sum((i - xm) ** 2 for i in range(n))
    return 0.0 if den == 0 else num / den


def ewma(values: List[float], alpha: float = 0.18) -> float:
    if not values:
        return 0.0
    x = values[0]
    for value in values[1:]:
        x = alpha * value + (1.0 - alpha) * x
    return x


@dataclass
class Trace:
    seed: int
    degraded: bool
    memory_integrity: List[float]
    tool_reliability: List[float]
    resource_pressure: List[float]
    context_saturation: List[float]
    error_rate: List[float]
    shock_cycle: int
    future_failure: bool


def make_trace(seed: int, cycles: int = 240, degraded: bool = True) -> Trace:
    rng = random.Random(8_310_077 + seed * 97_409 + (1 if degraded else 0))
    mi, tr, rp, cs, er = [], [], [], [], []
    latent = 0.0

    for i in range(cycles):
        progress = i / max(1, cycles - 1)

        if degraded:
            latent += 0.00135 + rng.uniform(-0.00022, 0.00022)
            memory = 0.985 - 0.060 * progress - 0.050 * latent
            tool = 0.985 - 0.055 * progress - 0.035 * latent
            resource = 0.30 + 0.27 * progress + 0.10 * latent
            context = 0.42 + 0.25 * progress + 0.08 * latent
            errors = 0.015 + 0.045 * progress + 0.025 * latent
        else:
            latent = max(0.0, latent + rng.uniform(-0.00010, 0.00010))
            memory = 0.982 + rng.uniform(-0.008, 0.008)
            tool = 0.982 + rng.uniform(-0.008, 0.008)
            resource = 0.32 + rng.uniform(-0.035, 0.035)
            context = 0.44 + rng.uniform(-0.040, 0.040)
            errors = 0.018 + rng.uniform(-0.008, 0.008)

        mi.append(clamp(memory + rng.uniform(-0.004, 0.004)))
        tr.append(clamp(tool + rng.uniform(-0.004, 0.004)))
        rp.append(clamp(resource + rng.uniform(-0.010, 0.010)))
        cs.append(clamp(context + rng.uniform(-0.010, 0.010)))
        er.append(clamp(errors + rng.uniform(-0.004, 0.004)))

    shock_cycle = int(cycles * 0.88)

    if degraded:
        burden = (
            (1.0 - statistics.mean(mi[-40:])) * 2.2
            + (1.0 - statistics.mean(tr[-40:])) * 1.8
            + statistics.mean(rp[-40:]) * 0.9
            + statistics.mean(cs[-40:]) * 0.7
            + statistics.mean(er[-40:]) * 2.5
        )
        failure_probability = clamp((burden - 0.95) / 1.20)
    else:
        failure_probability = 0.03

    future_failure = rng.random() < failure_probability

    return Trace(
        seed=seed,
        degraded=degraded,
        memory_integrity=mi,
        tool_reliability=tr,
        resource_pressure=rp,
        context_saturation=cs,
        error_rate=er,
        shock_cycle=shock_cycle,
        future_failure=future_failure,
    )


class AdaptiveMonitoringBaseline:
    def __init__(self):
        self.history = {k: [] for k in ("mi", "tr", "rp", "cs", "er")}
        self.warning_cycle = None
        self.scores = []

    def observe(self, cycle: int, sample: Dict[str, float]) -> float:
        for key, value in sample.items():
            self.history[key].append(value)

        score = 0.0
        score += max(0.0, -slope(self.history["mi"])) * 55
        score += max(0.0, -slope(self.history["tr"])) * 50
        score += max(0.0, slope(self.history["rp"])) * 35
        score += max(0.0, slope(self.history["cs"])) * 30
        score += max(0.0, slope(self.history["er"])) * 55
        score += max(0.0, 0.94 - ewma(self.history["mi"][-30:])) * 4.0
        score += max(0.0, 0.94 - ewma(self.history["tr"][-30:])) * 3.0
        score += max(0.0, ewma(self.history["rp"][-30:]) - 0.58) * 2.2
        score += max(0.0, ewma(self.history["cs"][-30:]) - 0.68) * 1.8
        score += max(0.0, ewma(self.history["er"][-30:]) - 0.055) * 4.0

        self.scores.append(score)
        if self.warning_cycle is None and score >= 0.22:
            self.warning_cycle = cycle
        return score


class PhysiologyMonitor:
    def __init__(self):
        self.debt = 0.0
        self.reserve = 1.0
        self.debt_history = []
        self.reserve_history = []
        self.warning_cycle = None
        self.scores = []

    def observe(self, cycle: int, sample: Dict[str, float]) -> float:
        burden = 0.0
        burden += max(0.0, 0.975 - sample["mi"]) * 1.6
        burden += max(0.0, 0.975 - sample["tr"]) * 1.3
        burden += max(0.0, sample["rp"] - 0.34) * 0.42
        burden += max(0.0, sample["cs"] - 0.46) * 0.38
        burden += max(0.0, sample["er"] - 0.020) * 1.5

        self.debt = clamp(self.debt * 0.988 + burden * 0.050)
        recovery = 0.003 if self.debt < 0.08 else 0.0
        self.reserve = clamp(
            self.reserve
            + recovery
            - 0.020 * self.debt
            - 0.006 * max(0.0, sample["rp"] - 0.50)
        )

        self.debt_history.append(self.debt)
        self.reserve_history.append(self.reserve)

        debt_trend = max(0.0, slope(self.debt_history, 30))
        reserve_trend = max(0.0, -slope(self.reserve_history, 30))

        score = clamp(
            0.55 * self.debt
            + 0.45 * (1.0 - self.reserve)
            + 8.0 * debt_trend
            + 6.0 * reserve_trend
        )

        self.scores.append(score)
        if self.warning_cycle is None and score >= 0.24:
            self.warning_cycle = cycle
        return score


def auc(labels: List[int], scores: List[float]) -> float:
    positives = [s for y, s in zip(labels, scores) if y == 1]
    negatives = [s for y, s in zip(labels, scores) if y == 0]
    if not positives or not negatives:
        return 0.5

    wins = 0.0
    total = 0
    for p in positives:
        for n in negatives:
            total += 1
            if p > n:
                wins += 1.0
            elif p == n:
                wins += 0.5
    return wins / total


def evaluate(trace: Trace, monitor_name: str) -> Dict[str, Any]:
    monitor = AdaptiveMonitoringBaseline() if monitor_name == "adaptive_monitoring" else PhysiologyMonitor()

    for i in range(len(trace.memory_integrity)):
        monitor.observe(
            i,
            {
                "mi": trace.memory_integrity[i],
                "tr": trace.tool_reliability[i],
                "rp": trace.resource_pressure[i],
                "cs": trace.context_saturation[i],
                "er": trace.error_rate[i],
            },
        )

    warning = monitor.warning_cycle
    warned_before_shock = warning is not None and warning < trace.shock_cycle

    row = {
        "seed": trace.seed,
        "degraded": trace.degraded,
        "future_failure": trace.future_failure,
        "monitor": monitor_name,
        "warning_cycle": warning if warning is not None else len(trace.memory_integrity),
        "warned_before_shock": warned_before_shock,
        "lead_time": trace.shock_cycle - warning if warned_before_shock else 0,
        "final_score": monitor.scores[-1],
    }
    if monitor_name == "physiology":
        row["final_debt"] = monitor.debt
        row["final_recovery_reserve"] = monitor.reserve
    return row


def summarize(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    output = []
    for monitor_name in ("adaptive_monitoring", "physiology"):
        group = [r for r in rows if r["monitor"] == monitor_name]
        failure = [r for r in group if r["future_failure"]]
        nonfailure = [r for r in group if not r["future_failure"]]
        labels = [1 if r["future_failure"] else 0 for r in group]
        scores = [float(r["final_score"]) for r in group]

        output.append({
            "monitor": monitor_name,
            "n": len(group),
            "future_failures": len(failure),
            "auc_failure_prediction": auc(labels, scores),
            "early_warning_recall": sum(r["warned_before_shock"] for r in failure) / max(1, len(failure)),
            "false_early_warning_rate": sum(r["warned_before_shock"] for r in nonfailure) / max(1, len(nonfailure)),
            "mean_lead_time_on_true_positives": statistics.mean(
                [r["lead_time"] for r in failure if r["warned_before_shock"]] or [0]
            ),
            "mean_final_score_failure": statistics.mean([r["final_score"] for r in failure] or [0]),
            "mean_final_score_nonfailure": statistics.mean([r["final_score"] for r in nonfailure] or [0]),
        })
    return output


def run_benchmark(seeds: Iterable[int] = range(200), cycles: int = 240) -> Dict[str, Any]:
    rows = []
    seed_list = [int(s) for s in seeds]

    for seed in seed_list:
        for degraded in (True, False):
            trace = make_trace(seed, cycles, degraded)
            rows.append(evaluate(trace, "adaptive_monitoring"))
            rows.append(evaluate(trace, "physiology"))

    return {
        "version": "MAO v0.5.1 - Longitudinal Health Benchmark",
        "seeds": seed_list,
        "cycles": cycles,
        "evaluation_rows": rows,
        "summary": summarize(rows),
    }


if __name__ == "__main__":
    result = run_benchmark(range(200))
    out = Path("results/mao-v0.5.1")
    out.mkdir(parents=True, exist_ok=True)

    (out / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    with (out / "evaluation_rows.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fields = sorted({k for row in result["evaluation_rows"] for k in row})
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result["evaluation_rows"])

    with (out / "summary.csv").open("w", newline="", encoding="utf-8-sig") as f:
        fields = sorted({k for row in result["summary"] for k in row})
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result["summary"])

    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
