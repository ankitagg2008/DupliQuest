from pathlib import Path
import csv
import argparse

FIELDNAMES = ["id","question1","question2","is_duplicate","semantic_label","label_reason","source_dataset","split"]


def read_rows(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            rows.append(r)
    return rows


def normalize_row(r: dict):
    out = {k: r.get(k, "") for k in FIELDNAMES}
    # ensure id exists
    if not out["id"]:
        out["id"] = r.get("pair_id", "") or r.get("qid", "") or ""
    return out


def combine(original: Path, augmented: Path, output: Path):
    orig_rows = read_rows(original)
    aug_rows = read_rows(augmented)

    combined = [normalize_row(r) for r in orig_rows] + [normalize_row(r) for r in aug_rows]

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in combined:
            writer.writerow(r)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--augmented", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    out = combine(args.original, args.augmented, args.output)
    print(f"Wrote combined file: {out}")
