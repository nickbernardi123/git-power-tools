# Git Helper Tools

This collection of tools helps you manage git commits, branches, and team workflows from the command line with an interactive menu.

## Features
- Amend commit dates and messages
- Create commits with custom dates
- Branch management (switch, create, delete, info, fix tracking)
- Team tools (view remote branches, pull requests, quick push/pull, stash, merges, unpushed commits)
- Automated backup before destructive actions
- Extra tools: rebase UI, commit templates, cherry-pick, etc.

## Requirements
- Python 3.7+
- See requirements.txt for dependencies

## Usage
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the tool:
   ```
   python git_helpers.py
   ```

## Customization
- You can add or remove features by editing the script or moving helpers to separate modules.
