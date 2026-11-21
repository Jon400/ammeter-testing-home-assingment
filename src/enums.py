"""Shared enums"""

from enum import Enum


class AmmeterType(str, Enum):
    """Supported ammeter types"""

    ENTES = "entes"
    CIRCUTOR = "circutor"
    GREENLEE = "greenlee"
    SIMULATOR = "simulator"
