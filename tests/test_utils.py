"""Comprehensive tests for utility functions."""

import sys
import subprocess
from unittest.mock import patch, MagicMock
import pytest  # type: ignore
from src.utils import extract_code, extract_file_path, execute_code_in_virtualenv


def test_extract_code():
    """Test Python code extraction from markdown."""
    text = "```python\nprint('hello')\n```"
    result = extract_code(text)
    assert result.strip() == "print('hello')"


def test_extract_code_no_match():
    """Test extraction with no code block."""
    text = "No code here"
    result = extract_code(text)
    assert result == ""


def test_extract_file_path_with_exception():
    """Test extract_file_path handles exceptions properly."""
    with patch("re.search", side_effect=ValueError("Regex error")):
        with pytest.raises(ValueError):
            extract_file_path('os.path.join("test", "file.txt")')


def test_extract_code_multiline():
    """Test extraction of multiline Python code."""
    text = """Here's some code:
```python
def hello():
    print('Hello World')
    return True
```
More text after."""
    result = extract_code(text)
    expected = "def hello():\n    print('Hello World')\n    return True"
    assert result.strip() == expected


def test_extract_file_path():
    """Test file path extraction from code."""
    code = 'file_path = os.path.join("output", "test.csv")'
    result = extract_file_path(code)
    assert "test.csv" in result
    assert "output" in result


def test_extract_file_path_no_match():
    """Test file path extraction when no os.path.join found."""
    code = 'some_other_code = "hello world"'
    result = extract_file_path(code)
    assert result is None


def test_extract_file_path_complex():
    """Test file path extraction with various formats."""
    test_cases = [
        ('output_path = os.path.join("data", "results.csv")', "data", "results.csv"),
        ('path = os.path.join( "folder" , "file.txt" )', "folder", "file.txt"),
        ("file = os.path.join('dir', 'name.json')", "dir", "name.json"),
    ]

    for code, expected_folder, expected_file in test_cases:
        result = extract_file_path(code)
        assert expected_folder in result
        assert expected_file in result


@patch("subprocess.run")
@patch("src.utils.extract_file_path")
@patch("src.utils.extract_code")
def test_execute_code_in_virtualenv_success(
    mock_extract_code, mock_extract_file_path, mock_subprocess
):
    """Test successful code execution."""
    # Setup mocks
    mock_extract_code.return_value = 'print("hello")'
    mock_extract_file_path.return_value = "output/test.csv"
    mock_subprocess.return_value = MagicMock()

    text = "```python\nprint('hello')\n```"
    result = execute_code_in_virtualenv(text)

    # Verify calls
    mock_extract_code.assert_called_once_with(text)
    mock_extract_file_path.assert_called_once_with('print("hello")')
    mock_subprocess.assert_called_once_with(
        [sys.executable, "-c", 'print("hello")'],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result == "output/test.csv"


@patch("subprocess.run")
@patch("src.utils.extract_code")
def test_execute_code_in_virtualenv_subprocess_error(
    mock_extract_code, mock_subprocess
):
    """Test code execution with subprocess error."""
    # Setup mocks
    mock_extract_code.return_value = "invalid_code()"
    error = subprocess.CalledProcessError(1, "cmd")
    error.stderr = "SyntaxError: invalid syntax"
    mock_subprocess.side_effect = error

    text = "```python\ninvalid_code()\n```"
    result = execute_code_in_virtualenv(text)

    # Should return error tuple
    assert isinstance(result, tuple)
    assert "Execution error:" in result[0]
    assert "SyntaxError: invalid syntax" in result[0]
    assert result[1] is None


def test_execute_code_in_virtualenv_no_interpreter():
    """Test code execution when no Python interpreter found."""
    with pytest.raises(OSError, match="Python interpreter not found"):
        execute_code_in_virtualenv(
            "```python\nprint('test')\n```", python_interpreter=None
        )


@patch("subprocess.run")
@patch("src.utils.extract_file_path")
@patch("src.utils.extract_code")
def test_execute_code_in_virtualenv_custom_interpreter(
    mock_extract_code, mock_extract_file_path, mock_subprocess
):
    """Test code execution with custom Python interpreter."""
    mock_extract_code.return_value = 'print("test")'
    mock_extract_file_path.return_value = "test.csv"
    mock_subprocess.return_value = MagicMock()

    custom_interpreter = "/usr/bin/python3.9"
    text = "```python\nprint('test')\n```"

    result = execute_code_in_virtualenv(text, python_interpreter=custom_interpreter)

    mock_subprocess.assert_called_once_with(
        [custom_interpreter, "-c", 'print("test")'],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result == "test.csv"


@patch("subprocess.run")
@patch("src.utils.extract_file_path")
@patch("src.utils.extract_code")
def test_execute_code_in_virtualenv_file_path_none(
    mock_extract_code, mock_extract_file_path, mock_subprocess
):
    """Test code execution when extract_file_path returns None."""
    mock_extract_code.return_value = 'print("hello")'
    mock_extract_file_path.return_value = None
    mock_subprocess.return_value = MagicMock()

    text = "```python\nprint('hello')\n```"
    result = execute_code_in_virtualenv(text)

    assert result is None


def test_logging_setup():
    """Test that logging is properly configured."""
    from src.utils import logger

    assert logger.name == "src.utils"
    assert logger.level <= 20  # INFO level or below
