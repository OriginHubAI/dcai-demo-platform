#!/bin/bash
set -e

LOG_FILE="backend.log"
MAX_SIZE=10485760  # 10MB in bytes

# Log rotation function
rotate_log() {
    if [ -f "$LOG_FILE" ]; then
        SIZE=$(wc -c < "$LOG_FILE")
        if [ "$SIZE" -gt "$MAX_SIZE" ]; then
            echo "🔄 Rotating log file (size: $SIZE bytes)"
            mv "$LOG_FILE" "${LOG_FILE}.old"
        fi
    fi
}

# Rotate log if needed
rotate_log

echo "🚀 Starting DCAI Platform Backend with DataFlow-WebUI..."
echo "📝 Logging to $LOG_FILE (max size: 10MB)"

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
script -q -f -c "uvicorn core.asgi:application --host 0.0.0.0 --port 18000 --reload" /dev/null 2>&1 | tee /dev/tty | sed -u 's/\x1b\[[0-9;]*[a-zA-Z]//g' >> "../$LOG_FILE"
