#!/bin/bash

# Script de démarrage du projet

echo "🚀 Démarrage de SportBooking..."

# Backend
echo "📦 Démarrage du backend..."
cd backend
python -m venv venv

# Activation du venv selon l'OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

pip install -r requirements.txt
python manage.py migrate
python manage.py initialize_data
python manage.py runserver 0.0.0.0:8000 &

BACKEND_PID=$!

# Frontend
echo "📱 Démarrage du frontend..."
cd ../frontend
npm install
npm start &

FRONTEND_PID=$!

echo "✅ Applications démarrées!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API docs: http://localhost:8000/api/docs/"

# Garder les processus actifs
wait
