#!/bin/bash

# setup.sh - Setup script for Super Git (sgit)
# Installs sgit and its shortcut scripts to make them available from anywhere

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;36m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "  _____                           _____  _  _   "
echo " / ____|                         / ____|(_)| |  "
echo "| (___   _   _  _ __    ___  _ _| |  __  _ | |_ "
echo " \___ \ | | | || '_ \  / _ \| '__| | |_ || || __|"
echo " ____) || |_| || |_) ||  __/| |  | |__| || || |_ "
echo "|_____/  \__,_|| .__/  \___||_|   \_____||_| \__|"
echo "               | |                               "
echo "               |_|                               "
echo -e "${NC}"

echo -e "${YELLOW}Setting up Super Git (sgit)...${NC}"
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

# Use the enhanced version if available, otherwise use standard sgit
if [ -f "$SCRIPT_DIR/sgit-enhanced" ]; then
  echo -e "${GREEN}Using enhanced sgit version${NC}"
  SGIT_SOURCE="$SCRIPT_DIR/sgit-enhanced"
else
  echo -e "${YELLOW}Using standard sgit version${NC}"
  SGIT_SOURCE="$SCRIPT_DIR/sgit"
fi

# Check if the files exist
if [ ! -f "$SGIT_SOURCE" ]; then
  echo -e "${RED}Error: sgit script not found at $SGIT_SOURCE${NC}"
  exit 1
fi

# Make files executable
chmod +x "$SGIT_SOURCE"
chmod +x "$SCRIPT_DIR/sgit-status" 2>/dev/null
chmod +x "$SCRIPT_DIR/sgit-pull" 2>/dev/null

# Check if user has permissions to write to install directory
if [ ! -w "$INSTALL_DIR" ]; then
  echo -e "${YELLOW}Insufficient permissions to write to $INSTALL_DIR${NC}"
  echo -e "${YELLOW}Running with sudo...${NC}"
  sudo_required=true
else
  sudo_required=false
fi

# Install the files
install_file() {
  local source=$1
  local dest=$2
  
  if [ -f "$source" ]; then
    if [[ "$sudo_required" == true ]]; then
      sudo cp "$source" "$dest" && sudo chmod +x "$dest"
    else
      cp "$source" "$dest" && chmod +x "$dest"
    fi
    
    if [ $? -eq 0 ]; then
      echo -e "${GREEN}Installed: $dest${NC}"
    else
      echo -e "${RED}Failed to install: $dest${NC}"
      return 1
    fi
  fi
  return 0
}

# Install sgit and shortcut scripts
install_file "$SGIT_SOURCE" "$INSTALL_DIR/sgit"
install_file "$SCRIPT_DIR/sgit-status" "$INSTALL_DIR/sgit-status"
install_file "$SCRIPT_DIR/sgit-pull" "$INSTALL_DIR/sgit-pull"
install_file "$SCRIPT_DIR/sgit-fetch" "$INSTALL_DIR/sgit-fetch"
install_file "$SCRIPT_DIR/sgit-unpushed" "$INSTALL_DIR/sgit-unpushed"

# Install shorter aliases
install_file "$SCRIPT_DIR/shorter-aliases/s-status" "$INSTALL_DIR/s-status"
install_file "$SCRIPT_DIR/shorter-aliases/s-pull" "$INSTALL_DIR/s-pull"
install_file "$SCRIPT_DIR/shorter-aliases/s-fetch" "$INSTALL_DIR/s-fetch"
install_file "$SCRIPT_DIR/shorter-aliases/s-unpushed" "$INSTALL_DIR/s-unpushed"

# Check if installation was successful
if command -v sgit &>/dev/null; then
  echo
  echo -e "${GREEN}Super Git (sgit) has been successfully installed!${NC}"
  echo
  echo -e "${YELLOW}You can now use sgit from any directory:${NC}"
  echo -e "  ${BLUE}sgit status${NC}              - Check status of all repositories"
  echo -e "  ${BLUE}sgit pull${NC}                - Pull all repositories"
  echo -e "  ${BLUE}sgit -r status${NC}           - Check status recursively"
  echo -e "  ${BLUE}sgit -p pull${NC}             - Pull all repositories in parallel"
  echo -e "  ${BLUE}sgit --help${NC}              - Show help with all options"
  echo
  echo -e "${YELLOW}Super Short Commands:${NC}"
  echo -e "  ${BLUE}s-status${NC}                 - Check status (shortest version)"
  echo -e "  ${BLUE}s-pull${NC}                   - Pull updates (shortest version)"
  echo -e "  ${BLUE}s-fetch${NC}                  - Fetch updates (shortest version)"
  echo -e "  ${BLUE}s-unpushed${NC}               - Check unpushed changes (shortest version)"
  echo
  echo -e "${YELLOW}Original Shortcut Commands (maintained for compatibility):${NC}"
  echo -e "  ${BLUE}sgit-status${NC}              - Check status of all repositories"
  echo -e "  ${BLUE}sgit-pull${NC}                - Pull all repositories"
  echo -e "  ${BLUE}sgit-fetch${NC}               - Fetch updates for all repositories"
  echo -e "  ${BLUE}sgit-unpushed${NC}            - Check for unpushed changes"
  echo
else
  echo
  echo -e "${RED}Installation might have failed. Please check if $INSTALL_DIR is in your PATH.${NC}"
  echo
  echo -e "${YELLOW}You can manually add sgit to your PATH:${NC}"
  echo -e "  export PATH=\"\$PATH:$SCRIPT_DIR\""
  echo
fi

exit 0
