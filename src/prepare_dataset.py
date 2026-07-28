import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT.parent / "DupliQuest" / "ques" / "ques_pairs.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "enriched_dataset.csv"


def normalize_text(text: str) -> str:
    text = (text or "").lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def tokenize(text: str) -> list[str]:
    return [token for token in normalize_text(text).split() if token]


def jaccard_similarity(left: str, right: str) -> float:
    left_tokens = set(tokenize(left))
    right_tokens = set(tokenize(right))
    if not left_tokens and not right_tokens:
        return 0.0
    inter = left_tokens & right_tokens
    union = left_tokens | right_tokens
    return len(inter) / len(union) if union else 0.0


def infer_label(question1: str, question2: str, is_duplicate: int) -> tuple[str, str]:
    normalized_q1 = normalize_text(question1)
    normalized_q2 = normalize_text(question2)

    if normalized_q1 and normalized_q1 == normalized_q2:
        return "exact_duplicate", "Questions are textually identical after normalization."

    similarity = jaccard_similarity(question1, question2)

    if int(is_duplicate) == 1:
        if similarity >= 0.6:
            return "paraphrase", f"High lexical overlap ({similarity:.2f}) with duplicate label."
        return "related_but_not_duplicate", f"Duplicate label but weak lexical overlap ({similarity:.2f})."

    if similarity >= 0.6:
        return "related_but_not_duplicate", f"High lexical overlap ({similarity:.2f}) but not marked as duplicate."
    if similarity >= 0.2:
        return "partial_overlap", f"Moderate lexical overlap ({similarity:.2f})."
    return "unrelated", f"Low lexical overlap ({similarity:.2f})."


def build_dataset(source_path: Path, output_path: Path, max_rows: int | None = None) -> Path:
    if not source_path.exists():
        raise FileNotFoundError(f"Source dataset not found: {source_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    with source_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader):
            if max_rows and index >= max_rows:
                break
            question1 = (row.get("question1") or "").strip()
            question2 = (row.get("question2") or "").strip()
            semantic_label, reason = infer_label(question1, question2, row.get("is_duplicate", 0))
            rows.append(
                {
                    "id": row.get("id", index),
                    "question1": question1,
                    "question2": question2,
                    "is_duplicate": row.get("is_duplicate", 0),
                    "semantic_label": semantic_label,
                    "label_reason": reason,
                    "source_dataset": source_path.name,
                    "split": "train",
                }
            )

    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an enriched semantic-label dataset from the original DupliQuest data")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--max-rows", type=int, default=5000)
    args = parser.parse_args()

    output_path = build_dataset(args.source, args.output, max_rows=args.max_rows)

    with output_path.open("r", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    counts = Counter(row["semantic_label"] for row in rows)
    print(f"Wrote {len(rows)} rows to {output_path}")
    print("Label distribution:")
    for label, count in counts.items():
        print(f"- {label}: {count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
