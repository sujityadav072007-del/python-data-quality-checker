import argparse
import csv
from datetime import datetime
from pathlib import Path


def parse_date_column_formats(values):
    """Convert COLUMN=FORMAT arguments into a dictionary."""
    date_formats = {}

    for value in values:
        if "=" not in value:
            raise ValueError(
                f"Invalid date-column setting '{value}'. Use COLUMN=FORMAT."
            )

        column, date_format = value.split("=", 1)
        if not column or not date_format:
            raise ValueError(
                f"Invalid date-column setting '{value}'. Use COLUMN=FORMAT."
            )
        if column in date_formats:
            raise ValueError(f"Date format specified more than once for '{column}'.")

        date_formats[column] = date_format

    return date_formats


def analyze_csv(file_path, numeric_columns=None, date_formats=None):
    """Analyze a CSV file and return basic data-quality statistics."""
    path = Path(file_path)
    numeric_columns = set(numeric_columns or [])
    date_formats = date_formats or {}

    with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            raise ValueError("The CSV file must contain a header row.")

        columns = reader.fieldnames
        unknown_numeric = numeric_columns.difference(columns)
        unknown_dates = set(date_formats).difference(columns)

        if unknown_numeric:
            names = ", ".join(sorted(unknown_numeric))
            raise ValueError(f"Unknown numeric column(s): {names}")
        if unknown_dates:
            names = ", ".join(sorted(unknown_dates))
            raise ValueError(f"Unknown date column(s): {names}")

        missing_values = {column: 0 for column in columns}
        invalid_numeric_values = {column: 0 for column in numeric_columns}
        invalid_date_values = {column: 0 for column in date_formats}
        seen_rows = set()
        duplicate_rows = 0
        total_rows = 0

        for row in reader:
            total_rows += 1
            row_values = tuple((row.get(column) or "").strip() for column in columns)

            for column, value in zip(columns, row_values):
                if value == "":
                    missing_values[column] += 1
                elif column in numeric_columns:
                    try:
                        float(value)
                    except ValueError:
                        invalid_numeric_values[column] += 1
                elif column in date_formats:
                    try:
                        datetime.strptime(value, date_formats[column])
                    except ValueError:
                        invalid_date_values[column] += 1

            if row_values in seen_rows:
                duplicate_rows += 1
            else:
                seen_rows.add(row_values)

    return {
        "file_name": path.name,
        "total_rows": total_rows,
        "total_columns": len(columns),
        "duplicate_rows": duplicate_rows,
        "missing_values": missing_values,
        "invalid_numeric_values": invalid_numeric_values,
        "invalid_date_values": invalid_date_values,
    }


def print_report(report):
    """Print the analysis in a readable format."""
    print(f"\nData Quality Report: {report['file_name']}")
    print("-" * 40)
    print(f"Total rows: {report['total_rows']}")
    print(f"Total columns: {report['total_columns']}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print("\nMissing values by column:")

    for column, count in report["missing_values"].items():
        print(f"  {column}: {count}")

    if report["invalid_numeric_values"]:
        print("\nInvalid numeric values by column:")
        for column, count in report["invalid_numeric_values"].items():
            print(f"  {column}: {count}")

    if report["invalid_date_values"]:
        print("\nInvalid date values by column:")
        for column, count in report["invalid_date_values"].items():
            print(f"  {column}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Check a CSV file for missing values, duplicates, and invalid data."
    )
    parser.add_argument("file", help="Path to the CSV file to analyze")
    parser.add_argument(
        "--numeric-columns",
        nargs="+",
        default=[],
        metavar="COLUMN",
        help="Column names that should contain numeric values",
    )
    parser.add_argument(
        "--date-columns",
        nargs="+",
        default=[],
        metavar="COLUMN=FORMAT",
        help="Date columns and their Python date formats, e.g. joined=%Y-%m-%d",
    )
    args = parser.parse_args()

    try:
        date_formats = parse_date_column_formats(args.date_columns)
        report = analyze_csv(
            args.file,
            numeric_columns=args.numeric_columns,
            date_formats=date_formats,
        )
        print_report(report)
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
