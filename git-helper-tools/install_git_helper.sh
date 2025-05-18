#!/bin/bash
# Install script for Git Helper Tool
# Installs dependencies and sets up git aliases for all users

set -e

# Install Python dependencies
pip install --user -r requirements.txt

# Add git aliases (global)
git config --global alias.helper '!python "$(pwd)/git_helper_consolidated.py"'
git config --global alias.gh '!python "$(pwd)/git_helper_consolidated.py"'

echo "\nGit Helper Tool installed!"
echo "You can now run 'git helper' or 'git gh' from anywhere."
echo "If you want to uninstall, remove the aliases from your global git config."
