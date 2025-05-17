#!/usr/bin/env python3
# Streamlined Git Helper Tool - Focused on branch and commit management

import os
import subprocess
import sys
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama for colored output

# ==================== Utility Functions ====================

def check_git_installed():
    """Check if Git is installed."""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print(Fore.RED + "Error: Git is not installed. Please install Git and try again.")
        exit(1)

def run_git_command(command, error_msg=None, success_msg=None, check=True):
    """Run a git command with proper error handling and feedback."""
    try:
        result = subprocess.run(command, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if success_msg:
            print(Fore.GREEN + success_msg)
        return result
    except subprocess.CalledProcessError as e:
        if error_msg:
            print(Fore.RED + error_msg)
        print(Fore.RED + f"Command failed: {e.stderr}")
        return None

def validate_date_format(date_str):
    """Validate the date format (YYYY-MM-DD HH:MM:SS)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def get_current_date():
    """Get the current date in the required format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def confirm_action(prompt_text):
    """Ask for confirmation before performing a critical action."""
    while True:
        choice = input(Fore.YELLOW + f"{prompt_text} (y/n): ").strip().lower()
        if choice in ["y", "yes", "1"]:
            return True
        elif choice in ["n", "no", "2"]:
            return False
        print(Fore.RED + "Please enter 'y' for yes or 'n' for no.")

def get_current_branch():
    """Get the name of the current branch."""
    result = run_git_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if result:
        return result.stdout.strip()
    return "unknown"

def get_tracking_branch():
    """Get the tracking branch for the current branch."""
    result = run_git_command(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], 
        check=False
    )
    if result and result.returncode == 0:
        return result.stdout.strip()
    return None

# ==================== Branch Management ====================

def list_branches():
    """List all local branches and mark the current one."""
    result = run_git_command(["git", "branch"], check=True)
    if not result:
        return []
    
    branches = []
    current_branch = ""
    
    for line in result.stdout.split('\n'):
        if line.strip():
            if line.startswith('*'):
                current_branch = line[2:].strip()
                branches.append(line[2:].strip())
            else:
                branches.append(line.strip())
    
    return branches, current_branch

