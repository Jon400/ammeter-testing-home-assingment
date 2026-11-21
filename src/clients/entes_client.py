"""Entes ammeter client"""

from src.clients.ammeter_client import AmmeterClient
from src.enums import AmmeterType


class EntesClient(AmmeterClient):
    AMMETER_TYPE = AmmeterType.ENTES
    MEASURE_COMMAND = b"MEASURE_ENTES -get_data"

    def get_current_command(self) -> bytes:
        """Get the command to measure current from the Entes ammeter."""
        return self.MEASURE_COMMAND

    def get_ammeter_type(self) -> AmmeterType:
        """Get the type of the ammeter."""
        return self.AMMETER_TYPE
