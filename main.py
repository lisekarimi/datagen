"""Entry point for the application."""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import gradio as gr
from src.ui import build_ui

# Create FastAPI app with custom docs URLs
app = FastAPI(
    docs_url="/api-docs", redoc_url="/api-redoc", openapi_url="/api-openapi.json"
)

# Get docs path
docs_path = Path(__file__).parent / "docs"


# Add redirect from /docs to /docs/ (must come BEFORE mounting)
@app.get("/docs")
async def redirect_to_docs():
    """Redirect to the /docs/ homepage."""
    return RedirectResponse(url="/docs/")


# Mount your documentation
if docs_path.exists():
    app.mount("/docs", StaticFiles(directory=str(docs_path), html=True), name="docs")

# Build Gradio UI
demo = build_ui()

# Mount Gradio to the root path (this should come LAST)
app = gr.mount_gradio_app(app, demo, path="")

# Main application entry point
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