def switch_branch(branch_name):
    """Switch to an existing branch and pull latest changes."""
    # First check if there are any uncommitted changes
    status_result = run_git_command(["git", "status", "--porcelain"])
    if status_result and status_result.stdout.strip():
        print(Fore.YELLOW + "You have uncommitted changes.")
        choice = input(Fore.YELLOW + "Do you want to (1) stash changes, (2) commit changes, or (3) abort? ").strip()
        if choice == "1":
            stash_msg = input("Enter a stash message (optional): ").strip()
            if stash_msg:
                run_git_command(["git", "stash", "save", stash_msg], 
                               error_msg="Failed to stash changes.",
                               success_msg="Changes stashed successfully.")
            else:
                run_git_command(["git", "stash"], 
                               error_msg="Failed to stash changes.",
                               success_msg="Changes stashed successfully.")
        elif choice == "2":
            commit_msg = input("Enter commit message: ").strip()
            if not commit_msg:
                print(Fore.RED + "Commit message cannot be empty.")
                return
            run_git_command(["git", "add", "."], 
                           error_msg="Failed to stage changes.")
            run_git_command(["git", "commit", "-m", commit_msg], 
                           error_msg="Failed to commit changes.",
                           success_msg="Changes committed successfully.")
        else:
            print(Fore.YELLOW + "Branch switch aborted.")
            return False

    # Switch to the branch
    print(Fore.CYAN + f"Switching to branch '{branch_name}'...")
    result = run_git_command(["git", "checkout", branch_name], 
                            error_msg=f"Failed to switch to branch '{branch_name}'.",
                            success_msg=f"Switched to branch '{branch_name}'.")
    if not result:
        return False
    
    # Check if the branch has a tracking relationship
    tracking = get_tracking_branch()
    
    if tracking:
        print(Fore.CYAN + f"Pulling latest changes from {tracking}...")
        run_git_command(["git", "pull"], 
                       error_msg="Failed to pull latest changes. You may need to resolve conflicts.",
                       success_msg="Successfully pulled latest changes.")
    else:
        print(Fore.YELLOW + f"Branch '{branch_name}' is not tracking any remote branch.")
        remote_branches = run_git_command(["git", "branch", "-r"], check=True)
        if remote_branches:
            matching_remotes = [rb.strip() for rb in remote_branches.stdout.split('\n') 
                               if rb.strip().endswith('/' + branch_name)]
            
            if matching_remotes:
                if len(matching_remotes) == 1:
                    remote = matching_remotes[0]
                    if confirm_action(f"Set up tracking for remote {remote}?"):
                        run_git_command(["git", "branch", "--set-upstream-to=" + remote, branch_name],
                                      error_msg=f"Failed to set upstream to {remote}",
                                      success_msg=f"Set upstream to {remote}")
                        run_git_command(["git", "pull"], 
                                      error_msg="Failed to pull latest changes.",
                                      success_msg="Successfully pulled latest changes.")
                else:
                    print(Fore.YELLOW + "Multiple potential remote branches found:")
                    for i, remote in enumerate(matching_remotes, 1):
                        print(f"{i}. {remote}")
                    choice = input("Select a remote to track (number) or press Enter to skip: ").strip()
                    if choice.isdigit() and 1 <= int(choice) <= len(matching_remotes):
                        remote = matching_remotes[int(choice) - 1]
                        run_git_command(["git", "branch", "--set-upstream-to=" + remote, branch_name],
                                      error_msg=f"Failed to set upstream to {remote}",
                                      success_msg=f"Set upstream to {remote}")
                        run_git_command(["git", "pull"], 
                                      error_msg="Failed to pull latest changes.",
                                      success_msg="Successfully pulled latest changes.")
    
    return True

def create_branch(branch_name):
    """Create a new branch and set it up for tracking."""
    result = run_git_command(["git", "checkout", "-b", branch_name], 
                            error_msg=f"Failed to create branch '{branch_name}'.",
                            success_msg=f"Created and switched to new branch '{branch_name}'.")
    if not result:
        return False
    
    if confirm_action(f"Do you want to push branch '{branch_name}' to remote and set up tracking?"):
        push_result = run_git_command(["git", "push", "--set-upstream", "origin", branch_name], 
                                    error_msg=f"Failed to push branch '{branch_name}' to remote.",
                                    success_msg=f"Branch '{branch_name}' pushed to remote and tracking established.")
        return push_result is not None
    
    return True

def delete_branch(branch_name):
    """Delete a branch locally and optionally remotely."""
    current = get_current_branch()
    if branch_name == current:
        print(Fore.RED + "Cannot delete the currently checked out branch.")
        return False
    
    # Check if branch exists locally
    branches, _ = list_branches()
    if branch_name not in branches:
        print(Fore.RED + f"Branch '{branch_name}' not found locally.")
        return False
    
    # Delete local branch
    result = run_git_command(["git", "branch", "-d", branch_name], 
                            error_msg=f"Failed to delete branch '{branch_name}'. It may have unmerged changes. Use -D to force.")
    
    if not result:
        force = confirm_action(f"Branch '{branch_name}' has unmerged changes. Force delete?")
        if force:
            result = run_git_command(["git", "branch", "-D", branch_name], 
                                   error_msg=f"Failed to force delete branch '{branch_name}'.",
                                   success_msg=f"Branch '{branch_name}' force deleted.")
        else:
            return False
    else:
        print(Fore.GREEN + f"Local branch '{branch_name}' deleted.")
    
    # Check if branch exists remotely
    remote_exists = run_git_command(["git", "ls-remote", "--heads", "origin", branch_name], check=False)
    if remote_exists and remote_exists.stdout.strip():
        if confirm_action(f"Do you also want to delete the remote branch 'origin/{branch_name}'?"):
            remote_result = run_git_command(["git", "push", "origin", "--delete", branch_name], 
                                         error_msg=f"Failed to delete remote branch 'origin/{branch_name}'.",
                                         success_msg=f"Remote branch 'origin/{branch_name}' deleted.")
            return remote_result is not None
    
    return True

