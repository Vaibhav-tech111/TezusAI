#!/bin/bash

echo "🔧 Setting up Tezus environment..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create .env file if missing
if [ ! -f .env ]; then
  echo "Creating .env file..."
  cat <<EOT >> .env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
ANTHROPIC_API_KEY=your_claude_key
EOT
fi

echo "✅ Environment setup complete."
