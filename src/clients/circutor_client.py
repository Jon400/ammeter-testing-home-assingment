"""Circutor ammeter client"""

from src.clients.ammeter_client import AmmeterClient
from src.enums import AmmeterType


class CircutorClient(AmmeterClient):
    AMMETER_TYPE = AmmeterType.CIRCUTOR
    MEASURE_COMMAND = b"MEASURE_CIRCUTOR -get_measurement -current"

    def get_current_command(self) -> bytes:
        """Get the command to measure current from the Circutor ammeter."""
        return self.MEASURE_COMMAND

    def get_ammeter_type(self) -> AmmeterType:
        """Get the type of the ammeter."""
        return self.AMMETER_TYPE