def push_changes():
    """Push changes with proper upstream handling."""
    current_branch = get_current_branch()
    tracking_branch = get_tracking_branch()
    
    if tracking_branch:
        print(Fore.CYAN + f"Pushing changes from '{current_branch}' to '{tracking_branch}'...")
        result = run_git_command(["git", "push"], 
                               error_msg="Failed to push changes.",
                               success_msg=f"Successfully pushed changes to {tracking_branch}.")
        return result is not None
    else:
        print(Fore.YELLOW + f"Branch '{current_branch}' doesn't have an upstream branch set.")
        if confirm_action(f"Set upstream to 'origin/{current_branch}' and push?"):
            result = run_git_command(["git", "push", "--set-upstream", "origin", current_branch], 
                                   error_msg=f"Failed to push and set upstream.",
                                   success_msg=f"Successfully pushed and set upstream to origin/{current_branch}.")
            return result is not None
        else:
            remote_name = input("Enter remote name [origin]: ").strip() or "origin"
            remote_branch = input(f"Enter remote branch name [{current_branch}]: ").strip() or current_branch
            
            result = run_git_command(["git", "push", "--set-upstream", remote_name, remote_branch], 
                                   error_msg=f"Failed to push to '{remote_name}/{remote_branch}'.",
                                   success_msg=f"Successfully pushed to '{remote_name}/{remote_branch}'.")
            return result is not None

# ==================== Commit Management ====================

def stage_changes():
    """Stage changes for commit with interactive selection."""
    # First, show status
    status = run_git_command(["git", "status", "-s"], check=True)
    if not status or not status.stdout.strip():
        print(Fore.YELLOW + "No changes to stage.")
        return False
    
    print(Fore.CYAN + "Changes to stage:")
    files = status.stdout.strip().split('\n')
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    choice = input(Fore.CYAN + "Options: (1) Stage all, (2) Stage specific files, (3) Back: ").strip()
    
    if choice == "1":
        run_git_command(["git", "add", "."], 
                       error_msg="Failed to stage all changes.",
                       success_msg="All changes staged.")
        return True
    elif choice == "2":
        file_nums = input("Enter file numbers separated by space (e.g., '1 3 5'): ").strip()
        try:
            nums = [int(n) for n in file_nums.split()]
            for num in nums:
                if 1 <= num <= len(files):
                    file_path = files[num-1][3:]  # Skip the status flags
                    run_git_command(["git", "add", file_path], 
                                  error_msg=f"Failed to stage '{file_path}'.",
                                  success_msg=f"Staged '{file_path}'.")
            return True
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter valid file numbers.")
            return False
    else:
        return False

def commit_changes():
    """Commit staged changes."""
    status = run_git_command(["git", "status"], check=True)
    if "nothing to commit" in status.stdout:
        print(Fore.YELLOW + "No changes to commit.")
        if confirm_action("Do you want to stage changes first?"):
            if stage_changes():
                # Re-check if we have changes to commit
                status = run_git_command(["git", "status"], check=True)
                if "nothing to commit" in status.stdout:
                    print(Fore.YELLOW + "Still no changes to commit after staging.")
                    return False
            else:
                return False
        else:
            return False
    
    commit_msg = input(Fore.CYAN + "Enter commit message: ").strip()
    if not commit_msg:
        print(Fore.RED + "Commit message cannot be empty.")
        return False
    
    result = run_git_command(["git", "commit", "-m", commit_msg], 
                           error_msg="Failed to commit changes.",
                           success_msg="Changes committed successfully.")
    
    if result and confirm_action("Do you want to push these changes?"):
        push_changes()
    
    return result is not None

