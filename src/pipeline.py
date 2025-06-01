"""Pipeline orchestration for dataset generation."""

import os
import logging
import threading
import gradio as gr
from src.datagen import DataGen
from src.constants import FILE_CLEANUP_SECONDS

logger = logging.getLogger(__name__)


def safe_delete(file_path):
    """Safely delete a file, ignoring errors if file doesn't exist."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass  # Ignore deletion errors


class DatasetPipeline:
    """Handles the dataset generation pipeline."""

    def __init__(self):
        """Initialize the pipeline with a DataGen instance."""
        self.generator = DataGen()

    def generate(
        self, business_problem, dataset_type, output_format, num_samples, model
    ):
        """Generate synthetic dataset based on user inputs."""
        # Check if business problem is empty
        if not business_problem.strip():
            error_msg = "❌ Please enter a business problem before generating."
            yield [gr.update(visible=False), gr.update(visible=True), error_msg]
            return

        # Initial feedback while generating
        yield [
            gr.update(visible=False),
            gr.update(visible=False),
            "⏳ Generating dataset...",
        ]

        try:
            # Pack inputs into a dictionary for the generator
            input_data = {
                "business_problem": business_problem,
                "dataset_type": dataset_type,
                "output_format": output_format,
                "num_samples": num_samples,
                "model": model,
            }

            # Generate dataset file
            file_path = self.generator.generate_dataset(**input_data)

            # Check if file exists and return success message + file path
            if isinstance(file_path, str) and os.path.exists(file_path):
                # Auto-delete after 5min with safe deletion
                threading.Timer(
                    FILE_CLEANUP_SECONDS, safe_delete, args=[file_path]
                ).start()
                success_update = [
                    gr.update(value=file_path, visible=True),
                    gr.update(visible=True),
                    "✅ Dataset ready for download.",
                ]
                yield success_update
            else:
                # Handle invalid or missing file
                error_update = [
                    gr.update(visible=False),
                    gr.update(visible=True),
                    "❌ Error: File not created or path invalid.",
                ]
                yield error_update

        except Exception as e:
            # Catch and display any errors in the pipeline
            logger.error("Pipeline error: %s", e)
            error_update = [
                gr.update(visible=False),
                gr.update(visible=True),
                f"❌ Pipeline error: {e}",
            ]
            yield error_update
