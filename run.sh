#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting build process..."

# Backend setup
echo "Setting up backend..."
cd backend
pip install -r requirements.txt
python manage.py migrate
cd ..

# Frontend setup
echo "Setting up frontend..."
cd frontend/ai-business-solutions
npm install
npm run build
cd ../..

# Copy frontend build to Django static directory
echo "Copying frontend build to Django static directory..."
mkdir -p backend/static/
cp -R frontend/ai-business-solutions/build/* backend/static/

# Collect static files
echo "Collecting static files..."
cd backend
python manage.py collectstatic --noinput
cd ..

echo "Build process completed successfully!"