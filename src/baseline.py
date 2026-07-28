import argparse
import csv
import math
from collections import Counter
from pathlib import Path

try:
    from sklearn.metrics import classification_report, accuracy_score
except ImportError:  # pragma: no cover
    classification_report = None
    accuracy_score = None

try:
    from sentence_transformers import SentenceTransformer, util
except ImportError:  # pragma: no cover
    SentenceTransformer = None
    util = None


LABELS = [
    "exact_duplicate",
    "paraphrase",
    "related_but_not_duplicate",
    "partial_overlap",
    "unrelated",
]


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def tokenize(text: str) -> set[str]:
    return set(normalize_text(text).split())


def jaccard_similarity(left: str, right: str) -> float:
    left_tokens = tokenize(left)
    right_tokens = tokenize(right)
    if not left_tokens or not right_tokens:
        return 0.0
    intersection = left_tokens & right_tokens
    union = left_tokens | right_tokens
    return len(intersection) / len(union)


def predict_by_jaccard(question1: str, question2: str) -> str:
    score = jaccard_similarity(question1, question2)
    if score >= 0.85:
        return "exact_duplicate"
    if score >= 0.6:
        return "paraphrase"
    if score >= 0.35:
        return "related_but_not_duplicate"
    if score >= 0.15:
        return "partial_overlap"
    return "unrelated"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def evaluate_predictions(y_true: list[str], y_pred: list[str]) -> dict[str, Any]:
    result = {"accuracy": None, "report": None}
    if accuracy_score is not None:
        result["accuracy"] = accuracy_score(y_true, y_pred)
    else:
        result["accuracy"] = sum(1 for a, b in zip(y_true, y_pred) if a == b) / len(y_true)

    if classification_report is not None:
        result["report"] = classification_report(y_true, y_pred, labels=LABELS, zero_division=0)
    else:
        counts = Counter((a, b) for a, b in zip(y_true, y_pred))
        report_lines = [f"Confusion counts: {counts}"]
        result["report"] = "\n".join(report_lines)
    return result


def run_jaccard_baseline(rows: list[dict[str, str]]) -> dict[str, Any]:
    y_true = []
    y_pred = []
    for row in rows:
        q1 = row.get("question1", "")
        q2 = row.get("question2", "")
        y_pred.append(predict_by_jaccard(q1, q2))
        y_true.append(row.get("semantic_label", "unrelated"))
    return evaluate_predictions(y_true, y_pred)


def run_embedding_baseline(rows: list[dict[str, str]], model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> dict[str, Any]:
    if SentenceTransformer is None or util is None:
        raise ImportError("sentence-transformers is required for embedding-based baseline.")
    model = SentenceTransformer(model_name)
    y_true = []
    y_pred = []
    for row in rows:
        q1 = row.get("question1", "")
        q2 = row.get("question2", "")
        emb1 = model.encode(q1, convert_to_tensor=True)
        emb2 = model.encode(q2, convert_to_tensor=True)
        score = util.cos_sim(emb1, emb2).item()
        if score >= 0.75:
            label = "paraphrase"
        elif score >= 0.55:
            label = "related_but_not_duplicate"
        elif score >= 0.35:
            label = "partial_overlap"
        else:
            label = "unrelated"
        y_pred.append(label)
        y_true.append(row.get("semantic_label", "unrelated"))
    return evaluate_predictions(y_true, y_pred)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run simple dataset baselines on question-pair data.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--gold", type=Path, default=None)
    parser.add_argument("--method", choices=["jaccard", "embedding"], default="jaccard")
    parser.add_argument("--sample", type=int, default=10000)
    parser.add_argument("--model-name", type=str, default="sentence-transformers/all-MiniLM-L6-v2")
    args = parser.parse_args()

    rows = load_csv(args.input)
    if args.gold:
        gold_rows = load_csv(args.gold)
        gold_ids = {row["id"]: row for row in gold_rows}
        rows = [row for row in rows if row["id"] in gold_ids]
        print(f"Evaluating on gold subset: {len(rows)} rows")
    else:
        print(f"Evaluating on input file: {len(rows)} rows")

    if args.sample and len(rows) > args.sample:
        rows = rows[: args.sample]
        print(f"Using sample size: {len(rows)}")

    if args.method == "jaccard":
        results = run_jaccard_baseline(rows)
    else:
        results = run_embedding_baseline(rows, args.model_name)

    print(f"Accuracy: {results['accuracy']:.4f}")
    print(results["report"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
