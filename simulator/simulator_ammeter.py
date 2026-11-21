"""A very basic ammeter simulator for testing, built like the emulators in Ammeters/."""

import random
import socket
from enum import Enum


class SimulatorError(str, Enum):
    NONE = "none"              
    NO_RESPONSE = "no_response"  # the server will not reply to the command, simulating a timeout
    BAD_REPLY = "bad_reply"      # replies with text that is not a number


class SimulatorAmmeter:
    def __init__(self, host: str = "localhost", port: int = 5004, error: SimulatorError = SimulatorError.NONE):
        self.host = host
        self.port = port
        self.error = error
        self.running = False

    @property
    def get_current_command(self) -> bytes:
        # Define the command to get the current from the simulator
        return b"MEASURE_SIMULATOR -get_current"

    def measure_current(self) -> float:
        return random.uniform(0.9, 1.1)  # Random current (0.9A - 1.1A)

    def start_server(self):
        with socket.create_server((self.host, self.port)) as s:
            s.settimeout(0.1)  # check every 0.1 s whether stop_server() was called
            self.running = True
            print(f"{self.__class__.__name__} is running on port {self.port}")
            while self.running:
                try:
                    conn, _ = s.accept()
                except socket.timeout:
                    continue  # no client yet
                with conn:
                    data = conn.recv(1024)
                    if data != self.get_current_command:
                        continue  # unknown command: close without replying
                    if self.error == SimulatorError.NO_RESPONSE:
                        conn.recv(1024)  # say nothing; wait until the client gives up
                    elif self.error == SimulatorError.BAD_REPLY:
                        conn.sendall(b"ERROR")
                    else:
                        conn.sendall(str(self.measure_current()).encode("utf-8"))

    def stop_server(self):
        self.running = False  # start_server() ends within 0.1 s
