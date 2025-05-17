#!/bin/bash
# setup.sh - Setup script for Git Helper Tool
# Installs git-helper and makes it available from anywhere

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "  ____ _ _       _   _      _                  "
echo " / ___(_) |_    | | | | ___| |_ __   ___ _ __ "
echo "| |  _| | __|   | |_| |/ _ \ | '_ \ / _ \ '__|"
echo "| |_| | | |_    |  _  |  __/ | |_) |  __/ |   "
echo " \____|_|\__|___|_| |_|\___|_| .__/ \___|_|   "
echo "           |_____|           |_|              "
echo -e "${NC}"

echo -e "${YELLOW}Setting up Git Helper Tool...${NC}"
echo

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if we're on Linux or macOS
if [[ "$(uname)" == "Darwin" ]]; then
  INSTALL_DIR="/usr/local/bin"
  echo -e "${YELLOW}Detected macOS${NC}"
elif [[ "$(uname)" == "Linux" ]]; then
  INSTALL_DIR="/usr/local/bin"
  echo -e "${YELLOW}Detected Linux${NC}"
else
  echo -e "${RED}Unsupported operating system. Please use Windows setup or install manually.${NC}"
  exit 1
fi

# Check for Python
if ! command -v python &>/dev/null && ! command -v python3 &>/dev/null; then
  echo -e "${RED}Error: Python is not installed. Please install Python 3.7+ and try again.${NC}"
  exit 1
fi

# Try to determine Python command (python or python3)
PYTHON_CMD="python"
if ! command -v python &>/dev/null && command -v python3 &>/dev/null; then
  PYTHON_CMD="python3"
fi

# Install colorama if not already installed
echo -e "${YELLOW}Checking for required Python packages...${NC}"
$PYTHON_CMD -c "import colorama" 2>/dev/null || {
  echo -e "${YELLOW}Installing colorama package...${NC}"
  pip install colorama || pip3 install colorama || {
    echo -e "${RED}Failed to install colorama. Please run: pip install colorama${NC}"
    exit 1
  }
  echo -e "${GREEN}Colorama installed successfully.${NC}"
}

# Check if user has permissions to write to install directory
if [ ! -w "$INSTALL_DIR" ]; then
  echo -e "${YELLOW}Insufficient permissions to write to $INSTALL_DIR${NC}"
  echo -e "${YELLOW}Running with sudo...${NC}"
  sudo_required=true
else
  sudo_required=false
fi

# Create a launcher script
echo -e "${YELLOW}Creating launcher script...${NC}"
LAUNCHER_CONTENT="#!/bin/bash
# Git Helper Tool Launcher
$PYTHON_CMD \"$SCRIPT_DIR/git_helpers_enhanced.py\" \"\$@\"
"

if [[ "$sudo_required" == true ]]; then
  echo "$LAUNCHER_CONTENT" | sudo tee "$INSTALL_DIR/git-helper" > /dev/null
  sudo chmod +x "$INSTALL_DIR/git-helper"
else
  echo "$LAUNCHER_CONTENT" > "$INSTALL_DIR/git-helper"
  chmod +x "$INSTALL_DIR/git-helper"
fi

if [ $? -eq 0 ]; then
  echo -e "${GREEN}Git Helper Tool has been successfully installed!${NC}"
  echo
  echo -e "${YELLOW}You can now use git-helper from any directory:${NC}"
  echo -e "  ${BLUE}git-helper${NC} - Run the enhanced Git Helper Tool"
  echo
else
  echo
  echo -e "${RED}Installation might have failed. Please check if $INSTALL_DIR is in your PATH.${NC}"
  echo
  echo -e "${YELLOW}You can manually add git-helper to your PATH:${NC}"
  echo -e "  export PATH=\"\$PATH:$SCRIPT_DIR\""
  echo
fi

exit 0
