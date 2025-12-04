#!/bin/bash

# Global Digital Skills Gap Navigator - Quick Start Script

echo "================================================================================"
echo "  GLOBAL DIGITAL SKILLS GAP NAVIGATOR - QUICK START"
echo "================================================================================"
echo ""

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if data integration has been run
if [ ! -f "../../data/skills_gap_navigator/data/integrated_dataset.csv" ]; then
    echo -e "${YELLOW}⚠ Data integration not completed. Running now...${NC}"
    cd data
    python3 data_integration.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Data integration failed. Please check errors above.${NC}"
        exit 1
    fi
    cd ..
    echo -e "${GREEN}✓ Data integration complete${NC}"
    echo ""
fi

# Check if model has been trained
if [ ! -f "visualizations/data/feature_importance.json" ]; then
    echo -e "${YELLOW}⚠ Model not trained yet. Running training now...${NC}"
    cd models
    python3 ebm_model.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Model training failed. Please check errors above.${NC}"
        exit 1
    fi
    cd ..
    echo -e "${GREEN}✓ Model training complete${NC}"
    echo ""
fi

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠ Flask not installed. Installing dependencies...${NC}"
    pip3 install -r requirements.txt
    echo ""
fi

# Start the server
echo -e "${CYAN}================================================================================${NC}"
echo -e "${GREEN}✓ All prerequisites met!${NC}"
echo -e "${CYAN}================================================================================${NC}"
echo ""
echo -e "${CYAN}🚀 Starting web server...${NC}"
echo ""
echo -e "${GREEN}👉 Open your browser to: ${CYAN}http://localhost:5001${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""
echo -e "${CYAN}================================================================================${NC}"
echo ""

python3 app.py
