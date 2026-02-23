#!/bin/bash

# Startup Script - SportBooking Platform
# Usage: ./startup.sh or ./startup.sh dev/prod

ENVIRONMENT=${1:-dev}

echo "🚀 SportBooking Platform Startup Script"
echo "Environment: $ENVIRONMENT"
echo ""

if [ "$ENVIRONMENT" = "dev" ]; then
    echo "📦 Installing dependencies..."
    
    # Backend
    cd backend
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py initialize_data
    
    # Frontend
    cd ../frontend
    npm install
    
    echo ""
    echo "✅ Dependencies installed!"
    echo ""
    echo "🎯 Starting development servers..."
    echo ""
    echo "Backend:  http://localhost:8000"
    echo "Frontend: http://localhost:3000"
    echo "API Docs: http://localhost:8000/api/schema/swagger/"
    echo ""
    
    # Terminal 1: Backend
    cd ../backend
    python manage.py runserver 0.0.0.0:8000 &
    BACKEND_PID=$!
    
    # Terminal 2: Frontend
    cd ../frontend
    npm start &
    FRONTEND_PID=$!
    
    echo "Ctrl+C to stop both servers"
    wait
    
elif [ "$ENVIRONMENT" = "prod" ]; then
    echo "🐳 Starting production with Docker..."
    
    # Build and start
    docker-compose -f docker-compose.prod.yml build
    docker-compose -f docker-compose.prod.yml up -d
    
    echo "✅ Production started!"
    echo ""
    echo "Services:"
    docker-compose -f docker-compose.prod.yml ps
    
elif [ "$ENVIRONMENT" = "docker" ]; then
    echo "🐳 Starting with Docker Compose (dev)..."
    docker-compose up
    
else
    echo "Usage: $0 [dev|prod|docker]"
    echo ""
    echo "Options:"
    echo "  dev    - Start development servers"
    echo "  prod   - Start production with Docker"
    echo "  docker - Start with Docker Compose"
    exit 1
fi
