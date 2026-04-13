"""Tests for AI model clients and API configuration."""

import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from src.models import get_gpt_completion


class TestModels:
    """Test cases for AI model functions."""

    @patch("src.models.openai")
    def test_get_gpt_completion_success(self, mock_openai):
        """Test successful GPT completion."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Generated response"
        mock_openai.chat.completions.create.return_value = mock_response

        prompt = "Test prompt"
        system_message = "Test system message"

        result = get_gpt_completion(prompt, system_message)

        # Verify the API was called correctly
        mock_openai.chat.completions.create.assert_called_once_with(
            model="gpt-4o-mini",  # From OPENAI_MODEL constant
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )

        assert result == "Generated response"

    @patch("src.models.logger")
    @patch("src.models.openai")
    def test_get_gpt_completion_error(self, mock_openai, mock_logger):
        """Test GPT completion error handling."""
        # Setup mock to raise exception
        mock_openai.chat.completions.create.side_effect = Exception("API Error")

        prompt = "Test prompt"
        system_message = "Test system message"

        with pytest.raises(Exception, match="API Error"):
            get_gpt_completion(prompt, system_message)

        # Verify error was logged
        mock_logger.error.assert_called_once()
        assert "GPT error: API Error" in str(mock_logger.error.call_args)

    @patch("src.models.openai")
    def test_get_gpt_completion_with_empty_prompt(self, mock_openai):
        """Test GPT completion with empty prompt."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Response to empty prompt"
        mock_openai.chat.completions.create.return_value = mock_response

        result = get_gpt_completion("", "System message")

        # Verify empty prompt is handled
        called_args = mock_openai.chat.completions.create.call_args[1]
        assert called_args["messages"][1]["content"] == ""
        assert result == "Response to empty prompt"

    @patch("src.models.openai")
    def test_get_gpt_completion_uses_correct_model(self, mock_openai):
        """Test that GPT completion uses the correct model from constants."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai.chat.completions.create.return_value = mock_response

        get_gpt_completion("test", "test")

        # Verify correct model is used
        called_args = mock_openai.chat.completions.create.call_args[1]
        assert called_args["model"] == "gpt-4o-mini"

    @patch("src.models.openai")
    def test_get_gpt_completion_message_structure(self, mock_openai):
        """Test that GPT messages are structured correctly."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_openai.chat.completions.create.return_value = mock_response

        prompt = "User prompt"
        system_msg = "System instructions"

        get_gpt_completion(prompt, system_msg)

        # Verify message structure
        called_args = mock_openai.chat.completions.create.call_args[1]
        messages = called_args["messages"]

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == system_msg
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == prompt
