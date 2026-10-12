"""Dependency-light ingestion and lexical retrieval for lesson evidence."""

from collections import Counter
from math import log
from pathlib import Path
import re
from typing import Iterable

from .schemas import KnowledgeChunk, RetrievedEvidence


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[\u4e00-\u9fff]")


def _tokens(text: str) -> tuple[str, ...]:
    return tuple(token.lower() for token in _TOKEN_RE.findall(text))


def load_markdown_directory(directory: Path) -> tuple[KnowledgeChunk, ...]:
    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"knowledge directory does not exist: {directory}")
    chunks: list[KnowledgeChunk] = []
    for path in sorted(directory.glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        title = next((line[2:].strip() for line in lines if line.startswith("# ")), path.stem)
        text = " ".join(line.strip() for line in lines if not line.startswith("#"))
        chunks.append(KnowledgeChunk(source_id=path.stem, title=title, text=text))
    return tuple(chunks)


class KnowledgeStore:
    def __init__(self, chunks: Iterable[KnowledgeChunk]):
        self._chunks = tuple(chunks)
        self._documents = tuple(set(_tokens(f"{c.title} {c.text}")) for c in self._chunks)

    def search(self, query: str, top_k: int = 5) -> tuple[RetrievedEvidence, ...]:
        query_terms = _tokens(query)
        if not query_terms or top_k <= 0:
            return ()
        query_counts = Counter(query_terms)
        document_frequency = Counter(term for document in self._documents for term in document)
        scored: list[tuple[float, str, KnowledgeChunk]] = []
        total_docs = max(1, len(self._documents))
        for chunk, document in zip(self._chunks, self._documents):
            if not document:
                continue
            score = 0.0
            for term, query_count in query_counts.items():
                if term in document:
                    idf = log((1 + total_docs) / (1 + document_frequency[term])) + 1
                    score += query_count * idf
            if score:
                scored.append((score, chunk.source_id, chunk))
        if not scored:
            return ()
        max_score = max(item[0] for item in scored)
        ranked = sorted(scored, key=lambda item: (-item[0], item[1]))[:top_k]
        return tuple(RetrievedEvidence(chunk=chunk, score=round(score / max_score, 6)) for score, _, chunk in ranked)

