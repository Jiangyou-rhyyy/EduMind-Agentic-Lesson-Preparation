"""Fail fast if private artifacts or credentials enter the public repository."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".pytest_cache", ".venv", "__pycache__", ".superpowers"}
TEXT_SUFFIXES = {".py", ".md", ".toml", ".txt", ".json", ".yml", ".yaml"}
FORBIDDEN_SUFFIXES = {".faiss", ".pkl", ".mp4", ".zip", ".pptx", ".pdf", ".docx", ".key", ".pem"}


def main() -> int:
    failures: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            failures.append(f"forbidden artifact: {path.relative_to(ROOT)}")
            continue
        if path.stat().st_size > 2_000_000:
            failures.append(f"oversized file: {path.relative_to(ROOT)}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        # Build sensitive fragments instead of storing a usable credential in this scanner.
        patterns = [
            r"sk" + r"-[A-Za-z0-9]{12,}",
            r"(?:api" + r"_key|app" + r"_key|app" + r"_secret)\s*=\s*['\"]",
        ]
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            failures.append(f"sensitive token pattern: {path.relative_to(ROOT)}")
    if failures:
        print("Repository hygiene check failed:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("Repository hygiene check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

