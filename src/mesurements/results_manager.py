"""Saves measurement results to JSON files and loads them back."""

import os

from src.enums import AmmeterType
from src.models import MeasurementResult
from src.utils.libraries.file_utils import FileUtils


class ResultsManager:

    def __init__(self, results_dir: str = "results"):
        self.results_dir = results_dir
        FileUtils.create_folder(results_dir)

    def save_result(self, result: MeasurementResult) -> str:
        """Save one result as <run_id>.json and return the file path."""
        file_path = os.path.join(self.results_dir, f"{result.run_id}.json")
        FileUtils.write_file(file_path, result.model_dump_json(indent=2))
        return file_path

    def load_result(self, run_id: str) -> MeasurementResult:
        """Load one result by its run id."""
        file_path = os.path.join(self.results_dir, f"{run_id}.json")
        if not FileUtils.file_exists(file_path):
            raise FileNotFoundError(f"No result with run id {run_id} in {self.results_dir}")
        return MeasurementResult.model_validate_json(FileUtils.read_file(file_path))

    def load_all_results(self, ammeter_type: AmmeterType | None = None) -> list[MeasurementResult]:
        """Load every saved result, oldest first. Give an ammeter type to load only that one."""
        results = []
        for file_name in FileUtils.list_files(self.results_dir, ".json"):
            results.append(self.load_result(file_name.removesuffix(".json")))

        if ammeter_type is not None:
            results = [result for result in results if result.ammeter_type == ammeter_type]

        return sorted(results, key=lambda result: result.started_at)
