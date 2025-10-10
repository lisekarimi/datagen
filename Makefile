# =====================================
# 🌱 Project & Environment Configuration
# =====================================

# Read from pyproject.toml using grep (works on all platforms)
PROJECT_NAME = $(shell python3 -c "import re; print(re.search('name = \"(.*)\"', open('pyproject.toml').read()).group(1))")
VERSION = $(shell python3 -c "import re; print(re.search('version = \"(.*)\"', open('pyproject.toml').read()).group(1))")

# Configuration
include .env
export DOCKER_USERNAME
DOCKER_IMAGE = $(DOCKER_USERNAME)/$(PROJECT_NAME)
TAG = $(VERSION)
CONTAINER_NAME = $(PROJECT_NAME)-container
PORT = 7860


# =====================================
# 🛠️  Environment Setup (using UV)
# =====================================
# uv add package-name - Add a new dependency
# uv add --dev package-name - Add a development dependency
# uv sync - Install/sync all dependencies
# uv remove package-name - Remove a dependency
# uv remove --dev package-name - Remove a development dependency
# uv cache clean - Clear the cache

activate:	## Activate the virtual environment
	@echo "To activate the virtual environment, run:"
	@echo "  .\.venv\Scripts\activate  (Windows)"
	@echo "  source .venv/bin/activate   (Mac/Linux)"


# =======================
# 🪝 Hooks
# =======================

install-hooks:	## Install pre-commit hooks
	uvx pre-commit install
	uvx pre-commit install --hook-type commit-msg


# =====================================
# ✨ Code Quality
# =====================================

lint:	## Run code linting and formatting
	uvx ruff check .
	uvx ruff format .

fix:	## Fix code issues and format
	uvx ruff check --fix .
	uvx ruff format .


# =====================================
# 🚀 Run App Locally
# =====================================

run:	## Run the app locally (no hot reload)
	uv run main.py

ui:	## Run the UI dev server with hot reloading
	uv run gradio main.py


# =======================
# 🐳 Docker Commands
# =======================

build: ## Build the Docker image for development
	docker build -t $(DOCKER_IMAGE):$(TAG) .

ls: ## List files in Docker image
	docker run --rm $(DOCKER_IMAGE):$(TAG) ls -la /app

# Workflow: Edit code → Ctrl+C → Run 'make docker-run' again to see changes
run:	## Run development container with live code changes (no rebuild needed)
	docker run --rm -d \
	--name $(CONTAINER_NAME) \
	--env-file .env \
	-p $(PORT):$(PORT) \
	-v $(CURDIR):/app \
	-w /app \
	$(DOCKER_IMAGE):$(TAG)
	@echo "🚀 Application is running in background at http://localhost:$(PORT)"

stop:	## Stop the running container
	docker stop $(CONTAINER_NAME)

restart:	## Restart the container
	@make stop || true
	@make run

clean: ## Remove container and image
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(DOCKER_IMAGE):$(TAG) || true


deep-clean: clean ## Clean everything including build cache
	docker builder prune -f

# =======================
# 🧪 Testing Commands
# =======================

test: 	## Run all tests in the tests/ directory
	uv run --isolated --with pytest pytest

test-file: 	## Run specific test file
	uv run --isolated --with pytest pytest tests/test_models.py

test-func: 	## Run specific test function by name
	uv run --isolated --with pytest pytest -k test_extract_code

test-cov: 	## Run tests with coverage
	uv run --isolated --with pytest --with pytest-cov pytest --cov=src

test-cov-html: 	## Run tests with coverage and generate HTML report
	uv run --isolated --with pytest --with pytest-cov pytest --cov=src --cov-report html

open-cov: 	## Open HTML coverage report in browser
	@echo "To open the HTML coverage report, run:"
	@echo "  start htmlcov\\index.html        (Windows)"
	@echo "  open htmlcov/index.html          (macOS)"
	@echo "  xdg-open htmlcov/index.html      (Linux)"

# =======================
# 🔍 Security Scanning
# =======================

# Install gitleaks first: https://github.com/gitleaks/gitleaks

check-secrets:		## Debug: Check secrets manually (also runs in pre-commit
	gitleaks detect --source . --verbose

audit:	## Audit dependencies for vulnerabilities
	uv run --with pip-audit pip-audit


# =====================================
# 📚 Documentation & Help
# =====================================

help: ## Show this help message
	@echo Available commands:
	@echo.
	@python3 -c "import re; lines=open('Makefile', encoding='utf-8').readlines(); targets=[re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$',l) for l in lines]; [print(f'  make {m.group(1):<20} {m.group(2)}') for m in targets if m]"


# =======================
# 🎯 PHONY Targets
# =======================

# Auto-generate PHONY targets (cross-platform)
.PHONY: $(shell python3 -c "import re; print(' '.join(re.findall(r'^([a-zA-Z_-]+):\s*.*?##', open('Makefile', encoding='utf-8').read(), re.MULTILINE)))")

# Test the PHONY generation
# test-phony:
# 	@echo "$(shell python3 -c "import re; print(' '.join(sorted(set(re.findall(r'^([a-zA-Z0-9_-]+):', open('Makefile', encoding='utf-8').read(), re.MULTILINE)))))")"