def amend_last_commit():
    """Amend the last commit message or date."""
    print(Fore.CYAN + "Amend options:")
    print("1. Amend commit message")
    print("2. Amend commit date")
    print("3. Amend both message and date")
    print("4. Back")
    
    choice = input("Choose an option: ").strip()
    
    if choice == "1":
        # Show current message
        last_msg = run_git_command(["git", "log", "-1", "--pretty=%B"], check=True)
        print(Fore.CYAN + f"Current message:\n{last_msg.stdout.strip()}")
        
        new_msg = input(Fore.CYAN + "Enter new commit message: ").strip()
        if not new_msg:
            print(Fore.RED + "Commit message cannot be empty.")
            return False
        
        result = run_git_command(["git", "commit", "--amend", "-m", new_msg], 
                               error_msg="Failed to amend commit message.",
                               success_msg="Commit message amended successfully.")
        
        if result and confirm_action("Do you want to force push this amended commit?"):
            run_git_command(["git", "push", "--force-with-lease"], 
                           error_msg="Failed to force push amended commit.",
                           success_msg="Amended commit force-pushed successfully.")
        
        return result is not None
    
    elif choice == "2":
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_date = input(Fore.CYAN + f"Enter new date ({current_date}): ").strip() or current_date
        
        if not validate_date_format(new_date):
            print(Fore.RED + "Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")
            return False
        
        os.environ["GIT_COMMITTER_DATE"] = new_date
        
        result = run_git_command(["git", "commit", "--amend", "--no-edit", "--date", new_date], 
                               error_msg="Failed to amend commit date.",
                               success_msg="Commit date amended successfully.")
        
        if result and confirm_action("Do you want to force push this amended commit?"):
            run_git_command(["git", "push", "--force-with-lease"], 
                           error_msg="Failed to force push amended commit.",
                           success_msg="Amended commit force-pushed successfully.")
        
        return result is not None
    
    elif choice == "3":
        # Amend both message and date
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_date = input(Fore.CYAN + f"Enter new date ({current_date}): ").strip() or current_date
        
        if not validate_date_format(new_date):
            print(Fore.RED + "Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")
            return False
        
        # Show current message
        last_msg = run_git_command(["git", "log", "-1", "--pretty=%B"], check=True)
        print(Fore.CYAN + f"Current message:\n{last_msg.stdout.strip()}")
        
        new_msg = input(Fore.CYAN + "Enter new commit message: ").strip()
        if not new_msg:
            print(Fore.RED + "Commit message cannot be empty.")
            return False
        
        os.environ["GIT_COMMITTER_DATE"] = new_date
        
        result = run_git_command(["git", "commit", "--amend", "-m", new_msg, "--date", new_date], 
                               error_msg="Failed to amend commit message and date.",
                               success_msg="Commit message and date amended successfully.")
        
        if result and confirm_action("Do you want to force push this amended commit?"):
            run_git_command(["git", "push", "--force-with-lease"], 
                           error_msg="Failed to force push amended commit.",
                           success_msg="Amended commit force-pushed successfully.")
        
        return result is not None
    
    else:
        return False

# ==================== Main Menu Functions ====================

