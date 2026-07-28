from pathlib import Path
import argparse
import csv
import random


def export_gold_subset(input_csv: Path, output_csv: Path, size: int = 2000) -> Path:
    input_csv = Path(input_csv)
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with input_csv.open("r", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    if len(rows) < size:
        raise ValueError(f"Input file has only {len(rows)} rows; requested {size}")

    sample = random.sample(rows, size)

    fieldnames = ["id", "question1", "question2", "is_duplicate", "semantic_label", "label_reason", "source_dataset", "split", "annotation_status"]
    with output_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in sample:
            row_out = dict(row)
            row_out["annotation_status"] = "pending"
            writer.writerow(row_out)

    return output_csv


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--size", type=int, default=2000)
    args = parser.parse_args()
    out = export_gold_subset(args.input, args.output, args.size)
    print(f"Wrote gold subset to {out}")
