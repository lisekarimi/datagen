"""Gradio web interface for synthetic data generation."""

import logging
import gradio as gr
from src.pipeline import DatasetPipeline
from src.constants import PROJECT_NAME, VERSION

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

pipeline = DatasetPipeline()

PROJECT_NAME_CAP = PROJECT_NAME.capitalize()
REPO_URL = f"https://github.com/lisekarimi/{PROJECT_NAME}"


def update_output_format(dataset_type):
    """Update output format choices based on selected dataset type."""
    if dataset_type in ["Tabular", "Time-series"]:
        return gr.update(choices=["JSON", "csv", "Parquet"], value="JSON")
    elif dataset_type == "Text":
        return gr.update(choices=["JSON", "Markdown"], value="JSON")


def build_ui(css_path="assets/styles.css"):
    """Build and return the complete Gradio user interface with error handling."""
    # Try to load CSS file with error handling
    try:
        with open(css_path, encoding="utf-8") as f:
            css = f.read()
    except Exception as e:
        css = ""
        logger.warning("⚠️ Failed to load CSS: %s", e)

    # Custom meta tags for SEO and social sharing
    custom_head = f"""
    <!-- HTML Meta Tags -->
    <title>🧬 {PROJECT_NAME_CAP} - AI-Powered Synthetic Dataset Generator</title>
    <meta name="description" content="Generate realistic synthetic datasets using AI models (GPT & Claude). Perfect for testing, development, and AI training. Multiple formats: JSON, CSV, Parquet, Markdown.">
    <meta name="keywords" content="synthetic data, dataset generator, AI, machine learning, GPT, Claude, data science, testing data, development data">
    <meta name="author" content="Lise Karimi">
    <meta name="robots" content="index, follow">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- Open Graph Meta Tags -->
    <meta property="og:url" content="https://datagen.lisekarimi.com">
    <meta property="og:type" content="website">
    <meta property="og:title" content="🧬 {PROJECT_NAME_CAP} - AI-Powered Synthetic Dataset Generator">
    <meta property="og:description" content="Generate realistic synthetic datasets using AI models (GPT & Claude). Perfect for testing, development, and AI training. Multiple formats: JSON, CSV, Parquet, Markdown.">
    <meta property="og:image" content="https://datagen.lisekarimi.com/assets/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="DataGen - AI-Powered Synthetic Dataset Generator">
    <meta property="og:site_name" content="DataGen">
    <meta property="og:locale" content="en_US">

    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="🧬 {PROJECT_NAME_CAP} - AI-Powered Synthetic Dataset Generator">
    <meta name="twitter:description" content="Generate realistic synthetic datasets using AI models (GPT & Claude). Perfect for testing, development, and AI training.">
    <meta name="twitter:image" content="https://datagen.lisekarimi.com/assets/og-image.png">
    <meta name="twitter:image:alt" content="DataGen - AI-Powered Synthetic Dataset Generator">

    <!-- Additional SEO Meta Tags -->
    <meta name="theme-color" content="#6366f1">
    <meta name="msapplication-TileColor" content="#6366f1">
    <link rel="canonical" href="https://datagen.lisekarimi.com">

    <!-- Favicon -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🧬</text></svg>">
    <link rel="apple-touch-icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🧬</text></svg>">
    """  # noqa: E501

    # Building the UI with error handling
    try:
        with gr.Blocks(css=css, head=custom_head, title=f"🧬{PROJECT_NAME_CAP}") as ui:
            with gr.Column(elem_id="app-container"):
                gr.Markdown(f"<h1 id='app-title'>🏷️ {PROJECT_NAME_CAP} </h1>")
                gr.Markdown(
                    "<h2 id='app-subtitle'>AI-Powered Synthetic Dataset Generator</h2>"
                )

                # Fix the f-string in HTML
                intro_html = f"""
                <div id="intro-text">
                    <p>With {PROJECT_NAME_CAP}, easily generate
                    <strong>diverse datasets</strong>
                    for testing, development, and AI training.</p>

                    <h4>🎯 How It Works:</h4>
                        <p>1️⃣ Define your business problem.</p>
                        <p>2️⃣ Select dataset type, format, model, and samples.</p>
                        <p>3️⃣ Download your synthetic dataset!</p>
                </div>
                """
                gr.HTML(intro_html)

                learn_more_html = """
                    <div id="learn-more-button">
                        <a href="https://datagen.lisekarimi.com/docs"
                           class="button-link">Documentation</a>
                    </div>
                    """
                gr.HTML(learn_more_html)

                examples_md = """
                    <p><strong>🧠 Need inspiration?</strong> Try these examples:</p>
                    <ul>
                    <li>Movie summaries for genre classification.</li>
                    <li>Customer chats with dialogue and sentiment labels.</li>
                    <li>Stock prices with date, ticker, open, close, volume.</li>
                    </ul>
                    """
                gr.Markdown(examples_md)

                gr.Markdown("<p><strong>Start generating now!</strong> 🗂️✨</p>")

                with gr.Group(elem_id="input-container"):
                    business_problem = gr.Textbox(
                        placeholder=(
                            "Describe the dataset you want "
                            "(e.g., Job postings, Customer reviews)"
                        ),
                        lines=2,
                        label="📌 Business Problem",
                        elem_classes=["label-box"],
                        elem_id="business-problem-box",
                    )

                    with gr.Row(elem_classes="column-gap"):
                        with gr.Column(scale=1):
                            dataset_type = gr.Dropdown(
                                ["Tabular", "Time-series", "Text"],
                                value="Tabular",
                                label="📊 Dataset Type",
                                elem_classes=["label-box"],
                                elem_id="custom-dropdown",
                            )

                        with gr.Column(scale=1):
                            output_format = gr.Dropdown(
                                choices=["JSON", "csv", "Parquet"],
                                value="JSON",
                                label="📁 Output Format",
                                elem_classes=["label-box"],
                                elem_id="custom-dropdown",
                            )

                        # Bind the update function to the dataset type dropdown
                        dataset_type.change(
                            update_output_format,
                            inputs=[dataset_type],
                            outputs=[output_format],
                        )

                    with gr.Row(elem_classes="row-spacer column-gap"):
                        with gr.Column(scale=1):
                            model = gr.Dropdown(
                                ["GPT", "Claude"],
                                value="GPT",
                                label="🤖 Model",
                                elem_classes=["label-box"],
                                elem_id="custom-dropdown",
                            )

                        with gr.Column(scale=1):
                            num_samples = gr.Slider(
                                minimum=10,
                                maximum=1000,
                                value=10,
                                step=1,
                                interactive=True,
                                label="🔢 Number of Samples",
                                elem_classes=["label-box"],
                            )

                # Hidden file component for dataset download
                file_download = gr.File(
                    visible=False, elem_id="download-box", label=None
                )

                # Component to display status messages
                status_message = gr.Markdown("", label="Status")

                # Button to trigger dataset generation
                run_btn = gr.Button("Create a dataset", elem_id="run-btn")
                run_btn.click(
                    pipeline.generate,
                    inputs=[
                        business_problem,
                        dataset_type,
                        output_format,
                        num_samples,
                        model,
                    ],
                    outputs=[file_download, run_btn, status_message],
                )

            # Bottom: version info
            gr.Markdown(
                f"""
                <p class="version-banner">
                    🔖 <strong>
                    <a href="{REPO_URL}/blob/main/CHANGELOG.md"
                    target="_blank">Version {VERSION}</a>
                    </strong>
                </p>
                """
            )

            # Floating chat button
            gr.HTML(
                """
                <a href="https://datagen.lisekarimi.com/docs" class="floating-chat-btn"
                    target="_blank">
                    💬 Chat with AI Assistant
                </a>
            """
            )

        return ui

    except Exception as e:
        logger.error("❌ Error building UI: %s", e)
        # Return a minimal error UI
        with gr.Blocks() as error_ui:
            gr.Markdown("# Error Loading Application")
            gr.Markdown(f"An error occurred: {str(e)}")
        return error_ui
