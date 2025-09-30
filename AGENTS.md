# Repository Guidelines

## Project Structure & Module Organization
The pipeline lives in modular packages: `agents/` hosts decision agents, `chains/` defines summarization and scoring flows, `composer/` formats finished newsletters, and `tools/` wraps external data sources. Runtime settings sit in `config/` (`settings.py`, `interests.yaml`), while `data/` and `data_module/` store cached inputs and generated outputs. Entry point `generate_newsletter.py` wires the pieces together, and root-level `test_*.py` exercises critical paths.

## Build, Test, and Development Commands
Set up Python 3.11+ with `python -m venv .venv && source .venv/bin/activate`, then install dependencies via `pip install -r requirements.txt`. Run the full pipeline locally using `python generate_newsletter.py`, or do a safe rehearsal with `python generate_newsletter.py --dry-run` to validate config without hitting APIs. Use `python generate_newsletter.py --config config/interests.yaml` when testing alternative profiles.

## Coding Style & Naming Conventions
We follow Black’s default formatting (88 characters, 4-space indent). Run `black .` before commits and lint with `flake8` to catch edge cases. Prefer explicit type hints, descriptive module-level docstrings, and snake_case for modules, packages, and functions. Class names stay in PascalCase, and constants belong in UPPER_SNAKE_CASE. Keep configuration keys lowercase with hyphen-free names for safe YAML parsing.

## Testing Guidelines
Pytest powers the suite; invoke `pytest` for the whole repo or target focused checks like `pytest test_pipeline.py -k newsletter`. Add new tests alongside implementation files (`test_<module>.py`) and mirror fixture naming after the feature under test. Integration changes should exercise `test_pipeline.py`; new tools need coverage in `test_tools.py`. Aim to keep deterministic mocks for API clients so CI can run without external connectivity.

## Commit & Pull Request Guidelines
Local history is currently sparse, so adopt Conventional Commit subjects (e.g., `feat: add reddit fetcher`, `fix: guard openai retries`) and keep bodies in present tense. Bundle related changes only, reference issue numbers when available, and note config or schema updates explicitly. Pull requests should outline the behavior change, mention new commands or toggles, and include screenshots or log excerpts when they clarify pipeline output.

## Configuration & Secrets
Store API credentials in a local `.env` (never commit) and load them through `config/settings.py`. Update `config/interests.yaml` for personalization, and drop sample artifacts in `data_module/temp/` rather than `data/outputs/` when collaborating to avoid polluting shipped content.
