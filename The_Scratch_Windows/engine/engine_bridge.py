import json
import socket
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "output"
MAX_OUTPUT_CHARS = 12000  # Scratch can be longer than LOT
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_TIMEOUT_SECONDS = 240


def _anti_ai_block(enabled: bool) -> str:
    if not enabled:
        return ""
    return """
STYLE (PLAIN / ANTI-AI):
- Avoid em dashes (—) and stylized punctuation
- Avoid filler transitions (e.g., "Overall", "In conclusion", "It's worth noting")
- Avoid "teacher voice" and blog tone
- Prefer short, direct sentences
- Preserve the author's keywords and phrasing where possible (do not synonym-swap unless needed for clarity)
- Slight roughness is acceptable; do not over-polish
""".strip()


def _base_rules() -> str:
    return """
You are The Scratch: Note Compiler.

You transform user-provided notes into structured written artifacts.

GLOBAL RULES:
- Operate only on the provided notes
- Do not introduce external facts
- Do not invent names, dates, numbers, or claims
- Do not add new topics
- If notes are unclear or incomplete, reflect that instead of guessing
- Return ONLY the compiled output (no meta commentary, no preamble)
""".strip()


def _build_prompt_summarize(notes: str, paragraphs: int, anti_ai: bool) -> str:
    return "\n\n".join(
        part for part in [
            _base_rules(),
            _anti_ai_block(anti_ai),
            f"""
OPERATION: COMPRESS
MODE: SUMMARIZE

Task:
- Reduce the notes into exactly {paragraphs} paragraphs.
Constraints:
- Preserve meaning
- Do not add new ideas
- Do not add external facts
""".strip(),
            "NOTES:\n" + notes,
        ] if part
    )


def _build_prompt_essay(notes: str, words: int, anti_ai: bool) -> str:
    return "\n\n".join(
        part for part in [
            _base_rules(),
            _anti_ai_block(anti_ai),
            f"""
OPERATION: EXPAND
MODE: ESSAY

Task:
- Expand the notes into a coherent essay of approximately {words} words.
Allowed:
- Reorder and connect ideas for clarity
- Light bridging to make the prose coherent
Not allowed:
- External facts, examples, or claims not grounded in the notes
- New names/dates/numbers not present in the notes
""".strip(),
            "NOTES:\n" + notes,
        ] if part
    )


def _build_prompt_outline(notes: str, detail: str, anti_ai: bool) -> str:
    detail = (detail or "MEDIUM").upper()
    if detail not in {"LOW", "MEDIUM", "HIGH"}:
        detail = "MEDIUM"

    return "\n\n".join(
        part for part in [
            _base_rules(),
            _anti_ai_block(anti_ai),
            f"""
OPERATION: EXPAND
MODE: OUTLINE

Task:
- Convert the notes into a structured outline.

Detail level:
- LOW: high-level headings only
- MEDIUM: headings + subpoints
- HIGH: full hierarchical outline (dense, but still outline-only)

Constraints:
- No prose paragraphs
- No filler language
- Structure only
""".strip(),
            "NOTES:\n" + notes,
        ] if part
    )


def _build_prompt_key_points_extract(
    notes: str,
    want_names: bool,
    want_dates: bool,
    want_numbers: bool,
    anti_ai: bool,
) -> str:
    return "\n\n".join(
        part for part in [
            _base_rules(),
            _anti_ai_block(anti_ai),
            f"""
OPERATION: COMPRESS
MODE: KEY POINTS (EXTRACT)

Task:
- Extract key points from the notes.
- Bullet format only.
- Extract ONLY what explicitly appears in the notes.
- Do NOT infer, elaborate, or add anything.

Include signals:
- Names: {"YES" if want_names else "NO"}
- Dates: {"YES" if want_dates else "NO"}
- Numbers: {"YES" if want_numbers else "NO"}

Output format:
- Use bullet points
- Keep bullets short and factual
""".strip(),
            "NOTES:\n" + notes,
        ] if part
    )


def _build_prompt_key_points_expand(key_points_text: str, anti_ai: bool) -> str:
    return "\n\n".join(
        part for part in [
            _base_rules(),
            _anti_ai_block(anti_ai),
            """
OPERATION: EXPAND
MODE: KEY POINTS (EXPAND)

Task:
- Expand each bullet point into one short paragraph.
Rules:
- Use only the content of the bullet points as source material.
- Do not add new facts.
- If a point is vague, keep it vague.
Format:
- Keep the original bullet, then an indented paragraph beneath it.
""".strip(),
            "KEY POINTS:\n" + key_points_text,
        ] if part
    )


def _ollama_request(path: str, payload: Optional[Dict[str, Any]] = None, timeout: int = 5) -> Dict[str, Any]:
    """Call the local Ollama HTTP API using only the Python standard library."""
    url = OLLAMA_BASE_URL + path
    data = None
    headers = {"Accept": "application/json"}

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")

    if not raw.strip():
        return {}
    return json.loads(raw)


def get_installed_models() -> List[str]:
    """Return installed Ollama model names in Ollama's reported order."""
    data = _ollama_request("/api/tags", timeout=5)
    models = []

    for item in data.get("models", []):
        if not isinstance(item, dict):
            continue
        name = item.get("name") or item.get("model")
        if name:
            models.append(str(name))

    return models


