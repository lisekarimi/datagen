# src/config/constants.py
"""Constants for configuration across the project."""

import os
import tomllib
from pathlib import Path
import logging

# ==================== PROJECT METADATA ====================
root = Path(__file__).parent.parent
with open(root / "pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

PROJECT_NAME = pyproject["project"]["name"]
VERSION = pyproject["project"]["version"]

# ==================== AI MODEL CONFIG ====================
OPENAI_MODEL = "gpt-4o-mini"
CLAUDE_MODEL = "claude-3-5-sonnet-20240620"

# Other constants can go here
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "output")
MAX_TOKENS = 2000

# ==================== LOGGING CONFIG ====================

# Configure logging once
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Create a shared logger
logger = logging.getLogger(__name__)

# ==================== FILE MANAGEMENT ====================
FILE_CLEANUP_SECONDS = 60  # 5 minutes
