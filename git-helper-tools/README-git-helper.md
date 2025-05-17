# Git Helper Tools

This streamlined tool helps you manage git commits and branches from the command line with an interactive menu.

## Features

### Enhanced Git Helper (Recommended)
- **Branch Management**
  - Automatically pulls changes when switching branches
  - Ensures correct upstream tracking is set when pushing
  - Interactive branch switching, creation and deletion
  - Clean handling of uncommitted changes during branch operations

- **Commit Management**
  - Interactive staging of changes
  - Simple commit creation with automatic push option
  - Amend commit messages and dates
  - View commit history

### Original Git Helper
- Amend commit dates and messages
- Create commits with custom dates
- Branch management (switch, create, delete, info, fix tracking)
- Team tools (view remote branches, pull requests, quick push/pull, stash, merges, unpushed commits)
- Automated backup before destructive actions
- Extra tools: rebase UI, commit templates, cherry-pick, etc.

## Requirements
- Python 3.7+
- Required Python packages: `colorama`

## Usage
1. Install dependencies:
   ```
   pip install colorama
   ```

2. Run the tool:
   ```bash
   # Run the enhanced version (recommended)
   python git_helpers_enhanced.py
   
   # Or run the original full-featured version
   python git_helpers.py
   ```

## Key Improvements in Enhanced Version
- **Simplified Interface**: Focus on the two most essential git workflows
- **Safer Operations**: Prevents common git mistakes
- **Automatic Tracking**: Always sets proper upstream tracking
- **Intelligent Pulling**: Automatically pulls changes when switching branches
