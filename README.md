# Ammeter Testing Framework

Measures current from three ammeter emulators (Greenlee, ENTES, CIRCUTOR) over TCP,
calculates statistics (mean, median, standard deviation, min, max), and saves every
test run as a JSON file with a unique run id.

## Prerequisites

- **Python 3.10 or newer** (tested with 3.11)
- **pip**
- **The ammeter emulators** from the assignment package (the `Ammeters/` folder and its `main.py`)
- **Ports 5001, 5002 and 5003** free on `localhost`

### Libraries installed

| Library  | Used for |
|----------|----------|
| pydantic | Config and result models, with validation |
| PyYAML   | Reading `config/config.yaml` |
| pytest   | Running the unit tests in `tests/` |

## Installation

From the project folder:

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## How to run

**1. Start the emulators** in a first terminal, from the assignment package folder:

```bash
python main.py
```

Leave this terminal open. The emulators must keep running during the tests.

**2. Run the tests** in a second terminal, from this project folder:

```bash
python main.py
```

Run it from the project folder, because the config path is `config/config.yaml`.

## Output

- **Console**: the log lines and a summary for each ammeter:
  ```
  2026-11-21 17:30:58,562 [INFO] test_greenlee: Test started: 10 samples at 2.0 Hz, at most 5.0 s
  2026-11-21 17:31:03,083 [INFO] test_greenlee: Test finished: count=10 mean=0.3789 std=0.6916 failed=0
  ...
  greenlee (run id 5a827ae2-82e5-4715-bb53-db07ae3bc073)
  count=10 mean=0.3789 median=0.1330 std=0.6916 min=0.0302 max=2.2988 failed=0
  ```
- **`results/<run_id>.json`**: one file per test run, with the run id, start time, ammeter type,
  sampling settings, every sample and the statistics.
- **`logs/<date>_<time>_<ammeter>.log`**: one log file per test, for example `logs/20261121_173058_greenlee.log`.

Both folders are created on the first run.

## Visualization

A tkinter window for browsing the saved results in `results/`. Run it from the project folder,
after at least one test run:

```bash
python viewer.py
```

The emulators do not need to be running. The viewer only reads the result JSON files.

The window has three parts:

| Part | What it shows |
|------|---------------|
| **Meter selector** | A dropdown to show `all` runs or only one ammeter's runs, and a **Refresh** button to reload the files after a new test run |
| **Results history** | One row per run, newest first: start time, meter, number of samples, mean, standard deviation and failed samples. The newest run is selected on load |
| **Run details** | For the selected run: run id, settings and all statistics, a table of every sample (time and current), and a chart of current over time with a dashed red line at the mean |

tkinter comes with Python, so nothing extra needs to be installed. On Linux it may need
the system package (for example `sudo apt install python3-tk`).

## Configuration

All settings are in `config/config.yaml`:

| Key | Meaning |
|-----|---------|
| `testing.sampling.measurements_count` | Number of samples per test |
| `testing.sampling.total_duration_seconds` | Maximum test time. The test stops early when it is reached |
| `testing.sampling.sampling_frequency_hz` | Samples per second |
| `ammeters.<name>.host` / `port` | Where each emulator listens. Remove an ammeter to skip it |
| `result_management.results_dir` | Folder for the result JSON files |
| `logging.log_dir` | Folder for the log files |
| `logging.log_level` | `DEBUG`, `INFO`, `WARNING` or `ERROR`. `DEBUG` also logs every reading |

## Project structure

```
├── config/
│   └── config.yaml                  # sampling, ammeters, results and logs folders
├── src/
│   ├── config.py                    # loads config.yaml into Pydantic models
│   ├── enums.py                     # AmmeterType
│   ├── models.py                    # samples, stats, result and summary models
│   ├── clients/                     # one TCP client per ammeter type
│   ├── mesurements/                 # MeasurementService (sampling, stats), ResultsManager (JSON files)
│   ├── testing/                     # AmmeterTestFramework (runs the tests)
│   └── utils/
│       ├── classes/test_logger.py   # TestLogger: one log file per test
│       └── libraries/file_utils.py  # FileUtils: file and folder helpers
├── measurements_visualizer/         # tkinter results viewer
│   ├── results_viewer.py            # ResultsViewer: the main window, joins the parts below
│   ├── meter_type_selector.py       # MeterTypeSelector: meter dropdown and Refresh button
│   ├── history_table.py             # HistoryTable: one row per run
│   ├── run_details_viewer.py        # RunDetailsViewer: stats and samples of one run
│   └── run_chart.py                 # RunChart: current over time chart
├── main.py                          # entry point: runs all tests and prints the results
├── viewer.py                        # entry point: opens the results viewer
├── requirements.txt
└── README.md
```

## Fix to the emulator main.py

The given `main.py` starts the emulators in daemon threads and then ends after about
5 seconds, which also stops the emulators. I replaced the `pass` at the end with a loop
that keeps them running until Ctrl+C:

```python
print("Emulators are running. Press Ctrl+C to stop.")
while True:
    time.sleep(1)
```

