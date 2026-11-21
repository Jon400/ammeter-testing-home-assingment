from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.config import SampleConfig
from src.enums import AmmeterType


class MeasurementStats(BaseModel):
    count: int
    mean_current: float
    median_current: float
    std_dev_current: float
    min_current: float
    max_current: float
    unit: str = "A"  # Default unit is Amperes


class MeasurementSample(BaseModel):
    timestamp: float  # seconds since the run started
    current: float
    unit: str = "A"  # Default unit is Amperes


class MeasurementData(BaseModel):
    samples: list[MeasurementSample]
    stats: MeasurementStats


class MeasurementResult(BaseModel):
    run_id: UUID = Field(default_factory=uuid4)
    started_at: datetime
    ammeter_type: AmmeterType
    sample_config: SampleConfig
    failed_samples: int = 0
    measurement_data: MeasurementData


class MeasurementSummary(BaseModel):
    results: list[MeasurementResult]