def get_ollama_status() -> Dict[str, Any]:
    """
    Return one of the supported UI states:
    - Connected: Ollama is reachable and at least one model is installed.
    - No models installed: Ollama is reachable, but no usable local model was found.
    - Ollama not available: the local Ollama server is not reachable.
    """
    try:
        models = get_installed_models()
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError):
        return {
            "state": "Ollama not available",
            "model": None,
            "models": [],
            "detail": "Ollama is not reachable at http://localhost:11434.",
        }
    except Exception as exc:
        return {
            "state": "Ollama not available",
            "model": None,
            "models": [],
            "detail": "Ollama status check failed: " + str(exc),
        }

    if not models:
        return {
            "state": "No models installed",
            "model": None,
            "models": [],
            "detail": "Ollama is running, but no local models are installed.",
        }

    return {
        "state": "Connected",
        "model": models[0],
        "models": models,
        "detail": "Using model: " + models[0],
    }


def _resolve_model(requested_model: Optional[str], installed_models: List[str]) -> Optional[str]:
    """Use the requested model if installed; otherwise fall back to the first installed model."""
    if requested_model and requested_model in installed_models:
        return requested_model
    if installed_models:
        return installed_models[0]
    return None


def _invoke_model(prompt: str, model_name: Optional[str] = None) -> Tuple[bool, str]:
    status = get_ollama_status()
    state = status.get("state")
    models = status.get("models", [])
    model = _resolve_model(model_name, models)

    if state == "Ollama not available":
        return False, (
            "Ollama not available.\n\n"
            "Start Ollama, then try again. The Scratch checks the local server at:\n"
            "http://localhost:11434"
        )

    if state == "No models installed" or not model:
        return False, (
            "No models installed.\n\n"
            "Ollama is running, but no local models are installed.\n\n"
            "Recommended beginner models:\n\n"
            "8 GB RAM:\n"
            "gemma3:4b\n\n"
            "16 GB RAM:\n"
            "qwen3.5:9b\n\n"
            "24+ GB RAM:\n"
            "gemma3:12b\n\n"
            "Install any Ollama model you prefer.\n"
            "The Scratch automatically detects installed models and uses the first available model."
        )

    payload = {
        "model": str(model),
        "prompt": prompt,
        "stream": False,
    }

    try:
        data = _ollama_request("/api/generate", payload=payload, timeout=OLLAMA_TIMEOUT_SECONDS)
    except urllib.error.HTTPError as exc:
        return False, "Model request failed: HTTP " + str(exc.code)
    except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError):
        return False, "Ollama disconnected during generation. Start Ollama and try again."
    except Exception as exc:
        return False, "Model request failed: " + str(exc)

    if data.get("error"):
        return False, "Model error: " + str(data.get("error"))

    output = str(data.get("response", "")).strip()
    if not output:
        return False, "Model returned no output."
    return True, output


def run_prompt(
    notes: str,
    mode: str,
    params: Optional[Dict[str, Any]] = None,
    anti_ai: bool = True,
    model_name: Optional[str] = None,
) -> str:
    notes = (notes or "").strip()
    if len(notes) < 10:
        return "Awaiting more complete notes."

    params = params or {}
    mode = (mode or "").strip().upper()

    summarize_paragraphs = int(params.get("summary_paragraphs", 2) or 2)
    essay_words = int(params.get("essay_words", 500) or 500)
    outline_detail = str(params.get("outline_detail", "MEDIUM") or "MEDIUM").upper()

    kp_all = bool(params.get("kp_all", False))
    kp_names = bool(params.get("kp_names", True))
    kp_dates = bool(params.get("kp_dates", True))
    kp_numbers = bool(params.get("kp_numbers", True))
    kp_expand = bool(params.get("kp_expand", False))

    if kp_all:
        kp_names = kp_dates = kp_numbers = True

    if mode == "KEY POINTS" and not (kp_names or kp_dates or kp_numbers):
        kp_names = kp_dates = kp_numbers = True

    if mode == "SUMMARIZE":
        prompt = _build_prompt_summarize(notes, summarize_paragraphs, anti_ai)
        ok, output = _invoke_model(prompt, model_name=model_name)
        if not ok:
            return output
        output = _apply_output_ceiling(output)
        save_output(output, "summarize")
        return output

    if mode == "ESSAY":
        prompt = _build_prompt_essay(notes, essay_words, anti_ai)
        ok, output = _invoke_model(prompt, model_name=model_name)
        if not ok:
            return output
        output = _apply_output_ceiling(output)
        save_output(output, "essay")
        return output

    if mode == "OUTLINE":
        prompt = _build_prompt_outline(notes, outline_detail, anti_ai)
        ok, output = _invoke_model(prompt, model_name=model_name)
        if not ok:
            return output
        output = _apply_output_ceiling(output)
        save_output(output, "outline")
        return output

    if mode == "KEY POINTS":
        extract_prompt = _build_prompt_key_points_extract(
            notes,
            want_names=kp_names,
            want_dates=kp_dates,
            want_numbers=kp_numbers,
            anti_ai=anti_ai,
        )
        ok, extracted = _invoke_model(extract_prompt, model_name=model_name)
        if not ok:
            return extracted

        extracted = _apply_output_ceiling(extracted.strip())

        if not kp_expand:
            save_output(extracted, "key_points")
            return extracted

        expand_prompt = _build_prompt_key_points_expand(extracted, anti_ai)
        ok2, expanded = _invoke_model(expand_prompt, model_name=model_name)
        if not ok2:
            save_output(extracted, "key_points")
            return extracted

        expanded = _apply_output_ceiling(expanded)
        final_out = _apply_output_ceiling(extracted + "\n\n" + expanded)
        save_output(final_out, "key_points_expanded")
        return final_out

    return "Invalid mode."


def _apply_output_ceiling(output: str) -> str:
    if len(output) > MAX_OUTPUT_CHARS:
        return output[:MAX_OUTPUT_CHARS] + "\n\n[...truncated]"
    return output


def save_output(content: str, tag: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_tag = "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in tag)
    path = OUTPUT_DIR / (ts + "_" + safe_tag + ".txt")
    path.write_text(content, encoding="utf-8")
    return path
