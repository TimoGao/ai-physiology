from __future__ import annotations
from typing import Dict, Any
from .runtime import MinimalArtificialOrganism
from .baseline import BaselineAgent


def run_chronic_degradation_experiment(cycles: int = 200, seed: int = 7) -> Dict[str, Any]:
    baseline = BaselineAgent(seed=seed)
    mao = MinimalArtificialOrganism(seed=seed)

    for i in range(cycles):
        task = {"task_id": i, "payload": "work"}

        if i % 10 == 0:
            baseline.inject_memory_noise(copies=3)
            mao.inject_memory_noise(copies=3, confidence=0.60)

        if i and i % 40 == 0:
            baseline.degrade_tool(0.06)
            mao.tool.degrade(0.06)

        if i > cycles * 0.60:
            mao.set_resource_pressure(0.75)

        baseline.cycle(task)
        mao.cycle(task)

    baseline_duplicates = _duplicate_ratio(baseline.memory)
    mao_duplicates = mao.memory.vital_variables.get("duplicate_ratio", 0.0)

    return {
        "experiment": "chronic_degradation",
        "cycles": cycles,
        "baseline": {
            "memory_size": len(baseline.memory),
            "duplicate_ratio": round(baseline_duplicates, 4),
            "tool_reliability": round(baseline.tool_reliability, 4),
            "failures": baseline.failures,
        },
        "mao": {
            "memory_size": len(mao.memory.records),
            "duplicate_ratio": round(mao_duplicates, 4),
            "memory_integrity": round(mao.memory.vital_variables.get("memory_integrity", 1.0), 4),
            "tool_reliability": round(mao.tool.vital_variables.get("tool_reliability", mao.tool.reliability), 4),
            "homeostatic_debt": round(mao.homeostatic_debt(), 4),
            "recovery_reserve": round(mao.recovery_reserve(), 4),
            "mode": mao.homeostasis.mode.value,
            "regulation_events": sum(bool(x["actions"]) for x in mao.history),
        },
    }


def _duplicate_ratio(items) -> float:
    if not items:
        return 0.0
    values = [repr(x) for x in items]
    return 1.0 - len(set(values)) / len(values)
