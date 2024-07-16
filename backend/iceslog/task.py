from typing import List
from celery import shared_task

from iceslog.core.config import settings
from iceslog.utils.scheduler_utils import create_celery



# @celery_app.task
# def celery_periodic_task():
#     print('执行了 Celery 任务')
    
    
# @app.on_event("startup")
# async def app_start():
#     celery_app.conf.beat_schedule = {
#         '每半分钟执行': {
#             'task': 'celery_periodic_task',
#             'schedule': 30.0,
#         },
#     }