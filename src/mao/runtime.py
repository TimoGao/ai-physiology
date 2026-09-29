from __future__ import annotations
from typing import Any, Dict, List
import random
from .blood import AIBlood
from .models import BloodPacket
from .homeostasis import HomeostasisLayer
from .organs.memory import MemoryOrgan
from .organs.tool import ToolOrgan


class MinimalArtificialOrganism:
    """Reference implementation for MAO v0.1.

    This is a research prototype, not production infrastructure.
    """

    def __init__(self, organism_id: str = "mao-001", seed: int = 7):
        random.seed(seed)
        self.organism_id = organism_id
        self.blood = AIBlood(organism_id)
        self.memory = MemoryOrgan(organism_id)
        self.tool = ToolOrgan(organism_id)
        self.homeostasis = HomeostasisLayer()
        self.low_priority_paused = False
        self.cycles = 0
        self.operator_interventions = 0
        self.unresolved_errors = 0
        self.security_risk = 0.0
        self.resource_pressure = 0.20
        self.history: List[Dict[str, Any]] = []

    def publish_task(self, task: Any, priority: int = 5) -> None:
        self.blood.publish(BloodPacket(
            organism_id=self.organism_id,
            source_organ="runtime",
            destination_scope="multi_organ",
            payload_type="task",
            body=task,
            priority=priority,
            confidence=1.0,
            risk_level=self.security_risk,
        ))

    def cycle(self, task: Any) -> Dict[str, Any]:
        self.cycles += 1
        self.publish_task(task)
        tool_packet = self.tool.execute(task)
        self.blood.publish(tool_packet)

        for packet in self.blood.drain():
            if packet.payload_type in {"tool_result", "task_result", "memory_candidate"}:
                self.memory.uptake(packet)

        if tool_packet.body.get("ok") is False:
            self.unresolved_errors += 1
        else:
            self.unresolved_errors = max(0, self.unresolved_errors - 1)

        signs = self.homeostasis.update(self.measure_vitals())
        actions = self.homeostasis.regulate(self)

        snapshot = {
            "cycle": self.cycles,
            "mode": self.homeostasis.mode.value,
            "vitals": {k: round(v.value, 4) for k, v in signs.items()},
            "actions": actions,
            "memory": self.memory.inspect_health(),
            "tool": self.tool.inspect_health(),
            "blood": self.blood.health(),
            "homeostatic_debt": round(self.homeostatic_debt(), 4),
            "recovery_reserve": round(self.recovery_reserve(), 4),
        }
        self.history.append(snapshot)
        return snapshot

    def measure_vitals(self) -> Dict[str, float]:
        memory_integrity = self.memory.vital_variables.get("memory_integrity", 1.0)
        tool_reliability = self.tool.vital_variables.get("tool_reliability", self.tool.reliability)
        context_saturation = self.memory.context_saturation()
        resource_pressure = min(1.0, max(self.resource_pressure, self.blood.pressure()))
        return {
            "context_saturation": context_saturation,
            "memory_integrity": memory_integrity,
            "resource_pressure": resource_pressure,
            "tool_reliability": tool_reliability,
            "security_risk": self.security_risk,
        }

    def homeostatic_debt(self) -> float:
        error_debt = min(1.0, self.unresolved_errors / 10)
        return min(1.0, 0.55 * self.memory.homeostatic_debt + 0.25 * self.tool.homeostatic_debt + 0.20 * error_debt)

    def recovery_reserve(self) -> float:
        return max(0.0, min(1.0, 0.5 * self.memory.recovery_reserve + 0.5 * self.tool.recovery_reserve))

    def quarantine_risky_packets(self) -> None:
        remaining = []
        while self.blood.queue:
            packet = self.blood.queue.popleft()
            if packet.risk_level >= 0.5:
                packet.quarantine_required = True
                self.blood.quarantine.append(packet)
                self.blood.quarantined += 1
            else:
                remaining.append(packet)
        for packet in remaining:
            self.blood.queue.append(packet)

    def inject_memory_noise(self, copies: int = 1, confidence: float = 0.55) -> None:
        for _ in range(copies):
            packet = BloodPacket(
                organism_id=self.organism_id,
                source_organ="noise_injector",
                destination_scope="organ",
                payload_type="memory_candidate",
                body={"fact": "duplicate-noise"},
                confidence=confidence,
                risk_level=0.10,
            )
            self.memory.uptake(packet)

    def set_security_risk(self, level: float) -> None:
        self.security_risk = max(0.0, min(1.0, level))

    def set_resource_pressure(self, level: float) -> None:
        self.resource_pressure = max(0.0, min(1.0, level))
