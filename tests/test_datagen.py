"""Tests for DataGen class."""

import pytest  # type: ignore
import os
import tempfile
import shutil
from unittest.mock import patch
from src.datagen import DataGen


class TestDataGen:
    """Test cases for DataGen class."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.datagen = DataGen(output_dir=self.temp_dir)

    def teardown_method(self):
        """Clean up after each test method."""
        # Remove temporary directory and contents
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_init_creates_output_directory(self):
        """Test that initialization creates the output directory."""
        assert os.path.exists(self.temp_dir)
        assert os.path.isdir(self.temp_dir)
        assert self.datagen.output_dir == self.temp_dir

    def test_init_with_existing_directory(self):
        """Test initialization with existing directory doesn't fail."""
        # Directory already exists from setup_method
        datagen2 = DataGen(output_dir=self.temp_dir)
        assert datagen2.output_dir == self.temp_dir
        assert os.path.exists(self.temp_dir)

    @patch("src.datagen.datetime")
    def test_get_timestamp(self, mock_datetime):
        """Test timestamp generation format."""
        mock_datetime.now.return_value.strftime.return_value = "20250529_143000"

        result = self.datagen.get_timestamp()

        assert result == "20250529_143000"
        mock_datetime.now.return_value.strftime.assert_called_once_with("%Y%m%d_%H%M%S")

    @patch("src.datagen.execute_code_in_virtualenv")
    @patch("src.datagen.get_gpt_completion")
    @patch("src.datagen.build_user_prompt")
    def test_generate_dataset_gpt(self, mock_prompt, mock_gpt, mock_execute):
        """Test dataset generation using GPT model."""
        # Setup mocks
        mock_prompt.return_value = "test prompt"
        mock_gpt.return_value = "test code"
        mock_execute.return_value = "test_file.csv"

        input_data = {
            "business_problem": "Test problem",
            "dataset_type": "Tabular",
            "output_format": "csv",
            "num_samples": 10,
            "model": "GPT",
        }

        result = self.datagen.generate_dataset(**input_data)

        # Verify calls
        mock_prompt.assert_called_once()
        assert mock_gpt.call_args[0][0] == "test prompt"
        assert "synthetic datasets" in mock_gpt.call_args[0][1]
        mock_execute.assert_called_once_with("test code")
        assert result == "test_file.csv"

        # Check that file_path was added to input_data
        called_args = mock_prompt.call_args[1]
        assert called_args["file_path"] == self.temp_dir

    @patch("src.datagen.execute_code_in_virtualenv")
    @patch("src.datagen.get_claude_completion")
    @patch("src.datagen.build_user_prompt")
    def test_generate_dataset_claude(self, mock_prompt, mock_claude, mock_execute):
        """Test dataset generation using Claude model."""
        # Setup mocks
        mock_prompt.return_value = "test prompt"
        mock_claude.return_value = "test code"
        mock_execute.return_value = "test_file.json"

        input_data = {
            "business_problem": "Test problem",
            "dataset_type": "Text",
            "output_format": "json",
            "num_samples": 50,
            "model": "Claude",
        }

        result = self.datagen.generate_dataset(**input_data)

        # Verify calls
        mock_prompt.assert_called_once()
        # Check that Claude was called with prompt and system_message
        assert mock_claude.call_args[0][0] == "test prompt"  # First arg is the prompt
        assert "synthetic datasets" in mock_claude.call_args[0][1]
        mock_execute.assert_called_once_with("test code")
        assert result == "test_file.json"

    @patch("src.datagen.build_user_prompt")
    def test_generate_dataset_invalid_model(self, mock_prompt):
        """Test that invalid model raises ValueError."""
        mock_prompt.return_value = "test prompt"

        input_data = {
            "business_problem": "Test problem",
            "dataset_type": "Tabular",
            "output_format": "csv",
            "num_samples": 10,
            "model": "INVALID_MODEL",
        }

        with pytest.raises(ValueError, match="Invalid model selected"):
            self.datagen.generate_dataset(**input_data)

    @patch("src.datagen.logger")
    @patch("src.datagen.build_user_prompt")
    def test_generate_dataset_error_handling(self, mock_prompt, mock_logger):
        """Test error handling and logging in generate_dataset."""
        # Make build_user_prompt raise an exception
        mock_prompt.side_effect = Exception("Test error")

        input_data = {
            "business_problem": "Test problem",
            "dataset_type": "Tabular",
            "output_format": "csv",
            "num_samples": 10,
            "model": "GPT",
        }

        with pytest.raises(Exception, match="Test error"):
            self.datagen.generate_dataset(**input_data)

        # Verify error was logged
        mock_logger.error.assert_called_once()
        error_msg = "Error in generate_dataset: Test error"
        assert error_msg in str(mock_logger.error.call_args)

    @patch("src.datagen.execute_code_in_virtualenv")
    @patch("src.datagen.get_gpt_completion")
    @patch("src.datagen.build_user_prompt")
    def test_generate_dataset_input_data_modification(
        self, mock_prompt, mock_gpt, mock_execute
    ):
        """Test that input_data is properly modified with file_path."""
        mock_prompt.return_value = "test prompt"
        mock_gpt.return_value = "test code"
        mock_execute.return_value = "test_file.csv"

        input_data = {
            "business_problem": "Test problem",
            "dataset_type": "Tabular",
            "output_format": "csv",
            "num_samples": 10,
            "model": "GPT",
        }

        original_keys = set(input_data.keys())
        self.datagen.generate_dataset(**input_data)

        # Verify that file_path was added
        called_with = mock_prompt.call_args[1]
        assert "file_path" in called_with
        assert called_with["file_path"] == self.temp_dir

        # Verify all original keys are still present
        for key in original_keys:
            assert key in called_with
            assert called_with[key] == input_data[key]

    def test_different_output_directories(self):
        """Test DataGen with different output directories."""
        temp_dir2 = tempfile.mkdtemp()
        try:
            datagen2 = DataGen(output_dir=temp_dir2)
            assert datagen2.output_dir == temp_dir2
            assert os.path.exists(temp_dir2)
            assert datagen2.output_dir != self.datagen.output_dir
        finally:
            shutil.rmtree(temp_dir2)
