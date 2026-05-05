from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    """Normalize document text for chunking and retrieval."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()
