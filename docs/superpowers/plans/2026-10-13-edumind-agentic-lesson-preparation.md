# EduMind Agentic Lesson Preparation - Implementation Plan

> Execute this plan in the dedicated repository at `work/edumind-agentic-lesson-preparation`.

## File map

- `pyproject.toml` - package metadata, Python version, and pytest configuration.
- `.gitignore` - excludes caches, local environments, generated outputs, and secrets.
- `src/edumind/schemas.py` - immutable typed contracts for requests, evidence, plans, and verification.
- `src/edumind/knowledge.py` - Markdown ingestion and deterministic lexical retrieval.
- `src/edumind/providers.py` - provider protocol plus offline demo provider with a clean vivo BlueLM integration seam.
- `src/edumind/agents.py` - research, planning, and verification roles.
- `src/edumind/pipeline.py` - end-to-end orchestration and error propagation.
- `src/edumind/render.py` - JSON and Markdown serialization.
- `src/edumind/demo.py` - command-line demonstration.
- `data/knowledge/*.md` - compact public teaching-note fixtures.
- `examples/lesson_preparation_demo.py` - copy-pasteable Python entry point.
- `tests/` - focused unit and integration tests.
- `README.md` - English paper-style technical documentation.
- `LICENSE` - Apache-2.0 license.

## Task 1 - Repository foundation and contracts

1. Add `pyproject.toml`, package `__init__.py`, `.gitignore`, and license.
2. Write tests for request validation, evidence provenance, plan shape, and verification report serialization.
3. Implement dataclasses/enums in `schemas.py` with explicit validation for non-empty topics, positive durations, and score ranges.
4. Run `python -m pytest -q tests/test_schemas.py` and commit.

## Task 2 - Knowledge ingestion and retrieval

1. Add a fixture note about a physics lesson and a note about misconceptions.
2. Write tests proving Markdown ingestion preserves source IDs and that retrieval ranks exact topic matches first.
3. Implement a dependency-light tokenizer, term-frequency/IDF-style scorer, deterministic tie-breaking, and top-k search in `knowledge.py`.
4. Run the knowledge tests and commit.

## Task 3 - Provider boundary and agent roles

1. Write tests for a provider-independent planner, deterministic demo output, and verifier failure cases.
2. Implement `LLMProvider` protocol, `DemoProvider`, `ResearchAgent`, `PlannerAgent`, and `VerifierAgent`.
3. Keep the provider abstraction free of concrete credentials, URLs, or request-signing details. A short code comment may identify the local provider as a demo fallback.
4. Run agent tests and commit.

## Task 4 - Pipeline and renderers

1. Write an integration test that runs the pipeline from fixture directory to verified `LessonPlan`.
2. Implement `LessonPreparationPipeline` with explicit stages: retrieve, plan, ground, verify.
3. Implement Markdown and JSON renderers with stable ordering and readable headings.
4. Run all tests and commit.

## Task 5 - CLI and examples

1. Add CLI argument parsing for topic, grade, duration, knowledge directory, and output paths.
2. Add a Python example that runs without network access.
3. Execute the CLI into a temporary directory and assert both output files are valid.
4. Commit the runnable demo.

## Task 6 - Paper-style README and repository hygiene

1. Write an English README with Overview, System Architecture, Core Pipeline, Quick Start, Project Structure, Demo Output, Design Notes, Testing, Extension Points, and Acknowledgements.
2. Mention vivo BlueLM only as a provider-level integration point; omit model names beyond that, endpoint details, credentials, and private project background.
3. Add a small architecture diagram in Mermaid and a compact sample output block.
4. Add a repository scanner test/script that fails on common secret patterns, original private filenames, large index extensions, and raw competition attachments.
5. Run README checks, the scanner, the complete test suite, and the CLI smoke test.
6. Commit documentation and hygiene checks.

## Task 7 - Final verification and handoff

1. Run the full test suite from a clean environment with no provider credentials set.
2. Run `python -m edumind.demo --help` and the end-to-end demo.
3. Inspect `git status`, tracked file list, repository size, and secret scan output.
4. Record the final commit hash and local path for publishing.
