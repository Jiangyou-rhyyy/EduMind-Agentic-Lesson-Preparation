# EduMind Agentic Lesson Preparation - Design Specification

## Intent

Create a clean, paper-style public repository for **EduMind: An LLM- and Knowledge-Augmented Agentic Lesson Preparation System**. The repository should communicate the technical method clearly and provide a runnable demonstration of the lesson-preparation workflow without requiring model training, private credentials, or access to the original competition codebase.

## Constraints

- Use the supplied project materials only as a source for publicly presentable technical concepts.
- Do not copy the original application code, binary indexes, private documents, hardcoded credentials, API secrets, or provider-specific request details.
- Mention vivo BlueLM only at the provider level; keep model invocation behind a replaceable interface.
- The default path must run offline with deterministic demo output.
- Any simplified behavior that stands in for a production service may be marked lightly in code, but the README should present the workflow as a technical reference implementation without exposing internal caveats.
- Keep the repository compact enough for normal GitHub cloning and review.

## Recommended architecture

The repository will implement a six-stage pipeline:

1. **Ingest** - load small Markdown teaching notes and normalize them into knowledge records.
2. **Retrieve** - score records against a lesson request using a deterministic lexical retriever with source metadata.
3. **Plan** - call an `LLMProvider` abstraction to produce learning objectives, a lesson sequence, activities, and assessment items.
4. **Ground** - attach retrieved evidence to the generated plan and preserve provenance.
5. **Verify** - run structural checks for objective coverage, timing, evidence presence, and required output fields.
6. **Render** - emit a human-readable Markdown lesson plan plus machine-readable JSON for downstream clients.

The agent layer will expose small role-based components (`ResearchAgent`, `PlannerAgent`, `VerifierAgent`) coordinated by a `LessonPreparationPipeline`. Provider implementations will include a deterministic local demo provider and a documented integration seam for vivo BlueLM without any concrete API code.

## Public interfaces

- Pydantic-like dataclasses in `schemas.py` for `LessonRequest`, `KnowledgeChunk`, `RetrievedEvidence`, `LessonPlan`, and `VerificationReport`.
- `KnowledgeStore.search(query, top_k)` for retrieval.
- `LLMProvider.generate(request, evidence)` for model-agnostic generation.
- `LessonPreparationPipeline.run(request)` for end-to-end orchestration.
- CLI entry point `python -m edumind.demo` with optional query and output path arguments.

## Repository layout

```text
src/edumind/
  schemas.py       # typed data contracts
  knowledge.py     # ingest and deterministic retrieval
  providers.py     # provider protocol and local demo adapter
  agents.py        # research, planning, and verification roles
  pipeline.py      # orchestration and provenance flow
  render.py        # Markdown and JSON output
  demo.py          # CLI demonstration
data/knowledge/   # small public teaching-note fixtures
examples/          # one end-to-end invocation
tests/             # unit and integration tests
README.md          # English technical documentation
pyproject.toml     # package metadata and test configuration
```

## Testing and acceptance

- Unit tests cover retrieval ranking, provider isolation, schema validation, verifier failures, and deterministic output.
- An integration test runs the full pipeline on the bundled knowledge fixture.
- A smoke command produces both Markdown and JSON outputs without network access.
- README links and command snippets use paths and package names that match the repository.
- A repository scanner confirms that secrets, private source filenames, large binary indexes, and raw competition attachments are absent.

## Documentation shape

README sections will prioritize technical content in this order: Overview, System Architecture, Core Pipeline, Quick Start, Project Structure, Demo Output, Design Notes, Testing, Extension Points, and Acknowledgements. The prose will mention the vivo BlueLM provider at a high level and will not include API keys, endpoint URLs, signing algorithms, or request payloads.

## Non-goals

- Reproducing the original full-stack production deployment.
- Training or fine-tuning a language model.
- Shipping the original frontend, backend, FAISS indexes, videos, PPTX files, or competition reports.
- Claiming benchmark numbers that are not present in the supplied materials or produced by this reference implementation.
