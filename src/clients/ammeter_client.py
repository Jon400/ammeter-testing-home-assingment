"""Ammeter client implementation"""


from abc import ABC, abstractmethod

from src.clients.base_tcp_client import BaseTCPClient
from src.enums import AmmeterType


class AmmeterClient(BaseTCPClient, ABC):

    def __init__(self, host: str, port: int, timeout: float = 5.0):
        super().__init__(host, port, timeout)
        
    
    @abstractmethod
    def get_current_command(self) -> bytes:
        """Get the command to measure current from the ammeter."""
        raise NotImplementedError("Subclasses must implement this method.")


    @abstractmethod
    def get_ammeter_type(self) -> AmmeterType:
        """Get the type of the ammeter."""
        raise NotImplementedError("Subclasses must implement this method.")


    def measure_current(self) -> float:
        """Measure the current from the ammeter."""
        try:
            self.connect()
            current_command = self.get_current_command()
            self.send(current_command)
            response = self.receive()
        finally:
            self.close()

        name = f"{self.get_ammeter_type().value} ammeter on {self.host}:{self.port}"

        # The emulator closes without replying when it does not know the command
        if not response:
            raise ConnectionError(f"{name} returned no data (check the command)")

        reply = response.decode("utf-8").strip()
        try:
            return float(reply)
        except ValueError:
            raise ValueError(f"{name} sent a reply that is not a number: {reply!r}") from None
        
        
