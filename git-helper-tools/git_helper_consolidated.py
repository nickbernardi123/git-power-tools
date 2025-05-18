#!/usr/bin/env python3
# Consolidated Git Helper Tool

import os
import subprocess
import sys
from datetime import datetime
from colorama import Fore, Style, init
from prompt_toolkit import prompt

init(autoreset=True)  # Initialize colorama for colored output

# ==================== Utility Functions ====================

def log_message(message):
    """Log messages to a file."""
    with open("git_helper.log", "a") as log_file:
        log_file.write(f"{datetime.now()} - {message}\n")

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
        print(Fore.RED + f"Command failed: {e.stderr.strip()}")  # Display full error message
        log_message(f"Error: {e.stderr.strip()}")
        return None

def list_branches():
    """List branches that can be switched to locally or remotely."""
    # Get local branches
    result_local = run_git_command(["git", "branch"], "Failed to list local branches.")
    local_branches = []
    if result_local:
        local_branches = [line.strip().replace("* ", "") for line in result_local.stdout.split("\n") if line.strip()]

    # Get remote branches
    result_remote = run_git_command(["git", "branch", "-r"], "Failed to list remote branches.")
    remote_branches = []
    if result_remote:
        remote_branches = [line.strip().split("/")[-1] for line in result_remote.stdout.split("\n") if line.strip() and "->" not in line]

    # Combine and deduplicate branches
    all_branches = sorted(set(local_branches + remote_branches))
    for i, branch in enumerate(all_branches, 1):
        print(f"{i}. {branch}")
    return local_branches, remote_branches, all_branches

def prompt_push_changes(set_upstream=False, branch_name=None):
    """Prompt the user to push changes to the remote repository."""
    while True:
        push_choice = input("Would you like to push your changes to the remote repository? (y/n): ").strip().lower()
        if push_choice == 'y':
            if set_upstream and branch_name:
                run_git_command(["git", "push", "--set-upstream", "origin", branch_name], f"Failed to push and set upstream for branch {branch_name}.", "Changes pushed and upstream set successfully.")
            else:
                run_git_command(["git", "push"], "Failed to push changes.", "Changes pushed successfully.")
            break
        elif push_choice == 'n':
            print(Fore.YELLOW + "Push skipped.")
            break
        else:
            print(Fore.RED + "Invalid choice. Please enter 'y' or 'n'.")

def fix_tracking_branch(branch_name):
    """Ensure the branch is tracking the correct remote branch."""
    result = run_git_command(["git", "rev-parse", "--abbrev-ref", f"{branch_name}@{{upstream}}"], check=False)
    if result is None:  # No upstream branch is set
        print(Fore.YELLOW + f"Branch '{branch_name}' is not tracking any remote branch.")
        run_git_command(["git", "push", "--set-upstream", "origin", branch_name], f"Failed to set upstream for branch '{branch_name}'.", f"Upstream set for branch '{branch_name}'.")

# ==================== Main Menu Functions ====================

def branch_management_menu():
    """Display and handle the branch management menu."""
    while True:
        print(Fore.CYAN + "\n===== Branch Management =====")
        print("1. List branches")
        print("2. Switch branch")
        print("3. Create new branch")
        print("4. Delete branch")
        print("5. Back")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            list_branches()
        elif choice == "2":
            local_branches, remote_branches, all_branches = list_branches()
            if all_branches:
                branch_num = input("Enter branch number to switch to (or 'b' to go back): ").strip()
                if branch_num.lower() == 'b':
                    continue
                try:
                    branch_index = int(branch_num) - 1
                    if 0 <= branch_index < len(all_branches):
                        branch_name = all_branches[branch_index]
                        run_git_command(["git", "checkout", branch_name], f"Failed to switch to branch {branch_name}.")
                        fix_tracking_branch(branch_name)
                    else:
                        print(Fore.RED + "Invalid branch number.")
                except ValueError:
                    print(Fore.RED + "Please enter a valid number.")
        elif choice == "3":
            branch = input("Enter new branch name (or 'b' to go back): ").strip()
            if branch.lower() == 'b':
                continue
            run_git_command(["git", "checkout", "-b", branch], f"Failed to create branch {branch}.")
            prompt_push_changes(set_upstream=True, branch_name=branch)
        elif choice == "4":
            local_branches, remote_branches, all_branches = list_branches()
            if all_branches:
                branch_num = input("Enter branch number to delete (or 'b' to go back): ").strip()
                if branch_num.lower() == 'b':
                    continue
                try:
                    branch_index = int(branch_num) - 1
                    if 0 <= branch_index < len(all_branches):
                        branch_to_delete = all_branches[branch_index]
                        if branch_to_delete not in local_branches:
                            # Attempt to delete the remote branch
                            run_git_command(["git", "push", "origin", "--delete", branch_to_delete], f"Failed to delete remote branch {branch_to_delete}.")
                        else:
                            # Delete the local branch
                            run_git_command(["git", "branch", "-d", branch_to_delete], f"Failed to delete local branch {branch_to_delete}.")
                            # Push the deletion to the remote repository
                            run_git_command(["git", "push", "origin", ":" + branch_to_delete], f"Failed to push deletion of branch {branch_to_delete} to remote.")
                        prompt_push_changes()
                    else:
                        print(Fore.RED + "Invalid branch number.")
                except ValueError:
                    print(Fore.RED + "Please enter a valid number.")
        elif choice == "5":
            return
        elif choice.lower() == "b":
            return
        else:
            print(Fore.RED + "Invalid choice.")

