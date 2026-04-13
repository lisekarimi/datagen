"""AI model clients and API configuration for OpenAI."""

from openai import OpenAI
import os
from dotenv import load_dotenv
from .constants import OPENAI_MODEL, logger

# Load environment variables from .env file
load_dotenv(override=True)

# Retrieve API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    logger.error("❌ OpenAI API Key is missing!")

# Initialize API client
openai = OpenAI(api_key=openai_api_key)


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
