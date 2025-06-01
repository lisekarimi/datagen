"""Tests for UI business logic functions."""

from src.ui import update_output_format, PROJECT_NAME_CAP, REPO_URL


class TestUpdateOutputFormat:
    """Test cases for update_output_format function."""

    def test_tabular_dataset_type(self):
        """Test output format update for Tabular dataset type."""
        result = update_output_format("Tabular")

        assert isinstance(result, dict)
        assert result["choices"] == ["JSON", "csv", "Parquet"]
        assert result["value"] == "JSON"

    def test_time_series_dataset_type(self):
        """Test output format update for Time-series dataset type."""
        result = update_output_format("Time-series")

        assert isinstance(result, dict)
        assert result["choices"] == ["JSON", "csv", "Parquet"]
        assert result["value"] == "JSON"

    def test_text_dataset_type(self):
        """Test output format update for Text dataset type."""
        result = update_output_format("Text")

        assert isinstance(result, dict)
        assert result["choices"] == ["JSON", "Markdown"]
        assert result["value"] == "JSON"

    def test_unknown_dataset_type(self):
        """Test output format update for unknown dataset type."""
        result = update_output_format("Unknown")

        assert result is None


class TestConstants:
    """Test cases for UI constants and variables."""

    def test_project_name_cap_formatting(self):
        """Test PROJECT_NAME_CAP is properly capitalized."""
        assert isinstance(PROJECT_NAME_CAP, str)
        assert len(PROJECT_NAME_CAP) > 0
        assert PROJECT_NAME_CAP[0].isupper()

    def test_repo_url_format(self):
        """Test REPO_URL is properly formatted."""
        assert isinstance(REPO_URL, str)
        assert REPO_URL.startswith("https://github.com/")
        assert "lisekarimi" in REPO_URL

    def test_constants_not_empty(self):
        """Test that constants are not empty."""
        assert PROJECT_NAME_CAP.strip() != ""
        assert REPO_URL.strip() != ""
