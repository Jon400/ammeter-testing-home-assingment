"""Takes measurements from an ammeter and calculates their statistics."""

import statistics
import time
from datetime import datetime, timezone

from src.clients.ammeter_client import AmmeterClient
from src.config import SampleConfig
from src.models import (
    MeasurementData,
    MeasurementResult,
    MeasurementSample,
    MeasurementStats,
    MeasurementSummary,
)


class MeasurementService:

    def take_measurements(
        self,
        ammeter_client: AmmeterClient,
        number_of_samples: int,
        sample_rate: float,
        total_duration: float,
    ) -> MeasurementResult:
        """
        Take measurements from the ammeter client.

        Args:
            ammeter_client (AmmeterClient): The ammeter client to use for measurements.
            number_of_samples (int): The number of samples to take.
            sample_rate (float): The rate at which to take samples (in Hz).
            total_duration (float): The total duration for taking samples (in seconds).

        Returns:
            MeasurementResult: The samples and their statistics.
        """
        # Raises ValueError if a value is not positive; also saved in the result
        if number_of_samples <= 0:
            raise ValueError("number_of_samples must be positive")
        if sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if total_duration <= 0:
            raise ValueError("total_duration must be positive")
        
        measurements = []
        failed_samples = 0
        started_at = datetime.now(timezone.utc)
        start_time = time.perf_counter() # using perf_counter for more accurate timing

        for i in range(number_of_samples):
            target_time = start_time + (i / sample_rate)
            sleep_time = target_time - time.perf_counter()
            if sleep_time > 0:
                time.sleep(sleep_time)

            # Stop if the total measurement duration has elapsed
            if time.perf_counter() - start_time >= total_duration:
                break
            
            try:
                current = ammeter_client.measure_current()
            except (OSError, ValueError) as error:
                failed_samples += 1
                print(f"Sample {i} failed: {error}")
                continue
            timestamp = time.perf_counter() - start_time

            measurements.append(MeasurementSample(timestamp=timestamp, current=current))

        if not measurements:
            raise RuntimeError(
                f"No measurements were taken ({failed_samples} failed). "
                "Please check the ammeter client and configuration."
            )

        return MeasurementResult(
            started_at=started_at,
            ammeter_type=ammeter_client.get_ammeter_type(),
            sample_config=SampleConfig(
                number_of_samples=number_of_samples,
                total_duration=total_duration,
                sample_rate=sample_rate,
            ),
            failed_samples=failed_samples,
            measurement_data=MeasurementData(
                samples=measurements,
                stats=self.calculate_stats(measurements),
            ),
        )

    def calculate_stats(self, samples: list[MeasurementSample]) -> MeasurementStats:
        """
        Calculate statistics from a list of measurement samples.

        Args:
            samples (list[MeasurementSample]): The list of measurement samples.

        Returns:
            MeasurementStats: The count, mean, median, standard deviation, min and max.
        """
        currents = [sample.current for sample in samples]

        return MeasurementStats(
            count=len(currents),
            mean_current=statistics.mean(currents),
            median_current=statistics.median(currents),
            std_dev_current=statistics.stdev(currents) if len(currents) > 1 else 0.0,
            min_current=min(currents),
            max_current=max(currents),
        )

    def get_measurement_summary(self, measurement_results: list[MeasurementResult]) -> MeasurementSummary:
        """
        Get a summary of multiple measurement results.

        Args:
            measurement_results (list[MeasurementResult]): The list of measurement results.

        Returns:
            MeasurementSummary: The summary of the measurement results.
        """
        return MeasurementSummary(results=measurement_results)
