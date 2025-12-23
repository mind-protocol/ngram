"""
Engine Health Module

Provides health aggregation and monitoring for the game engine.

Components:
- ConnectomeHealthService: Aggregates runtime health signals
- ActivityLogger: Two-tier logging (summary + detail)
"""

from .connectome_health_service import (
    ConnectomeHealthService,
    ConnectomeHealthPayload,
    get_health_service,
    get_current_health,
)

from .activity_logger import (
    ActivityLogger,
    get_activity_logger,
)

__all__ = [
    "ConnectomeHealthService",
    "ConnectomeHealthPayload",
    "get_health_service",
    "get_current_health",
    "ActivityLogger",
    "get_activity_logger",
]
