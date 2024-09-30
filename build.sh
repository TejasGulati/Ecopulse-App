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

# Ensure the ai_models directory is in the correct location
echo "Ensuring ai_models is in the correct location..."
if [ ! -d "backend/ai_models" ]; then
    echo "Moving ai_models to the correct location..."
    mv backend/GenAIRevolution/ai_models backend/
fi

echo "Build process completed successfully!"