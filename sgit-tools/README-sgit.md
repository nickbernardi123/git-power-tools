# Super Git (sgit)

Super Git (sgit) is a powerful command-line utility that allows you to run git commands on **all repositories** in a parent directory simultaneously. It's perfect for managing multiple repositories at once and maintaining consistency across all your projects.

## Features

- **Run any git command** on all repositories in a directory
- **Recursive search** to find git repositories in nested folders
- **Parallel execution** for faster operations on many repositories
- **Interactive selection** to choose which repositories to operate on
- **Colorful output** showing success and failure status
- **Skip directories** that aren't git repositories
- **Summary statistics** after command execution
- **Supports all git commands and parameters**
- **Convenient shortcut commands** for common operations:
  - **Super Short Commands**:
    - `s-status` - Check the status of all repositories (shortest)
    - `s-pull` - Pull updates for all repositories (shortest)
    - `s-fetch` - Fetch updates without merging (shortest)
    - `s-unpushed` - Check for unpushed changes (shortest)
  - **Original Shortcuts** (maintained for compatibility):
    - `sgit-status` - Check the status of all repositories
    - `sgit-pull` - Pull updates for all repositories
    - `sgit-fetch` - Fetch updates without merging
    - `sgit-unpushed` - Check for unpushed changes in all repositories

## Installation

### Windows

1. Copy all sgit files to a directory (e.g., `C:\customScripts\sgit-tools`)
2. Run `setup-sgit-windows.bat` to add the directory to your PATH
3. Restart your terminal to apply PATH changes

### Linux/macOS

1. Copy all sgit files to a directory
2. Run the setup script:
   ```bash
   chmod +x setup.sh && ./setup.sh
   ```

## Usage

Navigate to a directory containing multiple git repositories, then:

```bash
# Basic usage
sgit status                        # Show the status of all repositories
sgit pull                          # Pull updates for all repositories
sgit add .                         # Add all files in all repositories
sgit commit -m "Update repos"      # Commit changes in all repositories
sgit push                          # Push changes in all repositories
sgit checkout -b new-feature       # Create a new branch in all repositories

# Advanced options
sgit -r status                     # Search for git repositories recursively
sgit -d 3 status                   # Search up to 3 levels deep
sgit -p pull                       # Run commands in parallel (faster)
sgit -q status                     # Quiet mode with minimal output
sgit -s checkout -b feature        # Select which repositories to operate on
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `-h, --help` | Show help message |
| `-d, --depth <num>` | Maximum directory depth to search (default: 1) |
| `-p, --parallel` | Run commands in parallel (faster but mixed output) |
| `-q, --quiet` | Show only essential output |
| `-r, --recursive` | Search for git repositories recursively |
| `-s, --select` | Interactive mode to select which repositories to run on |

### Shortcut Commands

```bash
# Quick status check
sgit-status

# Pull updates for all repositories
sgit-pull

# Fetch updates without merging
sgit-fetch

# Check for unpushed changes
sgit-unpushed
```

## Examples

### Check status of all repositories

```bash
$ cd ~/projects
$ sgit status
[1/3] Processing: ./project-a
Executing: git status
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
Success: git status in ./project-a
----------------------------------------
[2/3] Processing: ./project-b
Executing: git status
On branch feature
Your branch is ahead of 'origin/feature' by 2 commits.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

Success: git status in ./project-b
----------------------------------------
Skipping: ./not-a-repo (Not a git repository)
----------------------------------------

Summary:
Repositories processed: 2
Non-git directories skipped: 1
Total directories scanned: 3
```

## How It Works

sgit searches for directories in the current location that contain a `.git` folder, then runs the specified git command in each valid repository. Results are displayed with color-coding to easily identify success or failure.

## Author

Original implementation by Nick B.