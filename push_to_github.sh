#!/bin/bash

echo "════════════════════════════════════════════════════════"
echo "📤 GITHUB PUSH HELPER SCRIPT"
echo "════════════════════════════════════════════════════════"
echo ""

# Check if GitHub username is provided
if [ -z "$1" ]; then
    echo "❌ ERROR: Please provide your GitHub username"
    echo ""
    echo "Usage:"
    echo "  ./push_to_github.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "Example:"
    echo "  ./push_to_github.sh petroivanovich"
    echo ""
    exit 1
fi

GITHUB_USERNAME="$1"
REPO_NAME="difficult-conversations"

echo "📋 Configuration:"
echo "  GitHub Username: $GITHUB_USERNAME"
echo "  Repository Name: $REPO_NAME"
echo ""
echo "⚠️  BEFORE RUNNING THIS SCRIPT:"
echo "  1. Go to https://github.com/new"
echo "  2. Create a repository named: $REPO_NAME"
echo "  3. DO NOT initialize with README"
echo ""
read -p "Have you created the GitHub repository? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please create the repository first, then run this script again."
    exit 1
fi

echo ""
echo "🔗 Adding GitHub remote..."
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git" 2>/dev/null || {
    echo "Remote 'origin' already exists. Updating URL..."
    git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
}

echo "🌿 Switching to main branch..."
git branch -M main

echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "════════════════════════════════════════════════════════"
    echo "✅ SUCCESS! Code pushed to GitHub"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo "🔗 Your repository:"
    echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo ""
    echo "🚀 Next: Deploy to Render.com"
    echo "   1. Visit: https://dashboard.render.com/"
    echo "   2. Click: New + → Web Service"
    echo "   3. Connect: github.com/$GITHUB_USERNAME/$REPO_NAME"
    echo "   4. Add env: OPENAI_API_KEY = sk-..."
    echo "   5. Deploy!"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "  • Repository doesn't exist on GitHub"
    echo "  • Authentication required (enter username/password or token)"
    echo "  • Network connection issue"
    echo ""
fi
