# models.py

class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False

    def complete(self):
        """Mark the task as completed."""
        self.completed = True
        print(f"✅ Task '{self.title}' completed.")


class User:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        """Add a task to the user's list."""
        self.tasks.append(task)
        print(f"📌 Task '{task.title}' added to {self.name}.")
        