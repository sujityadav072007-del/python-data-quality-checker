# Project Interview Walkthrough

## One-minute summary

Python Data Quality Checker is a command-line tool that reads a CSV file, checks common data-quality problems, prints a summary, and can export the results as JSON. It uses Python's standard library and includes automated unit tests.

## Problem

CSV files can contain blank cells, repeated records, invalid numbers, dates in unexpected formats, and values outside acceptable ranges. These issues can reduce the reliability of later analysis or data processing.

## How it works

1. The command-line interface collects the CSV path and optional validation rules.
2. The CSV reader loads the header and processes each record.
3. The analyzer counts missing values, normalizes surrounding whitespace for duplicate detection, and applies configured numeric, date, and range checks.
4. The report is returned as a Python dictionary.
5. The CLI prints the report and optionally writes it as JSON.

## Design decisions

- Python's standard library keeps installation simple.
- Validation rules are configurable because not every dataset uses the same columns or formats.
- Analysis is separated from printing and JSON export, making the core function easier to test.
- Unit tests use temporary files so test data does not alter the sample dataset.

## Test command

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs this command on pushes and pull requests targeting `main`.

## Current limitations

- The full set of rows is tracked in memory for duplicate detection, so very large files may need a different strategy.
- The tool does not infer data types or validation rules automatically.
- Date validation uses the format supplied by the user.
- It currently analyzes one CSV file per command.

## Possible future improvements

- Add configurable delimiter and encoding options.
- Add a summary of valid versus invalid records.
- Support streaming duplicate detection or an optional database-backed mode for large files.
- Add integration tests for command-line behavior.

## How to describe your contribution honestly

Be ready to explain the code you personally understand and have tested. Do not claim features that are not implemented. A good demonstration is to run the sample CSV, explain one validation option, show the JSON report, and describe one limitation and how you would improve it.