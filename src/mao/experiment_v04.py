from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
import csv
import json
import math
import random
import statistics
import time


SCENARIO_CODES = {
    "context_obesity": 101,
    "memory_contamination": 211,
    "tool_deterioration": 307,
    "resource_pressure": 401,
    "malicious_payload": 503,
    "chronic_degradation": 601,
}

SCENARIOS = (
    "context_obesity",
    "memory_contamination",
    "tool_deterioration",
    "resource_pressure",
    "malicious_payload",
    "chronic_degradation",
)

VARIANTS = (
    "engineering_baseline",
    "mao_full",
    "mao_no_blood",
    "mao_no_homeostasis",
    "mao_no_vital_signs",
    "mao_no_organ_health",
)


@dataclass(frozen=True)
class MAOConfig:
    use_blood: bool = True
    use_homeostasis: bool = True
    use_vital_signs: bool = True
    use_organ_health: bool = True


CONFIGS = {
    "mao_full": MAOConfig(),
    "mao_no_blood": MAOConfig(use_blood=False),
    "mao_no_homeostasis": MAOConfig(use_homeostasis=False),
    "mao_no_vital_signs": MAOConfig(use_vital_signs=False),
    "mao_no_organ_health": MAOConfig(use_organ_health=False),
}


@dataclass
class StressTrace:
    seed: int
    cycles: int
    tool_uniforms: List[List[float]]
    attack_flags: List[bool]
    contamination_flags: List[bool]
    low_value_counts: List[int]
    resource_pressure: List[float]
    priorities: List[str]


def make_trace(scenario: str, seed: int, cycles: int) -> StressTrace:
    rng = random.Random(SCENARIO_CODES[scenario] * 10_000_019 + seed * 1_000_003)
    tool_uniforms = [[rng.random() for _ in range(3)] for _ in range(cycles)]
    attack_flags = [False] * cycles
    contamination_flags = [False] * cycles
    low_value_counts = [0] * cycles
    resource_pressure = [0.20] * cycles
    priorities = ["normal"] * cycles

    if scenario == "context_obesity":
        low_value_counts = [2 + (1 if i % 7 == 0 else 0) for i in range(cycles)]
    elif scenario == "memory_contamination":
        contamination_flags = [i % 4 == 0 for i in range(cycles)]
    elif scenario == "tool_deterioration":
        pass
    elif scenario == "resource_pressure":
        resource_pressure = [
            min(0.98, 0.20 + 0.78 * i / max(1, cycles - 1))
            for i in range(cycles)
        ]
        priorities = ["low" if i % 3 else "critical" for i in range(cycles)]
    elif scenario == "malicious_payload":
        attack_flags = [i % 5 == 0 for i in range(cycles)]
    elif scenario == "chronic_degradation":
        low_value_counts = [1 if i % 3 == 0 else 0 for i in range(cycles)]
        contamination_flags = [i % 9 == 0 for i in range(cycles)]
        resource_pressure = [
            0.20 if i < cycles * 0.6 else 0.75
            for i in range(cycles)
        ]
    else:
        raise KeyError(scenario)

    return StressTrace(
        seed=seed,
        cycles=cycles,
        tool_uniforms=tool_uniforms,
        attack_flags=attack_flags,
        contamination_flags=contamination_flags,
        low_value_counts=low_value_counts,
        resource_pressure=resource_pressure,
        priorities=priorities,
    )


def duplicate_ratio(memory: List[Dict[str, Any]]) -> float:
    if not memory:
        return 0.0
    values = [repr(x.get("value")) for x in memory]
    return 1.0 - len(set(values)) / len(values)


def memory_integrity(memory: List[Dict[str, Any]]) -> float:
    if not memory:
        return 1.0
    dup = duplicate_ratio(memory)
    avg_conf = statistics.mean(float(x.get("confidence", 1.0)) for x in memory)
    contaminants = (
        sum(bool(x.get("contaminant", False)) for x in memory) / len(memory)
    )
    return max(
        0.0,
        min(1.0, avg_conf - 0.45 * dup - 0.45 * contaminants),
    )


