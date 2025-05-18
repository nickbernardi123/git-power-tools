#!/bin/bash
# Official universal installer for Git Helper Tool and sgit-tools
# Presents a menu to select which tools to install and which environment to target

set -e

# Welcome message
clear
cat <<EOF
====================================
  Git Power Tools Universal Installer
====================================
EOF

# Tool selection
PS3="Select the tool(s) to install (enter number): "
tools=("Git Helper Tool" "sgit-tools" "Both" "Cancel")
select tool in "${tools[@]}"; do
    case $REPLY in
        1) TO_INSTALL=("git-helper"); break;;
        2) TO_INSTALL=("sgit-tools"); break;;
        3) TO_INSTALL=("git-helper" "sgit-tools"); break;;
        4) echo "Installation cancelled."; exit 0;;
        *) echo "Invalid option. Please try again.";;
    esac
done

# Environment selection
PS3="\nInstall for which environment? (enter number): "
envs=("Bash (Linux/macOS/Git Bash)" "Windows CMD/Powershell" "Cancel")
select env in "${envs[@]}"; do
    case $REPLY in
        1) TARGET_ENV="bash"; break;;
        2) TARGET_ENV="windows"; break;;
        3) echo "Installation cancelled."; exit 0;;
        *) echo "Invalid option. Please try again.";;
    esac
done

# Install selected tools for the chosen environment
for tool in "${TO_INSTALL[@]}"; do
    if [[ "$tool" == "git-helper" ]]; then
        echo -e "\nInstalling Git Helper Tool..."
        if [[ "$TARGET_ENV" == "windows" ]]; then
            cmd.exe /c install_git_helper.bat
        else
            bash install_git_helper.sh
        fi
    fi
    if [[ "$tool" == "sgit-tools" ]]; then
        echo -e "\nInstalling sgit-tools..."
        if [[ "$TARGET_ENV" == "windows" ]]; then
            (cd ../sgit-tools && cmd.exe /c setup-sgit-windows.bat)
        else
            (cd ../sgit-tools && bash setup.sh)
        fi
    fi
done

# Offer to add this directory to PATH
read -p $'\nAdd this directory to your PATH so you can use the tools anywhere? (y/n): ' ADDPATH
if [[ "$ADDPATH" =~ ^[Yy]$ ]]; then
    if [[ "$TARGET_ENV" == "windows" ]]; then
        cmd.exe /c setx PATH "%PATH%;%cd%"
        echo "Added $(pwd) to PATH (Windows)."
    else
        if [[ ":$PATH:" != *":$(pwd):"* ]]; then
            echo "export PATH=\"$PATH:$(pwd)\"" >> ~/.bashrc
            echo "Added $(pwd) to PATH in ~/.bashrc."
        fi
    fi
fi

echo -e "\nSetup complete! You can now use 'git helper', 'git gh', or 'sgit' from any directory."
