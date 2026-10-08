"""Velo Alatau: строит отчёт out/report.json из файла data/records.csv."""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
 
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "records.csv"
OUT = ROOT / "out" / "report.json"
VARIANT = 8

def load_rows():
    with open(DATA, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))
 
 
def control_code(rows):
    text = "\n".join("|".join(row.values()) for row in rows)
    digest = hashlib.sha256(f"{VARIANT}\n{text}".encode("utf-8"))
    return digest.hexdigest()[:8].upper()
 
 
def money(value):
    return f"{value:,}".replace(",", " ") + " ₸"
 
 
def build(rows):
    starts = defaultdict(int)
    by_hour = defaultdict(lambda: [0, 0])
    for r in rows:
        starts[r["start_station"]] += 1
        h = by_hour[int(r["start_time"][11:13])]
        h[0] += 1
        h[1] += int(r["minutes"])
    total = sum(int(r["minutes"]) for r in rows)
    summary = [
        {"label": "Поездок", "value": len(rows)},
        {"label": "Всего минут", "value": total},
        {"label": "Средняя длительность", "value": f"{total / len(rows):.1f} мин"},
    ]
    stations = sorted(starts.items(), key=lambda kv: (-kv[1], kv[0]))
    hours = sorted(by_hour.items(), key=lambda kv: (-kv[1][0], kv[0]))
    tables = [
        {"title": "Самые популярные станции отправления",
         "columns": ["Станция", "Поездок"],
         "rows": [[k, v] for k, v in stations]},
        {"title": "Поездки по часам",
         "columns": ["Час", "Поездок", "Среднее, мин"],
         "rows": [[f"{k:02d}:00", v[0], round(v[1] / v[0], 1)] for k, v in hours]},
    ]
    return summary, tables
 
 
def main():
    rows = load_rows()
    summary, tables = build(rows)
    report = {
        "variant": VARIANT,
        "org": "Velo Alatau",
        "title": "Отчёт по поездкам велопроката",
        "records": len(rows),
        "control_code": control_code(rows),
        "summary": summary,
        "tables": tables,
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"out/report.json готов: {len(rows)} записей, контрольный код {report['control_code']}")
 
 
if __name__ == "__main__":
    main()
