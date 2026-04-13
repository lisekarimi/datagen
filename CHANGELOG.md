## 🏷️ [0.3.0]

### ✨ Added
- `docs/index.html` landing page for GitHub Pages

### 🚀 Deployment
- App deployed on Hugging Face Spaces for demo
- Landing page and docs deployed on GitHub Pages

### 🔄 Changed
- Removed Claude model support — OpenAI only


## 🏷️ [0.2.0]

### ✨ Added
- Documentation support using Docsify accessible at `/docs/` endpoint
- FastAPI integration to serve static documentation files
- Custom FastAPI app wrapper to handle both Gradio UI and documentation
- Redirect from `/docs` to `/docs/` for better URL handling
- ChatBot widget integration for enhanced user interaction

### 🔄 Changed
- Migrated from `demo.launch()` to custom FastAPI app with `gr.mount_gradio_app()`
- Moved FastAPI Swagger UI from `/docs` to `/api-docs` to avoid conflicts
- Updated application architecture to support static file serving

### ✅ Fixed
- Resolved routing conflicts between Gradio and static documentation
- Fixed double slash issue in root URL by using empty string for Gradio mount path
- Corrected trailing slash handling for documentation endpoint

### ⚙️ Technical
- Updated to use Gradio 5.31.0's mounting API
- Added `uvicorn` as runtime server
- Documentation files now properly served from `/app/docs` in Docker container


## 🏷️ [0.1.0]

### ✨ Added
- Generate realistic synthetic datasets from natural language prompts
- Support for two LLMs: GPT-4o-mini and Claude 3.5 Sonnet
- Multiple output formats: JSON, CSV, Parquet, and Markdown
- Downloadable files ready for immediate use
- Gradio UI with dark/light mode support and clean, user-friendly layout
- Few-shot prompt engineering for improved LLM guidance
- Customizable parameters for dataset type, output format, model selection, and sample size
