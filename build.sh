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

echo "Build process completed successfully!"