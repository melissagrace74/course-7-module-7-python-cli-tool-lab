import argparse
import json
import sys
import os

# Add the 'lib' directory to sys.path so that Python knows where to look for models.py
sys.path.insert(0, os.path.join(os.getcwd(), 'lib'))

from models import Task, User

# Global dictionary to store users and their tasks
users = {}

# Load users from a JSON file (if exists)
def load_users():
    try:
        with open('users.json', 'r') as file:
            data = json.load(file)
            for username, user_data in data.items():
                user = User(username)
                for task_title in user_data['tasks']:
                    task = Task(task_title)
                    user.add_task(task)
                users[username] = user
    except FileNotFoundError:
        pass  # If no file exists, proceed with an empty dictionary

# Save users to a JSON file
def save_users():
    data = {}
    for username, user in users.items():
        data[username] = {'tasks': [task.title for task in user.tasks]}
    
    with open('users.json', 'w') as file:
        json.dump(data, file)

# Function to add a task for a user
def add_task(args):
    """Add a task for a user."""
    user = users.get(args.user)  # Get the user from the dictionary
    
    # If the user doesn't exist, create a new User object and add to dictionary
    if not user:
        user = User(args.user)
        users[args.user] = user  # Save the user in the global dictionary
    
    task = Task(args.title)  # Create the task
    user.add_task(task)  # Add the task to the user's task list
    save_users()  # Save users to file after modifying

def complete_task(args):
    """Mark a task as complete for a user."""
    user = users.get(args.user)
    
    if not user:
        print("❌ User not found.")
        return

    task = next((task for task in user.tasks if task.title == args.title), None)
    
    if not task:
        print("❌ Task not found.")
        return

    task.complete()  # Mark the task as complete
    save_users()  # Save the changes after completing the task

# CLI entry point
def main():
    load_users()  # Load users from file before running commands

    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers()

    # Subparser for adding tasks
    add_parser = subparsers.add_parser("add-task", help="Add a task for a user")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    # Subparser for completing tasks
    complete_parser = subparsers.add_parser("complete-task", help="Complete a task for a user")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)  # Execute the function associated with the command
    else:
        parser.print_help()  # Print the help if no valid command is provided

    save_users()  # Save users back to file after running the command

if __name__ == "__main__":
    main()
    