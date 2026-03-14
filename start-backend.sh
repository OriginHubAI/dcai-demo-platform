#!/bin/bash
set -e

echo "🚀 Starting DCAI Platform Backend with DataFlow-WebUI..."

# Build DataFlow-WebUI frontend
if [ -d "dataflow-webui/frontend" ]; then
    echo "📦 Building DataFlow-WebUI frontend..."
    cd dataflow-webui/frontend

    # Install dependencies if node_modules doesn't exist
    if [ ! -d "node_modules" ]; then
        echo "📥 Installing frontend dependencies..."
        npm install
    fi

    npx vite build --mode embedded
    cd ../..
    echo "✅ DataFlow-WebUI frontend built successfully"
else
    echo "⚠️  Warning: dataflow-webui/frontend not found, skipping build"
fi

# Start ASGI server
echo "🌐 Starting ASGI server on port 18000..."
cd backend
uvicorn core.asgi:application --host 0.0.0.0 --port 18000 --reload
