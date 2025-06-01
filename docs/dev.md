# 🔧 Development Guide

## 📋 Prerequisites

### 🔧 System Requirements
- Python 3.11+
- [uv package manager](https://docs.astral.sh/uv/getting-started/installation/)
- **Make:** `winget install GnuWin32.Make` (Windows) | `brew install make` (macOS) | `sudo apt install make` (Linux)

### 🪝 Git Configuration
Ensure your default branch is `main` (required for pre-commit hooks and CI/CD):
```bash
git config --global init.defaultBranch main
```

## 🛠️ Development Setup

### 📦 Installation & Dependencies
```bash
git clone https://github.com/lisekarimi/datagen.git
cd datagen
uv sync
source .venv/bin/activate  # Unix/macOS
# or .\.venv\Scripts\activate on Windows
```

We use **uv** for fast dependency management. Dependencies are added or removed using uv commands (see `Makefile`), which automatically update both `pyproject.toml` and the lockfile.

For more details: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)

### ⚙️ Environment Configuration
1. Copy `.env.example` to `.env`
2. Populate it with the required secrets


## 🚀 Essential Commands

Run `make help` to see all available commands.

**Core Development:**
```bash
make run            # Run the application
make ui             # Run with hot reload for development
make test           # Run test suite
make lint           # Check code quality
make install-hooks  # Set up pre-commit hooks
```

**Docker:**
```bash
make docker-build
make docker-run
```

---

## 🛡️ Pre-commit Hooks

Pre-commit hooks catch code style, commit message, and security issues early—saving you from failed CI checks later.

**What the hooks check:**
- **Code Quality:** Ruff formatting and linting
- **Commit Standards:** Commitizen, custom 50-character limit check
- **Security:** Gitleaks to prevent committing secrets
- **CI Safety:** Ensures the remote branch is ahead by enforcing `git pull --rebase` to prevent merge conflicts.

**Install hooks:**
```bash
make install-hooks
```

This workflow enforces clean code and a smooth CI/CD process before anything hits GitHub.

---

## 🧪 Testing & Quality

### Unit Testing
We use **pytest** for comprehensive unit testing with isolated environments. Testing runs in **isolated environments** using `uv run --isolated` without affecting your main environment.

All test files are located in the `tests/` directory with options to run specific files, functions, or generate coverage reports with HTML visualization.

### Code Quality Standards
- **Test Coverage:** Prioritize coverage on critical modules (models, pipeline, utils)
- **Linting:** All code must pass Ruff checks 
- **Security:** No secrets or vulnerabilities in commits (checked with gitleaks and pip-audit)
- **Commit Messages:** Follow conventional commit format

All quality checks run locally via Makefile commands and are enforced by pre-commit hooks.