# Git Power Tools

This repository contains a collection of powerful Git utilities to enhance your workflow when working with Git repositories.

## Available Tools

### 1. Super Git (sgit)

Run git commands on multiple repositories simultaneously.

**Key Features:**
- Execute any git command across all repositories in a directory
- Colorful status output for each repository
- Skip non-git directories automatically
- Summary statistics of operations
- Shortcut commands for common operations

[➡️ Learn more about Super Git](./sgit-tools/README-sgit.md)

### 2. Git Helper

Interactive CLI tool for advanced Git operations.

**Key Features:**
- Manage git commits, branches, and team workflows
- Amend commit dates and messages
- Branch management (create, switch, delete)
- Team workflow tools

[➡️ Learn more about Git Helper](./git-helper-tools/README-git-helper.md)

## Installation

You can install either tool independently or both together:

### Installing Super Git (sgit)

```bash
# Clone just the sgit-tools folder
git clone --sparse https://github.com/nickbernardi123/git-power-tools
cd git-power-tools
git sparse-checkout set sgit-tools
cd sgit-tools
./setup-sgit-windows.bat  # On Windows
# or
chmod +x ./setup.sh && ./setup.sh  # On Linux/macOS
```

### Installing Git Helper

```bash
# Clone just the git-helper-tools folder
git clone --sparse https://github.com/nickbernardi123/git-power-tools
cd git-power-tools
git sparse-checkout set git-helper-tools
cd git-helper-tools
pip install -r requirements.txt
```

### Installing Both Tools

```bash
# Clone the entire repository
git clone https://github.com/nickbernardi123/git-power-tools
cd git-power-tools

# Set up sgit
cd sgit-tools
./setup-sgit-windows.bat  # On Windows
# or 
chmod +x ./setup.sh && ./setup.sh  # On Linux/macOS
cd ..

# Set up Git Helper
cd git-helper-tools
pip install -r requirements.txt
```

## Usage

See the README files in each tool's directory for detailed usage instructions:
- [Super Git Usage](./sgit-tools/README-sgit.md#usage)
- [Git Helper Usage](./git-helper-tools/README-git-helper.md#usage)

## License

MIT License
