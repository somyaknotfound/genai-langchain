"""Optional tiered-LLM layer for the practice agent.

Model routing (the 'switch models for tasks' requirement):
  - cheapModel  (Haiku)  -> high-volume, low-stakes: summarize each notebook
                            into 'concepts actually practiced'.
  - strongModel (Sonnet) -> single high-stakes reasoning call: write the
                            personalized practice set + coaching note.

Everything degrades gracefully: if the anthropic SDK isn't installed or
ANTHROPIC_API_KEY isn't set, `available()` returns False and the caller
uses the offline curated bank instead. No hard dependency.
"""
from __future__ import annotations
import os

try:
    import anthropic  # type: ignore
    _SDK = True
except Exception:
    _SDK = False


def available(cfg) -> bool:
    llm = cfg.get("llm", {})
    return bool(llm.get("enabled")) and _SDK and bool(os.getenv("ANTHROPIC_API_KEY"))


def _client():
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def _complete(model: str, system: str, user: str, max_tokens: int = 1200) -> str:
    resp = _client().messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in resp.content if getattr(block, "type", "") == "text").strip()


def summarize_notebook(cfg, title: str, text: str) -> str:
    """Cheap model: what concepts did this notebook actually practice? One line."""
    model = cfg["llm"]["cheapModel"]
    text = text[:6000]
    system = (
        "You label learning notebooks. Given a Jupyter notebook's text, reply with ONE "
        "terse line (max 20 words) naming the concrete GenAI/NLP/DL concepts the learner "
        "practiced. No preamble, no markdown."
    )
    try:
        return _complete(model, system, f"Notebook '{title}':\n\n{text}", max_tokens=80)
    except Exception as e:
        return f"(summary unavailable: {e})"


def generate_practice(cfg, context: str) -> str:
    """Strong model: produce the tailored practice markdown body."""
    model = cfg["llm"]["strongModel"]
    max_problems = cfg["llm"].get("maxProblems", 6)
    system = (
        "You are a rigorous GenAI course coach for a learner taking Krish Naik's "
        "'Complete Generative AI with LangChain & HuggingFace'. "
        "Write a focused practice set in GitHub-flavored markdown. Requirements:\n"
        f"- {max_problems} problems max, ordered easy -> hard, ending in one mini-project.\n"
        "- Tie problems to what the learner has ALREADY covered (given below). Do not "
        "assign topics they haven't reached.\n"
        "- Include 1-2 spaced-repetition questions on an earlier topic.\n"
        "- Each problem: a bold title, then a concrete, verifiable task (mention specific "
        "libraries: langchain, faiss/chroma, huggingface, gensim, keras, etc.).\n"
        "- End with a short '## Coaching note' (3-4 sentences) on what to focus on next.\n"
        "- No fluff, no restating the whole syllabus. Start directly with '## Practice problems'."
    )
    return _complete(model, system, context, max_tokens=2000)
