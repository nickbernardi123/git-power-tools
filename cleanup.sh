#!/bin/bash
# Cleanup script for customScripts folder

echo "Cleaning up customScripts folder..."

# Move to root directory to avoid any issues with current directory
cd /c

# Create backup folder for files we're going to remove
mkdir -p /c/customScripts/backup_files

# Move obsolete sgit files to the backup folder
echo "Moving obsolete sgit files to backup folder..."
mv /c/customScripts/sgit.sh /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/sgit /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/sgit.bat /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/sgit.new /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/sgit-status /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/sgit-status.bat /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/sgit-pull /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/sgit-pull.bat /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/setup-sgit.bat /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/setup-sgit-windows.bat /c/customScripts/backup_files/ 2>/dev/null
mv /c/customScripts/README-sgit.md /c/customScripts/backup_files/ 2>/dev/null

# Move any empty directories
rmdir /c/customScripts/sgit 2>/dev/null

echo "Cleanup complete!"
