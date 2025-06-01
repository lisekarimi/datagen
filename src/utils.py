"""Utility functions for extracting and executing Python code from LLM responses."""

import re
import os
import subprocess
import sys
import logging

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def extract_code(text):
    """Extract Python code block from LLM response text."""
    try:
        # Search for Python code block using regex
        match = re.search(r"```python(.*?)```", text, re.DOTALL)
        if match:
            code = match.group(0).strip()
        else:
            code = ""
            logger.warning("No matching code block found.")

        # Clean up markdown formatting
        return code.replace("```python\n", "").replace("```", "")
    except Exception as e:
        logger.error(f"Code extraction error: {e}")
        raise


def extract_file_path(code_str):
    """Extract file path from code string containing os.path.join() calls."""
    try:
        # Look for os.path.join() pattern with two string arguments
        pattern = r'os\.path\.join\(\s*["\'](.+?)["\']\s*,\s*["\'](.+?)["\']\s*\)'
        match = re.search(pattern, code_str)
        if match:
            folder = match.group(1)
            filename = match.group(2)
            return os.path.join(folder, filename)

        logger.error("No file path found.")
        return None
    except Exception as e:
        logger.error(f"File path extraction error: {e}")
        raise


def execute_code_in_virtualenv(text, python_interpreter=sys.executable):
    """Execute extracted Python code in a subprocess and return the file path."""
    if not python_interpreter:
        raise OSError("Python interpreter not found.")

    # Extract the Python code from the input text
    code_str = extract_code(text)

    # Prepare subprocess command
    command = [python_interpreter, "-c", code_str]

    try:
        # logger.info("✅ Running script: %s", command)

        # Execute the code in subprocess
        # Note: We capture the result but don't need to use it directly
        # The subprocess.run() with check=True will raise an exception if it fails
        subprocess.run(command, check=True, capture_output=True, text=True)

        # Extract file path from the executed code
        file_path = extract_file_path(code_str)
        logger.info("✅ Extracted file path: %s", file_path)

        return file_path
    except subprocess.CalledProcessError as e:
        # Return error information if subprocess execution fails
        return (f"Execution error:\n{e.stderr.strip()}", None)
