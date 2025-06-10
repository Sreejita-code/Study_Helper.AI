from plyer import notification
from core.task_manager import get_due_tasks

def notify_due_tasks():
    due = get_due_tasks()
    for task in due:
        notification.notify(
            title="⏰ Task Reminder",
            message=task['title'],
            timeout=10
        )