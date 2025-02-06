from celery import shared_task
from todo.models import Todo

@shared_task
def clear_completed_tasks():
    Todo.objects.filter(done=True).delete()
