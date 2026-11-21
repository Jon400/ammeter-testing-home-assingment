"""Greenlee ammeter client"""

from src.clients.ammeter_client import AmmeterClient
from src.enums import AmmeterType


class GreenleeClient(AmmeterClient):
    AMMETER_TYPE = AmmeterType.GREENLEE
    MEASURE_COMMAND = b"MEASURE_GREENLEE -get_measurement"

    def get_current_command(self) -> bytes:
        """Get the command to measure current from the Greenlee ammeter."""
        return self.MEASURE_COMMAND

    def get_ammeter_type(self) -> AmmeterType:
        """Get the type of the ammeter."""
        return self.AMMETER_TYPE
