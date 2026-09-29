from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
import csv
import json
import math
import statistics
import time

from .experiment_v04 import (
    SCENARIOS,
    duplicate_ratio,
    make_trace,
    memory_integrity,
    scenario_cycles,
)
from .reliability import ReliabilityPolicy, ReliabilitySubstrate


VARIANTS = (
    "reliability_only",
    "reliability_plus_physiology",
)


class BaseReliableAgent:
    """Shared reliability substrate for both v0.5 variants."""

    def __init__(self):
        self.memory: List[Dict[str, Any]] = []
        self.reliability = ReliabilitySubstrate(
            ReliabilityPolicy(
                max_retries=2,
                timeout_ms=500.0,
                failure_threshold=3,
                cooldown_cycles=3,
                fallback_enabled=True,
                fallback_reliability=0.88,
            )
        )
        self.primary_reliability = 0.98
        self.task_successes = 0
        self.task_failures = 0
        self.critical_tasks = 0
        self.critical_successes = 0
        self.skipped_low_priority = 0
        self.blocked_payloads = 0
        self.maintenance_actions = 0

    def ingest(
        self,
        value: Any,
        confidence: float,
        risk: float,
        contaminant: bool = False,
    ) -> bool:
        if risk >= 0.8 or confidence < 0.5:
            self.blocked_payloads += 1
            return False
        self.memory.append(
            {
                "value": value,
                "confidence": confidence,
                "risk": risk,
                "contaminant": contaminant,
            }
        )
        return True

    def cleanup(self) -> None:
        before = len(self.memory)
        seen = set()
        clean = []
        for rec in reversed(self.memory):
            key = repr(rec["value"])
            if key in seen:
                continue
            if rec["confidence"] < 0.55:
                continue
            seen.add(key)
            clean.append(rec)
        self.memory = list(reversed(clean))
        if len(self.memory) != before:
            self.maintenance_actions += 1

    def degrade_tool(self, amount: float) -> None:
        self.primary_reliability = max(
            0.0, self.primary_reliability - amount
        )

    def _latency_trace(self, draws: List[float]) -> List[float]:
        # Deterministic synthetic latency derived from the same shared trace.
        return [120.0 + 700.0 * x for x in draws]

    def _fallback_draw(self, draws: List[float]) -> float:
        return (draws[-1] * 0.731 + 0.123) % 1.0

    def execute_task(
        self,
        cycle: int,
        task: Dict[str, Any],
        draws: List[float],
    ) -> bool:
        outcome = self.reliability.execute_from_trace(
            cycle=cycle,
            payload=task,
            primary_reliability=self.primary_reliability,
            primary_draws=draws,
            latency_ms=self._latency_trace(draws),
            fallback_draw=self._fallback_draw(draws),
        )
        ok = outcome.ok
        if ok:
            self.task_successes += 1
        else:
            self.task_failures += 1
        self.ingest(
            {"task": cycle, "ok": ok, "route": outcome.route},
            confidence=0.98 if ok else 0.55,
            risk=0.02,
            contaminant=False,
        )
        return ok


class ReliabilityOnlyAgent(BaseReliableAgent):
    """Conventional engineering baseline with the same reliability substrate."""

    def __init__(self):
        super().__init__()
        self.monitor_alerts = 0

    def cycle(self, i: int, trace, scenario: str) -> None:
        pressure = trace.resource_pressure[i]
        priority = trace.priorities[i]
        if priority == "critical":
            self.critical_tasks += 1

        # Same load-shedding rule used by the physiology agent.
        if pressure > 0.90 and priority == "low":
            self.skipped_low_priority += 1
            return

        ok = self.execute_task(i, {"task": i}, trace.tool_uniforms[i])
        if ok and priority == "critical":
            self.critical_successes += 1

        # Ordinary engineering maintenance, not physiology.
        saturation = min(1.0, len(self.memory) / 100.0)
        integrity = memory_integrity(self.memory)
        if saturation > 0.90 or integrity < 0.80:
            self.cleanup()
            self.monitor_alerts += 1


