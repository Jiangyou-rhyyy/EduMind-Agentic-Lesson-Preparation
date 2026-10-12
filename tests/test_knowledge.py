from pathlib import Path

from edumind.knowledge import KnowledgeStore, load_markdown_directory


def test_markdown_ingestion_preserves_stable_source_ids(tmp_path: Path):
    (tmp_path / "free-fall.md").write_text("# Free Fall\nAcceleration is constant.", encoding="utf-8")
    chunks = load_markdown_directory(tmp_path)
    assert chunks[0].source_id == "free-fall"
    assert chunks[0].title == "Free Fall"


def test_search_ranks_exact_topic_match_first():
    store = KnowledgeStore(
        load_markdown_directory(Path("data/knowledge"))
    )
    results = store.search("free fall acceleration", top_k=2)
    assert results
    assert results[0].chunk.source_id == "physics-free-fall"
    assert results[0].score >= results[-1].score
