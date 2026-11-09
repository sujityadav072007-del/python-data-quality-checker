import csv
import json
import tempfile
import unittest
from pathlib import Path

from main import (
    analyze_csv,
    export_json,
    parse_date_column_formats,
    parse_numeric_ranges,
)


class TestAnalyzeCsv(unittest.TestCase):
    def write_csv(self, folder, rows):
        file_path = Path(folder) / "sample.csv"
        with file_path.open("w", newline="", encoding="utf-8") as csv_file:
            csv.writer(csv_file).writerows(rows)
        return file_path

    def test_counts_rows_columns_missing_and_duplicates(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [
                ["name", "age"], ["Asha", "21"], ["Ravi", ""], ["Asha", "21"]
            ])
            report = analyze_csv(path)
            self.assertEqual(report["total_rows"], 3)
            self.assertEqual(report["total_columns"], 2)
            self.assertEqual(report["duplicate_rows"], 1)
            self.assertEqual(report["missing_values"], {"name": 0, "age": 1})

    def test_whitespace_only_value_is_missing(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [["name", "city"], ["Meera", "   "]])
            self.assertEqual(analyze_csv(path)["missing_values"]["city"], 1)

    def test_header_only_file_has_zero_rows(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [["name", "age"]])
            report = analyze_csv(path)
            self.assertEqual(report["total_rows"], 0)
            self.assertEqual(report["duplicate_rows"], 0)

    def test_empty_file_raises_value_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "empty.csv"
            path.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                analyze_csv(path)

    def test_invalid_numeric_and_missing_are_separate(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [
                ["name", "age"], ["Asha", "21"], ["Ravi", "twenty"], ["Meera", ""]
            ])
            report = analyze_csv(path, numeric_columns=["age"])
            self.assertEqual(report["invalid_numeric_values"], {"age": 1})
            self.assertEqual(report["missing_values"]["age"], 1)

    def test_unknown_numeric_column_raises_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [["name"], ["Asha"]])
            with self.assertRaisesRegex(ValueError, "Unknown numeric column"):
                analyze_csv(path, numeric_columns=["salary"])

    def test_date_validation(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [
                ["name", "joined"], ["Asha", "2026-01-15"],
                ["Ravi", "15/01/2026"], ["Meera", ""]
            ])
            report = analyze_csv(path, date_formats={"joined": "%Y-%m-%d"})
            self.assertEqual(report["invalid_date_values"], {"joined": 1})
            self.assertEqual(report["missing_values"]["joined"], 1)

    def test_unknown_date_column_raises_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [["name"], ["Asha"]])
            with self.assertRaisesRegex(ValueError, "Unknown date column"):
                analyze_csv(path, date_formats={"joined": "%Y-%m-%d"})

    def test_parse_date_arguments(self):
        self.assertEqual(parse_date_column_formats(["joined=%Y-%m-%d"]),
                         {"joined": "%Y-%m-%d"})

    def test_reject_malformed_date_argument(self):
        with self.assertRaisesRegex(ValueError, "COLUMN=FORMAT"):
            parse_date_column_formats(["joined"])

    def test_numeric_ranges_count_below_and_above_values(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [
                ["name", "age"], ["Asha", "21"], ["Ravi", "17"],
                ["Meera", "61"], ["Kabir", "unknown"], ["Tara", ""]
            ])
            report = analyze_csv(path, numeric_ranges={"age": (18, 60)})
            self.assertEqual(report["out_of_range_values"], {"age": 2})
            self.assertEqual(report["invalid_numeric_values"], {"age": 1})
            self.assertEqual(report["missing_values"]["age"], 1)

    def test_parse_numeric_ranges(self):
        self.assertEqual(parse_numeric_ranges(["age=18:60", "marks=0:100"]),
                         {"age": (18.0, 60.0), "marks": (0.0, 100.0)})

    def test_reject_reversed_numeric_range(self):
        with self.assertRaisesRegex(ValueError, "Minimum cannot exceed"):
            parse_numeric_ranges(["age=60:18"])

    def test_reject_non_numeric_range(self):
        with self.assertRaisesRegex(ValueError, "must be numbers"):
            parse_numeric_ranges(["age=low:high"])

    def test_unknown_range_column_raises_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [["name"], ["Asha"]])
            with self.assertRaisesRegex(ValueError, "Unknown numeric column"):
                analyze_csv(path, numeric_ranges={"age": (18, 60)})

    def test_export_json_report(self):
        with tempfile.TemporaryDirectory() as folder:
            path = self.write_csv(folder, [["name"], ["Asha"]])
            report = analyze_csv(path)
            output = Path(folder) / "report.json"
            export_json(report, output)
            saved = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(saved["total_rows"], 1)
            self.assertEqual(saved["file_name"], "sample.csv")


if __name__ == "__main__":
    unittest.main()
