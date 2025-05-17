#!/bin/bash
# cleanup.sh - Move loose files into their appropriate folders

echo "Cleaning up the repository structure..."

# Get the script directory
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Make sure folders exist
mkdir -p "$BASE_DIR/git-helper-tools"
mkdir -p "$BASE_DIR/sgit-tools"

# Move git-helper files to git-helper-tools
if [ -f "$BASE_DIR/git-helper" ]; then
    cp "$BASE_DIR/git-helper" "$BASE_DIR/git-helper-tools/"
    rm "$BASE_DIR/git-helper"
    echo "Moved git-helper to git-helper-tools/"
fi

if [ -f "$BASE_DIR/git-helper.bat" ]; then
    cp "$BASE_DIR/git-helper.bat" "$BASE_DIR/git-helper-tools/"
    rm "$BASE_DIR/git-helper.bat"
    echo "Moved git-helper.bat to git-helper-tools/"
fi

if [ -f "$BASE_DIR/git_helpers.py" ]; then
    # This is a launcher script, let's convert it to a proper file in git-helper-tools
    echo "#!/bin/bash
# Global launcher for Git Helper Tool
# Simply redirects to the enhanced version of the tool

script_dir=\"\$(dirname \"\$(readlink -f \"\$0\")\")\"
python \"\$script_dir/git_helpers_enhanced.py\" \"\$@\"
" > "$BASE_DIR/git-helper-tools/git-helper"
    chmod +x "$BASE_DIR/git-helper-tools/git-helper"
    
    # Create Windows batch version
    echo "@echo off
REM Global launcher for Git Helper Tool
REM Redirects to the enhanced version

python \"%~dp0git_helpers_enhanced.py\" %*
" > "$BASE_DIR/git-helper-tools/git-helper.bat"
    
    rm "$BASE_DIR/git_helpers.py"
    echo "Converted git_helpers.py to proper launchers in git-helper-tools/"
fi

echo "Clean-up complete!"
