# ==================== Imports and Initialization ====================
# Import necessary modules and initialize settings
import os
import subprocess
from datetime import datetime
from prompt_toolkit import prompt, PromptSession
from colorama import Fore, Style, init

init(autoreset=True)

# Undo Feature
undo_stack = []

def undo_last_action():
    """Undo the last action performed."""
    if not undo_stack:
        print(Fore.YELLOW + "No actions to undo.")
        return

    last_action = undo_stack.pop()
    try:
        subprocess.run(last_action, check=True)
        print(Fore.GREEN + "Successfully undid the last action.")
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to undo the last action.")

# ==================== Utility Functions ====================
# General-purpose utility functions used across the script

def retry_operation(operation, *args, **kwargs):
    """Retry a failed operation with user confirmation."""
    while True:
        try:
            operation(*args, **kwargs)
            break
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
            if not confirm_action("Do you want to retry?"):
                break

def check_git_installed():
    """Check if Git is installed."""
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: Git is not installed. Please install Git and try again.")
        exit(1)

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

def get_default_date():
    """Generate a default date for the user to edit."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def prefill_input(prompt_text, default):
    """Pre-fill the input prompt with a default value that can be edited."""
    return prompt(f"{prompt_text}: ", default=default)

def confirm_action(prompt_text):
    """Ask for confirmation before performing a critical action."""
    while True:
        choice = input(Fore.YELLOW + f"{prompt_text} (y/n or 1/2, or 'b' to go back): ").strip().lower()
        if choice in ["y", "1"]:
            return True
        elif choice in ["n", "2"]:
            return False
        elif choice == "b":
            return "back"
        print(Fore.RED + "Error: Please enter 'y' for yes, 'n' for no, '1' for yes, '2' for no, or 'b' to go back.")

def log_action(action, status="INFO"):
    """Log an action or error to a log file with a timestamp."""
    log_file = os.path.join(os.path.dirname(__file__), 'git_helper.log')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{status}] {action}\n")

def error_message(msg, suggestion=None):
    """Display an error message with an optional suggestion."""
    print(Fore.RED + f"Error: {msg}")
    if suggestion:
        print(Fore.YELLOW + f"Suggestion: {suggestion}")

# ==================== Commit Management ====================
# Functions related to managing commits

def check_and_add_changes_before_commit():
    """Check for uncommitted changes and ask the user if they want to add them before committing."""
    try:
        result = subprocess.run(["git", "status", "--porcelain"], check=True, stdout=subprocess.PIPE, text=True)
        uncommitted_changes = result.stdout.strip()

        if uncommitted_changes:
            print(Fore.YELLOW + "There are uncommitted changes:")
            print(uncommitted_changes)
            choice = input("Do you want to add these changes before committing? (y/n): ").strip().lower()

            if choice in ["y", "yes"]:
                try:
                    subprocess.run(["git", "add", "-A"], check=True)
                    print(Fore.GREEN + "Changes added to the staging area.")
                except subprocess.CalledProcessError:
                    print(Fore.RED + "Error: Unable to add changes to the staging area.")
                    return False
            elif choice in ["n", "no"]:
                print("Proceeding without adding changes.")
            else:
                print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.")
                return check_and_add_changes_before_commit()
        else:
            print(Fore.GREEN + "No uncommitted changes detected.")
        return True

    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to check for uncommitted changes.")
        return False

def get_last_commit_message():
    """Retrieve the last commit message."""
    try:
        result = subprocess.run(["git", "log", "-1", "--pretty=%s"], check=True, stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve the last commit message.")
        exit(1)

def amend_last_commit(date, message):
    if not check_and_add_changes_before_commit():
        return
    os.environ["GIT_COMMITTER_DATE"] = date
    os.environ["GIT_AUTHOR_DATE"] = date

    if not message:
        message = input("Enter the new commit message [leave blank to keep the existing message]: ").strip()

    try:
        subprocess.run(["git", "commit", "--amend", "--no-edit", "--date", date, "-m", message], check=True)
        print("Successfully amended the last commit.")
    except subprocess.CalledProcessError:
        print("Error: Unable to amend the last commit.")
        exit(1)

def set_committer_date(date):
    """Set the committer date for the next commit."""
    os.environ["GIT_COMMITTER_DATE"] = date
    os.environ["GIT_AUTHOR_DATE"] = date
    print(f"Committer date set to {date} for the next commit.")

    # Verify that the environment variables are set correctly
    if os.environ.get("GIT_COMMITTER_DATE") != date or os.environ.get("GIT_AUTHOR_DATE") != date:
        print("Error: Failed to set committer date. Please try again.")
        exit(1)
    else:
        print("Environment variables for committer date set successfully.")

def set_committer_date_and_create_new_commit(date):
    if not check_and_add_changes_before_commit():
        return
    os.environ["GIT_COMMITTER_DATE"] = date
    os.environ["GIT_AUTHOR_DATE"] = date

    commit_message = input("Enter the commit message for the new commit: ").strip()
    if not commit_message:
        print("Error: Commit message cannot be empty.")
        exit(1)

    try:
        subprocess.run(["git", "commit", "--allow-empty", "--date", date, "-m", commit_message], check=True)
        print("New commit created successfully.")
    except subprocess.CalledProcessError:
        print("Error: Unable to create a new commit.")
        exit(1)

def view_previous_commits():
    """Display a list of previous commits with numbers."""
    try:
        result = subprocess.run(["git", "log", "--oneline"], check=True, stdout=subprocess.PIPE, text=True)
        commits = result.stdout.strip().split("\n")
        print("\nPrevious commits:")
        for i, commit in enumerate(commits, start=1):
            print(f"{i}. {commit}")
        return commits
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve the commit history.")
        exit(1)

def delete_commit_by_number(commits, commit_number):
    """Delete a specific commit by its number."""
    try:
        commit_hash = commits[commit_number - 1].split()[0]
        subprocess.run(["git", "rebase", "--onto", commit_hash + "^", commit_hash], check=True)
        print(f"Commit {commit_hash} deleted successfully.")
    except IndexError:
        print("Error: Invalid commit number. Please try again.")
    except subprocess.CalledProcessError:
        print(f"Error: Unable to delete commit. Please ensure the number is correct and try again.")
        exit(1)

def push_after_deletion():
    """Push changes to GitHub after deleting commits."""
    while True:
        action = confirm_action("Do you want to push the changes after deleting commits?")
        if action == "back":
            print("Returning to the main menu.")
            return
        if action:
            try:
                subprocess.run(["git", "push", "--force"], check=True)
                print("Changes force pushed successfully.")
            except subprocess.CalledProcessError:
                print("Error: Unable to force push the changes.")
                exit(1)
        break

# ==================== Branch Management ====================
# Functions related to managing branches

def list_branches():
    """List all available branches."""
    try:
        result = subprocess.run(["git", "branch"], check=True, stdout=subprocess.PIPE, text=True)
        branches = result.stdout.strip().split("\n")
        print(Fore.CYAN + "\nAvailable branches:")
        for branch in branches:
            print(branch.strip())
        return [branch.strip() for branch in branches]
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to retrieve branches.")
        return []

def manage_branches():
    """Provide options to manage branches."""
    while True:
        print(Fore.CYAN + "\nBranch Management:")
        print("1. Switch Branch")
        print("2. Create Branch")
        print("3. Delete Branch")
        print("4. Show Branch Info")
        print("5. Back to main menu")
        choice = input("Enter your choice (1/2/3/4/5 or 'b' to go back): ").strip()

        if choice == "1":
            branches = list_branches()
            branch_name = input("Enter the name of the branch to switch to: ").strip()
            if branch_name.lower() == 'b' or choice == "5":
                print("Returning to the main menu.")
                return
            if branch_name not in branches:
                print(Fore.RED + f"Error: '{branch_name}' is not a valid branch.")
                continue
            retry_operation(subprocess.run, ["git", "checkout", branch_name], check=True)
            print(Fore.GREEN + f"Switched to branch '{branch_name}'.")

        elif choice == "2":
            branch_name = input("Enter the name of the new branch: ").strip()
            if branch_name.lower() == 'b' or choice == "5":
                print("Returning to the main menu.")
                return
            retry_operation(subprocess.run, ["git", "checkout", "-b", branch_name], check=True)
            branches = list_branches()
            if branch_name in branches:
                print(Fore.GREEN + f"Branch '{branch_name}' created successfully.")
            else:
                print(Fore.RED + f"Error: Failed to create branch '{branch_name}'.")

        elif choice == "3":
            branches = list_branches()
            branch_name = input("Enter the name of the branch to delete: ").strip()
            if branch_name.lower() == 'b' or choice == "5":
                print("Returning to the main menu.")
                return
            if branch_name not in branches:
                print(Fore.RED + f"Error: '{branch_name}' is not a valid branch.")
                continue
            retry_operation(subprocess.run, ["git", "branch", "-d", branch_name], check=True)
            branches = list_branches()
            if branch_name not in branches:
                print(Fore.GREEN + f"Branch '{branch_name}' deleted successfully.")
            else:
                print(Fore.RED + f"Error: Failed to delete branch '{branch_name}'.")
        elif choice == "4":
            show_branch_info()
        elif choice == "5" or choice.lower() == "b":
            print("Returning to the main menu.")
            return
        else:
            print(Fore.RED + "Invalid choice. Returning to the main menu.")

# ==================== Team Collaboration Tools ====================
# Functions for team collaboration, such as pull requests and remote branches

def list_remote_branches():
    """List all active remote branches (excluding HEAD references)."""
    try:
        result = subprocess.run(["git", "branch", "-r"], check=True, stdout=subprocess.PIPE, text=True)
        branches = result.stdout.strip().split("\n")
        # Filter out HEAD references
        active_branches = [branch.strip() for branch in branches if 'HEAD' not in branch]
        print(Fore.CYAN + "\nActive remote branches:")
        for branch in active_branches:
            print(branch)
        return active_branches
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to retrieve remote branches.")
        return []

def fetch_and_checkout_remote_branch():
    """Fetch and checkout a remote branch."""
    branches = list_remote_branches()
    branch_name = input("Enter the remote branch to checkout (e.g., origin/feature-branch): ").strip()
    if branch_name.lower() == 'b':
        print("Returning to the team tools menu.")
        return
    if branch_name not in branches:
        print(Fore.RED + f"Error: '{branch_name}' is not a valid remote branch.")
        return
    local_branch = branch_name.split('/')[-1]
    try:
        subprocess.run(["git", "checkout", "-b", local_branch, branch_name], check=True)
        print(Fore.GREEN + f"Checked out remote branch '{branch_name}' as local '{local_branch}'.")
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to checkout remote branch.")

def view_pull_requests():
    """View open pull requests using GitHub CLI."""
    try:
        result = subprocess.run(["gh", "pr", "list", "--limit", "10"], check=True, stdout=subprocess.PIPE, text=True)
        print(Fore.CYAN + "\nOpen Pull Requests:")
        print(result.stdout)
    except FileNotFoundError:
        print(Fore.RED + "GitHub CLI (gh) not installed. Install from https://cli.github.com/")
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to retrieve pull requests.")

def show_branch_info():
    """Show info about all branches (last commit, author, subject)."""
    try:
        result = subprocess.run(
            ["git", "for-each-ref", "--format=%(refname:short) | %(authorname) | %(committerdate:relative) | %(subject)", "refs/heads/"],
            check=True, stdout=subprocess.PIPE, text=True
        )
        print(Fore.CYAN + "\nBranch Info (name | author | last commit | subject):")
        print(result.stdout)
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to show branch info.")

def team_tools_menu():
    """Menu for team collaboration tools."""
    while True:
        print(Fore.CYAN + "\nTeam Collaboration Tools:")
        print("1. List Remote Branches")
        print("2. Fetch & Checkout Remote Branch")
        print("3. View Open Pull Requests")
        print("4. Back to main menu")
        choice = input("Enter your choice (1/2/3/4 or 'b' to go back): ").strip()
        if choice == "1":
            list_remote_branches()
        elif choice == "2":
            fetch_and_checkout_remote_branch()
        elif choice == "3":
            view_pull_requests()
        elif choice == "4" or choice.lower() == "b":
            return
        else:
            print(Fore.RED + "Invalid choice.")

# ==================== Quick Actions ====================
# Functions for quick git operations like push, pull, and stash management

def quick_push():
    """Quick git push with feedback."""
    try:
        subprocess.run(["git", "push"], check=True)
        print(Fore.GREEN + "Pushed to remote successfully.")
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Push failed.")

def quick_pull():
    """Quick git pull with feedback."""
    try:
        subprocess.run(["git", "pull"], check=True)
        print(Fore.GREEN + "Pulled from remote successfully.")
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Pull failed.")

def show_stash_list():
    """Show git stash list and allow apply or drop."""
    try:
        result = subprocess.run(["git", "stash", "list"], check=True, stdout=subprocess.PIPE, text=True)
        stashes = result.stdout.strip().split("\n")
        if not stashes or stashes == ['']:
            print(Fore.YELLOW + "No stashes found.")
            return
        print(Fore.CYAN + "\nStash List:")
        for i, stash in enumerate(stashes, 1):
            print(f"{i}. {stash}")
        choice = input("Enter stash number to apply (a), drop (d), or 'b' to go back: ").strip()
        if choice.lower() == 'b':
            return
        try:
            num = int(choice[:-1])
            action = choice[-1].lower()
            if action == 'a':
                subprocess.run(["git", "stash", "apply", f"stash@{{{num-1}}}"], check=True)
                print(Fore.GREEN + f"Applied stash {num}.")
            elif action == 'd':
                subprocess.run(["git", "stash", "drop", f"stash@{{{num-1}}}"], check=True)
                print(Fore.GREEN + f"Dropped stash {num}.")
            else:
                print(Fore.RED + "Invalid action. Use e.g. '1a' to apply or '1d' to drop.")
        except Exception:
            print(Fore.RED + "Invalid input. Use e.g. '1a' to apply or '1d' to drop.")
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to show or manage stashes.")

def show_recent_merges():
    """Show recent merge commits."""
    try:
        result = subprocess.run(["git", "log", "--merges", "--oneline", "-n", "10"], check=True, stdout=subprocess.PIPE, text=True)
        print(Fore.CYAN + "\nRecent merge commits:")
        print(result.stdout)
    except subprocess.CalledProcessError:
        print(Fore.RED + "Error: Unable to show recent merges.")

# ==================== Menu System ====================
# Functions for displaying menus and handling user navigation

def print_help():
    """Display help information for each menu option."""
    print(Fore.YELLOW + "\nHelp - Menu Options:")
    print("1. Commit Management: Manage commits including amending, creating, viewing, and deleting.")
    print("2. Branch Management: Switch, create, delete branches, or show branch info.")
    print("3. Team Collaboration Tools: List remote branches, fetch/checkout remote branches, and view pull requests.")
    print("4. Quick Actions: Perform quick push, pull, stash management, and view recent merges.")
    print("5. Help: Show this help information.")
    print("6. Exit: Exit the script.")

def display_main_menu():
    """Display the main menu with submenus for better organization."""
    while True:
        print(Fore.CYAN + "\n==================== Git Helper Main Menu ====================")
        print("1. Commit Management")
        print("2. Branch Management")
        print("3. Team Collaboration Tools")
        print("4. Quick Actions")
        print("5. Help")
        print("6. Exit")
        print(Fore.CYAN + "============================================================")

        choice = input("Enter your choice (1-6 or 'b' to go back): ").strip()

        if choice == "1":
            display_commit_management_menu()
        elif choice == "2":
            manage_branches()
        elif choice == "3":
            team_tools_menu()
        elif choice == "4":
            display_quick_actions_menu()
        elif choice == "5":
            print_help()
        elif choice == "6":
            if confirm_action("Are you sure you want to exit?"):
                print("Exiting.")
                exit(0)
        elif choice.lower() == "b":
            print("Returning to the previous menu is not applicable here.")
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")

def display_commit_management_menu():
    """Display the commit management submenu."""
    while True:
        print(Fore.CYAN + "\n==================== Commit Management ====================")
        print("1. Amend Last Commit")
        print("2. Create Commit with Custom Date")
        print("3. View Previous Commits")
        print("4. Delete a Commit")
        print("5. Back to Main Menu")
        print(Fore.CYAN + "==========================================================")

        choice = input("Enter your choice (1-5 or 'b' to go back): ").strip()

        if choice == "1":
            default_date = get_default_date()
            date = prefill_input("Enter the new date (YYYY-MM-DD HH:MM:SS)", default_date)
            if validate_date_format(date):
                amend_last_commit(date, None)
            else:
                print(Fore.RED + "Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")
        elif choice == "2":
            default_date = get_default_date()
            date = prefill_input("Enter the new date (YYYY-MM-DD HH:MM:SS)", default_date)
            if validate_date_format(date):
                set_committer_date_and_create_new_commit(date)
            else:
                print(Fore.RED + "Invalid date format. Please use YYYY-MM-DD HH:MM:SS.")
        elif choice == "3":
            view_previous_commits()
        elif choice == "4":
            commits = view_previous_commits()
            try:
                commit_number = input("Enter the number of the commit to delete (or 'b' to go back): ").strip()
                if commit_number.lower() == 'b':
                    continue
                commit_number = int(commit_number)
                delete_commit_by_number(commits, commit_number)
                push_after_deletion()
            except ValueError:
                print(Fore.RED + "Invalid input. Please enter a valid number.")
        elif choice == "5" or choice.lower() == "b":
            return
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")

def display_quick_actions_menu():
    """Display the quick actions submenu."""
    while True:
        print(Fore.CYAN + "\n==================== Quick Actions ====================")
        print("1. Quick Push")
        print("2. Quick Pull")
        print("3. Show Stash List")
        print("4. Show Recent Merges")
        print("5. Back to Main Menu")
        print(Fore.CYAN + "======================================================")

        choice = input("Enter your choice (1-5 or 'b' to go back): ").strip()

        if choice == "1":
            quick_push()
        elif choice == "2":
            quick_pull()
        elif choice == "3":
            show_stash_list()
        elif choice == "4":
            show_recent_merges()
        elif choice == "5" or choice.lower() == "b":
            return
        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")

# ==================== Main Execution ====================
# Entry point for the script
if __name__ == "__main__":
    check_git_installed()

    # Check if inside a Git repository
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: Not inside a Git repository. Please run this script from within a Git project.")
        exit(1)

    display_main_menu()