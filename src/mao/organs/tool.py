from __future__ import annotations
from typing import Any
import random
from ..organ import Organ
from ..models import BloodPacket


class ToolOrgan(Organ):
    def __init__(self, organism_id: str, reliability: float = 0.98, organ_id: str = "tool"):
        super().__init__(organism_id, organ_id, "tool")
        self.reliability = reliability
        self.calls = 0
        self.failures = 0
        self.allowed_actions = ["execute", "degrade", "recover"]

    def execute(self, payload: Any) -> BloodPacket:
        self.calls += 1
        success = random.random() <= self.reliability
        if not success:
            self.failures += 1
            body = {"ok": False, "error": "simulated_tool_failure", "input": payload}
            confidence = 0.25
            risk = 0.25
        else:
            body = {"ok": True, "result": payload}
            confidence = 0.98
            risk = 0.02
        self._refresh_health()
        return BloodPacket(
            organism_id=self.organism_id,
            source_organ=self.organ_id,
            destination_scope="multi_organ",
            payload_type="tool_result",
            body=body,
            confidence=confidence,
            risk_level=risk,
        )

    def uptake(self, packet: BloodPacket) -> None:
        return

    def degrade(self, amount: float) -> None:
        self.reliability = max(0.0, self.reliability - amount)
        self._refresh_health()

    def recover(self, amount: float = 0.1) -> None:
        self.reliability = min(1.0, self.reliability + amount)
        self._refresh_health()

    def _refresh_health(self) -> None:
        observed = 1.0 - (self.failures / max(1, self.calls))
        blended = 0.5 * observed + 0.5 * self.reliability
        self.vital_variables = {"tool_reliability": max(0.0, min(1.0, blended))}
        self.homeostatic_debt = max(0.0, min(1.0, 1.0 - blended))
        self.recovery_reserve = max(0.0, min(1.0, self.reliability))
        self.set_status_from_debt()
