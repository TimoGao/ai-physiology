from __future__ import annotations
from typing import Dict, List
from .models import OrganismMode, VitalSign


class HomeostasisLayer:
    def __init__(self):
        self.mode = OrganismMode.NORMAL
        self.last_actions: List[str] = []
        self.vital_signs: Dict[str, VitalSign] = {}

    def update(self, values: Dict[str, float]) -> Dict[str, VitalSign]:
        specs = {
            "context_saturation": dict(preferred_min=0.30, preferred_max=0.70, viable_min=0.0, viable_max=0.90, critical_max=0.90),
            "memory_integrity": dict(preferred_min=0.95, preferred_max=1.0, viable_min=0.75, viable_max=1.0, critical_min=0.75),
            "resource_pressure": dict(preferred_min=0.0, preferred_max=0.70, viable_min=0.0, viable_max=0.90, critical_max=0.90),
            "tool_reliability": dict(preferred_min=0.95, preferred_max=1.0, viable_min=0.70, viable_max=1.0, critical_min=0.70),
            "security_risk": dict(preferred_min=0.0, preferred_max=0.20, viable_min=0.0, viable_max=0.70, critical_max=0.70),
        }
        for key, value in values.items():
            spec = specs[key]
            previous = self.vital_signs.get(key)
            trend = "unknown"
            if previous:
                if value > previous.value + 1e-6:
                    trend = "rising"
                elif value < previous.value - 1e-6:
                    trend = "falling"
                else:
                    trend = "stable"
            sign = VitalSign(id=key, value=value, trend=trend, **spec)
            sign.clamp()
            self.vital_signs[key] = sign
        return self.vital_signs

    def regulate(self, organism: "MinimalArtificialOrganism") -> List[str]:
        self.last_actions = []
        vs = self.vital_signs
        if vs["security_risk"].value > 0.70:
            self.mode = OrganismMode.ALERT
            organism.quarantine_risky_packets()
            self.last_actions.append("quarantine_risky_packets")
        elif vs["memory_integrity"].value < 0.80:
            self.mode = OrganismMode.RECOVERY
            result = organism.memory.maintenance()
            self.last_actions.append(f"memory_maintenance:{result['removed']}")
        elif vs["context_saturation"].value > 0.90:
            self.mode = OrganismMode.STRESS
            result = organism.memory.maintenance()
            self.last_actions.append(f"context_cleanup:{result['removed']}")
        elif vs["resource_pressure"].value > 0.90:
            self.mode = OrganismMode.STRESS
            organism.low_priority_paused = True
            self.last_actions.append("pause_low_priority_work")
        elif vs["tool_reliability"].value < 0.70:
            self.mode = OrganismMode.RECOVERY
            organism.tool.recover(0.12)
            self.last_actions.append("tool_recovery")
        else:
            self.mode = OrganismMode.NORMAL
            organism.low_priority_paused = False
        return list(self.last_actions)
