FROM python:3.11-slim

# Install uv
RUN pip install uv

WORKDIR /app

# Copy dependency files first (changes rarely)
COPY pyproject.toml uv.lock ./

# Put venv outside of /app so it won't be affected by volume mounts
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

# Install dependencies (this will now create venv at /opt/venv)
RUN uv sync --locked

# Copy all source code
COPY . .

# Create output directory with proper permissions
RUN mkdir -p /tmp/output && chmod 777 /tmp/output

# Set output directory environment variable for production
ENV OUTPUT_DIR=/tmp/output

# Disable UV cache entirely for production
ENV UV_NO_CACHE=1

CMD ["uv", "run", "main.py"]