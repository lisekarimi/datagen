"""Entry point for the application."""

import os
from src.ui import build_ui

demo = build_ui()

# Main application entry point
if __name__ == "__main__":
    demo.launch(
        allowed_paths=["output"],
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),
    )
