from __future__ import annotations

from typing import Any, Mapping

from .frame import ModulationFrame


def compute_modulation_frame(place_id: str, aggregates: Mapping[str, Any]) -> ModulationFrame:
    """Return a bounded modulation frame based on precomputed aggregates."""
    _ = place_id
    _ = aggregates
    return ModulationFrame.neutral()
