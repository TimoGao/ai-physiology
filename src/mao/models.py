from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time
import uuid


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    STRESSED = "stressed"
    INJURED = "injured"
    QUARANTINED = "quarantined"
    RECOVERING = "recovering"
    CRITICAL = "critical"
    OFFLINE = "offline"


class OrganismMode(str, Enum):
    NORMAL = "normal"
    STRESS = "stress"
    ALERT = "alert"
    RECOVERY = "recovery"


@dataclass
class VitalSign:
    id: str
    value: float
    confidence: float = 1.0
    preferred_min: Optional[float] = None
    preferred_max: Optional[float] = None
    viable_min: Optional[float] = None
    viable_max: Optional[float] = None
    critical_min: Optional[float] = None
    critical_max: Optional[float] = None
    trend: str = "unknown"
    updated_at: float = field(default_factory=time.time)

    def clamp(self) -> None:
        self.value = max(0.0, min(1.0, float(self.value)))
        self.confidence = max(0.0, min(1.0, float(self.confidence)))

    def is_critical(self) -> bool:
        if self.critical_min is not None and self.value < self.critical_min:
            return True
        if self.critical_max is not None and self.value > self.critical_max:
            return True
        return False


@dataclass
class BloodPacket:
    organism_id: str
    source_organ: str
    destination_scope: str
    payload_type: str
    body: Any
    priority: int = 5
    ttl_ms: int = 60000
    confidence: float = 1.0
    risk_level: float = 0.0
    quarantine_required: bool = False
    source_type: str = "organ"
    packet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: float = field(default_factory=time.time)
    hops: int = 0
    max_hops: int = 16
    lineage: List[str] = field(default_factory=list)

    def expired(self, now: Optional[float] = None) -> bool:
        now = time.time() if now is None else now
        return (now - self.created_at) * 1000 > self.ttl_ms

    def as_dict(self) -> Dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "organism_id": self.organism_id,
            "source_organ": self.source_organ,
            "destination_scope": self.destination_scope,
            "payload_type": self.payload_type,
            "body": self.body,
            "priority": self.priority,
            "ttl_ms": self.ttl_ms,
            "confidence": self.confidence,
            "risk_level": self.risk_level,
            "quarantine_required": self.quarantine_required,
            "source_type": self.source_type,
            "created_at": self.created_at,
            "hops": self.hops,
            "max_hops": self.max_hops,
            "lineage": list(self.lineage),
        }
