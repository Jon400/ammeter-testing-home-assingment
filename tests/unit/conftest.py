"""Fixtures shared by the unit tests."""

import os
import threading
import time

import pytest
import yaml

from simulator.simulator_ammeter import SimulatorAmmeter
from src.clients.simulator_client import SimulatorClient
from src.config import AmmeterConfig
from src.utils.libraries.file_utils import FileUtils


@pytest.fixture
def simulator_config() -> AmmeterConfig:
    """
    Load the simulator's host and port from config/config.yaml.

    Returns:
        AmmeterConfig: The simulator's host and port.
    """
    config_path = os.path.join(os.path.dirname(__file__), "../../config/config.yaml")  # two folders up
    return AmmeterConfig(**yaml.safe_load(FileUtils.read_file(config_path))["simulator"])


@pytest.fixture
def simulator(simulator_config: AmmeterConfig):
    """
    Start the simulator before the test and stop it after the test.

    Args:
        simulator_config (AmmeterConfig): The simulator's host and port.

    Yields:
        SimulatorAmmeter: The running simulator. Set its error to make it fail.
    """
    simulator = SimulatorAmmeter(simulator_config.host, simulator_config.port)
    thread = threading.Thread(target=simulator.start_server, daemon=True)
    thread.start()
    while not simulator.running and thread.is_alive():
        time.sleep(0.01)  # wait until it is listening (or it failed to start)

    yield simulator

    simulator.stop_server()
    thread.join()


@pytest.fixture
def client(simulator_config: AmmeterConfig) -> SimulatorClient:
    """
    Create a client for the simulator, with a short timeout so the tests are fast.

    Args:
        simulator_config (AmmeterConfig): The simulator's host and port.

    Returns:
        SimulatorClient: The client that talks to the simulator.
    """
    return SimulatorClient(simulator_config.host, simulator_config.port, timeout=0.5)