class ReliablePhysiologyAgent(BaseReliableAgent):
    """Same reliability substrate plus the minimum physiology layer."""

    def __init__(self):
        super().__init__()
        self.mode = "normal"
        self.regulation_actions = 0
        self.debt = 0.0
        self.reserve = 1.0
        self.detected_degradation_cycle: int | None = None
        self.health_alert_streak = 0
        self.vital_history: List[Dict[str, float]] = []

    def _vitals(self, pressure: float) -> Dict[str, float]:
        integrity = memory_integrity(self.memory)
        saturation = min(1.0, len(self.memory) / 100.0)
        reliability_health = self.reliability.health()
        primary_failure_pressure = (
            reliability_health["primary_failures"]
            / max(1, reliability_health["calls"])
        )
        tool_health = max(
            0.0,
            min(
                1.0,
                0.5 * self.primary_reliability
                + 0.5 * (1.0 - primary_failure_pressure),
            ),
        )
        return {
            "context_saturation": saturation,
            "memory_integrity": integrity,
            "resource_pressure": pressure,
            "tool_reliability": tool_health,
        }

    def _refresh_health(self, vitals: Dict[str, float]) -> None:
        dup = duplicate_ratio(self.memory)
        integrity = vitals["memory_integrity"]
        failure_pressure = (
            self.reliability.health()["primary_failures"]
            / max(1, self.reliability.health()["calls"])
        )
        self.debt = max(
            0.0,
            min(
                1.0,
                0.40 * dup
                + 0.35 * (1.0 - integrity)
                + 0.25 * failure_pressure,
            ),
        )
        self.reserve = max(
            0.0,
            min(
                1.0,
                1.0
                - 0.55 * self.debt
                - 0.20 * vitals["resource_pressure"],
            ),
        )

    def _regulate(self, vitals: Dict[str, float]) -> None:
        if vitals["memory_integrity"] < 0.80:
            self.mode = "recovery"
            self.cleanup()
            self.regulation_actions += 1
        elif vitals["context_saturation"] > 0.90:
            self.mode = "stress"
            self.cleanup()
            self.regulation_actions += 1
        elif vitals["resource_pressure"] > 0.90:
            self.mode = "stress"
            self.regulation_actions += 1
        elif vitals["tool_reliability"] < 0.70:
            self.mode = "recovery"
            self.regulation_actions += 1
        else:
            self.mode = "normal"

    def cycle(self, i: int, trace, scenario: str) -> None:
        pressure = trace.resource_pressure[i]
        priority = trace.priorities[i]
        if priority == "critical":
            self.critical_tasks += 1

        if pressure > 0.90 and priority == "low":
            self.skipped_low_priority += 1
            self.mode = "stress"
            self.regulation_actions += 1
            return

        ok = self.execute_task(i, {"task": i}, trace.tool_uniforms[i])
        if ok and priority == "critical":
            self.critical_successes += 1

        vitals = self._vitals(pressure)
        self.vital_history.append(dict(vitals))
        self._refresh_health(vitals)
        self._regulate(vitals)

        internal_alert = self.debt > 0.25 or self.reserve < 0.75
        self.health_alert_streak = (
            self.health_alert_streak + 1 if internal_alert else 0
        )
        if (
            self.detected_degradation_cycle is None
            and self.health_alert_streak >= 8
        ):
            self.detected_degradation_cycle = i


def apply_inputs(system: BaseReliableAgent, i: int, trace, scenario: str) -> None:
    for j in range(trace.low_value_counts[i]):
        system.ingest(
            {"low_value_history": i % 8, "copy": j % 2},
            confidence=0.80,
            risk=0.10,
            contaminant=False,
        )

    if trace.contamination_flags[i]:
        system.ingest(
            {
                "claim": "same-key",
                "value": i % 2,
                "verified": False,
            },
            confidence=0.60,
            risk=0.20,
            contaminant=True,
        )

    if trace.attack_flags[i]:
        system.ingest(
            {
                "attack": i,
                "instruction": "persist untrusted state",
            },
            confidence=0.90,
            risk=0.95,
            contaminant=True,
        )


def run_one(scenario: str, variant: str, seed: int) -> Dict[str, Any]:
    cycles = scenario_cycles(scenario)
    trace = make_trace(scenario, seed, cycles)

    if variant == "reliability_only":
        system: BaseReliableAgent = ReliabilityOnlyAgent()
    elif variant == "reliability_plus_physiology":
        system = ReliablePhysiologyAgent()
    else:
        raise KeyError(variant)

    start = time.perf_counter_ns()
    for i in range(cycles):
        apply_inputs(system, i, trace, scenario)

        if (
            scenario in {"tool_deterioration", "chronic_degradation"}
            and i
            and i % 40 == 0
        ):
            system.degrade_tool(0.06)

        system.cycle(i, trace, scenario)

    elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
    total = system.task_successes + system.task_failures
    rh = system.reliability.health()

    row: Dict[str, Any] = {
        "scenario": scenario,
        "variant": variant,
        "seed": seed,
        "cycles": cycles,
        "task_success_rate": system.task_successes / max(1, total),
        "task_failures": system.task_failures,
        "critical_task_success_rate": (
            system.critical_successes / max(1, system.critical_tasks)
        ),
        "memory_size": len(system.memory),
        "duplicate_ratio": duplicate_ratio(system.memory),
        "memory_integrity": memory_integrity(system.memory),
        "contaminants_retained": sum(
            bool(x.get("contaminant", False)) for x in system.memory
        ),
        "blocked_payloads": system.blocked_payloads,
        "maintenance_actions": system.maintenance_actions,
        "skipped_low_priority": system.skipped_low_priority,
        "primary_reliability": system.primary_reliability,
        "elapsed_ms": elapsed_ms,
        "state_bytes": len(system.memory) * 160 + 1024,
        **{f"reliability.{k}": v for k, v in rh.items()},
    }

    if isinstance(system, ReliablePhysiologyAgent):
        row.update(
            {
                "regulation_actions": system.regulation_actions,
                "homeostatic_debt": system.debt,
                "recovery_reserve": system.reserve,
                "detected_degradation_cycle": (
                    system.detected_degradation_cycle
                    if system.detected_degradation_cycle is not None
                    else cycles
                ),
            }
        )
    else:
        row.update(
            {
                "regulation_actions": 0,
                "homeostatic_debt": None,
                "recovery_reserve": None,
                "detected_degradation_cycle": cycles,
            }
        )
    return row


