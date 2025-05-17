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

Interactive CLI tool for advanced Git operations, available in two versions:

#### Enhanced Version (Recommended)
**Key Features:**
- Smart branch management with automatic pulling
- Safe commit and push operations with upstream tracking
- Interactive staging and committing workflow
- Simple and focused interface

#### Original Full-Featured Version
**Key Features:**
- Complete team workflow tools
- Extended branch management options
- Advanced commit operations
- Additional utilities

[➡️ Learn more about Git Helper](./git-helper-tools/README-git-helper.md)

## Installation

You can use our interactive installer or install tools individually:

### Interactive Installation (Recommended)

Install all tools with our interactive installer that lets you select which tools you want:

```bash
# Clone the repository
git clone https://github.com/nickbernardi123/git-power-tools
cd git-power-tools

# Run the interactive installer
./install.sh      # On Linux/macOS/Git Bash
# or
install.bat       # On Windows
```

The interactive installer:
- Lets you select which tools to install
- Automatically adds tools to your PATH
- Installs required dependencies
- Creates global shortcut commands

### Manual Installation

#### Installing Super Git (sgit)

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

#### Installing Git Helper

```bash
# Clone just the git-helper-tools folder
git clone --sparse https://github.com/nickbernardi123/git-power-tools
cd git-power-tools
git sparse-checkout set git-helper-tools
cd git-helper-tools
pip install -r requirements.txt

# Run setup script
./setup-git-helper-windows.bat  # On Windows
# or
chmod +x ./setup.sh && ./setup.sh  # On Linux/macOS
```

## Usage

See the README files in each tool's directory for detailed usage instructions:
- [Super Git Usage](./sgit-tools/README-sgit.md#usage)
- [Git Helper Usage](./git-helper-tools/README-git-helper.md#usage)

## License

MIT License
