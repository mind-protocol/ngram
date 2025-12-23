from .frame import ModulationFrame
from .provider import MembraneProvider
from .compute import compute_modulation_frame
from .functions import (
    MembraneContext,
    activation_threshold,
    clamp,
    decay_scale,
    dramatic_boost_scale,
    weight_transfer_multiplier,
)

__all__ = [
    "ModulationFrame",
    "MembraneProvider",
    "MembraneContext",
    "activation_threshold",
    "clamp",
    "compute_modulation_frame",
    "decay_scale",
    "dramatic_boost_scale",
    "weight_transfer_multiplier",
]
