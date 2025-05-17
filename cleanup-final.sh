#!/bin/bash

echo "Cleaning up unnecessary files and directories..."

# Remove backup files directory
rm -rf /c/customScripts/backup_files

# Remove duplicate or unnecessary files
rm -f /c/customScripts/README-github.md
rm -f /c/customScripts/cleanup.sh
rm -f /c/customScripts/setup-all.bat
rm -f /c/customScripts/git_helpers.py
rm -f /c/customScripts/git_helper.log

# Remove old git_helper directory
rm -rf /c/customScripts/git_helper

# Remove temporary files
rm -f /c/customScripts/sgit-tools/s

echo "Clean-up complete!"

