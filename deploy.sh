#!/bin/bash

echo "📄 PDF Compressor - GitHub Setup"
echo "================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first:"
    echo "   brew install git"
    exit 1
fi

# Get GitHub username
echo "Enter your GitHub username:"
read github_username

if [ -z "$github_username" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

echo ""
echo "🔧 Setting up git repository..."
git init
git add .
git commit -m "Initial commit - PDF Compressor"

echo ""
echo "🔗 Connecting to GitHub..."
git remote add origin https://github.com/$github_username/pdf-compressor.git
git branch -M main

echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Done! Your code is on GitHub"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://render.com"
echo "2. Sign up with your GitHub account"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select 'pdf-compressor' repository"
echo "5. Click 'Create Web Service'"
echo ""
echo "Your team will be able to access it at:"
echo "https://pdf-compressor-xxxx.onrender.com"
echo ""
