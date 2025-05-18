# Git Helper Tool (v2.2)

## Overview
An enhanced command-line interface for Git operations, focusing on branch management and commit workflows. This tool provides a streamlined interface to common Git operations and adds additional functionality for a better user experience.

## Features

### Core Git Operations
- Branch management (list, create, switch, delete)
- Commit workflows (stage, commit, amend)
- Remote operations (push, pull)

### Enhanced Features
- Interactive menu-based interface
- Colorized output for better readability
- Back navigation with 'b' shortcut throughout the tool
- Proper error handling and user feedback
- Custom date functionality for commits and amendments
- Detailed status information

### New in v2.2
- Added 'b' as keyboard shortcut to go back from all menus
- Improved error handling for keyboard interrupts
- Enhanced custom commit date functionality
- Fixed indentation issues throughout the codebase
- Better user feedback with colored output
- Remote branch deletion confirmation added
- Streamlined user interface

## Installation

### Windows
1. Clone or download this repository
2. Add the `git-helper-tools` directory to your PATH or create a symlink to `git-helper.bat` in a directory that's already in your PATH
3. Run `git-helper` from any Git repository

### Linux/macOS
1. Clone or download this repository
2. Add the `git-helper-tools` directory to your PATH or create a symlink to `git-helper` in a directory that's already in your PATH
3. Ensure the `git-helper` script is executable (`chmod +x git-helper`)
4. Run `git-helper` from any Git repository

## Requirements
- Python 3.6+
- Git
- Colorama package (`pip install colorama`)

## Usage
From any Git repository, run:
```
git-helper
```

This will display the main menu with numbered options. Select an option by entering its number and pressing Enter.

### Navigation Tips
- Use the 'b' key to go back to the previous menu
- Press Ctrl+C at any time to cancel the current operation
- Follow the on-screen prompts for each operation

## License
This project is licensed under the MIT License - see the LICENSE file for details.
