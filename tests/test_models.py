"""Tests for AI model clients and API configuration."""

import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from src.models import get_gpt_completion, get_claude_completion


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

    @patch("src.models.claude")
    def test_get_claude_completion_success(self, mock_claude):
        """Test successful Claude completion."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Claude generated response"
        mock_claude.messages.create.return_value = mock_response

        prompt = "Test prompt"
        system_message = "Test system message"

        result = get_claude_completion(prompt, system_message)

        # Verify the API was called correctly
        mock_claude.messages.create.assert_called_once_with(
            model="claude-3-5-sonnet-20240620",  # From CLAUDE_MODEL constant
            max_tokens=2000,  # From MAX_TOKENS constant
            system=system_message,
            messages=[{"role": "user", "content": prompt}],
        )

        assert result == "Claude generated response"

    @patch("src.models.logger")
    @patch("src.models.claude")
    def test_get_claude_completion_error(self, mock_claude, mock_logger):
        """Test Claude completion error handling."""
        # Setup mock to raise exception
        mock_claude.messages.create.side_effect = Exception("Claude API Error")

        prompt = "Test prompt"
        system_message = "Test system message"

        with pytest.raises(Exception, match="Claude API Error"):
            get_claude_completion(prompt, system_message)

        # Verify error was logged
        mock_logger.error.assert_called_once()
        assert "Claude error: Claude API Error" in str(mock_logger.error.call_args)

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

    @patch("src.models.claude")
    def test_get_claude_completion_with_empty_system_message(self, mock_claude):
        """Test Claude completion with empty system message."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Response with empty system"
        mock_claude.messages.create.return_value = mock_response

        result = get_claude_completion("Test prompt", "")

        # Verify empty system message is handled
        called_args = mock_claude.messages.create.call_args[1]
        assert called_args["system"] == ""
        assert result == "Response with empty system"

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

    @patch("src.models.claude")
    def test_get_claude_completion_uses_correct_model_and_tokens(self, mock_claude):
        """Test that Claude completion uses correct model.

        Also checks max_tokens from constants.
        """
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Test response"
        mock_claude.messages.create.return_value = mock_response

        get_claude_completion("test", "test")

        # Verify correct model and max_tokens are used
        called_args = mock_claude.messages.create.call_args[1]
        assert called_args["model"] == "claude-3-5-sonnet-20240620"
        assert called_args["max_tokens"] == 2000

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

    @patch("src.models.claude")
    def test_get_claude_completion_message_structure(self, mock_claude):
        """Test that Claude messages are structured correctly."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Test response"
        mock_claude.messages.create.return_value = mock_response

        prompt = "User prompt"
        system_msg = "System instructions"

        get_claude_completion(prompt, system_msg)

        # Verify message structure
        called_args = mock_claude.messages.create.call_args[1]

        assert called_args["system"] == system_msg
        assert len(called_args["messages"]) == 1
        assert called_args["messages"][0]["role"] == "user"
        assert called_args["messages"][0]["content"] == prompt
