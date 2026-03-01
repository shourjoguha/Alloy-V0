#!/bin/bash

# Hyrox Workouts Scraper - Quick Start Script
# This script handles dependency installation and runs the scraper

set -e  # Exit on error

echo "=========================================="
echo "Hyrox Workouts Scraper - Quick Start"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.12+
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)"; then
    echo "ERROR: Python 3.12 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi

echo "✓ Python version OK"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Install Playwright browsers
echo "Installing Playwright Chromium..."
playwright install chromium
echo "✓ Playwright Chromium installed"
echo ""

# Check if we want to run validation too
if [ "$1" == "--with-validation" ] || [ "$1" == "-v" ]; then
    VALIDATE=true
else
    VALIDATE=false
fi

# Run scraper
echo "=========================================="
echo "Running Hyrox Scraper..."
echo "=========================================="
echo ""

python3 scripts/hyrox_scraper_comprehensive.py

SCRAPER_EXIT_CODE=$?

if [ $SCRAPER_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Scraper completed successfully!"
    echo "=========================================="
    
    # Find the most recent output file
    LATEST_JSON=$(ls -t hyrox_workouts_scraped_*.json 2>/dev/null | head -1)
    
    if [ -n "$LATEST_JSON" ]; then
        echo ""
        echo "Latest output file: $LATEST_JSON"
        
        # Run validation if requested
        if [ "$VALIDATE" = true ]; then
            echo ""
            echo "=========================================="
            echo "Running Validation..."
            echo "=========================================="
            echo ""
            
            REPORT_FILE="validation_report_$(date +%Y%m%d_%H%M%S).txt"
            python3 scripts/validate_hyrox_scraper.py "$LATEST_JSON" "$REPORT_FILE"
            
            echo ""
            echo "✓ Validation report saved to: $REPORT_FILE"
        fi
    else
        echo "WARNING: No output JSON file found"
    fi
else
    echo ""
    echo "=========================================="
    echo "✗ Scraper failed with exit code $SCRAPER_EXIT_CODE"
    echo "=========================================="
    echo ""
    echo "Check log files in logs/ directory for details"
fi

echo ""
echo "Done!"
