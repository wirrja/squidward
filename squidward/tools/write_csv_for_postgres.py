import os
import csv
from django.conf import settings
from .parsers import SquidLogParser, SquidLogParserGz, PptpLogParser
from ..models import SquidFullData

import locale
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

def find_logs(name):
    """
    Return list of log filenames in
    folder with logs
    """
    list_files = os.listdir(path=settings.SQUID_LOGDIR)
    list_log = list(filter(
        lambda x: '{}'.format(name) in x, list_files))

    return list_log



def select_last_datetime():
    """
    SELECT from DB max(datetime)
    """
    max_datetime = SquidFullData.objects.raw('''
    SELECT 1 as id, max(datetime) as last_datetime
    FROM squidward_squidfulldata
    ''')
    for raw in max_datetime:
        max_datetime = raw.last_datetime
    return max_datetime


def write_csv_header(csv_file, fieldnames):
    # create fieldnames
    with open(csv_file, 'w', newline='') as fcsv:
        writer = csv.DictWriter(fcsv, fieldnames=fieldnames)
        writer.writeheader()


def create_csv_access():
    """
    get max(datetim) from select_last_datetime,
    search it in log, write it into csv
    """
    max_datetime = select_last_datetime()
    list_access_log = find_logs(name='access')
    filenames_dot_gz = []
    filenames_dot_log =[]
    fieldnames = ['datetime', 'duration', 'pptpip', 'size', 'resource']

    write_csv_header(csv_file=settings.CSV_FILE, fieldnames=fieldnames)

    for filename in list_access_log:
        if '.gz' in filename:
            filenames_dot_gz.append(filename)
        else:
            filenames_dot_log.append(filename)


    with open(settings.CSV_FILE, 'a', newline='') as fcsv:
        for filename_gz in filenames_dot_gz:
            big_csv = SquidLogParserGz(settings.SQUID_LOGDIR + filename_gz, max_datetime)
            writer = csv.writer(fcsv)
            writer.writerows(big_csv)

        for filename_log in filenames_dot_log:
            big_csv = SquidLogParser(settings.SQUID_LOGDIR + filename_log, max_datetime)
            writer = csv.writer(fcsv)
            writer.writerows(big_csv)

def create_csv_messages():
    """
    get max(datetim) from select_last_datetime,
    search it in log, write it into csv
    """
    max_datetime = select_last_datetime()
    list_message_log = find_logs(name='message')
    fieldnames = ['datetime', 'pptp_id', 'pptp_ip']

    write_csv_header(csv_file=settings.CSV_FILE_MESSAGES_WHITE, fieldnames=fieldnames)
    write_csv_header(csv_file=settings.CSV_FILE_MESSAGES_GRAY, fieldnames=fieldnames)

    with open(settings.CSV_FILE_MESSAGES_WHITE, 'a', newline='') as fcsv:
        for filename in list_message_log:
            full_path = settings.SQUID_LOGDIR + filename

            big_csv = PptpLogParser(file_txt=full_path,
                type='white', max_datetime=max_datetime)
            writer = csv.writer(fcsv)
            writer.writerows(big_csv)

    with open(settings.CSV_FILE_MESSAGES_GRAY, 'a', newline='') as fcsv:
        for filename in list_message_log:
            full_path = settings.SQUID_LOGDIR + filename
            big_csv = PptpLogParser(file_txt=full_path,
                type='gray', max_datetime=max_datetime)
            writer = csv.writer(fcsv)
            writer.writerows(big_csv)



