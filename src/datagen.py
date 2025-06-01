"""Main data generation class for creating synthetic datasets using AI models."""

import os
from datetime import datetime
from .prompts import build_user_prompt, system_message
from .models import get_gpt_completion, get_claude_completion
from .utils import execute_code_in_virtualenv
from .constants import OUTPUT_DIR, logger


class DataGen:
    """Handles synthetic data generation using AI models."""

    def __init__(self, output_dir=None):
        """Initialize the data generator with output directory."""
        # Use provided output_dir, or fall back to OUTPUT_DIR constant
        self.output_dir = output_dir or OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def get_timestamp(self):
        """Return current timestamp for file naming."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate_dataset(self, **input_data):
        """Generate synthetic dataset based on input parameters and model choice."""
        try:
            # Ensure output directory exists before generating
            os.makedirs(self.output_dir, exist_ok=True)

            # Add output directory path to input data for file generation
            input_data["file_path"] = self.output_dir

            # Build the prompt to send to the selected LLM
            prompt = build_user_prompt(**input_data)

            # Call the selected LLM based on the model parameter
            if input_data["model"] == "GPT":
                code = get_gpt_completion(prompt, system_message)
            elif input_data["model"] == "Claude":
                code = get_claude_completion(prompt, system_message)
            else:
                raise ValueError("Invalid model selected.")

            # Execute the generated code and return the output file path
            file_path = execute_code_in_virtualenv(code)
            return file_path

        except Exception as e:
            # Log and re-raise any errors that occur during generation
            logger.error(f"Error in generate_dataset: {e}")
            raise
