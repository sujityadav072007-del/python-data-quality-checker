# Python Data Quality Checker

A beginner-friendly command-line project that checks a CSV file for common data-quality issues.

## Current features

- Counts the number of data rows and columns.
- Counts missing values in each column. Empty cells and cells containing only spaces are treated as missing.
- Counts duplicate rows (the first occurrence is not counted as a duplicate).
- Optionally checks selected columns for numeric values.
- Optionally checks selected date columns against a specified date format.
- Reports invalid non-empty numeric and date values separately from missing values.
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

Check that the `age` column contains numeric values:

```bash
python main.py sample_data.csv --numeric-columns age
```

Check a date column using year-month-day format:

```bash
python main.py customers.csv --date-columns joined=%Y-%m-%d
```

Check multiple date columns with different formats:

```bash
python main.py customers.csv --date-columns joined=%Y-%m-%d birth_date=%d/%m/%Y
```

You can combine numeric and date checks:

```bash
python main.py customers.csv --numeric-columns age --date-columns joined=%Y-%m-%d
```

On some systems, use `python3` instead of `python`.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Example dataset

The included `sample_data.csv` intentionally contains a missing age, a missing city, and one repeated row. Try the numeric check with `--numeric-columns age`.

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

- Numeric and date validation must be requested explicitly for each column.
- Numeric validation accepts values understood by Python's `float()`, including decimal and scientific notation.
- Date validation uses Python's `datetime.strptime()` and the format supplied for each column.
- It does not yet validate numeric ranges or custom business rules.
- It reads the CSV file into memory while checking for duplicate rows, so very large files may need a more memory-efficient approach.

## Planned improvements

1. Add configurable numeric minimum and maximum ranges.
2. Export the report to a file.
3. Improve command-line options and error messages.
4. Add more test cases and documentation.

## Learning note

This project uses Python's standard-library modules: `csv`, `argparse`, `pathlib`, `datetime`, and `unittest`. The goal is to keep the first version small, understandable, and easy to extend.
