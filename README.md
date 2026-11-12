# Python Data Quality Checker

[![Tests](https://github.com/sujityadav072007-del/python-data-quality-checker/actions/workflows/tests.yml/badge.svg)](https://github.com/sujityadav072007-del/python-data-quality-checker/actions/workflows/tests.yml)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)
![Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)

A Python command-line tool that checks CSV files for common data-quality problems and can export a structured JSON report. It uses Python's standard library and requires no third-party packages.

## Project highlights

- Detects empty and whitespace-only values
- Finds duplicate rows after trimming surrounding cell whitespace
- Counts rows with too few or too many fields compared with the CSV header
- Validates selected numeric columns
- Validates dates using configurable Python date formats
- Checks numeric values against inclusive minimum and maximum ranges
- Exports results as JSON for further use
- Includes automated tests with unittest and a GitHub Actions workflow

## Requirements

- Python 3.8 or newer
- No external dependencies

## Quick start

Clone the repository and enter the project directory:

```bash
git clone https://github.com/sujityadav072007-del/python-data-quality-checker.git
cd python-data-quality-checker
```

Run the checker:

```bash
python main.py sample_data.csv
```

On some systems, use python3 instead of python.

## Common examples

Check numeric values in the age column:

```bash
python main.py sample_data.csv --numeric-columns age
```

Validate dates in the joined column using year-month-day format:

```bash
python main.py customers.csv --date-columns joined=%Y-%m-%d
```

Check that ages and marks are within allowed ranges:

```bash
python main.py customers.csv --range age=18:60 marks=0:100
```

Export a JSON report while running multiple checks:

```bash
python main.py sample_data.csv --numeric-columns age --range age=18:60 --output report.json
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the test suite on pushes and pull requests to the configured branch. The badge at the top links to the workflow.

## Project structure

```text
python-data-quality-checker/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── docs/
│   └── INTERVIEW_GUIDE.md
├── tests/
│   └── test_data_quality.py
├── main.py
├── sample_data.csv
├── CONTRIBUTING.md
├── SECURITY.md
└── README.md
```

## Report contents

The JSON report includes the input file name, row and column counts, duplicate-row count, malformed-row count (records with too few or too many fields), and per-column counts for missing values, invalid numeric values, out-of-range values, and invalid dates. A short row is also reflected in the missing-value count for the absent field.

## Design notes and limitations

- Numeric, date, and range checks are opt-in and must be configured by the user.
- Date parsing follows Python datetime.strptime format rules.
- Duplicate detection keeps previously seen rows in memory, so extremely large CSV files may require a different approach.

## Concepts demonstrated

Python functions, dictionaries, sets, loops, exception handling, file handling, CSV processing, command-line arguments, JSON serialization, and unit testing.

## Interview preparation

See the [interview walkthrough](docs/INTERVIEW_GUIDE.md) for the problem statement, design decisions, testing approach, limitations, and possible future improvements.

## Contributing and security

- Read [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes.
- See [SECURITY.md](SECURITY.md) for responsible vulnerability reporting.

## About the Developer

**Sujit Yadav** is a B.Sc. Information Technology student interested in Python development, data quality, software engineering, and research-oriented problem solving.

- GitHub: https://github.com/sujityadav072007-del
- LinkedIn: https://linkedin.com/in/sujityadav

---

Built as a hands-on project to practise Python, data validation, testing, and clear technical documentation.
