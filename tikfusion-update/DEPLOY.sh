#!/bin/bash
# === TikFusion Deploy Script ===
# Run this in your tikfusion-mvp Codespace or local clone:
#   bash DEPLOY.sh
#
# It will copy app.py to the right place and push to main.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if we're in tikfusion-mvp
if [ -f "app.py" ] && [ -d "src" ]; then
    REPO_DIR="."
elif [ -f "../app.py" ] && [ -d "../src" ]; then
    REPO_DIR=".."
else
    echo "Run this script from inside your tikfusion-mvp repo!"
    exit 1
fi

cd "$REPO_DIR"

echo "Copying updated app.py..."
cp "$SCRIPT_DIR/app.py" ./app.py

echo "Copying updated requirements.txt..."
cp "$SCRIPT_DIR/requirements.txt" ./requirements.txt

# Remove postbridge if it still exists
if [ -f "src/postbridge.py" ]; then
    echo "Removing src/postbridge.py..."
    rm src/postbridge.py
fi

echo "Committing changes..."
git add app.py requirements.txt
git add -u src/postbridge.py 2>/dev/null || true
git commit -m "Design compact + suppression Publier tab + rename tabs"

echo "Pushing to main..."
git push origin main

echo ""
echo "Done! Streamlit Cloud will auto-deploy in ~1 minute."
echo "Check: https://tikfusion.streamlit.app"
