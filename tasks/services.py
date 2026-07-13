from django.db import transaction
from .models import Task

ALLOWED_STATUS_TRANSITIONS = {
    Task.STATUS_TODO: [Task.STATUS_IN_PROGRESS],
    Task.STATUS_IN_PROGRESS: [Task.STATUS_DONE],
    Task.STATUS_DONE: [],
}

def validate_status_transition(old_status, new_status):
    if new_status not in ALLOWED_STATUS_TRANSITIONS[old_status]:
        raise ValueError("Invalid task status transition")


@transaction.atomic
def change_task_status(*, task, new_status):
    validate_status_transition(task.status, new_status)
    task.status = new_status
    task.save(update_fields=['status'])
    return task
