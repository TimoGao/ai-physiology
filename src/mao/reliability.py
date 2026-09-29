from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Sequence

@dataclass(frozen=True)
class ReliabilityPolicy:
    max_retries: int = 2
    timeout_ms: float = 500.0
    failure_threshold: int = 3
    cooldown_cycles: int = 3
    fallback_enabled: bool = True
    fallback_reliability: float = 0.88

@dataclass
class ReliabilityOutcome:
    ok: bool
    result: Any = None
    attempts: int = 0
    retries: int = 0
    fallback_used: bool = False
    route: str = "primary"

class ReliabilitySubstrate:
    """Ordinary reliability mechanisms used below the physiology layer."""

    def __init__(self, policy: ReliabilityPolicy | None = None):
        self.policy = policy or ReliabilityPolicy()
        self.consecutive_failures = 0
        self.open_until = -1
        self.calls = 0
        self.retries = 0
        self.timeouts = 0
        self.primary_failures = 0
        self.fallback_calls = 0
        self.circuit_trips = 0
        self.circuit_rejections = 0

    def execute_from_trace(
        self,
        cycle: int,
        payload: Any,
        primary_reliability: float,
        primary_draws: Sequence[float],
        latency_ms: Sequence[float],
        fallback_draw: float,
    ) -> ReliabilityOutcome:
        if cycle < self.open_until:
            self.circuit_rejections += 1
            return self._fallback(payload, fallback_draw)

        max_attempts = min(len(primary_draws), self.policy.max_retries + 1)
        for attempt in range(max_attempts):
            self.calls += 1
            timed_out = attempt < len(latency_ms) and latency_ms[attempt] > self.policy.timeout_ms
            if timed_out:
                self.timeouts += 1
            success = (not timed_out) and primary_draws[attempt] <= primary_reliability
            if success:
                self.consecutive_failures = 0
                return ReliabilityOutcome(
                    ok=True,
                    result=payload,
                    attempts=attempt + 1,
                    retries=attempt,
                    route="primary",
                )
            self.primary_failures += 1
            if attempt < max_attempts - 1:
                self.retries += 1

        self.consecutive_failures += 1
        if self.consecutive_failures >= self.policy.failure_threshold:
            self.open_until = cycle + self.policy.cooldown_cycles
            self.circuit_trips += 1

        return self._fallback(payload, fallback_draw)

    def _fallback(self, payload: Any, draw: float) -> ReliabilityOutcome:
        if not self.policy.fallback_enabled:
            return ReliabilityOutcome(ok=False, route="none")
        self.fallback_calls += 1
        ok = draw <= self.policy.fallback_reliability
        return ReliabilityOutcome(
            ok=ok,
            result=payload if ok else None,
            attempts=1,
            fallback_used=True,
            route="fallback",
        )

    def health(self) -> Dict[str, int]:
        return {
            "calls": self.calls,
            "retries": self.retries,
            "timeouts": self.timeouts,
            "primary_failures": self.primary_failures,
            "fallback_calls": self.fallback_calls,
            "circuit_trips": self.circuit_trips,
            "circuit_rejections": self.circuit_rejections,
        }