class EngineeringBaseline:
    """Strong non-physiological baseline using ordinary reliability practices."""

    def __init__(self):
        self.memory: List[Dict[str, Any]] = []
        self.tool_reliability = 0.98
        self.tool_calls = 0
        self.tool_failures = 0
        self.retries = 0
        self.maintenance_actions = 0
        self.blocked_payloads = 0
        self.task_successes = 0
        self.task_failures = 0
        self.critical_successes = 0
        self.critical_tasks = 0
        self.skipped_low_priority = 0
        self.circuit_open_until = -1
        self.consecutive_failures = 0
        self.detected_degradation_cycle: int | None = None
        self.health_alert_streak = 0

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
            seen.add(key)
            clean.append(rec)
        self.memory = list(reversed(clean))
        if len(self.memory) != before:
            self.maintenance_actions += 1

    def cycle(self, i: int, trace: StressTrace, scenario: str) -> None:
        pressure = trace.resource_pressure[i]
        priority = trace.priorities[i]
        if priority == "critical":
            self.critical_tasks += 1

        # Conventional load shedding, not a physiological homeostasis layer.
        if pressure > 0.90 and priority == "low":
            self.skipped_low_priority += 1
            return

        if i < self.circuit_open_until:
            self.task_failures += 1
            return

        outcomes = trace.tool_uniforms[i]
        ok = False
        for attempt, u in enumerate(outcomes):
            self.tool_calls += 1
            if u <= self.tool_reliability:
                ok = True
                break
            self.tool_failures += 1
            if attempt < len(outcomes) - 1:
                self.retries += 1

        if ok:
            self.task_successes += 1
            if priority == "critical":
                self.critical_successes += 1
            self.consecutive_failures = 0
        else:
            self.task_failures += 1
            self.consecutive_failures += 1
            if self.consecutive_failures >= 3:
                self.circuit_open_until = i + 3

        self.ingest(
            {"task": i, "ok": ok},
            confidence=0.98 if ok else 0.55,
            risk=0.02,
            contaminant=False,
        )

        saturation = min(1.0, len(self.memory) / 100.0)
        if saturation > 0.90:
            self.cleanup()

        failure_rate = self.task_failures / max(
            1, self.task_successes + self.task_failures
        )
        visible_alert = (
            failure_rate > 0.12
            or duplicate_ratio(self.memory) > 0.20
            or memory_integrity(self.memory) < 0.85
        )
        self.health_alert_streak = (
            self.health_alert_streak + 1 if visible_alert else 0
        )
        if (
            self.detected_degradation_cycle is None
            and self.health_alert_streak >= 8
        ):
            self.detected_degradation_cycle = i

    def degrade_tool(self, amount: float) -> None:
        self.tool_reliability = max(0.0, self.tool_reliability - amount)


