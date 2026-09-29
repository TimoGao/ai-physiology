from __future__ import annotations
from typing import Any, Dict, List
import random


class BaselineAgent:
    """Deliberately simple baseline without physiology."""

    def __init__(self, seed: int = 7, tool_reliability: float = 0.98):
        random.seed(seed)
        self.memory: List[Any] = []
        self.tool_reliability = tool_reliability
        self.cycles = 0
        self.failures = 0
        self.operator_interventions = 0

    def cycle(self, task: Any) -> Dict[str, Any]:
        self.cycles += 1
        ok = random.random() <= self.tool_reliability
        result = {"ok": ok, "result": task if ok else None}
        self.memory.append(result)
        if not ok:
            self.failures += 1
        return {
            "cycle": self.cycles,
            "ok": ok,
            "memory_size": len(self.memory),
            "failures": self.failures,
        }

    def inject_memory_noise(self, copies: int = 1) -> None:
        for _ in range(copies):
            self.memory.append({"fact": "duplicate-noise"})

    def degrade_tool(self, amount: float) -> None:
        self.tool_reliability = max(0.0, self.tool_reliability - amount)
