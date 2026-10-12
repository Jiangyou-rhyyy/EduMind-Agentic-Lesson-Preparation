import json

import pytest

from edumind.demo import main


def test_demo_writes_markdown_and_json_outputs(tmp_path):
    markdown_path = tmp_path / "lesson.md"
    json_path = tmp_path / "lesson.json"
    exit_code = main(
        [
            "--topic",
            "free fall",
            "--markdown-output",
            str(markdown_path),
            "--json-output",
            str(json_path),
        ]
    )
    assert exit_code == 0
    assert "Lesson Plan" in markdown_path.read_text(encoding="utf-8")
    assert json.loads(json_path.read_text(encoding="utf-8"))["verification"]["passed"]


def test_demo_reports_missing_knowledge_directory(tmp_path):
    with pytest.raises(SystemExit):
        main(["--knowledge-dir", str(tmp_path / "missing")])