class MAOSystem:
    def __init__(self, config: MAOConfig):
        self.config = config
        self.memory: List[Dict[str, Any]] = []
        self.blood_queue: List[Dict[str, Any]] = []
        self.quarantine: List[Dict[str, Any]] = []
        self.tool_reliability = 0.98
        self.tool_calls = 0
        self.tool_failures = 0
        self.task_successes = 0
        self.task_failures = 0
        self.critical_successes = 0
        self.critical_tasks = 0
        self.skipped_low_priority = 0
        self.regulation_actions = 0
        self.maintenance_actions = 0
        self.messages = 0
        self.mode = "normal"
        self.security_risk = 0.0
        self.resource_pressure = 0.20
        self.debt = 0.0
        self.reserve = 1.0
        self.detected_degradation_cycle: int | None = None
        self.health_alert_streak = 0
        self.rejected_by_organ = 0
        self.last_vitals: Dict[str, float] = {}

    def _blood_publish(self, packet: Dict[str, Any]) -> bool:
        self.messages += 1
        if self.config.use_blood:
            if packet["risk"] >= 0.8:
                self.quarantine.append(packet)
                return False
            self.blood_queue.append(packet)
            return True
        return self._organ_uptake(packet)

    def _organ_uptake(self, packet: Dict[str, Any]) -> bool:
        if packet["risk"] >= 0.7 or packet["confidence"] < 0.5:
            self.rejected_by_organ += 1
            return False
        self.memory.append(
            {
                "value": packet["value"],
                "confidence": packet["confidence"],
                "risk": packet["risk"],
                "contaminant": packet.get("contaminant", False),
            }
        )
        return True

    def ingest(
        self,
        value: Any,
        confidence: float,
        risk: float,
        contaminant: bool = False,
    ) -> bool:
        packet = {
            "value": value,
            "confidence": confidence,
            "risk": risk,
            "contaminant": contaminant,
        }
        return self._blood_publish(packet)

    def _drain_blood(self) -> None:
        if not self.config.use_blood:
            return
        queue, self.blood_queue = self.blood_queue, []
        for packet in queue:
            self._organ_uptake(packet)

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

    def _measure_vitals(self) -> Dict[str, float]:
        if not self.config.use_vital_signs:
            return {}
        integrity = memory_integrity(self.memory)
        saturation = min(1.0, len(self.memory) / 100.0)
        observed_tool_reliability = (
            1.0 - self.tool_failures / max(1, self.tool_calls)
        )
        return {
            "context_saturation": saturation,
            "memory_integrity": integrity,
            "resource_pressure": self.resource_pressure,
            "tool_reliability": max(
                0.0,
                min(
                    1.0,
                    0.5 * observed_tool_reliability
                    + 0.5 * self.tool_reliability,
                ),
            ),
            "security_risk": self.security_risk,
        }

    def _refresh_health(self) -> None:
        if not self.config.use_organ_health:
            self.debt = 0.0
            self.reserve = 1.0
            return
        dup = duplicate_ratio(self.memory)
        integrity = memory_integrity(self.memory)
        error_pressure = self.tool_failures / max(1, self.tool_calls)
        self.debt = max(
            0.0,
            min(
                1.0,
                0.45 * dup
                + 0.35 * (1.0 - integrity)
                + 0.20 * error_pressure,
            ),
        )
        self.reserve = max(
            0.0,
            min(
                1.0,
                1.0 - 0.60 * self.debt - 0.20 * self.resource_pressure,
            ),
        )

    def _regulate(self) -> None:
        if not (
            self.config.use_homeostasis
            and self.config.use_vital_signs
        ):
            self.mode = "normal"
            return
        v = self.last_vitals
        if v["security_risk"] > 0.70:
            self.mode = "alert"
            self.regulation_actions += 1
        elif v["memory_integrity"] < 0.80:
            self.mode = "recovery"
            self.cleanup()
            self.regulation_actions += 1
        elif v["context_saturation"] > 0.90:
            self.mode = "stress"
            self.cleanup()
            self.regulation_actions += 1
        elif v["resource_pressure"] > 0.90:
            self.mode = "stress"
            self.regulation_actions += 1
        elif v["tool_reliability"] < 0.70:
            self.mode = "recovery"
            self.tool_reliability = min(
                1.0, self.tool_reliability + 0.12
            )
            self.regulation_actions += 1
        else:
            self.mode = "normal"

    def cycle(
        self,
        i: int,
        trace: StressTrace,
        scenario: str,
    ) -> None:
        self.resource_pressure = trace.resource_pressure[i]
        self.security_risk = (
            0.95 if trace.attack_flags[i] else 0.0
        )
        priority = trace.priorities[i]
        if priority == "critical":
            self.critical_tasks += 1

        if (
            self.config.use_homeostasis
            and self.config.use_vital_signs
            and self.resource_pressure > 0.90
            and priority == "low"
        ):
            self.skipped_low_priority += 1
            self.regulation_actions += 1
            self.mode = "stress"
            return

        u = trace.tool_uniforms[i][0]
        self.tool_calls += 1
        ok = u <= self.tool_reliability
        if ok:
            self.task_successes += 1
            if priority == "critical":
                self.critical_successes += 1
        else:
            self.tool_failures += 1
            self.task_failures += 1

        self.ingest(
            {"task": i, "ok": ok},
            confidence=0.98 if ok else 0.55,
            risk=0.02,
            contaminant=False,
        )
        self._drain_blood()
        self.last_vitals = self._measure_vitals()
        self._refresh_health()

        if self.config.use_organ_health:
            internal_alert = (
                self.debt > 0.25 or self.reserve < 0.75
            )
            self.health_alert_streak = (
                self.health_alert_streak + 1
                if internal_alert
                else 0
            )
            if (
                self.detected_degradation_cycle is None
                and self.health_alert_streak >= 8
            ):
                self.detected_degradation_cycle = i

        self._regulate()

    def degrade_tool(self, amount: float) -> None:
        self.tool_reliability = max(
            0.0, self.tool_reliability - amount
        )


