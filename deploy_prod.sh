#!/bin/bash

#!/bin/bash

echo "🚀 Starting deployment..."

# Navigate to client directory and install dependencies
echo "📦 Installing client dependencies..."
cd client
npm install

# Build the client application
echo "🛠️ Building client application..."
npm run build

# Navigate back to root
cd ..

# Start the server
echo "🚀 Starting production server..."
python wsgi.py