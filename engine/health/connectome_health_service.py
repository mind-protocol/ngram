"""
Connectome Health Service

Aggregates health signals from ALL systems:
1. Graph schema health (node/link validation)
2. Physics tick metrics (energy flow, completions)
3. Attention split stats (sink set size, allocations)
4. Contradiction pressure (narrative conflict values)
5. Project doctor health (optional, if available)

DOCS: docs/connectome/health/HEALTH_Connectome_Live_Signals.md
"""

import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class RunnerState:
    """Runner/tick state."""
    speed: str = "pause"
    tick: int = 0
    last_interrupt: Optional[Dict[str, Any]] = None


@dataclass
class AttentionStats:
    """Attention split statistics."""
    sink_set_size: Dict[str, int] = field(default_factory=lambda: {"p50": 0, "p95": 0})
    neighborhood_size: Dict[str, int] = field(default_factory=lambda: {"nodes": 0, "edges": 0})
    focus_reconfig_rate_per_min: float = 0.0
    plateau_seconds: int = 0


@dataclass
class PressureStats:
    """Contradiction pressure statistics."""
    contradiction: float = 0.0
    top_edges: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class Counters:
    """Hard invariant counters."""
    query_write_attempts: int = 0
    dmz_violation_attempts: int = 0
    async_epoch_mismatch: int = 0


@dataclass
class StatusInfo:
    """Overall health status."""
    state: str = "UNKNOWN"  # OK, WARN, ERROR, UNKNOWN
    score: float = 0.0
    notes: List[str] = field(default_factory=list)


@dataclass
class ConnectomeHealthPayload:
    """Full health payload matching SSE event format."""
    ts: int = 0
    playthrough_id: str = ""
    place_id: str = ""
    status: StatusInfo = field(default_factory=StatusInfo)
    runner: RunnerState = field(default_factory=RunnerState)
    counters: Counters = field(default_factory=Counters)
    attention: AttentionStats = field(default_factory=AttentionStats)
    pressure: PressureStats = field(default_factory=PressureStats)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ts": self.ts,
            "playthrough_id": self.playthrough_id,
            "place_id": self.place_id,
            "status": asdict(self.status),
            "runner": {
                "speed": self.runner.speed,
                "tick": self.runner.tick,
                "last_interrupt": self.runner.last_interrupt,
            },
            "counters": asdict(self.counters),
            "attention": {
                "sink_set_size": self.attention.sink_set_size,
                "neighborhood_size": self.attention.neighborhood_size,
                "focus_reconfig_rate_per_min": self.attention.focus_reconfig_rate_per_min,
                "plateau_seconds": self.attention.plateau_seconds,
            },
            "pressure": {
                "contradiction": self.pressure.contradiction,
                "top_edges": self.pressure.top_edges,
            },
        }


class ConnectomeHealthService:
    """
    Aggregates health signals from all engine systems.

    Usage:
        service = ConnectomeHealthService()

        # After each tick:
        service.record_tick(tick_result)
        service.record_attention(attention_result)
        service.record_pressure(pressure_result)

        # Get current health:
        payload = service.get_health()
    """

    def __init__(self):
        self._runner = RunnerState()
        self._attention = AttentionStats()
        self._pressure = PressureStats()
        self._counters = Counters()
        self._playthrough_id = ""
        self._place_id = ""
        self._last_interrupt: Optional[Dict[str, Any]] = None
        self._interrupt_history: List[int] = []  # timestamps for rate calc
        self._last_focus_change: int = 0

    def set_context(self, playthrough_id: str, place_id: str):
        """Set current playthrough/place context."""
        self._playthrough_id = playthrough_id
        self._place_id = place_id

    def set_speed(self, speed: str):
        """Update runner speed (pause, x1, x2, x3)."""
        self._runner.speed = speed

    def record_tick(self, tick: int, energy_total: float = 0.0, completions: int = 0):
        """Record tick advancement."""
        self._runner.tick = tick

    def record_interrupt(self, reason: str, moment_id: str = ""):
        """Record an interrupt event."""
        now = int(time.time())
        self._last_interrupt = {
            "reason": reason,
            "moment_id": moment_id,
            "age_ticks": 0,
        }
        self._runner.last_interrupt = self._last_interrupt
        self._interrupt_history.append(now)
        # Keep last 60 seconds
        cutoff = now - 60
        self._interrupt_history = [t for t in self._interrupt_history if t >= cutoff]

    def record_attention(
        self,
        sink_count: int,
        node_count: int = 0,
        edge_count: int = 0,
    ):
        """Record attention split statistics."""
        # Simple p50/p95 approximation (would need history for real percentiles)
        self._attention.sink_set_size = {"p50": sink_count, "p95": sink_count}
        self._attention.neighborhood_size = {"nodes": node_count, "edges": edge_count}
        # Reconfig rate from interrupt history
        self._attention.focus_reconfig_rate_per_min = len(self._interrupt_history)

    def record_pressure(self, pressure: float, top_edges: List[Dict[str, Any]] = None):
        """Record contradiction pressure."""
        self._pressure.contradiction = pressure
        if top_edges:
            self._pressure.top_edges = top_edges[:5]  # Limit to top 5

    def record_violation(self, violation_type: str):
        """Record a hard invariant violation."""
        if violation_type == "query_write":
            self._counters.query_write_attempts += 1
        elif violation_type == "dmz":
            self._counters.dmz_violation_attempts += 1
        elif violation_type == "async_epoch":
            self._counters.async_epoch_mismatch += 1

    def get_health(self) -> ConnectomeHealthPayload:
        """Get current health payload."""
        # Compute status
        notes = []
        state = "OK"
        score = 1.0

        # Hard violations = ERROR
        if self._counters.query_write_attempts > 0:
            state = "ERROR"
            score = 0.0
            notes.append(f"Query write violations: {self._counters.query_write_attempts}")

        if self._counters.dmz_violation_attempts > 0:
            state = "ERROR"
            score = 0.0
            notes.append(f"DMZ violations: {self._counters.dmz_violation_attempts}")

        # Async mismatches = WARN
        if self._counters.async_epoch_mismatch > 0 and state != "ERROR":
            state = "WARN"
            score = min(score, 0.7)
            notes.append(f"Async epoch mismatches: {self._counters.async_epoch_mismatch}")

        # High pressure = WARN
        if self._pressure.contradiction > 0.8 and state == "OK":
            state = "WARN"
            score = min(score, 0.8)
            notes.append(f"High contradiction pressure: {self._pressure.contradiction:.2f}")

        if not notes:
            notes.append("All systems nominal")

        return ConnectomeHealthPayload(
            ts=int(time.time()),
            playthrough_id=self._playthrough_id,
            place_id=self._place_id,
            status=StatusInfo(state=state, score=score, notes=notes),
            runner=self._runner,
            counters=self._counters,
            attention=self._attention,
            pressure=self._pressure,
        )


# Singleton for global access
_health_service: Optional[ConnectomeHealthService] = None


def get_health_service() -> ConnectomeHealthService:
    """Get the global health service singleton."""
    global _health_service
    if _health_service is None:
        _health_service = ConnectomeHealthService()
    return _health_service


def get_current_health() -> Dict[str, Any]:
    """Get current health as a dict (for SSE broadcasting)."""
    return get_health_service().get_health().to_dict()
