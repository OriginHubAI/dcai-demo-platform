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

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Copy and install backend dependencies
COPY backend/requirements.txt /tmp/backend-requirements.txt
RUN pip install --no-cache-dir -r /tmp/backend-requirements.txt

# Copy and install dataflow-webui dependencies
COPY dataflow-webui/backend/requirements.txt /tmp/dataflow-requirements.txt
RUN pip install --no-cache-dir -r /tmp/dataflow-requirements.txt

# Install claude-code CLI
RUN pip install --no-cache-dir claude-code

# Copy and install frontend dependencies
COPY package.json package-lock.json* /tmp/dcai-frontend/
WORKDIR /tmp/dcai-frontend
RUN npm install

# Copy and install dataflow-webui frontend dependencies
COPY dataflow-webui/frontend/package.json dataflow-webui/frontend/package-lock.json* /tmp/dataflow-frontend/
WORKDIR /tmp/dataflow-frontend
RUN npm install

# Reset working directory
WORKDIR /workspace

# Keep the container running
CMD ["/bin/bash"]
