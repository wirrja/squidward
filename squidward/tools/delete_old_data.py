import datetime
import os
import time
from django.conf import settings
from ..models import SquidFullData
from django.conf import settings
from django.db import connection, transaction


def delete_old_data():
    dt_today = datetime.datetime.now().strftime('%Y %m %d')
    ts_today = int(time.mktime(time.strptime(dt_today, '%Y %m %d')))

    delete_before = int(ts_today - settings.DB_STORE_TIME)

    with connection.cursor() as curs:
        curs.execute('''
                    DELETE FROM squidward_squidfulldata
                    WHERE datetime < %s
                    ''' % (delete_before))
        connection.commit()
    list_files = os.listdir(path=settings.SQUID_LOGDIR)
    list_access = list(filter(lambda x: '{}'.format('acces') in x, list_files))
    list_messages = list(filter(lambda x: '{}'.format('messages') in x, list_files))
    list_delete = list_access + list_messages
    try:
        for file in list_delete:
            os.remove(settings.SQUID_LOGDIR + file)
    except:
        pass


