#!/bin/bash
set -e

echo "🔧 Installing dependencies..."
pip install --upgrade pip setuptools wheel

echo "📦 Installing requirements..."
pip install --no-cache-dir -r requirements.txt

echo "🗄️ Running database migrations..."
alembic upgrade head

echo "✅ Build completed successfully!"