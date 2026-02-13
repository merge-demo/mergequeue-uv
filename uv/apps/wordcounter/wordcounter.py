"""Word counter application - displays word dictionary statistics."""

from __future__ import annotations

import os
from pathlib import Path


def _find_dict_path() -> Path:
    """Resolve path to uv/dict (workspace word lists). Prefer env, else relative to this file."""
    env_path = os.environ.get("WORDCOUNTER_DICT_PATH") or os.environ.get("UV_DICT_PATH")
    if env_path:
        return Path(env_path).resolve()
    # Editable install: this file is in uv/apps/wordcounter/ -> parent.parent.parent is uv/
    this_file = Path(__file__).resolve()
    uv_root = this_file.parent.parent.parent  # uv/
    return uv_root / "dict"


def _load_words_from_file(txt_path: Path) -> list[str]:
    """Load words from a text file (one word per line)."""
    words = []
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if word:
                words.append(word)
    return words


def _load_word_dict() -> dict[str, list[str]]:
    """Discover dict subdirs and load <name>.txt from each into WORD_DICT."""
    dict_path = _find_dict_path()
    if not dict_path.is_dir():
        return {}
    result = {}
    for subdir in sorted(dict_path.iterdir()):
        if not subdir.is_dir():
            continue
        name = subdir.name
        txt_file = subdir / f"{name}.txt"
        if txt_file.exists():
            result[name] = _load_words_from_file(txt_file)
    return result


# Load from filesystem at import so WORD_DICT is available for scripts/importers
WORD_DICT = _load_word_dict()

__all__ = ["WORD_DICT", "main"]


def main():
    """Main entry point - displays word dictionary statistics."""
    print("UV Word Dictionary")
    print("=" * 50)

    for folder, words in WORD_DICT.items():
        print(f"{folder}: {len(words)} words")

    print("\nTotal words:", sum(len(words) for words in WORD_DICT.values()))


if __name__ == "__main__":
    main()
