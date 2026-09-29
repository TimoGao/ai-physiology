from __future__ import annotations
from typing import Any, Dict, List
from .models import HealthStatus, BloodPacket


class Organ:
    def __init__(self, organism_id: str, organ_id: str, organ_type: str):
        self.organism_id = organism_id
        self.organ_id = organ_id
        self.organ_type = organ_type
        self.health_status = HealthStatus.HEALTHY
        self.vital_variables: Dict[str, float] = {}
        self.homeostatic_debt: float = 0.0
        self.recovery_reserve: float = 1.0
        self.allowed_actions: List[str] = []
        self.warning_conditions: List[str] = []
        self.critical_conditions: List[str] = []
        self.history: List[Dict[str, Any]] = []

    def uptake(self, packet: BloodPacket) -> None:
        raise NotImplementedError

    def release(self) -> List[BloodPacket]:
        return []

    def inspect_health(self) -> Dict[str, Any]:
        return {
            "organ_id": self.organ_id,
            "organ_type": self.organ_type,
            "health_status": self.health_status.value,
            "vital_variables": dict(self.vital_variables),
            "homeostatic_debt": round(self.homeostatic_debt, 4),
            "recovery_reserve": round(self.recovery_reserve, 4),
        }

    def set_status_from_debt(self) -> None:
        if self.health_status in {HealthStatus.OFFLINE, HealthStatus.QUARANTINED}:
            return
        if self.homeostatic_debt >= 0.8 or self.recovery_reserve <= 0.2:
            self.health_status = HealthStatus.CRITICAL
        elif self.homeostatic_debt >= 0.5 or self.recovery_reserve <= 0.4:
            self.health_status = HealthStatus.DEGRADED
        elif self.homeostatic_debt >= 0.25:
            self.health_status = HealthStatus.STRESSED
        else:
            self.health_status = HealthStatus.HEALTHY