## Troubleshooting

| Problem | Cause and fix |
|---------|---------------|
| `Test failed: No measurements were taken` | The emulator for that ammeter is not running, or its port in `config.yaml` is wrong. Start the emulators first. |
| `FileNotFoundError: ... config/config.yaml` | Run `python main.py` from the project folder. |
| `UnicodeEncodeError` in the Greenlee emulator | It prints the `Ω` sign, which fails on Windows when the output is not UTF-8. Start the emulators in UTF-8 mode: `$env:PYTHONUTF8=1` (PowerShell) or `set PYTHONUTF8=1` (cmd), then `python main.py`. |

## AI Usage

I used an AI coding assistant for planning, code suggestions and some of the code.
I made the design decisions, reviewed every change, and changed or rejected code that
was too complex or did not match my style.

### Tools and models

| Tool | Model | Used for |
|------|-------|----------|
| Claude Code (VS Code extension) | Claude Opus 5.5 (`claude-opus-5-5`) | Most of the work: architecture, measurements, testing framework, logger, simulator, unit tests, viewer, docs |
| Claude Code (VS Code extension) | Claude Sonnet 5.5 (`claude-sonnet-5-5`) | Early sessions: `AmmeterType` enum, abstract client class, first architecture questions |

### What was implemented with AI

| Area | How AI was used |
|------|-----------------|
| **Folder structure and architecture** | Suggestions only. I asked for the folders and class names, then wrote the code myself |
| **Clients** (`src/clients/`) | AI wrote the Greenlee, ENTES and CIRCUTOR subclasses and the `AmmeterType` enum. I asked to make the base client abstract (ABC) |
| **Measurements and results** (`src/mesurements/`, `src/models.py`, `src/config.py`) | AI showed the sampler code in chat first. Later, with my permission, it wrote `MeasurementService`, `ResultsManager`, the Pydantic models and the config loader, built on my `FileUtils` |
| **Testing framework** (`src/testing/`, `main.py`) | AI wrote `AmmeterTestFramework`, and moved the logs and results folders and the log level into `config.yaml` |
| **Logger** (`src/utils/classes/test_logger.py`) | AI wrote `TestLogger`. I kept it for the test infra only, not inside the measurement code |
| **Simulator and unit tests** (`simulator/`, `tests/unit/`) | AI wrote a short simulator with error modes (for example no response), the pytest fixtures in `conftest.py` and `test_error_handling.py` |
| **Viewer** (`measurements_visualizer/`, `viewer.py`) | I wrote the skeleton and method names. AI split it into component files in my code style and wrote `viewer.py` |
| **Docs and setup** | AI wrote this README, `requirements.txt`, `.gitignore`, `pytest.ini` and `.vscode/` |

### Prompts used

The main prompts, grouped by topic (shortened and with typos fixed):

**Planning**
- "I want to create a folder with a base TCP client for this repo. Only give me a suggestion, do not implement anything."
- "Look at the repo again, there might be a different command to measure current. Should `BaseTcpClient` be an ABC?"
- "How would you plan the measurements?" (with the assignment's sampling and analysis requirements pasted in) "Use Pydantic. Only give me the folders and suggestions, I will implement this."
- "How would you manage the measurement settings in the config and manage the results? Which classes would you build for this?"
- "Help me architect my code for measurements and results. I have the clients of the 3 types of meter so far."
- "Look at the benchmark (another QA automation repo) and give some advice for here."

**Clients**
- "Please create `enums.py` for all ammeter types. Add also get ammeter type."
- "Please create the 3 subclasses for me." / "It should be abstract."

**Measurements and testing framework**
- "Help me do the test framework for the measurement and organise it well. Where to put the unique run id?"
- "Show me the code of the sampler." / "Only show the code here."
- "How to write the testing framework for this?" (with the problem statement pasted in)
- "Now how do I write the results?"
- "Please use time utils instead of Python's `time`. Give simple method names."

**Logger and config**
- "Create a logger in utils, in classes. Call it TestLogger, it gets the test name. This is a logger for our test infra."
- "Add the measurement results dir, the log dir and the debug level to the config YAML. Use fixtures for the path."

**Simulator and unit tests**
- "Add a new type called simulator for my ammeter and a very basic simulator for my testing. Allow me to set some errors inside, such as the ammeter not responding. The simulator should be very short."
- "Add the simulator, run it and close it as a fixture in `tests/unit` to test the error handling."
- "Remove the simulator from the main. It is used only for the unit test. Load the simulator config from `config.yaml`. Keep the conftest."

**Viewer**
- "Where to add the UI? Create the components of the screen: choose the meter, see the results history and look into one experiment."

**Docs and repo**
- "Add `requirements.txt` and a README that explains how to run." / "Add the viewer part to the README."
- "Don't add comments in requirements, add tkinter if needed." / "Everything else is in the Python standard library, remove it and add pytest."
- "Create `.gitignore`."
- "Add a section for AI usage: what was implemented, models, prompts used."
