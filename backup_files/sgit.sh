#!/bin/bash

# Super Git (sgit) - Run git commands on all repositories in the current directory
# Author: Nick B
# Date: May 17, 2025

# Get the command to run
command="$@"

if [ -z "$command" ]; then
  echo "Usage: sgit [git command]"
  echo "Example: sgit status"
  echo "         sgit pull"
  echo "         sgit commit -m \"Update all repositories\""
  exit 1
fi

# Set text colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print header
echo -e "${BLUE}===== Running 'git $command' on all repositories =====${NC}\n"

# Get all directories in the current directory
directories=()
while IFS= read -r -d '' dir; do
  directories+=("$dir")
done < <(find . -maxdepth 1 -type d -not -path "*/\.*" -not -path "." -print0)

# Count directories
total=${#directories[@]}
count=0
skip_count=0
success_count=0
failure_count=0

# Execute the command in each directory if it contains a .git folder
for dir in "${directories[@]}"; do
  # Check if the directory is a git repository
  if [ -d "$dir/.git" ]; then
    ((count++))
    echo -e "${YELLOW}[${count}/${total}] Processing: ${BLUE}${dir}${NC}"
    
    # Change to the directory, execute the command, and return
    (
      cd "$dir" || { echo -e "${RED}Failed to enter directory: $dir${NC}"; exit 1; }
      
      echo -e "${CYAN}Executing: git $command${NC}"
      if git $command; then
        echo -e "${GREEN}Success: git $command in $dir${NC}"
        ((success_count++))
      else
        echo -e "${RED}Failed: git $command in $dir${NC}"
        ((failure_count++))
      fi
    ) 
    
    # We have to manually update the counts after the subshell
    if [ $? -eq 0 ]; then
      success_count=$((success_count))
    else
      failure_count=$((failure_count))
    fi
  else
    ((skip_count++))
    echo -e "${PURPLE}Skipping: $dir (Not a git repository)${NC}"
  fi
  
  # Add a separator between repositories for readability
  echo -e "${YELLOW}----------------------------------------${NC}"
done

# Calculate the counts now since we can't reliably track them in subshells
# Count git directories
git_dirs=$(find . -maxdepth 2 -name ".git" -type d | wc -l)

# Print summary
echo -e "${BLUE}Summary:${NC}"
echo -e "${GREEN}Repositories processed: $git_dirs${NC}"
echo -e "${PURPLE}Non-git directories skipped: $skip_count${NC}"
echo -e "${YELLOW}Total directories scanned: $total${NC}"

exit 0