def commit_management_menu():
    """Display and handle the commit management menu."""
    while True:
        print(Fore.CYAN + "\n===== Commit Management =====\n")
        print("1. Stage changes")
        print("2. Commit changes")
        print("3. Amend last commit")
        print("4. Back")
        print("5. Delete a commit\n")

        choice = input("Enter your choice: ").strip()
        if choice.lower() == "b":
            return
        if choice == "1":
            run_git_command(["git", "add", "-A"], "Failed to stage changes.", "Changes staged successfully.")
        elif choice == "2":
            # Check if there are staged files
            status_result = run_git_command(["git", "status", "--porcelain"], "Failed to check repository status.")
            if status_result and not status_result.stdout.strip():
                print(Fore.YELLOW + "No changes staged for commit. Stage files before committing.")
                continue

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            custom_date = prompt("Enter custom commit date: ", default=current_time)

            commit_message = input("Enter commit message (or 'b' to go back): ").strip()
            if commit_message.lower() == 'b':
                continue
            if commit_message:
                os.environ['GIT_AUTHOR_DATE'] = custom_date
                os.environ['GIT_COMMITTER_DATE'] = custom_date

                run_git_command([
                    "git", "commit", "-m", commit_message
                ], "Failed to commit changes.", "Changes committed successfully.")
                prompt_push_changes()
            else:
                print(Fore.RED + "Commit message cannot be empty.")
        elif choice == "3":
            commit_message = input("Enter new commit message (or 'b' to go back): ").strip()
            if commit_message.lower() == 'b':
                continue
            if commit_message:
                run_git_command(["git", "commit", "--amend", "-m", commit_message], "Failed to amend commit.", "Commit amended successfully.")
                prompt_push_changes()
            else:
                print(Fore.RED + "Commit message cannot be empty.")
        elif choice == "5":
            print(Fore.CYAN + "\n===== Delete a Commit =====\n")
            # List recent commits
            result = run_git_command(["git", "log", "--oneline"], "Failed to list commits.")
            if result:
                commits = result.stdout.strip().split("\n")
                for i, commit in enumerate(commits, 1):
                    print(f"{i}. {commit}")
                print()  # Add spacing after the list

                commit_num = input("Enter the number of the commit to delete (or 'b' to go back): ").strip()
                if commit_num.lower() == 'b':
                    continue
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
                print(Fore.RED + "No commits found.")
            print()  # Add spacing after the operation
        elif choice == "4":
            return
        else:
            print(Fore.RED + "Invalid choice.")

def main_menu():
    """Main menu for the Git Helper Tool."""
    while True:
        print(Fore.CYAN + "\n===== Git Helper Tool =====")
        print("1. Branch Management")
        print("2. Commit Management")
        print("3. Exit")
        print("6. Create a new Git repository\n")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            branch_management_menu()
        elif choice == "2":
            commit_management_menu()
        elif choice == "3":
            print(Fore.GREEN + "Goodbye!")
            sys.exit(0)
        elif choice == "6":
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
        else:
            print(Fore.RED + "Invalid choice.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nExiting Git Helper Tool.")
        sys.exit(0)
