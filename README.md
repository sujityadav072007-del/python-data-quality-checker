# Python Data Quality Checker

[![Tests](https://github.com/sujityadav072007-del/python-data-quality-checker/actions/workflows/tests.yml/badge.svg)](https://github.com/sujityadav072007-del/python-data-quality-checker/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

A command-line tool for checking common data-quality issues in CSV files and exporting a structured JSON report. It uses Python's standard library, so no third-party packages are required.

## What it checks

- **Missing values:** empty and whitespace-only cells.
- **Duplicate rows:** repeated rows after surrounding cell whitespace is removed.
- **Numeric values:** values that cannot be converted to numbers in selected columns.
- **Date values:** values that do not match a configured Python date format.
- **Numeric ranges:** values outside configured inclusive minimum and maximum bounds.

## Requirements

- Python 3.8 or newer
- No external dependencies

## Quick start

Clone the repository and move into the project directory:

```bash
git clone https://github.com/sujityadav072007-del/python-data-quality-checker.git
cd python-data-quality-checker
```

Run the checker against a CSV file:

```bash
python main.py sample_data.csv
```

On some systems, use `python3` instead of `python`.

## Examples

Check whether values in the `age` column are numeric:

```bash
python main.py sample_data.csv --numeric-columns age
```

Validate dates in the `joined` column using year-month-day format:

```bash
python main.py customers.csv --date-columns joined=%Y-%m-%d
```

Check that ages and marks are within allowed ranges:

```bash
python main.py customers.csv --range age=18:60 marks=0:100
```

Export a JSON report while running multiple checks:

```bash
python main.py customers.csv --numeric-columns age --date-columns joined=%Y-%m-%d --range age=18:60 --output report.json
```

## Run the tests

Run the automated test suite with:

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the test suite when changes are pushed or a pull request is opened. The badge at the top links to the workflow status.

## Project structure

```text
python-data-quality-checker/
├── .github/
│   └── workflows/
│       └── tests.yml
├── tests/
│   └── test_data_quality.py
├── main.py
├── sample_data.csv
├── .gitignore
└── README.md
```

## Report fields

The report includes the input file name, total row and column counts, duplicate-row count, and per-column counts for missing values, invalid numeric values, out-of-range values, and invalid dates.

## Current limitations

- Numeric, date, and range checks must be configured by the user.
- Date parsing follows Python's `datetime.strptime()` format rules.
- Duplicate detection stores previously seen rows in memory, which may not be suitable for extremely large CSV files.

## Concepts demonstrated

Python functions, dictionaries, sets, loops, exception handling, file handling, CSV processing, command-line arguments, JSON serialization, and unit testing.
