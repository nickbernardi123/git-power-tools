#!/bin/bash
# git-helper-demo.sh - Demonstrates the Git Helper Tool

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}
  ____ _ _       _   _      _                  
 / ___(_) |_    | | | | ___| |_ __   ___ _ __ 
| |  _| | __|   | |_| |/ _ \ | '_ \ / _ \ '__|
| |_| | | |_    |  _  |  __/ | |_) |  __/ |   
 \____|_|\__|___|_| |_|\___|_| .__/ \___|_|   
           |_____|           |_|              
${NC}"
echo -e "${YELLOW}Git Helper Tool Demo${NC}\n"

echo -e "${GREEN}This script demonstrates the two versions of the Git Helper Tool:${NC}"
echo -e "1. ${YELLOW}Enhanced Git Helper${NC} - Streamlined for branch and commit management"
echo -e "2. ${YELLOW}Original Git Helper${NC} - Full-featured with additional tools\n"

# Display feature comparison
echo -e "${BLUE}Enhanced Git Helper Features:${NC}"
echo "• Branch Management with automatic pull"
echo "• Smart upstream tracking for pushes"
echo "• Interactive commit staging and amending"
echo "• Simplified user interface for common tasks"
echo ""

echo -e "${BLUE}Original Git Helper Features:${NC}"
echo "• All branch and commit management features"
echo "• Team collaboration tools"
echo "• Advanced rebasing and cherry-picking"
echo "• Stash management and more"
echo ""

# Explain usage
echo -e "${GREEN}How to use:${NC}"
echo -e "Run either version with Python:\n"
echo -e "${YELLOW}# Run the enhanced version (recommended)${NC}"
echo -e "python git_helpers_enhanced.py"
echo ""
echo -e "${YELLOW}# Run the original full-featured version${NC}"
echo -e "python git_helpers.py"
echo ""

echo -e "${GREEN}Requirements:${NC}"
echo -e "Both versions require Python 3.7+ and the colorama package."
echo -e "Install with: pip install colorama"
echo ""

# Ask which version to run
echo -e "${BLUE}Would you like to run a demo now?${NC}"
echo "1. Run Enhanced Git Helper"
echo "2. Run Original Git Helper"
echo "3. Exit Demo"

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo -e "${YELLOW}Starting Enhanced Git Helper...${NC}"
        python "$(dirname "$0")/git_helpers_enhanced.py"
        ;;
    2)
        echo -e "${YELLOW}Starting Original Git Helper...${NC}"
        python "$(dirname "$0")/git_helpers.py"
        ;;
    *)
        echo -e "${GREEN}Demo completed. You can run either tool using the commands shown above.${NC}"
        ;;
esac
