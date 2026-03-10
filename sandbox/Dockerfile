FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    curl \
    vim \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 22 (for Gemini CLI)
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g @google/gemini-cli && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /workspace

# Copy and install backend dependencies if available
# Note: we use /tmp to avoid copying the whole context during build if possible, 
# but for a simple sandbox, we can just copy them.
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Keep the container running
CMD ["/bin/bash"]
