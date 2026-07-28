import json
import os
import re
import shutil
import subprocess
from typing import Any

import requests


def get_ollama_base_url() -> str:
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    if not base_url:
        raise ValueError("OLLAMA_BASE_URL must be set to the local Ollama HTTP endpoint.")
    return base_url.rstrip("/")


def build_llm_prompt(question: str) -> str:
    return (
        "Generate 3 high-quality paraphrases for the following question, "
        "keeping the meaning unchanged and preserving question intent:\n\n"
        f"Question: {question}\n\n"
        "Paraphrases:"
    )


def parse_ollama_response_text(response_text: str) -> str:
    if not response_text:
        return ""

    try:
        data = json.loads(response_text)
        if isinstance(data, dict):
            if "text" in data:
                return data["text"]
            if "choices" in data and data["choices"]:
                first = data["choices"][0]
                if isinstance(first, dict) and "text" in first:
                    return first["text"]
                if isinstance(first, dict) and "message" in first:
                    return first["message"].get("content", "")
            if "response" in data:
                return str(data["response"])
            if "message" in data and isinstance(data["message"], dict):
                return data["message"].get("content", "")
    except json.JSONDecodeError:
        pass

    chunks: list[str] = []
    for line in response_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("data:"):
            line = line[len("data:") :].strip()
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            if isinstance(event.get("response"), str) and event.get("response"):
                chunks.append(event["response"])
            elif isinstance(event.get("message"), dict):
                content = event["message"].get("content", "")
                if content:
                    chunks.append(content)
            elif isinstance(event.get("payload"), dict):
                payload = event["payload"]
                if isinstance(payload.get("text"), str) and payload.get("text"):
                    chunks.append(payload["text"])
                elif isinstance(payload.get("content"), str) and payload.get("content"):
                    chunks.append(payload["content"])
    return "".join(chunks).strip()


def generate_paraphrases_with_ollama(question: str, model: str = "qwen3.5", max_tokens: int = 150, timeout: int = 120) -> list[str]:
    """Try Ollama HTTP API first; fall back to the local `ollama` CLI if needed.

    Returns a list of paraphrase strings (may be empty if parsing fails).
    """
    prompt = build_llm_prompt(question)

    # Attempt HTTP API call
    try:
        base_url = get_ollama_base_url()
        url = f"{base_url}/api/generate?model={model}"
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "stream": False,
        }
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        text = parse_ollama_response_text(response.text)
        if text:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if lines:
                return [line for line in lines if line]
    except Exception:
        # swallow and try CLI fallback below
        pass

    # Fallback: use the local Ollama CLI `ollama run MODEL PROMPT --format json`
    try:
        cli = shutil.which("ollama") or os.environ.get("OLLAMA_CLI_PATH") or r"C:\\Users\\ankit\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
        if not cli or not os.path.exists(cli):
            raise FileNotFoundError(f"Ollama CLI not found at {cli}")

        # Build command. Provide prompt via stdin to avoid shell quoting issues.
        cmd = [cli, "run", model, "--format", "json"]
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        out = (proc.stdout or proc.stderr or "").strip()
        # Strip ANSI escape sequences and other control characters that may
        # appear in the CLI JSON/text stream (e.g. thinking/debug tokens).
        out = re.sub(r"\x1b\[[0-9;?]*[ -/]*[@-~]", "", out)
        if not out:
            raise RuntimeError("Ollama CLI produced no output")

        # Try to parse JSON first, then fallback to text parsing
        try:
            data = json.loads(out)
            # Common shapes: {"text": "..."} or {"choices":[{"text":"..."}]}
            if isinstance(data, dict):
                if "text" in data and data["text"]:
                    text = data["text"]
                elif "choices" in data and data["choices"]:
                    first = data["choices"][0]
                    text = first.get("text") or first.get("message", {}).get("content", "")
                else:
                    text = json.dumps(data)
            else:
                text = str(data)
        except json.JSONDecodeError:
            text = out

        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return [l for l in lines if l]
    except Exception as ex:
        raise RuntimeError(f"Ollama generation failed (HTTP+CLI): {ex}")


def prepare_llm_input_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [{"id": row.get("id", ""), "question": row.get("question1", "")} for row in rows]


def sample_llm_augmentation(rows: list[dict[str, str]], sample_size: int = 100) -> list[dict[str, str]]:
    return rows[:sample_size]
