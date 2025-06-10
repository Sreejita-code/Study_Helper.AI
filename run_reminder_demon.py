import schedule
import time
from core.notifier import notify_due_tasks

def reminder_loop():
    schedule.every(1).minutes.do(notify_due_tasks)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    reminder_loop()