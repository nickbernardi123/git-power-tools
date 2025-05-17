#!/bin/bash

# sgit-demo.sh - Demo script to show the power of sgit
# Author: Nick B
# Date: May 17, 2025

# Set text colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

clear

# Print banner
echo -e "${BLUE}${BOLD}"
echo "  _____                           _____  _  _     _____                       "
echo " / ____|                         / ____|(_)| |   |  __ \                      "
echo "| (___   _   _  _ __    ___  _ _| |  __  _ | |_  | |  | |  ___  _ __ ___   ___  "
echo " \___ \ | | | || '_ \  / _ \| '__| | |_ || || __| | |  | | / _ \| '_ \` _ \ / _ \ "
echo " ____) || |_| || |_) ||  __/| |  | |__| || || |_  | |__| ||  __/| | | | | | (_) |"
echo "|_____/  \__,_|| .__/  \___||_|   \_____||_| \__| |_____/  \___||_| |_| |_|\___/ "
echo "               | |                                                           "
echo "               |_|                                                           "
echo -e "${NC}"

echo -e "${YELLOW}This demo will show you the power of Super Git (sgit).${NC}"
echo

# Check if sgit is available
if ! command -v sgit &>/dev/null; then
    echo -e "${RED}sgit command not found. Please make sure it's installed and in your PATH.${NC}"
    exit 1
fi

# Create a temporary directory for the demo
echo -e "${BLUE}${BOLD}Step 1: Creating demo repositories...${NC}"
DEMO_DIR=$(mktemp -d)
cd "$DEMO_DIR" || exit 1
echo -e "${GREEN}Created demo directory: $DEMO_DIR${NC}"
echo

# Create some test repositories
create_repo() {
    local name=$1
    mkdir -p "$name"
    cd "$name" || return
    git init > /dev/null 2>&1
    echo "# $name Repository" > README.md
    git add README.md
    git commit -m "Initial commit" > /dev/null 2>&1
    cd ..
}

create_repo "project-a"
create_repo "project-b"
create_repo "project-c"
mkdir -p "not-a-repo"
echo "This is not a git repository" > "not-a-repo/file.txt"

echo -e "${GREEN}Created 3 git repositories and 1 regular directory.${NC}"
echo

# Basic sgit demo
echo -e "${BLUE}${BOLD}Step 2: Basic sgit status command...${NC}"
echo -e "${YELLOW}Running: sgit status${NC}"
echo
sgit status
echo

# Quiet mode demo
echo -e "${BLUE}${BOLD}Step 3: Quiet mode for minimal output...${NC}"
echo -e "${YELLOW}Running: sgit -q status${NC}"
echo
sgit -q status
echo

# Make changes to repositories
echo -e "${BLUE}${BOLD}Step 4: Making changes to repositories...${NC}"
echo "Added feature" >> project-a/feature.txt
cd project-b && git checkout -b new-feature > /dev/null 2>&1 && echo "New feature" > feature.txt && cd ..
echo

# Show changes with sgit
echo -e "${BLUE}${BOLD}Step 5: Showing changes across all repositories...${NC}"
echo -e "${YELLOW}Running: sgit status${NC}"
echo
sgit status
echo

# Add changes with sgit
echo -e "${BLUE}${BOLD}Step 6: Adding all changes with one command...${NC}"
echo -e "${YELLOW}Running: sgit add .${NC}"
echo
sgit add .
echo

# Interactive mode demo
echo -e "${BLUE}${BOLD}Step 7: Using interactive mode to select repositories...${NC}"
echo -e "${YELLOW}Running: sgit -s status${NC}"
echo -e "${YELLOW}(Select repositories when prompted)${NC}"
echo
sgit -s status
echo

# Clean up
echo -e "${BLUE}${BOLD}Step 8: Cleaning up demo...${NC}"
cd /tmp || exit
rm -rf "$DEMO_DIR"
echo -e "${GREEN}Demo files cleaned up.${NC}"
echo

echo -e "${BLUE}${BOLD}Demo complete!${NC}"
echo -e "${YELLOW}Now you can use sgit in your own projects.${NC}"
echo
echo -e "${GREEN}Try these commands:${NC}"
echo "  sgit status                  - Check status of all repos"
echo "  sgit -r status               - Check status recursively"
echo "  sgit -p pull                 - Pull all repos in parallel"
echo "  sgit -s checkout -b feature  - Create feature branch in selected repos"
echo
echo -e "${GREEN}For more information:${NC}"
echo "  sgit --help"
echo
