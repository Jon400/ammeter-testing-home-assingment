"""Runs the measurement test on every ammeter in config/config.yaml and prints the results.
"""

from src.testing.test_framework import AmmeterTestFramework


def main():
    framework = AmmeterTestFramework("config/config.yaml")
    summary = framework.run_all_tests()

    for result in summary.results:
        stats = result.measurement_data.stats
        print(f"{result.ammeter_type.value} (run id {result.run_id})")
        print(
            f"count={stats.count} mean={stats.mean_current:.4f} median={stats.median_current:.4f} "
            f"std={stats.std_dev_current:.4f} min={stats.min_current:.4f} max={stats.max_current:.4f} "
            f"failed={result.failed_samples}"
        )

    print(f"Results saved in {framework.config.results_dir}/")


if __name__ == "__main__":
    main()
