#!/bin/bash

# Build and deployment script for the interview agents
# This script handles all the setup and deployment

set -e  # Exit on any error

echo "🚀 Starting build and deployment process..."

# Get directories
DEPLOYMENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$DEPLOYMENT_DIR")"
INTERVIEW_AGENTS_DIR="$PROJECT_ROOT/interview-agents"
LOCAL_COPY_DIR="$DEPLOYMENT_DIR/interview-agents-local"

# Step 1: Install interview-agents package
echo ""
echo "📦 Step 1: Installing interview-agents package..."
cd "$INTERVIEW_AGENTS_DIR"
poetry install
echo "✅ Successfully installed interview-agents dependencies"

# Step 2: Copy interview-agents to local directory
echo ""
echo "📁 Step 2: Copying interview-agents to local directory..."
cd "$DEPLOYMENT_DIR"

# Remove existing local copy if it exists
if [ -d "$LOCAL_COPY_DIR" ]; then
    rm -rf "$LOCAL_COPY_DIR"
fi

# Copy the interview-agents directory, excluding .git and other unnecessary files
rsync -av --exclude='.git' --exclude='.venv' --exclude='__pycache__' --exclude='*.pyc' --exclude='.gitignore' --exclude='poetry.lock' "$INTERVIEW_AGENTS_DIR/" "$LOCAL_COPY_DIR/"
echo "✅ Successfully copied interview-agents to local directory"

# Step 3: Update the deployment configuration
echo ""
echo "🔧 Step 3: Updating deployment configuration..."

# Update remote.py to use local copy
sed -i 's|"/home/amineh/WorkSpace/interview-platform/interview-agents"|"./interview-agents-local"|g' remote.py

# Remove the interview-agents dependency from pyproject.toml
sed -i '/interview-agents = {path = "..\/interview-agents", develop = true}/d' pyproject.toml

echo "✅ Successfully updated deployment configuration"

# Step 4: Install deployment dependencies
echo ""
echo "📦 Step 4: Installing deployment dependencies..."
poetry install
echo "✅ Successfully installed deployment dependencies"

# Step 5: Run the deployment
echo ""
echo "🚀 Step 5: Running deployment..."
poetry run python remote.py --create
echo "✅ Deployment completed successfully!"

echo ""
echo "🎉 Build and deployment process completed successfully!"
