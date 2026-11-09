# Python Data Quality Checker

A command-line Python tool that checks CSV files for common data-quality issues and can save a JSON report. It uses only Python's standard library.

## Features

- Counts data rows and columns.
- Counts missing values (empty and whitespace-only cells).
- Counts duplicate rows (excluding the first occurrence).
- Validates selected numeric columns.
- Validates selected date columns using a specified Python date format.
- Checks inclusive minimum and maximum ranges for numeric columns.
- Exports the results to a JSON file.
- Includes automated tests and a GitHub Actions test workflow.

## Requirements

- Python 3.8 or newer
- No third-party packages required.

## Run examples

Basic report:

```bash
python main.py sample_data.csv
```

Check numeric values:

```bash
python main.py sample_data.csv --numeric-columns age
```

Validate dates (format is year-month-day):

```bash
python main.py customers.csv --date-columns joined=%Y-%m-%d
```

Check numeric ranges (both endpoints are allowed):

```bash
python main.py customers.csv --range age=18:60 marks=0:100
```

Save the report as JSON:

```bash
python main.py sample_data.csv --numeric-columns age --range age=18:60 --output report.json
```

Combine date, numeric, and range checks:

```bash
python main.py customers.csv --numeric-columns age --date-columns joined=%Y-%m-%d --range age=18:60 --output report.json
```

On some systems, use `python3` instead of `python`.

## Run tests locally

```bash
python -m unittest discover -s tests -v
```

GitHub Actions also runs the test suite when changes are pushed or a pull request is opened.

## Sample data

`sample_data.csv` includes missing values and a repeated row. Try the commands above with the sample file.

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

## How validation is counted

- Missing values are counted separately from invalid values.
- Invalid numeric values are non-empty values that Python cannot convert to a float.
- Out-of-range values are valid numbers outside the configured inclusive range.
- Invalid dates are non-empty values that do not match the specified date format.
- Duplicate rows are exact matches after surrounding whitespace is stripped from each cell.

## Limitations

- Numeric, date, and range checks must be configured by the user.
- Date parsing follows Python's `datetime.strptime()` format rules.
- Duplicate detection keeps previously seen rows in memory, so extremely large CSV files may need a different approach.

## Learning goals

This project demonstrates Python functions, dictionaries, sets, loops, exception handling, file handling, CSV processing, command-line arguments, JSON output, and unit testing.
