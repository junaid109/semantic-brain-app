FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for build
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (optional for build phase, but needed if we want to compile core inside container)
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# ENV PATH="/root/.cargo/bin:${PATH}"

COPY pyproject.toml .
RUN pip install .

COPY . .

# Note: We use the bridge.py fallback if Rust isn't compiled.
# If you want to compile Rust, you'd run 'maturin develop' here.

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
