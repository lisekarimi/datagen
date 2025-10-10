# 🧬 Datagen Docs Overview

Datagen is an AI-powered toolkit for generating realistic synthetic datasets to accelerate testing, prototyping, and ML experimentation. This documentation provides a high-level guide to the project’s architecture, local development, deployment, and CI/CD.

<img src="https://github.com/lisekarimi/datagen/blob/main/assets/screenshot.png?raw=true" alt="DataGen interface" width="450">

## ✨ What DataGen Does

DataGen transforms simple descriptions into structured datasets using AI. Perfect for researchers, data scientists, and developers who need realistic test data fast.

**Key Features:**
- **Type what you want → Get real data**
- **Multiple formats:** CSV, JSON, Parquet, Markdown
- **Dataset types:** Tables, time-series, text data
- **AI-powered:** Uses GPT and Claude models
- **Instant download** with clean, ready-to-use datasets


## 🧑‍💻 How to Use

1. **Describe your data:** "Customer purchase history with demographics"
2. **Choose format:** CSV, JSON, Parquet, or Markdown
3. **Select AI model:** GPT or Claude
4. **Set sample size:** Number of records to generate
5. **Generate & download** your dataset

## 🗂️ What’s in this project

- UI: A Gradio web app that lets you describe a dataset, choose type/format/model, and download generated data
- Core: A pipeline that orchestrates prompt construction, model calls, validation, and file export
- Formats: JSON, CSV, Parquet (for Tabular/Time-series) and JSON/Markdown (for Text)
- Docs: Docsify-powered site served from `/docs/`


## 📖 Core docs

- Architecture: how UI, pipeline, prompts, and utilities fit together
- Development: local setup, commands, and conventions
- CI/CD: linting, tests, scans, and deployment workflow

## 🧩 Key components (code)

- `main.py`: app entrypoint; mounts Docsify at `/docs`
- `src/ui.py`: Gradio Blocks UI and event wiring
- `src/pipeline.py`: dataset generation orchestration
- `src/datagen.py`, `src/prompts.py`, `src/utils.py`: helper logic for generation and formatting
- `tests/`: unit tests per module

## 🚀 Deployment

- Containerized via `Dockerfile` using `uv`
- Expose the app at your domain (e.g., `https://datagen.lisekarimi.com`)
- Docs served at `https://datagen.lisekarimi.com/docs`

## 🛠️ Troubleshooting

- Docs 404: ensure `main.py` mounts `/docs` and the `docs/` folder is present in the container
- Missing styles/icons: check CDN access (corporate proxies/ad-blockers can block external assets)
