#!/bin/bash

# 🚀 IntelliVest AI - Quick Deploy Script
# ========================================

echo "🚀 IntelliVest AI - Quick Deploy to Render"
echo "=========================================="

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please navigate to your project directory."
    exit 1
fi

# Check if we have uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Please commit them first:"
    git status --short
    echo ""
    echo "Run these commands:"
    echo "  git add ."
    echo "  git commit -m 'Prepare for deployment'"
    echo "  git push"
    exit 1
fi

# Check if we have a remote origin
if ! git remote get-url origin &> /dev/null; then
    echo "❌ No remote origin found. Please add your GitHub repository:"
    echo "  git remote add origin https://github.com/username/repository.git"
    exit 1
fi

echo "✅ Git repository is ready"
echo ""

# Show current status
echo "📊 Current Status:"
echo "  Branch: $(git branch --show-current)"
echo "  Remote: $(git remote get-url origin)"
echo "  Last commit: $(git log -1 --oneline)"
echo ""

# Check if we need to push
if [ "$(git rev-list HEAD...origin/main --count)" != "0" ]; then
    echo "🔄 Pushing changes to GitHub..."
    git push origin main
    if [ $? -eq 0 ]; then
        echo "✅ Changes pushed successfully"
    else
        echo "❌ Failed to push changes"
        exit 1
    fi
else
    echo "✅ Code is already up to date on GitHub"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. Go to https://render.com and sign in"
echo "2. Click 'New +' → 'Web Service'"
echo "3. Connect your GitHub repository"
echo "4. Configure the service:"
echo "   - Name: intellivest-ai"
echo "   - Environment: Python 3"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: streamlit run streamlit_app.py --server.port \$PORT --server.address 0.0.0.0 --server.headless true"
echo "5. Set environment variables (see DEPLOYMENT_GUIDE.md)"
echo "6. Click 'Create Web Service'"
echo ""
echo "📚 For detailed instructions, see DEPLOYMENT_GUIDE.md"
echo ""
echo "🚀 Happy Deploying!" 