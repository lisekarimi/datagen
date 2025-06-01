"""Tests for pipeline functionality."""

from unittest.mock import patch, MagicMock
from src.pipeline import DatasetPipeline, safe_delete


class TestSafeDelete:
    """Test cases for safe_delete function."""

    @patch("src.pipeline.os.path.exists")
    @patch("src.pipeline.os.remove")
    def test_delete_existing_file(self, mock_remove, mock_exists):
        """Test deletion of existing file."""
        mock_exists.return_value = True

        safe_delete("test_file.txt")

        mock_exists.assert_called_once_with("test_file.txt")
        mock_remove.assert_called_once_with("test_file.txt")

    @patch("src.pipeline.os.path.exists")
    @patch("src.pipeline.os.remove")
    def test_delete_nonexistent_file(self, mock_remove, mock_exists):
        """Test deletion of non-existent file."""
        mock_exists.return_value = False

        safe_delete("nonexistent_file.txt")

        mock_exists.assert_called_once_with("nonexistent_file.txt")
        mock_remove.assert_not_called()

    @patch("src.pipeline.os.path.exists")
    @patch("src.pipeline.os.remove")
    def test_delete_with_exception(self, mock_remove, mock_exists):
        """Test safe deletion when os.remove raises exception."""
        mock_exists.return_value = True
        mock_remove.side_effect = OSError("Permission denied")

        # Should not raise exception
        safe_delete("protected_file.txt")

        mock_exists.assert_called_once_with("protected_file.txt")
        mock_remove.assert_called_once_with("protected_file.txt")


class TestDatasetPipeline:
    """Test cases for DatasetPipeline class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.pipeline = DatasetPipeline()

    def test_initialization(self):
        """Test pipeline initialization."""
        assert hasattr(self.pipeline, "generator")
        assert self.pipeline.generator is not None

    def test_empty_business_problem(self):
        """Test pipeline with empty business problem."""
        generator = self.pipeline.generate("", "Tabular", "JSON", 10, "GPT")
        result = next(generator)

        assert "❌ Please enter a business problem" in result[2]
        assert result[0]["visible"] is False
        assert result[1]["visible"] is True

    def test_whitespace_only_business_problem(self):
        """Test pipeline with whitespace-only business problem."""
        generator = self.pipeline.generate("   ", "Tabular", "JSON", 10, "GPT")
        result = next(generator)

        assert "❌ Please enter a business problem" in result[2]

    @patch("src.pipeline.threading.Timer")
    @patch("src.pipeline.os.path.exists")
    def test_successful_generation(self, mock_exists, mock_timer):
        """Test successful dataset generation."""
        # Mock the generator
        mock_generator = MagicMock()
        mock_generator.generate_dataset.return_value = "test_file.csv"
        self.pipeline.generator = mock_generator

        mock_exists.return_value = True
        mock_timer.return_value = MagicMock()

        generator = self.pipeline.generate("Test problem", "Tabular", "CSV", 50, "GPT")

        # First yield should be loading message
        loading_result = next(generator)
        assert "⏳ Generating dataset..." in loading_result[2]
        assert loading_result[0]["visible"] is False
        assert loading_result[1]["visible"] is False

        # Second yield should be success
        success_result = next(generator)
        assert "✅ Dataset ready for download" in success_result[2]
        assert success_result[0]["visible"] is True
        assert success_result[0]["value"] == "test_file.csv"
        assert success_result[1]["visible"] is True

    def test_generation_exception(self):
        """Test handling of generation exceptions."""
        # Mock the generator to raise exception
        mock_generator = MagicMock()
        mock_generator.generate_dataset.side_effect = Exception("Generation failed")
        self.pipeline.generator = mock_generator

        generator = self.pipeline.generate("Test problem", "Tabular", "JSON", 10, "GPT")

        # Skip loading message
        next(generator)

        # Should yield error message
        error_result = next(generator)
        assert "❌ Pipeline error: Generation failed" in error_result[2]
        assert error_result[0]["visible"] is False
        assert error_result[1]["visible"] is True

    @patch("src.pipeline.os.path.exists")
    def test_file_not_created(self, mock_exists):
        """Test handling when file is not created."""
        # Mock the generator
        mock_generator = MagicMock()
        mock_generator.generate_dataset.return_value = "nonexistent_file.csv"
        self.pipeline.generator = mock_generator

        mock_exists.return_value = False

        generator = self.pipeline.generate(
            "Test problem", "Tabular", "CSV", 25, "Claude"
        )

        # Skip loading message
        next(generator)

        # Should yield file creation error
        error_result = next(generator)
        assert "❌ Error: File not created or path invalid" in error_result[2]
        assert error_result[0]["visible"] is False
        assert error_result[1]["visible"] is True

    @patch("src.pipeline.threading.Timer")
    @patch("src.pipeline.os.path.exists")
    def test_generator_called_with_correct_params(self, mock_exists, mock_timer):
        """Test that generator is called with correct parameters."""
        # Mock the generator
        mock_generator = MagicMock()
        mock_generator.generate_dataset.return_value = "test_file.json"
        self.pipeline.generator = mock_generator

        mock_exists.return_value = True
        mock_timer.return_value = MagicMock()

        generator = self.pipeline.generate(
            "Test problem", "Text", "JSON", 100, "Claude"
        )

        # Skip loading message
        next(generator)
        # Get success message
        next(generator)

        # Verify generator was called with correct parameters
        expected_params = {
            "business_problem": "Test problem",
            "dataset_type": "Text",
            "output_format": "JSON",
            "num_samples": 100,
            "model": "Claude",
        }
        mock_generator.generate_dataset.assert_called_once_with(**expected_params)

    def test_generator_returns_non_string_path(self):
        """Test handling when generator returns non-string file path."""
        # Mock the generator to return non-string
        mock_generator = MagicMock()
        mock_generator.generate_dataset.return_value = None
        self.pipeline.generator = mock_generator

        generator = self.pipeline.generate("Test problem", "Tabular", "JSON", 10, "GPT")

        # Skip loading message
        next(generator)

        # Should yield error message
        error_result = next(generator)
        assert "❌ Error: File not created or path invalid" in error_result[2]
        assert error_result[0]["visible"] is False
        assert error_result[1]["visible"] is True
