from tasks import celery_app


@celery_app.task()
def celery_task_test():
    return [i for i in range(10)]