from pathlib import Path
import argparse
import csv
from collections import Counter


def compute_stats(csv_path: Path) -> dict:
    counts = Counter()
    total = 0
    with csv_path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            total += 1
            label = row.get("semantic_label") or row.get("label") or "unknown"
            counts[label] += 1
    return {"total_rows": total, "label_counts": dict(counts)}


def print_stats(stats: dict):
    print(f"Total rows: {stats['total_rows']}")
    print("Label counts:")
    for label, count in sorted(stats["label_counts"].items()):
        print(f"  - {label}: {count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    stats = compute_stats(args.input)
    print_stats(stats)
