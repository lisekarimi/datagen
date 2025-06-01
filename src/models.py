"""AI model clients and API configuration for OpenAI and Anthropic."""

from openai import OpenAI
import anthropic
import os
from dotenv import load_dotenv
from .constants import OPENAI_MODEL, CLAUDE_MODEL, MAX_TOKENS, logger

# Load environment variables from .env file
load_dotenv(override=True)

# Retrieve API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Warn if any API key is missing for proper error handling
if not openai_api_key:
    logger.error("❌ OpenAI API Key is missing!")

if not anthropic_api_key:
    logger.error("❌ Anthropic API Key is missing!")

# Initialize API clients with the retrieved keys
openai = OpenAI(api_key=openai_api_key)
claude = anthropic.Anthropic()


def get_gpt_completion(prompt, system_message):
    """Call OpenAI's GPT model with prompt and system message."""
    try:
        # Create chat completion with system and user messages
        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            stream=False,
        )
        # Extract and return the generated content
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"GPT error: {e}")
        raise


def get_claude_completion(prompt, system_message):
    """Call Anthropic's Claude model with prompt and system message."""
    try:
        # Create message with Claude API using system prompt and user message
        result = claude.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            system=system_message,
            messages=[{"role": "user", "content": prompt}],
        )
        # Extract and return the text content from response
        return result.content[0].text
    except Exception as e:
        logger.error(f"Claude error: {e}")
        raise
