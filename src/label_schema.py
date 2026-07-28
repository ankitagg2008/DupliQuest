import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "configs" / "label_taxonomy.json"


def load_label_schema(path: str | None = None) -> dict:
    config_path = Path(path) if path else CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_label_names(path: str | None = None) -> list[str]:
    schema = load_label_schema(path)
    return [item["name"] for item in schema.get("labels", [])]


def validate_label(label: str, path: str | None = None) -> bool:
    return label in get_label_names(path)
