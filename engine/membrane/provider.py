from __future__ import annotations

from typing import Dict, Optional

from .frame import ModulationFrame


class MembraneProvider:
    """Stores place-scoped modulation frames for hot-path read access."""

    def __init__(self) -> None:
        self._frames: Dict[str, ModulationFrame] = {}

    def set_frame(self, place_id: str, frame: Optional[ModulationFrame]) -> None:
        self._frames[place_id] = frame or ModulationFrame.neutral()

    def get_frame(self, place_id: str) -> ModulationFrame:
        return self._frames.get(place_id, ModulationFrame.neutral())

    def reset_place(self, place_id: str) -> None:
        self._frames.pop(place_id, None)
