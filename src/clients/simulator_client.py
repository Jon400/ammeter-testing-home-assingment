"""Simulator ammeter client"""

from src.clients.ammeter_client import AmmeterClient
from src.enums import AmmeterType


class SimulatorClient(AmmeterClient):
    AMMETER_TYPE = AmmeterType.SIMULATOR
    MEASURE_COMMAND = b"MEASURE_SIMULATOR -get_current"

    def get_current_command(self) -> bytes:
        """Get the command to measure current from the simulator."""
        return self.MEASURE_COMMAND

    def get_ammeter_type(self) -> AmmeterType:
        """Get the type of the ammeter."""
        return self.AMMETER_TYPE
