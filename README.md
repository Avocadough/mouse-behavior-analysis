<div align="center">

# Mouse Behavior Analysis

**Turning mouse-tracking coordinates into reproducible movement features.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-Tracking%20Data-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Exploratory%20Research-5A6472)

[Overview](#overview) · [How it works](#what-the-code-does) · [Run](#run-locally) · [Repository guide](#repository-guide)

</div>

## Overview

An exploratory project using DeepLabCut tracking coordinates to inspect mouse movement. The original [notebook](model_training.ipynb) contains data cleaning, trajectory plots, manually defined movement categories, and classifier experiments. The Python module adds a small, repeatable way to apply those original threshold rules to the CSV files already in this repository.

> **Research limitation:** the notebook creates labels from movement thresholds and trains classifiers using those same features. A high score in that setup measures agreement with the rules, not the ability to identify independently annotated behavior or infer a drug effect. The repository does not establish treatment assignments, calibrated units, animal-level validation, or clinical conclusions.

## What the code does

1. Reads a cleaned tracking CSV or the DeepLabCut multi-row header in `cleaned_VITE1002.csv`.
2. Computes the Euclidean change in `bodypart1` position between consecutive recorded rows.
3. Assigns the notebook's illustrative labels: distance below 1 is `stopping`, above 10 is `exploring`, and the rest is `moving`.
4. Starts a new segment when the frame number resets to zero, avoiding a false movement jump between recordings. Unexpected nonzero frame reversals, missing columns, and non-finite coordinates are rejected.

The notebook calls distance per sample `speed` and assumes a time interval of 1. This is **not calibrated physical speed**: frame rate and coordinate scale are not supplied. The threshold labels are not manually verified animal behavior. Frame gaps are measured between the available observations.

## Run locally

Python 3.10+ is recommended. Create an environment, install the small set of dependencies, and process one of the included CSVs:

```bash
python -m pip install -r requirements.txt
python -m mouse_behavior --input cleaned_BL_real.csv --output behavior_output.csv
```

The output CSV contains the original columns plus `distance`, `speed`, and rule-derived `behavior`. If the input already has these three columns, the output contains freshly calculated values in their place; the input file remains unchanged. Choose a new output path: the command refuses to overwrite an existing file. You can also use `cleaned_VITE1002.csv` as input. To run the tests, install `pytest` in the same environment and run `python -m pytest -q`.

## Repository guide

| Path | Purpose |
| --- | --- |
| [`model_training.ipynb`](model_training.ipynb) | Original Colab exploration and historical outputs; some cells depend on paths/files outside this repo. |
| [`mouse_behavior/io.py`](mouse_behavior/io.py) | Read the two tracked CSV formats. |
| [`mouse_behavior/analysis.py`](mouse_behavior/analysis.py) | Calculate movement and the notebook's rule-based labels. |
| [`mouse_behavior/__main__.py`](mouse_behavior/__main__.py) | Command-line interface. |
| [`tests/`](tests/) | Threshold, frame-boundary, input and command-line checks. |
| `cleaned*.csv` | Historical tracking data, including one file with previously calculated fields. |

This is an exploratory artifact, not a validated behavioral classifier. Data provenance, permission to reuse, recording-level splits, ground-truth annotation and temporal calibration need to be established before drawing scientific conclusions.
