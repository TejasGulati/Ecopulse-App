#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting build process..."

# Backend setup
echo "Setting up backend..."
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
cd ..

# Frontend setup
echo "Setting up frontend..."
cd frontend/ai-business-solutions
npm install
npm run build
cd ../..

# Copy frontend build to Django static files
echo "Copying frontend build to Django static files..."
mkdir -p backend/staticfiles/
cp -R frontend/ai-business-solutions/build/* backend/staticfiles/

# Ensure the .env file is in the correct location
echo "Checking .env file..."
ENV_FILE="/Users/tejasgulati/Desktop/untitled folder 3/EcoPulse/.env"
if [ -f "$ENV_FILE" ]; then
    cp "$ENV_FILE" backend/.env
    echo ".env file copied to backend directory"
else
    echo "Error: .env file not found at $ENV_FILE"
    exit 1
fi

echo "Build process completed successfully!"