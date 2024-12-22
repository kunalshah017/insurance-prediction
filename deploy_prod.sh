#!/bin/bash

echo "🚀 Starting deployment..."

# Error handling
set -e

# Navigate to client directory and install dependencies
echo "📦 Installing client dependencies..."
cd client || exit
npm install
npm install vite @vitejs/plugin-react --save-dev

# Build the client application
echo "🛠️ Building client application..."
npm run build

# Navigate back to root
cd ..

# Start the server
echo "🚀 Starting production server..."
python wsgi.py