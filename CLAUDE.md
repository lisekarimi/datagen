# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DataGen is an AI-powered synthetic data generator that transforms natural language business problem descriptions into downloadable datasets. It uses OpenAI GPT-4o-mini to generate Python code, executes that code in a subprocess, and returns the resulting file.

## Commands

All commands are in the `Makefile`. Run `make help` to list them.

## Architecture

The request flow is: **UI → Pipeline → DataGen → Models → Utils**

```
main.py           FastAPI app with Gradio mounted at root, uvicorn on PORT (default 7860)
src/ui.py         Gradio Blocks interface; calls pipeline.generate() as a generator
src/pipeline.py   DatasetPipeline.generate() validates input, yields Gradio UI updates,
                  spawns a threading.Timer for automatic file cleanup after 60s
src/datagen.py    DataGen.generate_dataset() builds prompt, calls LLM, executes returned code
src/models.py     get_gpt_completion() — OpenAI client wrapper (gpt-4o-mini)
src/prompts.py    system_message + build_user_prompt(); instructs the LLM on code structure
src/utils.py      extract_code(), extract_file_path(), execute_code_in_virtualenv()
src/constants.py  Project config: model name, output dir, token limits, cleanup timer
```

The LLM returns executable Python code. `utils.execute_code_in_virtualenv()` runs it in a subprocess; `extract_file_path()` then parses the file path from the generated code via regex on `os.path.join()` calls.

## Key Constraints

**Generated code rules** (enforced via `src/prompts.py` system message):
- Must use `os.path.join("folder", "filename")` with literal string arguments — no f-strings or variables — so `extract_file_path()` can parse the path via regex.
- Standard library and pre-installed packages only (no pip installs).

**Python version:** 3.11+ required (uses `tomllib` in `constants.py` to read `pyproject.toml`).

**Output directory:** Defaults to `output/` locally, `/tmp/output` in Docker (set via `OUTPUT_DIR` env var).

## Testing

Every change or new feature must be accompanied by tests and all tests must pass (`make test`) before the work is considered done.

## Code Style

Ruff is configured with `E, W, F, D, UP, B` rules and Google-style docstrings (`D` convention). Run `make fix` before committing. Pre-commit hooks enforce this.