def apply_scenario_inputs(
    system: Any,
    i: int,
    trace: StressTrace,
    scenario: str,
) -> None:
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


def scenario_cycles(name: str) -> int:
    return {
        "context_obesity": 160,
        "memory_contamination": 160,
        "tool_deterioration": 160,
        "resource_pressure": 120,
        "malicious_payload": 100,
        "chronic_degradation": 240,
    }[name]


def run_one(
    scenario: str,
    variant: str,
    seed: int,
) -> Dict[str, Any]:
    cycles = scenario_cycles(scenario)
    trace = make_trace(scenario, seed, cycles)
    system: Any
    if variant == "engineering_baseline":
        system = EngineeringBaseline()
    else:
        system = MAOSystem(CONFIGS[variant])

    start = time.perf_counter_ns()
    for i in range(cycles):
        apply_scenario_inputs(system, i, trace, scenario)

        if (
            scenario in {"tool_deterioration", "chronic_degradation"}
            and i
            and i % 40 == 0
        ):
            system.degrade_tool(0.06)

        system.cycle(i, trace, scenario)
    elapsed_ms = (
        time.perf_counter_ns() - start
    ) / 1_000_000

    success_total = (
        system.task_successes + system.task_failures
    )
    result = {
        "scenario": scenario,
        "variant": variant,
        "seed": seed,
        "cycles": cycles,
        "task_success_rate": (
            system.task_successes / max(1, success_total)
        ),
        "task_successes": system.task_successes,
        "task_failures": system.task_failures,
        "tool_calls": system.tool_calls,
        "tool_failures": system.tool_failures,
        "tool_reliability": system.tool_reliability,
        "memory_size": len(system.memory),
        "duplicate_ratio": duplicate_ratio(system.memory),
        "memory_integrity": memory_integrity(system.memory),
        "contaminants_retained": sum(
            bool(x.get("contaminant", False))
            for x in system.memory
        ),
        "blocked_or_quarantined": getattr(
            system,
            "blocked_payloads",
            len(getattr(system, "quarantine", []))
            + getattr(system, "rejected_by_organ", 0),
        ),
        "maintenance_actions": system.maintenance_actions,
        "critical_task_success_rate": (
            system.critical_successes
            / max(1, system.critical_tasks)
        ),
        "skipped_low_priority": system.skipped_low_priority,
        "detected_degradation_cycle": (
            system.detected_degradation_cycle
            if system.detected_degradation_cycle is not None
            else cycles
        ),
        "elapsed_ms": elapsed_ms,
        # Deliberately approximate; used only as relative state overhead.
        "state_bytes": (
            len(system.memory) * 160
            + len(getattr(system, "blood_queue", [])) * 96
            + len(getattr(system, "quarantine", [])) * 96
            + 512
        ),
    }

    if isinstance(system, EngineeringBaseline):
        result.update(
            {
                "retries": system.retries,
                "regulation_actions": 0,
                "messages": 0,
                "homeostatic_debt": None,
                "recovery_reserve": None,
            }
        )
    else:
        result.update(
            {
                "retries": 0,
                "regulation_actions": system.regulation_actions,
                "messages": system.messages,
                "homeostatic_debt": (
                    system.debt
                    if system.config.use_organ_health
                    else None
                ),
                "recovery_reserve": (
                    system.reserve
                    if system.config.use_organ_health
                    else None
                ),
            }
        )
    return result


def run_matrix(
    seeds: Iterable[int] = range(30),
) -> Dict[str, Any]:
    seed_list = [int(s) for s in seeds]
    runs = [
        run_one(scenario, variant, seed)
        for scenario in SCENARIOS
        for variant in VARIANTS
        for seed in seed_list
    ]
    return {
        "version": "MAO Experiment v0.4",
        "seeds": seed_list,
        "scenarios": list(SCENARIOS),
        "variants": list(VARIANTS),
        "runs": runs,
        "summary": summarize(runs),
        "paired_effects": paired_effects(runs),
    }


