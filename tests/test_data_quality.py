import csv
import tempfile
import unittest
from pathlib import Path

from main import analyze_csv


class TestAnalyzeCsv(unittest.TestCase):
    def write_csv(self, folder, rows):
        file_path = Path(folder) / "sample.csv"
        with file_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)
        return file_path

    def test_counts_rows_columns_missing_and_duplicates(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = self.write_csv(
                folder,
                [
                    ["name", "age"],
                    ["Asha", "21"],
                    ["Ravi", ""],
                    ["Asha", "21"],
                ],
            )

            report = analyze_csv(file_path)

            self.assertEqual(report["total_rows"], 3)
            self.assertEqual(report["total_columns"], 2)
            self.assertEqual(report["duplicate_rows"], 1)
            self.assertEqual(report["missing_values"], {"name": 0, "age": 1})

    def test_whitespace_only_value_is_missing(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = self.write_csv(
                folder,
                [["name", "city"], ["Meera", "   "]],
            )

            report = analyze_csv(file_path)

            self.assertEqual(report["missing_values"]["city"], 1)

    def test_header_only_file_has_zero_data_rows(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = self.write_csv(folder, [["name", "age"]])

            report = analyze_csv(file_path)

            self.assertEqual(report["total_rows"], 0)
            self.assertEqual(report["duplicate_rows"], 0)

    def test_empty_file_raises_value_error(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = Path(folder) / "empty.csv"
            file_path.write_text("", encoding="utf-8")

            with self.assertRaises(ValueError):
                analyze_csv(file_path)

    def test_counts_invalid_numeric_values_and_ignores_missing_values(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = self.write_csv(
                folder,
                [
                    ["name", "age"],
                    ["Asha", "21"],
                    ["Ravi", "twenty"],
                    ["Meera", ""],
                    ["Kabir", "18.5"],
                ],
            )

            report = analyze_csv(file_path, numeric_columns=["age"])

            self.assertEqual(report["invalid_numeric_values"], {"age": 1})
            self.assertEqual(report["missing_values"]["age"], 1)

    def test_unknown_numeric_column_raises_value_error(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = self.write_csv(
                folder,
                [["name", "age"], ["Asha", "21"]],
            )

            with self.assertRaisesRegex(ValueError, "Unknown numeric column"):
                analyze_csv(file_path, numeric_columns=["salary"])


if __name__ == "__main__":
    unittest.main()
