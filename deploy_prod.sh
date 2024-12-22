#!/bin/bash

echo "🚀 Starting deployment..."

# Error handling
set -e

# Navigate to client directory and install dependencies
echo "📦 Installing client dependencies..."
cd client || exit
npm install

# Build the client application using npx
echo "🛠️ Building client application..."
npx vite build

# Navigate back to root
cd ..

# Start the server
echo "🚀 Starting production server..."
python wsgi.py