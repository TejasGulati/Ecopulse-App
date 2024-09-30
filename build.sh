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
if [ -f "frontend/ai-business-solutions/.env" ]; then
    cp frontend/ai-business-solutions/.env backend/.env
    echo ".env file copied to backend directory"
else
    echo "Warning: .env file not found in frontend/ai-business-solutions/"
fi

echo "Build process completed successfully!"