"""Tests for prompt templates and management."""

import pytest  # type: ignore
from unittest.mock import patch
from src.prompts import build_user_prompt, system_message


def test_system_message_exists():
    """Test that system message is defined and not empty."""
    assert system_message is not None
    assert len(system_message.strip()) > 0
    assert "synthetic datasets" in system_message


def test_system_message_contains_key_instructions():
    """Test that system message contains essential instructions."""
    assert "os.path.join" in system_message
    assert "CSV:" in system_message
    assert "JSON:" in system_message
    assert "Parquet:" in system_message
    assert "Markdown" in system_message


@patch("src.prompts.datetime")
def test_build_user_prompt_basic(mock_datetime):
    """Test basic user prompt building functionality."""
    # Mock datetime to return predictable timestamp
    mock_datetime.now.return_value.strftime.return_value = "20250529_120000"

    input_data = {
        "file_path": "output",
        "dataset_type": "Tabular",
        "output_format": "json",
        "business_problem": "Generate customer data",
        "num_samples": 100,
    }

    result = build_user_prompt(**input_data)

    assert "Generate a synthetic tabular" in result
    assert "dataset in JSON format" in result
    assert "Business problem: Generate customer data" in result
    assert "Samples: 100" in result
    assert "Directory: output" in result
    assert "Timestamp: 20250529_120000" in result


def test_build_user_prompt_path_normalization():
    """Test that Windows paths are normalized to forward slashes."""
    input_data = {
        "file_path": "C:\\Users\\test\\output",
        "dataset_type": "Text",
        "output_format": "markdown",
        "business_problem": "Test problem",
        "num_samples": 50,
    }

    result = build_user_prompt(**input_data)

    assert "Directory: C:/Users/test/output" in result
    assert "C:\\Users" not in result


def test_build_user_prompt_case_handling():
    """Test proper case handling for dataset type and output format."""
    input_data = {
        "file_path": "output",
        "dataset_type": "TIME-SERIES",
        "output_format": "csv",
        "business_problem": "Stock prices",
        "num_samples": 25,
    }

    result = build_user_prompt(**input_data)

    assert "synthetic time-series" in result
    assert "dataset in CSV format" in result


def test_build_user_prompt_missing_key():
    """Test that KeyError is raised for missing required keys."""
    incomplete_data = {
        "file_path": "output",
        "dataset_type": "Tabular",
        # Missing other required keys
    }

    with pytest.raises(KeyError):
        build_user_prompt(**incomplete_data)


def test_build_user_prompt_all_parameters_included():
    """Test that all input parameters are included in the prompt."""
    input_data = {
        "file_path": "test/path",
        "dataset_type": "Tabular",
        "output_format": "parquet",
        "business_problem": "E-commerce analytics",
        "num_samples": 500,
    }

    result = build_user_prompt(**input_data)

    # Check all parameters are mentioned
    assert "tabular" in result.lower()
    assert "PARQUET" in result
    assert "E-commerce analytics" in result
    assert "500" in result
    assert "test/path" in result


@patch("src.prompts.datetime")
def test_build_user_prompt_timestamp_format(mock_datetime):
    """Test that timestamp is properly formatted."""
    mock_datetime.now.return_value.strftime.return_value = "20250101_235959"

    input_data = {
        "file_path": "output",
        "dataset_type": "Text",
        "output_format": "json",
        "business_problem": "News articles",
        "num_samples": 10,
    }

    result = build_user_prompt(**input_data)

    assert "Timestamp: 20250101_235959" in result
    # Verify strftime was called with correct format
    mock_datetime.now.return_value.strftime.assert_called_with("%Y%m%d_%H%M%S")
