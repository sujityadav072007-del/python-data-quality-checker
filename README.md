# Python Data Quality Checker

A beginner-friendly command-line project that checks a CSV file for common data-quality issues.

## Current features

- Counts the number of data rows and columns.
- Counts missing values in each column. Empty cells and cells containing only spaces are treated as missing.
- Counts duplicate rows (the first occurrence is not counted as a duplicate).
- Prints a readable report in the terminal.
- Includes automated tests using Python's built-in `unittest` module.

## Requirements

- Python 3.8 or newer
- No third-party packages are required.

## Run the checker

Clone or download this repository, open a terminal in the project folder, and run:

```bash
python main.py sample_data.csv
```

On some systems, use `python3` instead of `python`.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Example dataset

The included `sample_data.csv` intentionally contains a missing age, a missing city, and one repeated row so you can see the checker report issues.

## Project structure

```text
python-data-quality-checker/
├── main.py
├── sample_data.csv
├── tests/
│   └── test_data_quality.py
├── .gitignore
└── README.md
```

## Current limitations

- The first version checks missing values and exact duplicate rows only.
- It does not yet validate data types, date formats, or custom business rules.
- It reads the CSV file into memory while checking for duplicate rows, so very large files may need a more memory-efficient approach.

## Planned improvements

1. Add configurable column validation rules.
2. Export the report to a file.
3. Improve command-line options and error messages.
4. Add more test cases and documentation.

## Learning note

This project uses Python's standard-library modules: `csv`, `argparse`, `pathlib`, and `unittest`. The goal is to keep the first version small, understandable, and easy to extend.
