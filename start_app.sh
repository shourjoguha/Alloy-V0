#!/bin/bash
# Alloy Dev Startup Script
# Runs both backend (FastAPI) and frontend (Vite) concurrently

set -o pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root (script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# PID tracking for cleanup
BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo -e "\n${YELLOW}Shutting down services...${NC}"
    
    if [[ -n "$FRONTEND_PID" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo -e "${BLUE}Stopping frontend (PID: $FRONTEND_PID)${NC}"
        kill "$FRONTEND_PID" 2>/dev/null
        wait "$FRONTEND_PID" 2>/dev/null
    fi
    
    if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${BLUE}Stopping backend (PID: $BACKEND_PID)${NC}"
        kill "$BACKEND_PID" 2>/dev/null
        wait "$BACKEND_PID" 2>/dev/null
    fi
    
    echo -e "${GREEN}All services stopped.${NC}"
    exit 0
}

# Trap signals for clean shutdown
trap cleanup SIGINT SIGTERM EXIT

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Alloy AI Fitness - Development Mode  ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if backend dependencies are available
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo -e "${RED}Error: FastAPI not found. Please activate your virtual environment:${NC}"
    echo -e "  source .venv/bin/activate"
    exit 1
fi

# Check if frontend dependencies are installed
if [[ ! -d "frontend/node_modules" ]]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    (cd frontend && npm install) || exit 1
fi

# Start backend
echo -e "${BLUE}Starting backend on http://localhost:8000 ...${NC}"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for backend to be ready
echo -e "${YELLOW}Waiting for backend to start...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is ready${NC}"
        break
    fi
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${RED}Backend process died unexpectedly${NC}"
        exit 1
    fi
    sleep 1
done

# Check if backend started successfully
if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${RED}Backend failed to start within 30 seconds${NC}"
    exit 1
fi

# Start frontend
echo -e "${BLUE}Starting frontend on http://localhost:5173 ...${NC}"
(cd frontend && npm run dev) &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Services running:${NC}"
echo -e "${GREEN}    Backend:  http://localhost:8000${NC}"
echo -e "${GREEN}    Frontend: http://localhost:5173${NC}"
echo -e "${GREEN}    API Docs: http://localhost:8000/docs${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Wait for processes (poll both since wait -n isn't portable)
while true; do
    # Check if backend is still running
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${RED}Backend process exited unexpectedly${NC}"
        break
    fi
    # Check if frontend is still running
    if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo -e "${RED}Frontend process exited unexpectedly${NC}"
        break
    fi
    sleep 2
done

cleanup
