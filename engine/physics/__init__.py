"""
Graph Physics Engine

Energy flow, decay, pressure, and flip detection.
The living world simulation that runs without LLM.

Usage:
    from engine.physics import GraphTick

    tick = GraphTick()
    tick.run(elapsed_minutes=30)
"""

from .tick import GraphTick
from .constants import *

__all__ = ['GraphTick']
