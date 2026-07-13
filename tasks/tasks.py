from celery import shared_task

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=10)
def send_task_notification(self, task_id):
    print(f"[NOTIFICATION] Task updated: {task_id}")


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=10)
def send_task_email(self, email):
    print(f"[EMAIL] Notification sent to {email}")
