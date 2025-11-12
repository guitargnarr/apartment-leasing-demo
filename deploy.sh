#!/bin/bash

# LeaseFlow Quick Deploy Script
# This script helps you deploy LeaseFlow to production

set -e  # Exit on error

echo "🏢 LeaseFlow Deployment Helper"
echo "================================"
echo ""

# Check if user has deployment CLI tools installed
echo "Checking for deployment tools..."
echo ""

# Function to check and install tools
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 not found"
        return 1
    else
        echo "✅ $1 found"
        return 0
    fi
}

# Check for tools
HAS_VERCEL=false
HAS_NETLIFY=false

if check_tool vercel; then
    HAS_VERCEL=true
fi

if check_tool netlify; then
    HAS_NETLIFY=true
fi

echo ""
echo "================================"
echo "Choose deployment method:"
echo "1. Deploy Frontend to Vercel (requires Vercel CLI)"
echo "2. Deploy Frontend to Netlify (requires Netlify CLI)"
echo "3. Open GitHub for manual deployment"
echo "4. Show deployment instructions"
echo "5. Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        if [ "$HAS_VERCEL" = false ]; then
            echo "Installing Vercel CLI..."
            npm install -g vercel
        fi
        echo "Deploying to Vercel..."
        cd frontend
        vercel --prod
        ;;
    2)
        if [ "$HAS_NETLIFY" = false ]; then
            echo "Installing Netlify CLI..."
            npm install -g netlify-cli
        fi
        echo "Deploying to Netlify..."
        cd frontend
        netlify deploy --prod
        ;;
    3)
        echo "Opening GitHub repository..."
        echo "Go to Settings → Pages or connect to Vercel/Netlify/Render"
        if command -v open &> /dev/null; then
            open "https://github.com/guitargnarr/apartment-leasing-demo"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "https://github.com/guitargnarr/apartment-leasing-demo"
        fi
        ;;
    4)
        cat DEPLOYMENT.md
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "Next steps:"
echo "1. Deploy backend to Render.com: https://render.com"
echo "2. Update VITE_API_URL in frontend environment"
echo "3. Run load_seed_data.py on your backend"
echo ""
echo "See DEPLOYMENT.md for detailed instructions"