def branch_management_menu():
    """Display and handle the branch management menu."""
    while True:
        branches, current_branch = list_branches()
        
        print(Fore.CYAN + "\n===== Branch Management =====")
        print(Fore.YELLOW + f"Current branch: {current_branch}")
        print(Fore.CYAN + "Available local branches:")
        
        for i, branch in enumerate(branches, 1):
            if branch == current_branch:
                print(f"{i}. {branch} " + Fore.GREEN + "(current)")
            else:
                print(f"{i}. {branch}")
        
        print("\nOptions:")
        print("1. Switch to branch")
        print("2. Create new branch")
        print("3. Delete branch")
        print("4. Push changes")
        print("5. Show branch details")
        print("6. Back to main menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":  # Switch branch
            branch_num = input("Enter branch number to switch to: ").strip()
            try:
                idx = int(branch_num) - 1
                if 0 <= idx < len(branches):
                    switch_branch(branches[idx])
                else:
                    print(Fore.RED + "Invalid branch number.")
            except ValueError:
                print(Fore.RED + "Please enter a valid number.")
        
        elif choice == "2":  # Create branch
            branch_name = input("Enter new branch name: ").strip()
            if branch_name:
                create_branch(branch_name)
            else:
                print(Fore.RED + "Branch name cannot be empty.")
        
        elif choice == "3":  # Delete branch
            branch_num = input("Enter branch number to delete: ").strip()
            try:
                idx = int(branch_num) - 1
                if 0 <= idx < len(branches):
                    delete_branch(branches[idx])
                else:
                    print(Fore.RED + "Invalid branch number.")
            except ValueError:
                print(Fore.RED + "Please enter a valid number.")
        
        elif choice == "4":  # Push changes
            push_changes()
        
        elif choice == "5":  # Show branch details
            print(Fore.CYAN + "\nBranch Details:")
            # Get current branch details
            run_git_command(["git", "branch", "-vv"], check=True)
            
            # Show remote branches
            print(Fore.CYAN + "\nRemote Branches:")
            run_git_command(["git", "branch", "-r"], check=True)
            
            # Show recent commits
            print(Fore.CYAN + "\nRecent Commits:")
            run_git_command(["git", "log", "--oneline", "-n", "5"], check=True)
            
            input("\nPress Enter to continue...")
        
        elif choice == "6":  # Back
            return
        
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")

def commit_management_menu():
    """Display and handle the commit management menu."""
    while True:
        print(Fore.CYAN + "\n===== Commit Management =====")
        print("1. Stage changes")
        print("2. Commit changes")
        print("3. Amend last commit")
        print("4. View recent commits")
        print("5. Back to main menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":  # Stage changes
            stage_changes()
        
        elif choice == "2":  # Commit changes
            commit_changes()
        
        elif choice == "3":  # Amend last commit
            amend_last_commit()
        
        elif choice == "4":  # View recent commits
            num_commits = input("Number of commits to view [10]: ").strip() or "10"
            try:
                num = int(num_commits)
                print(Fore.CYAN + f"\nLast {num} commits:")
                run_git_command(["git", "log", f"-{num}", "--pretty=format:%h %ad | %s%d [%an]", "--graph", "--date=short"], 
                              check=True)
                input("\nPress Enter to continue...")
            except ValueError:
                print(Fore.RED + "Please enter a valid number.")
        
        elif choice == "5":  # Back
            return
        
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")

def main_menu():
    """Display and handle the main menu."""
    while True:
        current_branch = get_current_branch()
        
        print(Fore.CYAN + "\n===== Git Helper Tool =====")
        print(Fore.YELLOW + f"Current branch: {current_branch}")
        print(Fore.CYAN + "1. Branch Management")
        print("2. Commit Management")
        print("3. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            branch_management_menu()
        elif choice == "2":
            commit_management_menu()
        elif choice == "3":
            print(Fore.GREEN + "Exiting Git Helper Tool. Goodbye!")
            sys.exit(0)
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")

# ==================== Main Entry Point ====================

if __name__ == "__main__":
    check_git_installed()
    
    # Check if inside a Git repository
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Not inside a Git repository. Please run this script from within a Git project.")
        sys.exit(1)
    
    # Display header
    print(Fore.GREEN + """
  ____ _ _       _   _      _                  
 / ___(_) |_    | | | | ___| |_ __   ___ _ __ 
| |  _| | __|   | |_| |/ _ \ | '_ \ / _ \ '__|
| |_| | | |_    |  _  |  __/ | |_) |  __/ |   
 \____|_|\__|___|_| |_|\___|_| .__/ \___|_|   
           |_____|           |_|              
    """)
    print(Fore.CYAN + "A streamlined git workflow helper focused on branch and commit management")
    print(Fore.YELLOW + "Version 2.0\n")
    
    main_menu()
