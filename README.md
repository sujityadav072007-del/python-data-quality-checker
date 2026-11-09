# Python Data Quality Checker

A beginner-friendly command-line project that checks a CSV file for common data-quality issues.

## Current features

- Counts the number of data rows and columns.
- Counts missing values in each column. Empty cells and cells containing only spaces are treated as missing.
- Counts duplicate rows (the first occurrence is not counted as a duplicate).
- Optionally checks selected columns for numeric values.
- Reports non-empty values that cannot be converted to numbers.
- Prints a readable report in the terminal.
- Includes automated tests using Python's built-in `unittest` module.

## Requirements

- Python 3.8 or newer
- No third-party packages are required.

## Run the checker

Basic analysis:

```bash
python main.py sample_data.csv
```

To check that the `age` column contains numeric values:

```bash
python main.py sample_data.csv --numeric-columns age
```

You can check more than one numeric column:

```bash
python main.py customers.csv --numeric-columns age salary
```

On some systems, use `python3` instead of `python`.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Example dataset

The included `sample_data.csv` intentionally contains a missing age, a missing city, and one repeated row so you can see the checker report issues. Try adding `--numeric-columns age` to check the age column.

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

- Numeric validation must be requested explicitly for each column.
- Numeric validation accepts values understood by Python's `float()`, including decimal and scientific notation.
- It does not yet validate dates, ranges, or custom business rules.
- It reads the CSV file into memory while checking for duplicate rows, so very large files may need a more memory-efficient approach.

## Planned improvements

1. Add date and range validation.
2. Export the report to a file.
3. Improve command-line options and error messages.
4. Add more test cases and documentation.

## Learning note

This project uses Python's standard-library modules: `csv`, `argparse`, `pathlib`, and `unittest`. The goal is to keep the first version small, understandable, and easy to extend.