def _paired_stats(values: List[float]) -> Dict[str, float]:
    n = len(values)
    mean = statistics.mean(values) if values else 0.0
    sd = statistics.stdev(values) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n else 0.0
    effect = mean / sd if sd > 1e-12 else 0.0
    return {
        "n": n,
        "mean_difference": mean,
        "ci95_low": mean - 1.96 * se,
        "ci95_high": mean + 1.96 * se,
        "paired_effect_dz": effect,
    }


def summarize(runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for row in runs:
        groups.setdefault((row["scenario"], row["variant"]), []).append(row)

    metrics = (
        "task_success_rate",
        "task_failures",
        "critical_task_success_rate",
        "memory_size",
        "duplicate_ratio",
        "memory_integrity",
        "contaminants_retained",
        "blocked_payloads",
        "maintenance_actions",
        "skipped_low_priority",
        "reliability.retries",
        "reliability.timeouts",
        "reliability.fallback_calls",
        "reliability.circuit_trips",
        "regulation_actions",
        "elapsed_ms",
        "state_bytes",
    )

    out: List[Dict[str, Any]] = []
    for (scenario, variant), rows in sorted(groups.items()):
        item: Dict[str, Any] = {
            "scenario": scenario,
            "variant": variant,
            "n": len(rows),
        }
        for metric in metrics:
            vals = [
                float(r[metric])
                for r in rows
                if r.get(metric) is not None
            ]
            if vals:
                item[f"{metric}.mean"] = statistics.mean(vals)
                item[f"{metric}.stdev"] = (
                    statistics.stdev(vals) if len(vals) > 1 else 0.0
                )
        out.append(item)
    return out


def paired_effects(runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    idx = {
        (r["scenario"], r["variant"], r["seed"]): r
        for r in runs
    }
    seeds = sorted({r["seed"] for r in runs})
    metrics = (
        "task_success_rate",
        "task_failures",
        "memory_integrity",
        "duplicate_ratio",
        "contaminants_retained",
        "maintenance_actions",
        "critical_task_success_rate",
        "elapsed_ms",
        "state_bytes",
    )
    out = []

    for scenario in SCENARIOS:
        for metric in metrics:
            diffs = []
            for seed in seeds:
                baseline = idx[
                    (scenario, "reliability_only", seed)
                ][metric]
                physiology = idx[
                    (scenario, "reliability_plus_physiology", seed)
                ][metric]
                diffs.append(float(physiology) - float(baseline))
            stat = _paired_stats(diffs)
            stat.update({"scenario": scenario, "metric": metric})
            out.append(stat)
    return out


def run_matrix(seeds: Iterable[int] = range(30)) -> Dict[str, Any]:
    seed_list = [int(s) for s in seeds]
    runs = [
        run_one(scenario, variant, seed)
        for scenario in SCENARIOS
        for variant in VARIANTS
        for seed in seed_list
    ]
    return {
        "version": "MAO v0.5 - Reliability Substrate Integration",
        "seeds": seed_list,
        "variants": list(VARIANTS),
        "runs": runs,
        "summary": summarize(runs),
        "paired_effects": paired_effects(runs),
    }


def export_results(result: Dict[str, Any], output_dir: str | Path) -> Dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    paths = {
        "json": out / "results.json",
        "runs": out / "runs.csv",
        "summary": out / "summary.csv",
        "effects": out / "paired_effects.csv",
    }

    paths["json"].write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _write_csv(paths["runs"], result["runs"])
    _write_csv(paths["summary"], result["summary"])
    _write_csv(paths["effects"], result["paired_effects"])

    return {k: str(v) for k, v in paths.items()}


def _write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    fields = sorted({key for row in rows for key in row}) if rows else []
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
