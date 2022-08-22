"""Defines the Celery app."""
import logging
from typing import List, Dict

from celery import Celery
from celery import current_app 
from celery.signals import after_setup_logger

from augur.application.logs import TaskLogConfig
from augur.application.db.session import DatabaseSession
from augur.tasks.init import redis_db_number, redis_conn_string

start_tasks = ['augur.tasks.start_tasks']

github_tasks = ['augur.tasks.github.contributors.tasks',
                'augur.tasks.github.issues.tasks',
                'augur.tasks.github.pull_requests.tasks',
                'augur.tasks.github.events.tasks',
                'augur.tasks.github.messages.tasks',
                'augur.tasks.github.facade_github.tasks',
                'augur.tasks.github.releases.tasks',
                'augur.tasks.github.repo_info.tasks']

git_tasks = ['augur.tasks.git.facade_tasks']

data_analysis_tasks = ['augur.tasks.data_analysis.message_insights.tasks',
                       'augur.tasks.data_analysis.clustering_worker.tasks',
                       'augur.tasks.data_analysis.discourse_analysis.tasks',
                       'augur.tasks.data_analysis.pull_request_analysis_worker.tasks.py']

tasks = start_tasks + github_tasks + git_tasks + data_analysis_tasks

# initialize the celery app
BROKER_URL = f'{redis_conn_string}{redis_db_number}'
BACKEND_URL = f'{redis_conn_string}{redis_db_number+1}'
celery_app = Celery('tasks', broker=BROKER_URL,
             backend=BACKEND_URL, include=tasks)

#Setting to be able to see more detailed states of running tasks
celery_app.conf.task_track_started = True


def split_tasks_into_groups(augur_tasks: List[str]) -> Dict[str, List[str]]:
    """Split tasks on the celery app into groups.

    Args:
        augur_tasks: list of tasks specified in augur

    Returns
        The tasks so that they are grouped by the module they are defined in
    """
    grouped_tasks = {}

    for task in augur_tasks: 
        task_divided = task.split(".")

        try:
            grouped_tasks[task_divided[-2]].append(task_divided[-1])
        except KeyError:
            grouped_tasks[task_divided[-2]] = [task_divided[-1]]
    
    return grouped_tasks


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(app: Celery, **kwargs):
    """Setup task scheduler.

    Note:
        This is where all task scedules are defined and added the celery beat

    Args:
        app: Celery app

    Returns
        The tasks so that they are grouped by the module they are defined in
    """
    from augur.tasks.start_tasks import start_task
    logger = logging.getLogger(__name__)

    with DatabaseSession(logger) as session:

        collection_interval = session.config.get_value('Tasks', 'collection_interval')
        app.add_periodic_task(collection_interval, start_task.s())


@after_setup_logger.connect
def setup_loggers(*args,**kwargs):
    """Override Celery loggers with our own."""

    all_celery_tasks = list(current_app.tasks.keys())

    augur_tasks = [task for task in all_celery_tasks if 'celery.' not in task]
    
    TaskLogConfig(split_tasks_into_groups(augur_tasks))
