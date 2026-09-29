from __future__ import annotations
from typing import Any, Dict, List
import time
from ..organ import Organ
from ..models import BloodPacket


class MemoryOrgan(Organ):
    def __init__(self, organism_id: str, organ_id: str = "memory"):
        super().__init__(organism_id, organ_id, "memory")
        self.records: List[Dict[str, Any]] = []
        self.allowed_actions = ["store", "deduplicate", "remove_stale", "quarantine_low_confidence"]

    def uptake(self, packet: BloodPacket) -> None:
        if packet.payload_type not in {"memory_candidate", "tool_result", "task_result"}:
            return
        if packet.risk_level >= 0.7 or packet.confidence < 0.5:
            self.homeostatic_debt = min(1.0, self.homeostatic_debt + 0.04)
            return
        self.records.append({
            "value": packet.body,
            "confidence": packet.confidence,
            "created_at": packet.created_at,
            "source": packet.source_organ,
        })
        self._refresh_health()

    def _refresh_health(self) -> None:
        if not self.records:
            integrity = 1.0
            duplicate_ratio = 0.0
            stale_ratio = 0.0
        else:
            values = [repr(r["value"]) for r in self.records]
            duplicate_ratio = 1.0 - (len(set(values)) / len(values))
            now = time.time()
            stale_ratio = sum((now - r["created_at"]) > 3600 for r in self.records) / len(self.records)
            avg_conf = sum(r["confidence"] for r in self.records) / len(self.records)
            integrity = max(0.0, min(1.0, avg_conf - 0.45 * duplicate_ratio - 0.35 * stale_ratio))
        self.vital_variables = {
            "memory_integrity": integrity,
            "duplicate_ratio": duplicate_ratio,
            "stale_ratio": stale_ratio,
        }
        self.homeostatic_debt = min(1.0, 0.65 * duplicate_ratio + 0.35 * stale_ratio)
        self.recovery_reserve = max(0.0, 1.0 - 0.8 * self.homeostatic_debt)
        self.set_status_from_debt()

    def maintenance(self) -> Dict[str, int]:
        before = len(self.records)
        seen = set()
        clean = []
        for r in reversed(self.records):
            key = repr(r["value"])
            if key in seen:
                continue
            if r["confidence"] < 0.55:
                continue
            seen.add(key)
            clean.append(r)
        self.records = list(reversed(clean))
        self._refresh_health()
        return {"removed": before - len(self.records), "remaining": len(self.records)}

    def context_saturation(self, soft_capacity: int = 100) -> float:
        return min(1.0, len(self.records) / max(1, soft_capacity))
