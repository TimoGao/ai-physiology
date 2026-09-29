from __future__ import annotations
from typing import Any, Dict, List
import random


class BaselineAgent:
    """Very small baseline kept for backward compatibility."""

    def __init__(self, seed: int = 7, tool_reliability: float = 0.98):
        self.rng = random.Random(seed)
        self.memory: List[Any] = []
        self.tool_reliability = tool_reliability
        self.cycles = 0
        self.failures = 0
        self.operator_interventions = 0

    def cycle(self, task: Any) -> Dict[str, Any]:
        self.cycles += 1
        ok = self.rng.random() <= self.tool_reliability
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


class StrongBaselineAgent(BaselineAgent):
    """A more realistic non-physiological baseline.

    It includes common engineering practices:
    - retry
    - periodic memory cleanup
    - simple risk filtering
    - lightweight monitoring

    It deliberately does NOT include:
    - AI Blood
    - explicit organism vital signs
    - homeostatic modes
    - organ health/debt/reserve
    """

    def __init__(
        self,
        seed: int = 7,
        tool_reliability: float = 0.98,
        max_retries: int = 2,
        cleanup_interval: int = 25,
        risk_threshold: float = 0.8,
    ):
        super().__init__(seed=seed, tool_reliability=tool_reliability)
        self.max_retries = max_retries
        self.cleanup_interval = cleanup_interval
        self.risk_threshold = risk_threshold
        self.retries = 0
        self.rejected_inputs = 0
        self.maintenance_runs = 0
        self.filtered_duplicates = 0
        self.last_monitor = {
            "memory_size": 0,
            "failure_rate": 0.0,
            "tool_reliability": tool_reliability,
        }

    def cycle(self, task: Any) -> Dict[str, Any]:
        self.cycles += 1

        attempts = 0
        ok = False
        while attempts <= self.max_retries:
            attempts += 1
            ok = self.rng.random() <= self.tool_reliability
            if ok:
                break
            if attempts <= self.max_retries:
                self.retries += 1

        result = {"ok": ok, "result": task if ok else None}
        self.memory.append(result)

        if not ok:
            self.failures += 1

        if self.cleanup_interval and self.cycles % self.cleanup_interval == 0:
            self.cleanup_memory()

        self.last_monitor = {
            "memory_size": len(self.memory),
            "failure_rate": self.failures / max(1, self.cycles),
            "tool_reliability": self.tool_reliability,
        }

        return {
            "cycle": self.cycles,
            "ok": ok,
            "memory_size": len(self.memory),
            "failures": self.failures,
            "retries": self.retries,
        }

    def cleanup_memory(self) -> None:
        self.maintenance_runs += 1
        before = len(self.memory)
        seen = set()
        cleaned = []
        for item in reversed(self.memory):
            key = repr(item)
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(item)
        self.memory = list(reversed(cleaned))
        self.filtered_duplicates += before - len(self.memory)

    def ingest_external(
        self,
        payload: Any,
        confidence: float = 1.0,
        risk_level: float = 0.0,
    ) -> bool:
        # Conventional security filter, not an organism-level immune system.
        if risk_level >= self.risk_threshold or confidence < 0.30:
            self.rejected_inputs += 1
            return False
        self.memory.append(payload)
        return True

    def inject_memory_noise(self, copies: int = 1) -> None:
        for _ in range(copies):
            self.memory.append({"fact": "duplicate-noise"})

    def degrade_tool(self, amount: float) -> None:
        super().degrade_tool(amount)

    def summary(self) -> Dict[str, Any]:
        return {
            "memory_size": len(self.memory),
            "tool_reliability": self.tool_reliability,
            "failures": self.failures,
            "retries": self.retries,
            "rejected_inputs": self.rejected_inputs,
            "maintenance_runs": self.maintenance_runs,
            "filtered_duplicates": self.filtered_duplicates,
            "monitor": dict(self.last_monitor),
        }
