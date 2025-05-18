#!/usr/bin/env python3
# Consolidated Git Helper Tool

import os
import subprocess
import sys
from datetime import datetime
from colorama import Fore, Style, init
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import PromptSession

init(autoreset=True)  # Initialize colorama for colored output

# ==================== Utility Functions ====================

def log_message(message):
    """Log messages to a file."""
    with open("git_helper.log", "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

def run_git_command(command, error_msg=None, success_msg=None, check=True):
    """Run a git command with proper error handling and feedback."""
    try:
        # Check if git is installed and in PATH
        try:
            subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(Fore.RED + "Git is not installed or not in the PATH. Please install Git and try again.")
            return None

        # Check if we're in a valid git repository for commands that require it
        if command[0] == "git" and command[1] not in ["init", "--version", "help"]:
            try:
                is_git_repo = subprocess.run(
                    ["git", "rev-parse", "--is-inside-work-tree"], 
                    check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
            except subprocess.CalledProcessError:
                print(Fore.RED + "Current directory is not a Git repository. Initialize a repository first.")
                return None

        # Run the actual command
        result = subprocess.run(command, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Handle success case
        if success_msg and not result.stderr:
            print(Fore.GREEN + success_msg)
        elif result.stderr:
            # Command succeeded but with warnings
            print(Fore.YELLOW + "Command completed with warnings:")
            print(Fore.YELLOW + result.stderr.strip())
            
        return result
        
    except subprocess.CalledProcessError as e:
        if error_msg:
            print(Fore.RED + error_msg)
        
        # Provide more specific error messages based on common git errors
        stderr = e.stderr.strip()
        print(Fore.RED + f"Command failed: {stderr}")
        
        # Log the error for debugging
        log_message(f"Error running command {' '.join(command)}: {stderr}")
        
        # Provide helpful suggestions based on common errors
        if "not a git repository" in stderr.lower():
            print(Fore.YELLOW + "Tip: Initialize a Git repository first with option 6 from the main menu.")
        elif "did not match any file(s) known to git" in stderr.lower():
            print(Fore.YELLOW + "Tip: Make sure the file exists and is tracked by Git.")
        elif "failed to push" in stderr.lower() and "rejected" in stderr.lower():
            print(Fore.YELLOW + "Tip: Try pulling the latest changes first before pushing.")
        elif "permission denied" in stderr.lower():
            print(Fore.YELLOW + "Tip: Check your permissions for this repository or SSH key configuration.")
        
        return None

def list_branches():
    """List branches that can be switched to locally or remotely."""
    # Get current branch
    current_branch = None
    current_result = run_git_command(["git", "branch", "--show-current"], "Failed to get current branch.", check=False)
    if current_result:
        current_branch = current_result.stdout.strip()
    
    # Get local branches
    result_local = run_git_command(["git", "branch"], "Failed to list local branches.", check=False)
    local_branches = []
    if result_local:
        local_branches = [line.strip().replace("* ", "") for line in result_local.stdout.split("\n") if line.strip()]

    # Get remote branches
    result_remote = run_git_command(["git", "branch", "-r"], "Failed to list remote branches.", check=False)
    remote_branches = []
    if result_remote:
        remote_branches = [line.strip().split("/", 1)[-1] for line in result_remote.stdout.split("\n") 
                          if line.strip() and "->" not in line]

    # Combine and deduplicate branches
    all_branches = sorted(set(local_branches + remote_branches))
    
    if not all_branches:
        print(Fore.YELLOW + "No branches found. This might be a new repository.")
        return [], [], []
        
    print(Fore.CYAN + "\nAvailable Branches:\n" + "=" * 20)
    for i, branch in enumerate(all_branches, 1):
        # Format display - show current branch with a star
        if branch == current_branch:
            print(f"{i}. {Fore.GREEN}{branch} (current){Fore.RESET}")
        # Show if it's a local or remote branch
        elif branch in local_branches and branch in remote_branches:
            print(f"{i}. {branch} (local & remote)")
        elif branch in local_branches:
            print(f"{i}. {branch} (local)")
        else:
            print(f"{i}. {branch} (remote)")
            
    return local_branches, remote_branches, all_branches

def prompt_push_changes(set_upstream=False, branch_name=None):
    """Prompt the user to push changes to the remote repository."""
    # Check if a remote is configured
    remote_result = run_git_command(["git", "remote"], check=False)
    if not remote_result or not remote_result.stdout.strip():
        print(Fore.YELLOW + "No remote repository configured.")
        configure = input("Would you like to configure a remote repository now? (y/n): ").strip().lower()
        if configure == 'y':
            remote_name = input("Enter remote name (default 'origin'): ").strip() or "origin"
            remote_url = input("Enter remote URL: ").strip()
            if remote_url:
                run_git_command(["git", "remote", "add", remote_name, remote_url], 
                                f"Failed to add remote '{remote_name}'.",
                                f"Remote '{remote_name}' added successfully.")
            else:
                print(Fore.RED + "Remote URL cannot be empty.")
                return
        else:
            return
    
    # Get current branch
    branch_result = run_git_command(["git", "branch", "--show-current"], check=False)
    current_branch = branch_result.stdout.strip() if branch_result else ""
    
    if not branch_name:
        branch_name = current_branch
    
    # Check if the branch exists on the remote
    branch_exists_on_remote = False
    if branch_name:
        remote_branches_result = run_git_command(["git", "branch", "-r"], check=False)
        if remote_branches_result:
            remote_branches = remote_branches_result.stdout.strip().split("\n")
            branch_exists_on_remote = any(f"origin/{branch_name}" in branch for branch in remote_branches)
    
    while True:
        push_choice = input("Would you like to push your changes to the remote repository? (y/n): ").strip().lower()
        if push_choice == 'y':
            # Set appropriate push command based on branch status
            if set_upstream or (branch_name and not branch_exists_on_remote):
                print(Fore.CYAN + f"Setting up tracking for branch '{branch_name}' to remote...")
                run_git_command(["git", "push", "--set-upstream", "origin", branch_name], 
                               f"Failed to push and set upstream for branch {branch_name}.", 
                               "Changes pushed and upstream set successfully.")
            else:
                push_result = run_git_command(["git", "push"], 
                                             "Failed to push changes.", 
                                             "Changes pushed successfully.")
                
                # If push fails due to divergent branches, offer to force push or pull
                if not push_result:
                    print(Fore.YELLOW + "Push failed. Remote and local branches have diverged.")
                    resolution = input("Would you like to: (1) Force Push (dangerous), (2) Pull then Push, or (3) Cancel?: ").strip()
                    if resolution == "1":
                        confirm = input(Fore.RED + "Warning: Force push will overwrite remote changes. Continue? (y/n): ").strip().lower()
                        if confirm == 'y':
                            run_git_command(["git", "push", "--force"], 
                                          "Failed to force push changes.", 
                                          "Changes force-pushed successfully.")
                    elif resolution == "2":
                        run_git_command(["git", "pull", "--rebase"], 
                                      "Failed to pull changes.", 
                                      "Changes pulled successfully.")
                        run_git_command(["git", "push"], 
                                      "Failed to push changes.", 
                                      "Changes pushed successfully.")
            break
        elif push_choice == 'n':
            print(Fore.YELLOW + "Changes were not pushed to the remote repository.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter 'y' or 'n'.")

def fix_tracking_branch(branch_name):
    """Set up tracking for a branch if not already tracked."""
    # Check if branch exists on remote
    remote_branches_result = run_git_command(["git", "branch", "-r"], check=False)
    if remote_branches_result:
        remote_branches = remote_branches_result.stdout.strip().split("\n")
        if not any(f"origin/{branch_name}" in branch for branch in remote_branches if branch.strip()):
            # Branch doesn't exist on remote, ask to push
            print(Fore.YELLOW + f"Branch '{branch_name}' is not tracked on the remote.")
            track_choice = input("Would you like to push and set tracking? (y/n): ").strip().lower()
            if track_choice == 'y':
                run_git_command(["git", "push", "--set-upstream", "origin", branch_name], 
                               f"Failed to push and set upstream for branch {branch_name}.", 
                               f"Branch '{branch_name}' pushed and tracking set successfully.")
        else:
            # Check if local branch is tracking remote
            tracking_result = run_git_command(["git", "branch", "-vv"], check=False)
            if tracking_result:
                tracking_info = tracking_result.stdout.strip().split("\n")
                current_branch_info = next((line for line in tracking_info if line.strip().startswith("*")), None)
                
                if current_branch_info and "[origin/" not in current_branch_info:
                    print(Fore.YELLOW + f"Branch '{branch_name}' is not tracking its remote counterpart.")
                    run_git_command(["git", "branch", "--set-upstream-to", f"origin/{branch_name}", branch_name], 
                                   f"Failed to set tracking for branch {branch_name}.", 
                                   f"Branch '{branch_name}' is now tracking 'origin/{branch_name}'.")

def check_repo_status():
    """Check and display the current repository status."""
    print(Fore.CYAN + "\n===== Repository Status =====\n")
    
    # Check if we're in a git repository
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                      check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print(Fore.RED + "Current directory is not a Git repository.")
        return False
    
    # Show current branch
    branch_result = run_git_command(["git", "branch", "--show-current"], check=False)
    if branch_result:
        print(Fore.GREEN + f"Current branch: {branch_result.stdout.strip()}")
    
    # Show commit information
    last_commit = run_git_command(["git", "log", "-1", "--oneline"], check=False)
    if last_commit and last_commit.stdout:
        print(Fore.GREEN + f"Last commit: {last_commit.stdout.strip()}")
    else:
        print(Fore.YELLOW + "No commits yet.")
    
    # Show remote information
    remote_result = run_git_command(["git", "remote", "-v"], check=False)
    if remote_result and remote_result.stdout:
        print(Fore.GREEN + "Remote repositories:")
        for line in remote_result.stdout.strip().split("\n"):
            if line:
                print(f"  {line}")
    else:
        print(Fore.YELLOW + "No remote repositories configured.")
    
    # Show modified files
    status_result = run_git_command(["git", "status", "--short"], check=False)
    if status_result and status_result.stdout:
        print(Fore.YELLOW + "\nModified files:")
        for line in status_result.stdout.strip().split("\n"):
            if line:
                print(f"  {line}")
    else:
        print(Fore.GREEN + "\nWorking directory clean.")
    
    input("\nPress Enter to return to the main menu...")
    return True

def configure_remote_menu():
    """Menu for configuring remote repositories."""
    # List current remotes
    remote_result = run_git_command(["git", "remote", "-v"], check=False)
    if remote_result and remote_result.stdout.strip():
        print(Fore.CYAN + "\nCurrent remotes:")
        for line in remote_result.stdout.strip().split("\n"):
            if line:
                print(Fore.GREEN + f"  {line}")
        print()
    else:
        print(Fore.YELLOW + "\nNo remotes configured.\n")
    
    # Define menu options
    options = [
        ("1", "Add a new remote"),
        ("2", "Remove a remote"),
        ("3", "Change remote URL"),
        ("4", "Back")
    ]
    
    # Show menu
    choice = show_simple_menu("Git configure", options)
    
    if choice.lower() == "b" or choice == "4":
        return
    elif choice == "1":
        remote_name = input("Enter remote name (default 'origin'): ").strip() or "origin"
        remote_url = input("Enter remote URL: ").strip()
        if remote_url:
            run_git_command(["git", "remote", "add", remote_name, remote_url], 
                           f"Failed to add remote '{remote_name}'.",
                           f"Remote '{remote_name}' added successfully.")
        else:
            print(Fore.RED + "Remote URL cannot be empty.")
    elif choice == "2":
        remote_name = input("Enter remote name to remove: ").strip()
        if remote_name:
            confirm = input(f"Are you sure you want to remove remote '{remote_name}'? (y/n): ").strip().lower()
            if confirm == 'y':
                run_git_command(["git", "remote", "remove", remote_name], 
                              f"Failed to remove remote '{remote_name}'.",
                              f"Remote '{remote_name}' removed successfully.")
        else:
            print(Fore.RED + "Remote name cannot be empty.")
    elif choice == "3":
        remote_name = input("Enter remote name to change: ").strip()
        if remote_name:
            remote_url = input("Enter new remote URL: ").strip()
            if remote_url:
                run_git_command(["git", "remote", "set-url", remote_name, remote_url], 
                              f"Failed to change URL for remote '{remote_name}'.",
                              f"URL for remote '{remote_name}' changed successfully.")
            else:
                print(Fore.RED + "Remote URL cannot be empty.")
        else:
            print(Fore.RED + "Remote name cannot be empty.")
    else:
        print(Fore.RED + "Invalid choice.")

def show_simple_menu(title, options, show_back=True):
    """
    Display a simple menu with number options and keyboard shortcuts.
    
    Args:
        title (str): The title of the menu.
        options (list): List of (value, label) tuples representing menu options.
        show_back (bool): Whether to show the back option.
        
    Returns:
        The value of the selected option.
    """
    print(Fore.CYAN + f"\n{'=' * 10} {title} {'=' * 10}\n")
    
    # Display options with highlighted shortcuts (always first letter)
    for value, label in options:
        highlighted_label = f"{Fore.GREEN}{label[0]}{Fore.RESET}{label[1:]}"
        print(f"{Fore.YELLOW}{value}{Fore.RESET}. {highlighted_label}")
    
    # Add back option if requested
    if show_back:
        print(f"\n{Fore.YELLOW}b{Fore.RESET}. {Fore.GREEN}B{Fore.RESET}ack")
    
    print()  # Add extra line for spacing
    
    # Create a completer with valid options
    valid_options = [value for value, _ in options]
    shortcuts = [label[0].lower() for _, label in options]
    
    if show_back:
        valid_options.append("b")
    
    all_options = valid_options + shortcuts
    completer = WordCompleter(all_options)
    
    # Create a prompt session with completion
    session = PromptSession(
        completer=completer,
        complete_while_typing=True,
    )

    # Get user choice with completion and handle various input formats
    choice = session.prompt("Enter your choice: ").strip().lower()

    # Check if the input is a shortcut (first letter of an option)
    if choice in shortcuts:
        index = shortcuts.index(choice)
        return valid_options[index]

    return choice

# ==================== Main Menu Functions ====================

def switch_branch():
    """Switch to a selected branch."""
    local_branches, remote_branches, all_branches = list_branches()
    if not all_branches:
        print(Fore.YELLOW + "No branches found. Create a branch first.")
        input("Press Enter to continue...")
        return
        
    branch_num = input("Enter branch number to switch to (or 'b' to go back): ").strip()
    if branch_num.lower() == 'b':
        return
    try:
        branch_index = int(branch_num) - 1
        if 0 <= branch_index < len(all_branches):
            branch_name = all_branches[branch_index]
            
            # Check if there are uncommitted changes
            status = run_git_command(["git", "status", "--porcelain"], check=False)
            if status and status.stdout.strip():
                print(Fore.YELLOW + "Warning: You have uncommitted changes that might be overwritten when switching branches.")
                confirm = input("Do you want to continue anyway? (y/n): ").strip().lower()
                if confirm != 'y':
                    print(Fore.YELLOW + "Branch switch cancelled.")
                    input("Press Enter to continue...")
                    return
            
            run_git_command(["git", "checkout", branch_name], f"Failed to switch to branch {branch_name}.", f"Switched to branch '{branch_name}' successfully.")
            fix_tracking_branch(branch_name)
        else:
            print(Fore.RED + "Invalid branch number.")
    except ValueError:
        print(Fore.RED + "Please enter a valid number.")
    
    input("Press Enter to continue...")

def create_branch():
    """Create a new branch."""
    branch = input("Enter new branch name (or 'b' to go back): ").strip()
    if branch.lower() == 'b':
        return
    
    run_git_command(["git", "checkout", "-b", branch], f"Failed to create branch {branch}.", f"Created and switched to branch '{branch}' successfully.")
    prompt_push_changes(set_upstream=True, branch_name=branch)
    input("Press Enter to continue...")

def delete_branch():
    """Delete a selected branch."""
    local_branches, remote_branches, all_branches = list_branches()
    if all_branches:
        branch_num = input("Enter branch number to delete (or 'b' to go back): ").strip()
        if branch_num.lower() == 'b':
            return
        try:
            branch_index = int(branch_num) - 1
            if 0 <= branch_index < len(all_branches):
                branch_to_delete = all_branches[branch_index]
                
                # Check if we're trying to delete the current branch
                current_branch_result = run_git_command(["git", "branch", "--show-current"], check=False)
                if current_branch_result and current_branch_result.stdout.strip() == branch_to_delete:
                    print(Fore.RED + f"Cannot delete the current branch '{branch_to_delete}'. Switch to another branch first.")
                    input("Press Enter to continue...")
                    return
                
                if branch_to_delete in local_branches:
                    # Delete the local branch
                    run_git_command(["git", "branch", "-d", branch_to_delete], f"Failed to delete local branch {branch_to_delete}.")
                    # Push the deletion to the remote repository
                    run_git_command(["git", "push", "origin", ":" + branch_to_delete], f"Failed to push deletion of branch {branch_to_delete} to remote.")
                
                if branch_to_delete in remote_branches:
                    # Attempt to delete the remote branch
                    run_git_command(["git", "push", "origin", "--delete", branch_to_delete], f"Failed to delete remote branch {branch_to_delete}.")
                
                print(Fore.GREEN + f"Branch '{branch_to_delete}' deleted successfully.")
            else:
                print(Fore.RED + "Invalid branch number.")
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")
    else:
        print(Fore.YELLOW + "No branches found to delete.")
    
    input("Press Enter to continue...")

def stage_changes():
    """Stage changes in the working directory."""
    # Show status before staging
    status_result = run_git_command(["git", "status", "--short"], check=False)
    if status_result and not status_result.stdout.strip():
        print(Fore.YELLOW + "No changes detected in the working directory.")
        input("Press Enter to continue...")
        return
        
    # Show changes before staging
    if status_result:
        print(Fore.CYAN + "\nChanges to be staged:")
        print(status_result.stdout)
        
    # Ask which files to stage
    stage_choice = input("Stage all changes? (y/n/b to go back): ").strip().lower()
    if stage_choice == 'b':
        return
    elif stage_choice == 'y':
        run_git_command(["git", "add", "-A"], "Failed to stage changes.", "All changes staged successfully.")
    else:
        # Interactive staging
        file_path = input("Enter file/path pattern to stage (or '.' for current directory): ").strip()
        if file_path:
            run_git_command(["git", "add", file_path], f"Failed to stage {file_path}.", f"Changes in {file_path} staged successfully.")
    
    input("Press Enter to continue...")

def commit_changes():
    """Commit staged changes."""
    # Check if there are staged files
    status_result = run_git_command(["git", "status", "--porcelain"], "Failed to check repository status.", check=False)
    
    if status_result:
        # Parse status output to detect staged files
        staged_files = [line for line in status_result.stdout.splitlines() 
                       if line.startswith("M ") or line.startswith("A ") or line.startswith("D ")]
        
        if not staged_files:
            print(Fore.YELLOW + "No changes staged for commit. Stage files first.")
            stage_prompt = input("Would you like to stage all changes now? (y/n): ").strip().lower()
            if stage_prompt == 'y':
                run_git_command(["git", "add", "-A"], "Failed to stage changes.", "All changes staged successfully.")
            else:
                input("Press Enter to continue...")
                return

    from datetime import datetime
    import os
    from prompt_toolkit import prompt

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    custom_date = prompt("Enter custom commit date: ", default=current_time)
    
    # Show staged files before committing
    staged_files_result = run_git_command(["git", "diff", "--name-status", "--cached"], check=False)
    if staged_files_result and staged_files_result.stdout:
        print(Fore.CYAN + "\nFiles to be committed:")
        print(staged_files_result.stdout)

    commit_message = input("Enter commit message (or 'b' to go back): ").strip()
    if commit_message.lower() == 'b':
        return
    if commit_message:
        # Set environment variables for author and committer dates
        os.environ['GIT_AUTHOR_DATE'] = custom_date
        os.environ['GIT_COMMITTER_DATE'] = custom_date

        commit_result = run_git_command([
            "git", "commit", "-m", commit_message
        ], "Failed to commit changes.", "Changes committed successfully.")
        
        if commit_result:
            # Show the commit hash
            hash_result = run_git_command(["git", "rev-parse", "HEAD"], check=False)
            if hash_result:
                print(Fore.GREEN + f"Commit hash: {hash_result.stdout.strip()}")
            prompt_push_changes()
    else:
        print(Fore.RED + "Commit message cannot be empty.")
    
    input("Press Enter to continue...")

def amend_commit():
    """Amend the last commit."""
    commit_message = input("Enter new commit message (or 'b' to go back): ").strip()
    if commit_message.lower() == 'b':
        return
    if commit_message:
        run_git_command(["git", "commit", "--amend", "-m", commit_message], "Failed to amend commit.", "Commit amended successfully.")
        prompt_push_changes()
    else:
        print(Fore.RED + "Commit message cannot be empty.")
    
    input("Press Enter to continue...")

def delete_commit():
    """Delete a selected commit by reverting it."""
    print(Fore.CYAN + "\n===== Delete a Commit =====\n")
    result = run_git_command(["git", "log", "--oneline"], "Failed to list commits.")
    if result:
        commits = result.stdout.strip().split("\n")
        if not commits:
            print(Fore.YELLOW + "No commits found in the repository.")
            input("Press Enter to continue...")
            return
            
        for i, commit in enumerate(commits, 1):
            print(f"{i}. {commit}")
        print()  # Add spacing after the list

        commit_num = input("Enter the number of the commit to delete (or 'b' to go back): ").strip()
        if commit_num.lower() == 'b':
            return
        try:
            commit_index = int(commit_num) - 1
            if 0 <= commit_index < len(commits):
                commit_hash = commits[commit_index].split()[0]
                run_git_command(["git", "revert", "--no-commit", commit_hash], f"Failed to delete commit {commit_hash}.", "Commit deleted successfully.")
                run_git_command(["git", "commit", "--amend", "--no-edit"], "Failed to finalize commit deletion.", "Commit history updated successfully.")
            else:
                print(Fore.RED + "Invalid commit number.")
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")
    else:
        print(Fore.RED + "Failed to retrieve commit history. Ensure the repository is initialized and has commits.")
    
    input("Press Enter to continue...")

def branch_management_menu():
    """Display and handle the branch management menu."""
    while True:
        # Verify we're in a git repository before showing branch options
        try:
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print(Fore.RED + "Current directory is not a Git repository. Initialize a repository first.")
            input("Press Enter to continue...")
            return
            
        # Show current branch
        branch_result = run_git_command(["git", "branch", "--show-current"], check=False)
        if branch_result:
            current_branch = branch_result.stdout.strip()
            print(f"{Fore.GREEN}Current branch: {current_branch}{Fore.RESET}")
            
        # Define menu options with descriptive labels
        options = [
            ("1", "List all branches"),
            ("2", "Switch to a branch"),
            ("3", "Create new branch"),
            ("4", "Delete a branch"),
            ("5", "Back to main menu")
        ]
        
        # Show menu with enhanced appearance
        choice = show_simple_menu("Branch Management", options)
        
        if choice == "b" or choice == "5":
            return
        elif choice == "1" or choice == "l":  # L for List
            local_branches, remote_branches, all_branches = list_branches()
            print(f"\n{Fore.CYAN}Found {len(local_branches)} local and {len(remote_branches)} remote branches{Fore.RESET}")
            input("Press Enter to continue...")
        elif choice == "2" or choice == "s":  # S for Switch
            switch_branch()
        elif choice == "3" or choice == "c":  # C for Create
            create_branch()
        elif choice == "4" or choice == "d":  # D for Delete
            delete_branch()
        else:
            print(Fore.RED + "Invalid choice." + Fore.RESET)
            input("Press Enter to continue...")

def commit_management_menu():
    """Display and handle the commit management menu."""
    while True:
        # Check if we're in a git repository
        try:
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print(Fore.RED + "Current directory is not a Git repository. Initialize a repository first.")
            input("Press Enter to continue...")
            return
        
        # Show current branch
        branch_result = run_git_command(["git", "branch", "--show-current"], check=False)
        if branch_result:
            current_branch = branch_result.stdout.strip()
            print(f"{Fore.GREEN}Current branch: {current_branch}{Fore.RESET}")
        
        # Define menu options with descriptive labels
        options = [
            ("1", "Stage changes"),
            ("2", "Commit changes"),
            ("3", "Amend last commit"),
            ("4", "Delete a commit"),
            ("5", "Back to main menu")
        ]
        
        # Show menu with enhanced appearance
        choice = show_simple_menu("Commit Management", options)
        
        if choice == "b" or choice == "5":
            return
        elif choice == "1" or choice == "s":  # S for Stage
            stage_changes()
        elif choice == "2" or choice == "c":  # C for Commit
            commit_changes()
        elif choice == "3" or choice == "a":  # A for Amend
            amend_commit()
        elif choice == "4" or choice == "d":  # D for Delete
            delete_commit()
        else:
            print(Fore.RED + "Invalid choice." + Fore.RESET)
            input("Press Enter to continue...")

def main_menu():
    """Main menu for the Git Helper Tool."""
    while True:
        # Define menu options with first-letter shortcut keys
        options = [
            ("1", "Branch Management"),
            ("2", "Commit Management"),
            ("3", "Repository Status"),
            ("4", "Git configure"),
            ("5", "Make new repository"),
            ("6", "Exit")
        ]
        
        # Clear screen for cleaner look
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except:
            pass  # Fail silently if clearing screen doesn't work
            
        print(f"{Fore.GREEN}Git Helper Tool v1.0{Fore.RESET}")
        print(f"{Fore.YELLOW}Current directory: {os.getcwd()}{Fore.RESET}")
        
        # Check if we're in a git repository
        try:
            subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], 
                          check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            branch_result = run_git_command(["git", "branch", "--show-current"], check=False)
            if branch_result:
                current_branch = branch_result.stdout.strip()
                print(f"{Fore.GREEN}Current branch: {current_branch}{Fore.RESET}")
        except:
            print(f"{Fore.RED}Not in a git repository{Fore.RESET}")
        
        # Show menu with enhanced appearance
        choice = show_simple_menu("Main Menu", options, show_back=False)
        
        # Handle shortcuts: first letter of each option
        if choice == "b":
            print(Fore.YELLOW + "Already at main menu." + Fore.RESET)
            continue
        elif choice == "1" or choice == "b":  # B for Branch
            branch_management_menu()
        elif choice == "2" or choice == "c":  # C for Commit
            commit_management_menu()
        elif choice == "3" or choice == "r":  # R for Repository
            check_repo_status()
        elif choice == "4" or choice == "o":  # O for remote cOnfiguration
            configure_remote_menu()
        elif choice == "5" or choice == "n":  # N for New repository
            create_new_repository()
        elif choice == "6" or choice == "e" or choice == "q":  # E for Exit or Q for Quit
            print(Fore.GREEN + "Thank you for using Git Helper Tool. Goodbye!" + Fore.RESET)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Fore.RESET)
            input("Press Enter to continue...")

def create_new_repository():
    """Create a new Git repository in the current folder."""
    print(Fore.CYAN + "\n===== Create a New Git Repository =====\n")
    confirmation = input("Are you sure you want to initialize a new Git repository in the current folder? (y/n): ").strip().lower()
    if confirmation == 'y':
        result = run_git_command(["git", "init"], "Failed to initialize a new Git repository.", "Git repository initialized successfully.")
        if result:
            # Check for files to commit
            run_git_command(["git", "add", "-A"], "Failed to stage files.", "Files staged successfully.")
            commit_result = run_git_command(["git", "commit", "-m", "Initial commit"], "No files to commit.", "Initial commit created successfully.")
            if not commit_result:
                print(Fore.YELLOW + "No files were found to commit. Add files to your repository and commit them.")

            # Prompt to configure a remote repository
            remote_url = input("Would you like to configure a remote repository? Enter the remote URL (or press Enter to skip): ").strip()
            if remote_url:
                run_git_command(["git", "remote", "add", "origin", remote_url], "Failed to add remote repository.", "Remote repository configured successfully.")
            else:
                print(Fore.YELLOW + "You can configure a remote repository later using 'git remote add origin <url>'.")
    else:
        print(Fore.YELLOW + "Operation canceled.")
    
    input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nExiting Git Helper Tool.")
        sys.exit(0)
