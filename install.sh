#!/bin/bash
# install.sh - Interactive installer for Git Power Tools
# Allows users to select which tools to install using arrow keys and space bar

# Check if running on Windows via Git Bash or WSL
if [[ "$(uname -s)" == MINGW* ]] || [[ "$(uname -s)" == CYGWIN* ]]; then
  IS_WINDOWS=true
else
  IS_WINDOWS=false
fi

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "   _____ _ _     _____                        _____           _     "
echo "  / ____(_) |   |  __ \                      |_   _|         | |    "
echo " | |  __ _| |_  | |__) |____      _____ _ __   | |  ___   ___| |___ "
echo " | | |_ | | __| |  ___/ _ \ \ /\ / / _ \ '__|  | | / _ \ / _ \ / __|"
echo " | |__| | | |_  | |  | (_) \ V  V /  __/ |    _| || (_) | (_) \__ \\"
echo "  \_____|_|\__| |_|   \___/ \_/\_/ \___|_|   |_____\___/ \___/|___/"
echo -e "${NC}"
echo -e "${YELLOW}Interactive Installer${NC}\n"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check for required dependencies
check_dependencies() {
  local missing_deps=()

  echo -e "${BLUE}Checking dependencies...${NC}"
  
  if ! command_exists git; then
    missing_deps+=("git")
  fi

  if ! command_exists python || ! command_exists python3; then
    missing_deps+=("python")
  fi

  # For the menu system
  if ! command_exists whiptail && ! command_exists dialog; then
    if $IS_WINDOWS; then
      # On Windows, we'll use a simpler selection mechanism
      echo -e "${YELLOW}Note: Installing whiptail or dialog would provide a better menu experience${NC}"
    else
      missing_deps+=("whiptail/dialog")
    fi
  fi

  if [ ${#missing_deps[@]} -ne 0 ]; then
    echo -e "${RED}The following dependencies are missing:${NC}"
    for dep in "${missing_deps[@]}"; do
      echo "  - $dep"
    done
    
    echo -e "\n${YELLOW}Please install these dependencies and run the installer again.${NC}"
    
    if $IS_WINDOWS; then
      echo -e "${YELLOW}For Windows users:${NC}"
      echo "  - Git: Download from https://git-scm.com/download/win"
      echo "  - Python: Download from https://www.python.org/downloads/"
    else
      echo -e "${YELLOW}For Linux/macOS users:${NC}"
      echo "  - Git: sudo apt install git (Ubuntu/Debian) or brew install git (macOS)"
      echo "  - Python: sudo apt install python3 (Ubuntu/Debian) or brew install python (macOS)"
      echo "  - Whiptail: sudo apt install whiptail (Ubuntu/Debian) or brew install newt (macOS)"
    fi
    
    exit 1
  fi
  
  echo -e "${GREEN}All dependencies found!${NC}"
}

# Function to get Python command (python or python3)
get_python_cmd() {
  if command_exists python3; then
    echo "python3"
  else
    echo "python"
  fi
}

# Function to install Python package
install_python_package() {
  local package=$1
  local python_cmd=$(get_python_cmd)
  
  echo -e "${BLUE}Checking for $package...${NC}"
  
  # Check if package is already installed
  if $python_cmd -c "import $package" 2>/dev/null; then
    echo -e "${GREEN}$package is already installed.${NC}"
    return 0
  fi
  
  echo -e "${YELLOW}Installing $package...${NC}"
  
  # Try with pip3 first, then pip
  if command_exists pip3; then
    pip3 install $package
  elif command_exists pip; then
    pip install $package
  else
    echo -e "${RED}Error: pip not found. Please install pip and try again.${NC}"
    return 1
  fi
  
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}Successfully installed $package.${NC}"
    return 0
  else
    echo -e "${RED}Failed to install $package.${NC}"
    return 1
  fi
}

# Function to get script directory
get_script_dir() {
  local source="${BASH_SOURCE[0]}"
  local dir=""
  
  # Resolve $SOURCE until the file is no longer a symlink
  while [ -h "$source" ]; do
    dir="$(cd -P "$(dirname "$source")" && pwd)"
    source="$(readlink "$source")"
    # If $SOURCE was a relative symlink, we need to resolve it relative to the path
    # where the symlink file was located
    [[ $source != /* ]] && source="$dir/$source"
  done
  
  dir="$(cd -P "$(dirname "$source")" && pwd)"
  echo "$dir"
}

# Function to add directory to PATH in bashrc/zshrc/bash_profile
add_to_path() {
  local dir_to_add=$1
  local shell_rc=""
  
  if [ -f ~/.bashrc ]; then
    shell_rc=~/.bashrc
  elif [ -f ~/.zshrc ]; then
    shell_rc=~/.zshrc
  elif [ -f ~/.bash_profile ]; then
    shell_rc=~/.bash_profile
  else
    echo -e "${YELLOW}Could not find shell configuration file. Please add the following to your shell configuration:${NC}"
    echo -e "  export PATH=\"\$PATH:$dir_to_add\""
    return 1
  fi
  
  # Check if path is already in shell_rc
  if grep -q "export PATH=.*$dir_to_add" "$shell_rc"; then
    echo -e "${GREEN}Path already added to $shell_rc${NC}"
    return 0
  fi
  
  echo -e "${BLUE}Adding $dir_to_add to $shell_rc${NC}"
  echo "# Added by Git Power Tools installer" >> "$shell_rc"
  echo "export PATH=\"\$PATH:$dir_to_add\"" >> "$shell_rc"
  
  echo -e "${GREEN}Successfully added $dir_to_add to PATH in $shell_rc${NC}"
  echo -e "${YELLOW}Please restart your terminal or run 'source $shell_rc' to update your PATH.${NC}"
  return 0
}

# Function to add directory to Windows PATH
add_to_windows_path() {
  local dir_to_add=$1
  local normalized_path=$(echo "$dir_to_add" | sed 's|/|\\|g')
  
  echo -e "${BLUE}Adding $normalized_path to Windows PATH...${NC}"
  
  # Use PowerShell to add the directory to PATH permanently
  powershell.exe -Command "[Environment]::SetEnvironmentVariable('PATH', [Environment]::GetEnvironmentVariable('PATH', 'User') + ';$normalized_path', 'User')"
  
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}Successfully added to Windows PATH!${NC}"
    echo -e "${YELLOW}You'll need to restart your terminal for the PATH changes to take effect.${NC}"
    return 0
  else
    echo -e "${RED}Failed to modify Windows PATH.${NC}"
    echo -e "${YELLOW}Please manually add '$normalized_path' to your PATH:${NC}"
    echo "1. Right-click on 'This PC' > Properties > Advanced system settings"
    echo "2. Click 'Environment Variables'"
    echo "3. Edit the 'Path' user variable"
    echo "4. Add '$normalized_path' to the list"
    return 1
  fi
}

# Function to install Super Git (sgit)
install_sgit() {
  echo -e "\n${BLUE}Installing Super Git (sgit)...${NC}"
  
  local script_dir=$(get_script_dir)
  local sgit_dir="$script_dir/sgit-tools"
  
  if [ ! -d "$sgit_dir" ]; then
    echo -e "${RED}Error: sgit-tools directory not found at $sgit_dir${NC}"
    return 1
  fi
  
  # Make sgit scripts executable
  echo -e "${BLUE}Setting executable permissions on sgit scripts...${NC}"
  chmod +x "$sgit_dir/sgit" "$sgit_dir/sgit-status" "$sgit_dir/sgit-pull" "$sgit_dir/sgit-fetch" "$sgit_dir/sgit-unpushed" 2>/dev/null
  chmod +x "$sgit_dir/shorter-aliases/s-status" "$sgit_dir/shorter-aliases/s-pull" "$sgit_dir/shorter-aliases/s-fetch" "$sgit_dir/shorter-aliases/s-unpushed" 2>/dev/null
  
  # Check for enhanced version and use it if available
  if [ -f "$sgit_dir/sgit-enhanced" ]; then
    echo -e "${BLUE}Using enhanced sgit version...${NC}"
    cp -f "$sgit_dir/sgit-enhanced" "$sgit_dir/sgit"
    echo -e "${GREEN}Enhanced version activated!${NC}"
  fi
  
  if $IS_WINDOWS; then
    add_to_windows_path "$sgit_dir"
    add_to_windows_path "$sgit_dir/shorter-aliases"
  else
    # For macOS and Linux
    local bin_dir="/usr/local/bin"
    
    if [ ! -w "$bin_dir" ]; then
      echo -e "${YELLOW}Insufficient permissions to write to $bin_dir${NC}"
      echo -e "${YELLOW}Will add tools to PATH instead...${NC}"
      add_to_path "$sgit_dir"
      add_to_path "$sgit_dir/shorter-aliases"
    else
      echo -e "${BLUE}Creating symbolic links in $bin_dir...${NC}"
      ln -sf "$sgit_dir/sgit" "$bin_dir/sgit"
      ln -sf "$sgit_dir/sgit-status" "$bin_dir/sgit-status"
      ln -sf "$sgit_dir/sgit-pull" "$bin_dir/sgit-pull"
      ln -sf "$sgit_dir/sgit-fetch" "$bin_dir/sgit-fetch"
      ln -sf "$sgit_dir/sgit-unpushed" "$bin_dir/sgit-unpushed"
      ln -sf "$sgit_dir/shorter-aliases/s-status" "$bin_dir/s-status"
      ln -sf "$sgit_dir/shorter-aliases/s-pull" "$bin_dir/s-pull"
      ln -sf "$sgit_dir/shorter-aliases/s-fetch" "$bin_dir/s-fetch"
      ln -sf "$sgit_dir/shorter-aliases/s-unpushed" "$bin_dir/s-unpushed"
      echo -e "${GREEN}Symbolic links created successfully!${NC}"
    fi
  fi
  
  echo -e "${GREEN}Super Git (sgit) has been installed successfully!${NC}"
  echo -e "${BLUE}You can now use:${NC}"
  echo -e "  ${YELLOW}sgit status${NC} - Check status of all repositories"
  echo -e "  ${YELLOW}s-status${NC}   - Short version for status check"
  echo -e "  ${YELLOW}sgit --help${NC} - Show all available options"
}

# Function to install Git Helper Tool
install_git_helper() {
  echo -e "\n${BLUE}Installing Git Helper Tool...${NC}"
  
  local script_dir=$(get_script_dir)
  local helper_dir="$script_dir/git-helper-tools"
  
  if [ ! -d "$helper_dir" ]; then
    echo -e "${RED}Error: git-helper-tools directory not found at $helper_dir${NC}"
    return 1
  fi
  
  # Install required Python packages
  install_python_package "colorama"
  
  # Make scripts executable
  chmod +x "$helper_dir/git_helpers.py" "$helper_dir/git_helpers_enhanced.py" 2>/dev/null
  
  # Create launcher script for Git Helper
  local python_cmd=$(get_python_cmd)
  local launcher_file="git-helper"
  local launcher_content="#!/bin/bash
# Git Helper Tool Launcher
$python_cmd \"$helper_dir/git_helpers_enhanced.py\" \"\$@\"
"
  local launcher_windows_content="@echo off
REM Git Helper Tool Launcher
$python_cmd \"$helper_dir\\git_helpers_enhanced.py\" %*
"

  if $IS_WINDOWS; then
    # Create Windows batch file
    echo -e "${BLUE}Creating git-helper.bat launcher...${NC}"
    echo "$launcher_windows_content" > "$helper_dir/git-helper.bat"
    
    # Add to Windows PATH
    add_to_windows_path "$helper_dir"
  else
    # Create bash launcher
    local bin_dir="/usr/local/bin"
    
    if [ ! -w "$bin_dir" ]; then
      echo -e "${YELLOW}Insufficient permissions to write to $bin_dir${NC}"
      echo -e "${YELLOW}Creating launcher in tools directory and adding to PATH...${NC}"
      echo "$launcher_content" > "$helper_dir/$launcher_file"
      chmod +x "$helper_dir/$launcher_file"
      add_to_path "$helper_dir"
    else
      echo -e "${BLUE}Creating launcher in $bin_dir...${NC}"
      echo "$launcher_content" > "$bin_dir/$launcher_file"
      chmod +x "$bin_dir/$launcher_file"
      echo -e "${GREEN}Launcher created successfully!${NC}"
    fi
  fi
  
  echo -e "${GREEN}Git Helper Tool has been installed successfully!${NC}"
  echo -e "${BLUE}You can now use:${NC}"
  echo -e "  ${YELLOW}git-helper${NC} - Launch the Git Helper Tool"
}

# Interactive menu for selecting tools to install
select_tools() {
  local selected_tools=()
  
  if command_exists whiptail; then
    # Use whiptail for selection if available
    whiptail --title "Git Power Tools Installer" --checklist \
      "Select tools to install (use SPACE to select/deselect, ENTER to confirm):" 15 60 2 \
      "sgit" "Super Git - Run git commands on multiple repositories" ON \
      "git-helper" "Git Helper - Branch and commit management tool" ON 2>tempfile
      
    selected_tools=($(cat tempfile))
    rm -f tempfile
  elif command_exists dialog; then
    # Use dialog as fallback
    dialog --title "Git Power Tools Installer" --checklist \
      "Select tools to install (use SPACE to select/deselect, ENTER to confirm):" 15 60 2 \
      "sgit" "Super Git - Run git commands on multiple repositories" ON \
      "git-helper" "Git Helper - Branch and commit management tool" ON 2>tempfile
      
    selected_tools=($(cat tempfile))
    rm -f tempfile
  else
    # Simple CLI selection if neither whiptail nor dialog is available
    echo -e "${BLUE}Select tools to install:${NC}"
    echo "1. Super Git (sgit) - Run git commands on multiple repositories"
    echo "2. Git Helper - Branch and commit management tool"
    echo "3. Install all tools"
    echo "4. Cancel installation"
    
    local choice
    read -p "Enter your choice (1/2/3/4): " choice
    
    case $choice in
      1) selected_tools=("sgit") ;;
      2) selected_tools=("git-helper") ;;
      3) selected_tools=("sgit" "git-helper") ;;
      4) selected_tools=() ;;
      *) echo -e "${RED}Invalid choice. Exiting.${NC}"; exit 1 ;;
    esac
  fi
  
  echo "${selected_tools[@]}"
}

# Main installation process
main() {
  # Check dependencies
  check_dependencies
  
  # Select tools to install
  local tools_to_install=($(select_tools))
  
  if [ ${#tools_to_install[@]} -eq 0 ]; then
    echo -e "${YELLOW}No tools selected. Installation cancelled.${NC}"
    exit 0
  fi
  
  echo -e "\n${GREEN}Installing selected tools...${NC}"
  
  # Install selected tools
  for tool in "${tools_to_install[@]}"; do
    case $tool in
      "sgit") install_sgit ;;
      "git-helper") install_git_helper ;;
    esac
  done
  
  echo -e "\n${GREEN}Installation complete!${NC}"
  echo -e "${YELLOW}Please restart your terminal for all changes to take effect.${NC}"
}

# Run main function
main
