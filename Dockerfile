FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/
COPY tests/ ./tests/
COPY .githooks/ ./.githooks/
COPY install-hooks.sh ./

# Install dependencies
RUN uv sync --all-extras

# Configure git for testing
RUN git config --global user.email "test@example.com" && \
    git config --global user.name "Test User" && \
    git config --global init.defaultBranch main

CMD ["bash"]

