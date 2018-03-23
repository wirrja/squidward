from celery import task
from .tools.write_csv_for_postgres import create_csv_access, create_csv_messages
from .tools.copy_csv_postgresql import copy_csv_postgresql, copy_csv_messages_postgresql
from .tools.delete_old_data import delete_old_data
from .tools.download_logs_sftp import download_logs_sftp




@task
def task_download_logs_sftp():
    download_logs_sftp()

@task
def task_write_csv_postgresql():
    create_csv_messages()
    create_csv_access()


@task
def task_copy_csv_postgresql():
    copy_csv_messages_postgresql()
    copy_csv_postgresql()


@task
def task_delete_old_data():
    delete_old_data()

