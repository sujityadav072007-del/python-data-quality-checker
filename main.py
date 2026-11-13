import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path


def parse_column_values(values, option_name):
    """Parse repeated COLUMN=VALUE arguments."""
    parsed = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"Invalid {option_name} setting '{item}'. Use COLUMN=VALUE.")
        column, value = item.split("=", 1)
        if not column or not value:
            raise ValueError(f"Invalid {option_name} setting '{item}'. Use COLUMN=VALUE.")
        if column in parsed:
            raise ValueError(f"{option_name} specified more than once for '{column}'.")
        parsed[column] = value
    return parsed


def parse_date_column_formats(values):
    """Convert COLUMN=FORMAT arguments into a dictionary."""
    parsed = {}
    for item in values:
        if "=" not in item:
            raise ValueError(
                f"Invalid date-column setting '{item}'. Use COLUMN=FORMAT."
            )
        column, date_format = item.split("=", 1)
        if not column or not date_format:
            raise ValueError(
                f"Invalid date-column setting '{item}'. Use COLUMN=FORMAT."
            )
        if column in parsed:
            raise ValueError(f"date-column specified more than once for '{column}'.")
        parsed[column] = date_format
    return parsed


def parse_numeric_ranges(values):
    """Convert COLUMN=MIN:MAX arguments into numeric bounds."""
    ranges = {}
    for item in values:
        if "=" not in item:
            raise ValueError(f"Invalid range setting '{item}'. Use COLUMN=MIN:MAX.")
        column, bounds = item.split("=", 1)
        if not column or ":" not in bounds:
            raise ValueError(f"Invalid range setting '{item}'. Use COLUMN=MIN:MAX.")
        minimum_text, maximum_text = bounds.split(":", 1)
        try:
            minimum = float(minimum_text)
            maximum = float(maximum_text)
        except ValueError as error:
            raise ValueError(f"Range bounds must be numbers: '{item}'.") from error
        if not math.isfinite(minimum) or not math.isfinite(maximum):
            raise ValueError(f"Range bounds must be finite numbers: '{item}'.")
        if minimum > maximum:
            raise ValueError(f"Minimum cannot exceed maximum for '{column}'.")
        if column in ranges:
            raise ValueError(f"Range specified more than once for '{column}'.")
        ranges[column] = (minimum, maximum)
    return ranges


def analyze_csv(file_path, numeric_columns=None, date_formats=None, numeric_ranges=None):
    """Analyze a CSV file and return basic data-quality statistics."""
    path = Path(file_path)
    numeric_columns = set(numeric_columns or [])
    date_formats = date_formats or {}
    numeric_ranges = numeric_ranges or {}

    with path.open("r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            raise ValueError("The CSV file must contain a header row.")

        columns = reader.fieldnames
        seen_columns = set()
        duplicate_columns = []
        for column in columns:
            if column in seen_columns and column not in duplicate_columns:
                duplicate_columns.append(column)
            seen_columns.add(column)
        if duplicate_columns:
            raise ValueError(
                "Duplicate column name(s): " + ", ".join(duplicate_columns)
            )

        configured_columns = numeric_columns | set(numeric_ranges)
        unknown_numeric = configured_columns.difference(columns)
        unknown_dates = set(date_formats).difference(columns)
        if unknown_numeric:
            raise ValueError("Unknown numeric column(s): " + ", ".join(sorted(unknown_numeric)))
        if unknown_dates:
            raise ValueError("Unknown date column(s): " + ", ".join(sorted(unknown_dates)))

        missing_values = {column: 0 for column in columns}
        invalid_numeric_values = {column: 0 for column in configured_columns}
        out_of_range_values = {column: 0 for column in numeric_ranges}
        invalid_date_values = {column: 0 for column in date_formats}
        seen_rows = set()
        duplicate_rows = 0
        malformed_rows = 0
        total_rows = 0

        for row in reader:
            total_rows += 1
            has_extra_fields = None in row
            has_missing_fields = any(row.get(column) is None for column in columns)
            if has_extra_fields or has_missing_fields:
                malformed_rows += 1

            row_values = tuple((row.get(column) or "").strip() for column in columns)

            for column, value in zip(columns, row_values):
                if value == "":
                    missing_values[column] += 1
                    continue

                if column in configured_columns:
                    try:
                        number = float(value)
                    except ValueError:
                        invalid_numeric_values[column] += 1
                    else:
                        if not math.isfinite(number):
                            invalid_numeric_values[column] += 1
                        elif column in numeric_ranges:
                            minimum, maximum = numeric_ranges[column]
                            if not minimum <= number <= maximum:
                                out_of_range_values[column] += 1

                if column in date_formats:
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
        "malformed_rows": malformed_rows,
        "missing_values": missing_values,
        "invalid_numeric_values": invalid_numeric_values,
        "out_of_range_values": out_of_range_values,
        "invalid_date_values": invalid_date_values,
    }


def validate_output_path(input_path, output_path):
    """Prevent a JSON report from overwriting the source CSV file."""
    if Path(input_path).resolve() == Path(output_path).resolve():
        raise ValueError(
            "JSON output path must be different from the input CSV path."
        )


def export_json(report, output_path):
    """Write the report as JSON."""
    Path(output_path).write_text(
        json.dumps(report, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def print_report(report):
    """Print the analysis in a readable format."""
    print(f"\nData Quality Report: {report['file_name']}")
    print("-" * 40)
    print(f"Total rows: {report['total_rows']}")
    print(f"Total columns: {report['total_columns']}")
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print(f"Malformed rows (wrong number of fields): {report['malformed_rows']}")

    sections = [
        ("Missing values", report["missing_values"]),
        ("Invalid numeric values", report["invalid_numeric_values"]),
        ("Out-of-range numeric values", report["out_of_range_values"]),
        ("Invalid date values", report["invalid_date_values"]),
    ]
    for title, values in sections:
        if values:
            print(f"\n{title}:")
            for column, count in values.items():
                print(f"  {column}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Check a CSV file for missing values, duplicates, and invalid data."
    )
    parser.add_argument("file", help="Path to the CSV file to analyze")
    parser.add_argument("--numeric-columns", nargs="+", default=[], metavar="COLUMN",
                        help="Columns that should contain numeric values")
    parser.add_argument("--date-columns", nargs="+", default=[], metavar="COLUMN=FORMAT",
                        help="Date columns and formats, e.g. joined=%Y-%m-%d")
    parser.add_argument("--range", dest="numeric_ranges", nargs="+", default=[],
                        metavar="COLUMN=MIN:MAX",
                        help="Allowed inclusive numeric range, e.g. age=18:60")
    parser.add_argument("--output", metavar="FILE",
                        help="Optional path to save the report as JSON")
    args = parser.parse_args()

    try:
        if args.output:
            validate_output_path(args.file, args.output)
        date_formats = parse_date_column_formats(args.date_columns)
        numeric_ranges = parse_numeric_ranges(args.numeric_ranges)
        report = analyze_csv(
            args.file,
            numeric_columns=args.numeric_columns,
            date_formats=date_formats,
            numeric_ranges=numeric_ranges,
        )
        print_report(report)
        if args.output:
            export_json(report, args.output)
            print(f"\nJSON report saved to: {args.output}")
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
