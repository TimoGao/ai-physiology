from __future__ import annotations
from collections import deque
from typing import Deque, Dict, List
import time
from .models import BloodPacket


class AIBlood:
    """A tiny in-memory circulation layer for MAO v0.1.

    It is intentionally not a production message bus. Its purpose is to make
    provenance, TTL, risk and circulation health explicit.
    """

    def __init__(self, organism_id: str, max_queue: int = 1000):
        self.organism_id = organism_id
        self.max_queue = max_queue
        self.queue: Deque[BloodPacket] = deque()
        self.quarantine: Deque[BloodPacket] = deque()
        self.published = 0
        self.delivered = 0
        self.dropped = 0
        self.expired = 0
        self.quarantined = 0
        self.delivery_latencies_ms: List[float] = []

    def publish(self, packet: BloodPacket) -> bool:
        if packet.organism_id != self.organism_id:
            self.dropped += 1
            return False
        if packet.quarantine_required or packet.risk_level >= 0.8:
            self.quarantine.append(packet)
            self.quarantined += 1
            return False
        if len(self.queue) >= self.max_queue:
            self.dropped += 1
            return False
        self.queue.append(packet)
        self.published += 1
        return True

    def drain(self, limit: int = 100) -> List[BloodPacket]:
        now = time.time()
        out: List[BloodPacket] = []
        for _ in range(min(limit, len(self.queue))):
            packet = self.queue.popleft()
            if packet.expired(now) or packet.hops >= packet.max_hops:
                self.expired += 1
                continue
            packet.hops += 1
            packet.lineage.append("blood")
            self.delivery_latencies_ms.append((now - packet.created_at) * 1000)
            self.delivered += 1
            out.append(packet)
        return out

    def pressure(self) -> float:
        queue_ratio = min(1.0, len(self.queue) / max(1, self.max_queue))
        drop_ratio = self.dropped / max(1, self.published + self.dropped)
        quarantine_ratio = self.quarantined / max(1, self.published + self.quarantined)
        return min(1.0, 0.65 * queue_ratio + 0.25 * drop_ratio + 0.10 * quarantine_ratio)

    def health(self) -> Dict[str, float]:
        avg_latency = (
            sum(self.delivery_latencies_ms) / len(self.delivery_latencies_ms)
            if self.delivery_latencies_ms else 0.0
        )
        return {
            "pressure": round(self.pressure(), 4),
            "queue_depth": len(self.queue),
            "quarantine_depth": len(self.quarantine),
            "published": self.published,
            "delivered": self.delivered,
            "dropped": self.dropped,
            "expired": self.expired,
            "quarantined": self.quarantined,
            "avg_latency_ms": round(avg_latency, 4),
        }
