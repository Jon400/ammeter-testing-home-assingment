"""
This module contains configuration settings for the ammeter testing application.
"""

from typing import Literal

import yaml
from pydantic import BaseModel, Field

from src.enums import AmmeterType
from src.utils.libraries.file_utils import FileUtils


class SampleConfig(BaseModel):
    number_of_samples: int = Field(default=10, gt=0)
    total_duration: float = Field(default=5.0, gt=0)  # in seconds
    sample_rate: float = Field(default=2.0, gt=0)  # in Hz


class AmmeterConfig(BaseModel):
    host: str = "localhost"
    port: int = Field(gt=0)


class LoggingConfig(BaseModel):
    log_dir: str = "logs"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"


class AppConfig(BaseModel):
    sampling: SampleConfig
    ammeters: dict[AmmeterType, AmmeterConfig]
    results_dir: str = "results"
    logging: LoggingConfig


def load_config(config_path: str) -> AppConfig:
    """
    Load the config file.

    Args:
        config_path (str): Path to the YAML config file.

    Returns:
        AppConfig: The sampling settings, the ammeters, and where to save results and logs.
    """
    data = yaml.safe_load(FileUtils.read_file(config_path))
    sampling = data["testing"]["sampling"]
    result_management = data["result_management"]

    return AppConfig(
        sampling=SampleConfig(
            number_of_samples=sampling["measurements_count"],
            total_duration=sampling["total_duration_seconds"],
            sample_rate=sampling["sampling_frequency_hz"],
        ),
        ammeters=data["ammeters"],
        results_dir=result_management["results_dir"],
        logging=data["logging"],
    )
