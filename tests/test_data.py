"""Velo Alatau: тесты бизнес-правил для данных."""
import csv
import json
import unittest
from pathlib import Path
 
ROOT = Path(__file__).resolve().parent.parent
with open(ROOT / "data" / "records.csv", encoding="utf-8-sig", newline="") as f:
    ROWS = list(csv.DictReader(f))
 
COLUMNS = ["trip_id", "start_station", "end_station", "start_time", "minutes", "rider"]
STATIONS = ["Esentai", "KBTU", "Arbat", "Atakent", "Mega Alma-Ata", "KazNU",
            "Botanical Garden"]
 
 
class DataRulesTest(unittest.TestCase):
    def test_columns(self):
        self.assertEqual(list(ROWS[0].keys()), COLUMNS)
 
    def test_own_records_added(self):
        self.assertGreaterEqual(len(ROWS), 35, "добавьте свои 5 записей в конец records.csv")
 
    def test_report_created(self):
        report = json.loads((ROOT / "out" / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["records"], len(ROWS))
        self.assertEqual(len(report["control_code"]), 8)
 
    def test_stations_exist(self):
        for line, r in enumerate(ROWS, start=2):
            with self.subTest(line=line):
                self.assertIn(r["start_station"], STATIONS)
                self.assertIn(r["end_station"], STATIONS)
 
    def test_minutes_range(self):
        for line, r in enumerate(ROWS, start=2):
            with self.subTest(line=line):
                self.assertTrue(1 <= int(r["minutes"]) <= 180)
 
    def test_trip_id_unique(self):
        ids = [r["trip_id"] for r in ROWS]
        self.assertEqual(len(ids), len(set(ids)))
 
 
if __name__ == "__main__":
    unittest.main()
