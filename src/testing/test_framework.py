"""Runs measurement tests on the ammeters listed in the config file."""

import os
from datetime import datetime

from src.clients.ammeter_client import AmmeterClient
from src.clients.circutor_client import CircutorClient
from src.clients.entes_client import EntesClient
from src.clients.greenlee_client import GreenleeClient
from src.config import load_config
from src.enums import AmmeterType
from src.mesurements.measurements_service import MeasurementService
from src.mesurements.results_manager import ResultsManager
from src.models import MeasurementResult, MeasurementSummary
from src.utils.classes.test_logger import TestLogger
from src.utils.libraries.file_utils import FileUtils

# Which client class talks to which ammeter type
CLIENT_CLASSES = {
    AmmeterType.GREENLEE: GreenleeClient,
    AmmeterType.ENTES: EntesClient,
    AmmeterType.CIRCUTOR: CircutorClient,
}


class AmmeterTestFramework:

    def __init__(self, config_path: str = "config/config.yaml"):
        # Set up once, shared by every test
        self.config = load_config(config_path)
        self.results_dir = self.config.results_dir
        self.log_dir = self.config.logging.log_dir
        self.service = MeasurementService()
        self.results_manager = ResultsManager(self.results_dir)

    #################################
    # Fixtures
    #################################

    def create_client(self, ammeter_type: AmmeterType) -> AmmeterClient:
        """Create the client for an ammeter type, with its host and port from the config."""
        ammeter_type = AmmeterType(ammeter_type)
        if ammeter_type not in self.config.ammeters:
            raise ValueError(f"{ammeter_type.value} is not in the config file")

        ammeter = self.config.ammeters[ammeter_type]
        return CLIENT_CLASSES[ammeter_type](ammeter.host, ammeter.port)

    def create_logger(self, test_name: str) -> TestLogger:
        """Create a logger for a test, writing to its own file in the config's log folder."""
        FileUtils.create_folder(self.log_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.log_dir, f"{timestamp}_{test_name}.log")
        return TestLogger(test_name, log_file, self.config.logging.log_level)

    #################################
    # Tests
    #################################

    def run_test(self, ammeter_type: AmmeterType) -> MeasurementResult:
        """Measure one ammeter with the config's sampling settings, save the result, and return it."""
        ammeter_type = AmmeterType(ammeter_type)  # also accepts the name as text, e.g. "greenlee"
        logger = self.create_logger(ammeter_type.value)
        sampling = self.config.sampling

        try:
            logger.info(
                f"Test started: {sampling.number_of_samples} samples at {sampling.sample_rate} Hz, "
                f"at most {sampling.total_duration} s"
            )
            result = self.service.take_measurements(
                self.create_client(ammeter_type),
                sampling.number_of_samples,
                sampling.sample_rate,
                sampling.total_duration,
            )
            for sample in result.measurement_data.samples:
                logger.debug(f"{sample.timestamp:.3f} s: {sample.current} {sample.unit}")

            stats = result.measurement_data.stats
            logger.info(
                f"Test finished: count={stats.count} mean={stats.mean_current:.4f} "
                f"std={stats.std_dev_current:.4f} failed={result.failed_samples}"
            )
            logger.info(f"Result saved to {self.results_manager.save_result(result)}")
            return result
        except RuntimeError as error:
            logger.error(f"Test failed: {error}")
            raise
        finally:
            logger.close()  # close the log file, even if the test failed

    def run_all_tests(self) -> MeasurementSummary:
        """Run the test on every ammeter in the config. An ammeter that fails is logged and skipped."""
        results = []
        for ammeter_type in self.config.ammeters:
            try:
                results.append(self.run_test(ammeter_type))
            except RuntimeError:
                pass  # run_test already logged why it failed; go on with the next ammeter

        return self.service.get_measurement_summary(results)
