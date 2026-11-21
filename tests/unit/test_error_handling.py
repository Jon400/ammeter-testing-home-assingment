"""
Tests for error handling in the simulator client and measurement service.
"""

import pytest

from simulator.simulator_ammeter import SimulatorError
from src.clients.simulator_client import SimulatorClient
from src.mesurements.measurements_service import MeasurementService

# The fixtures (simulator_config, simulator, client) are in conftest.py


def take_measurements(client: SimulatorClient):
    """Take 3 samples at 10 Hz, for at most 1 second."""
    return MeasurementService().take_measurements(
        client,
        number_of_samples=3,
        sample_rate=10.0,
        total_duration=1.0,
    )


#################################
# Client
#################################

@pytest.mark.usefixtures("simulator")  # start the simulator; the test does not change it
def test_client_reads_current(client):
    assert 0.9 <= client.measure_current() <= 1.1


def test_client_times_out_when_ammeter_does_not_respond(simulator, client):
    simulator.error = SimulatorError.NO_RESPONSE
    with pytest.raises(TimeoutError):
        client.measure_current()


def test_client_rejects_reply_that_is_not_a_number(simulator, client):
    simulator.error = SimulatorError.BAD_REPLY
    with pytest.raises(ValueError, match="not a number"):
        client.measure_current()


#################################
# Measurement service
#################################

@pytest.mark.usefixtures("simulator")
def test_service_takes_all_samples(client):
    result = take_measurements(client)
    assert result.measurement_data.stats.count == 3
    assert result.failed_samples == 0


def test_service_fails_when_ammeter_does_not_respond(simulator, client):
    simulator.error = SimulatorError.NO_RESPONSE
    with pytest.raises(RuntimeError, match="No measurements were taken"):
        take_measurements(client)


def test_service_fails_when_every_reply_is_bad(simulator, client):
    simulator.error = SimulatorError.BAD_REPLY
    with pytest.raises(RuntimeError, match=r"No measurements were taken \(3 failed\)"):
        take_measurements(client)