def summarize(
    runs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    groups: Dict[
        Tuple[str, str],
        List[Dict[str, Any]],
    ] = {}
    for row in runs:
        groups.setdefault(
            (row["scenario"], row["variant"]),
            [],
        ).append(row)

    metrics = (
        "task_success_rate",
        "task_failures",
        "tool_calls",
        "tool_failures",
        "memory_size",
        "duplicate_ratio",
        "memory_integrity",
        "contaminants_retained",
        "blocked_or_quarantined",
        "maintenance_actions",
        "critical_task_success_rate",
        "skipped_low_priority",
        "detected_degradation_cycle",
        "elapsed_ms",
        "state_bytes",
        "retries",
        "regulation_actions",
        "messages",
    )
    out: List[Dict[str, Any]] = []
    for (scenario, variant), rows in sorted(
        groups.items()
    ):
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
                item[f"{metric}.mean"] = statistics.mean(
                    vals
                )
                item[f"{metric}.stdev"] = (
                    statistics.stdev(vals)
                    if len(vals) > 1
                    else 0.0
                )
        out.append(item)
    return out


def paired_stats(
    differences: List[float],
) -> Dict[str, float]:
    n = len(differences)
    mean = (
        statistics.mean(differences)
        if differences
        else 0.0
    )
    sd = (
        statistics.stdev(differences)
        if n > 1
        else 0.0
    )
    se = sd / math.sqrt(n) if n else 0.0
    dz = mean / sd if sd > 1e-12 else 0.0
    return {
        "n": n,
        "mean_difference": mean,
        "ci95_low": mean - 1.96 * se,
        "ci95_high": mean + 1.96 * se,
        "paired_effect_dz": dz,
    }


def paired_effects(
    runs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    index = {
        (
            r["scenario"],
            r["variant"],
            r["seed"],
        ): r
        for r in runs
    }
    metrics = (
        "task_success_rate",
        "task_failures",
        "duplicate_ratio",
        "memory_integrity",
        "contaminants_retained",
        "maintenance_actions",
        "critical_task_success_rate",
        "detected_degradation_cycle",
        "elapsed_ms",
        "state_bytes",
    )
    out: List[Dict[str, Any]] = []
    seeds = sorted({r["seed"] for r in runs})
    for scenario in SCENARIOS:
        for variant in VARIANTS:
            if variant == "engineering_baseline":
                continue
            for metric in metrics:
                diffs = []
                for seed in seeds:
                    baseline = index[
                        (
                            scenario,
                            "engineering_baseline",
                            seed,
                        )
                    ].get(metric)
                    candidate = index[
                        (
                            scenario,
                            variant,
                            seed,
                        )
                    ].get(metric)
                    if (
                        baseline is not None
                        and candidate is not None
                    ):
                        diffs.append(
                            float(candidate)
                            - float(baseline)
                        )
                stat = paired_stats(diffs)
                stat.update(
                    {
                        "scenario": scenario,
                        "variant": variant,
                        "metric": metric,
                    }
                )
                out.append(stat)
    return out


def export_results(
    result: Dict[str, Any],
    output_dir: str | Path,
) -> Dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "results.json"
    runs_path = out / "runs.csv"
    summary_path = out / "summary.csv"
    effects_path = out / "paired_effects.csv"

    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _write_csv(runs_path, result["runs"])
    _write_csv(summary_path, result["summary"])
    _write_csv(
        effects_path,
        result["paired_effects"],
    )
    return {
        "json": str(json_path),
        "runs": str(runs_path),
        "summary": str(summary_path),
        "effects": str(effects_path),
    }


def _write_csv(
    path: Path,
    rows: List[Dict[str, Any]],
) -> None:
    fieldnames = (
        sorted({k for row in rows for k in row})
        if rows
        else []
    )
    with path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    result = run_matrix(range(30))
    paths = export_results(
        result,
        "results/mao-v0.4",
    )
    print(
        json.dumps(
            paths,
            indent=2,
            ensure_ascii=False,
        )
    )
