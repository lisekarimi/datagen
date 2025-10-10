---
title: DataGen
emoji: 🧬
colorFrom: indigo
colorTo: pink
sdk: docker
short_description: AI-powered synthetic data generator
---

# 🧬 DataGen: AI-Powered Synthetic Data Generator

Generate realistic synthetic datasets by simply describing what you need.

[🚀 **Try the Live Demo**](https://datagen.lisekarimi.com)

<img src="https://github.com/lisekarimi/datagen/blob/main/assets/screenshot.png?raw=true" alt="DataGen interface" width="450">

## ✨ What DataGen Does

DataGen transforms simple descriptions into structured datasets using AI. Perfect for researchers, data scientists, and developers who need realistic test data fast.

**Key Features:**
- **Type what you want → Get real data**
- **Multiple formats:** CSV, JSON, Parquet, Markdown
- **Dataset types:** Tables, time-series, text data
- **AI-powered:** Uses GPT and Claude models
- **Instant download** with clean, ready-to-use datasets

To understand the full workflow from user input to file output, see the [architecture section](https://datagen.lisekarimi.com/docs/#/archi).


## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [uv package manager](https://docs.astral.sh/uv/getting-started/installation/)

### Installation
```bash
git clone https://github.com/lisekarimi/datagen.git
cd datagen
uv sync
source .venv/bin/activate  # Unix/macOS
# or .\.venv\Scripts\activate on Windows
```

### Configuration
1. Copy `.env.example` to `.env`
2. Populate it with the required secrets

### Run DataGen
```bash
# Local development
make run

# With hot reload
make ui
```

*For complete setup instructions, commands, and development guidelines, see [the Docs Page](https://datagen.lisekarimi.com/docs).*

## 🧑‍💻 How to Use

1. **Describe your data:** "Customer purchase history with demographics"
2. **Choose format:** CSV, JSON, Parquet, or Markdown
3. **Select AI model:** GPT or Claude
4. **Set sample size:** Number of records to generate
5. **Generate & download** your dataset

## 🛡️ Quality & Security

DataGen maintains high standards with comprehensive test coverage, automated security scanning, and code quality enforcement.

*For CI/CD setup and technical details, see [the docs Page](https://datagen.lisekarimi.com/docs/#/cicd).*

## 📝 Notes
- Generated files are automatically cleaned up after 5 minutes
- Supports 10-1000 samples per dataset
- JSON output includes proper indentation for readability
- Cross-platform compatibility (Windows, macOS, Linux)

## 📄 License

MIT
