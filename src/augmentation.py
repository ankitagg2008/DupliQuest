import os
import csv
import random
import re
from pathlib import Path

from llm_augmentation import build_llm_prompt, generate_paraphrases_with_ollama

SYNONYM_MAP = {
    "what": ["which"],
    "how": ["in what way"],
    "most": ["maximum", "majority"],
    "people": ["persons", "individuals"],
    "state": ["region", "province"],
    "country": ["nation"],
}


def simple_synonym_replace(text: str) -> str:
    words = text.split()
    out = []
    for w in words:
        key = re.sub(r"[^a-zA-Z]", "", w.lower())
        if key in SYNONYM_MAP and random.random() < 0.4:
            out.append(random.choice(SYNONYM_MAP[key]))
        else:
            out.append(w)
    return " ".join(out)


def shuffle_phrases(text: str) -> str:
    parts = re.split(r"(,|;|\?|\.)", text)
    random.shuffle(parts)
    return "".join(parts).strip()


def generate_simple_paraphrase(text: str) -> str:
    if not text:
        return text
    t = simple_synonym_replace(text)
    if len(t.split()) <= 6 and random.random() < 0.3:
        t = " ".join(reversed(t.split()))
    return t


def augment_dataset(input_csv: Path, output_csv: Path, mode: str = "paraphrase", model: str | None = None, max_rows: int | None = None) -> Path:
    """Read CSV with columns question1, question2 and append augmented paraphrases."""
    input_csv = Path(input_csv)
    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    with input_csv.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for idx, r in enumerate(reader):
            if max_rows and idx >= max_rows:
                break
            rows.append(r)

    augmented = []
    for r in rows:
        q1 = r.get("question1", "")
        q2 = r.get("question2", "")
        if mode == "paraphrase":
            new_q1 = generate_simple_paraphrase(q1)
            new_q2 = generate_simple_paraphrase(q2)
        elif mode == "ollama":
            new_q1 = generate_paraphrases_with_ollama(q1, model=model or os.environ.get("OLLAMA_MODEL", "qwen3.5"))
            new_q1 = new_q1[0] if new_q1 else q1
            new_q2 = generate_paraphrases_with_ollama(q2, model=model or os.environ.get("OLLAMA_MODEL", "qwen3.5"))
            new_q2 = new_q2[0] if new_q2 else q2
        else:
            raise ValueError(f"Unsupported augmentation mode: {mode}")

        augmented.append({
            "id": f"aug-{r.get('id')}",
            "question1": new_q1,
            "question2": q2,
            "is_duplicate": r.get("is_duplicate", 0),
            "semantic_label": "paraphrase",
            "label_reason": f"synthetic_{mode}_paraphrase",
            "source_dataset": input_csv.name,
            "split": r.get("split", "train"),
        })

    fieldnames = ["id", "question1", "question2", "is_duplicate", "semantic_label", "label_reason", "source_dataset", "split"]
    with output_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for a in augmented:
            writer.writerow(a)

    return output_csv


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mode", choices=["paraphrase", "ollama"], default="paraphrase")
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--max-rows", type=int, default=500)
    args = parser.parse_args()
    out = augment_dataset(args.input, args.output, args.mode, model=args.model, max_rows=args.max_rows)
    print(f"Wrote augmented file: {out}")
