#!/bin/bash

echo "🚀 Starting deployment..."

# Error handling
set -e

# Install bun
echo " Installing bun..."
curl -fsSL https://bun.sh/install | bash
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# Navigate to client directory and install dependencies
echo "📦 Installing client dependencies..."
cd client || exit
bun install

# Build the client application
echo "🛠️ Building client application..."
bun run build

# Navigate back to root
cd ..

# Start the server
echo "🚀 Starting production server..."
python wsgi.py