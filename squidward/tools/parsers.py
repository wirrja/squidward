import gzip
import time
import re
from urllib.parse import urlparse
from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')


class SquidLogParser:
    """
    Iterator, takes path_to_file_txt
    with Squid logs, gives formatting string:
    datetime, duration, pptpip, size, resource
    """

    def __init__(self, file, last_datetime=0):
        self.file = file
        self.last_datetime = last_datetime
    def __iter__(self):
        return self.parse_replace()

    def parse_replace(self):
        with open(self.file, 'r', encoding='latin1') as f:
            for line in f:
                line = line.replace('\n', '')
                line = line.split()
                line_0 = int(float(line[0]))
                if line_0 > self.last_datetime and int(line[1]) > 0:
                    check = urlparse(line[6]).hostname
                    if check == None:
                        line[6] = line[6].rsplit(':')[0]
                        line = line_0, line[1], line[2], line[4], line[6]
                    else:
                        line[6] = check
                        line = line_0, line[1], line[2], line[4], line[6]
                    yield line

                else:
                    pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(exc_type, exc_value, traceback)
        return self

    def __str__(self):
        return 'SquidLogParser({}'.format(
            'file')

    def __repr__(self):
        return "SquidLogParser(file='{})".format(
            self.file)


class SquidLogParserGz(SquidLogParser):

    def parse_replace(self):
        with gzip.open(self.file, 'rt', encoding='latin1') as f:
            for line in f:
                line = line.replace('\n', '')
                line = line.split()
                line_0 = int(float(line[0]))
                if line_0 > int(self.last_datetime) and int(line[1]) > 0:
                    check = urlparse(line[6]).hostname
                    if check == None:
                        line[6] = line[6].rsplit(':')[0]
                        line = line_0, line[1], line[2], line[4], line[6]
                    else:
                        line[6] = check
                        line = line_0, line[1], line[2], line[4], line[6]
                    yield line

                else:
                    pass

    def __str__(self):
        return 'SquidLogParserGz({}'.format(
            'file')

    def __repr__(self):
        return "SquidLogParserGz(file='{})".format(
            self.file)


class PptpLogParser:
    """Iterator, takes path_to_file_txt
    with PoPToP logs, gives formatting string
    for import to csv format
    """

    def __init__(self, file_txt, type, max_datetime):
        self.file_txt = file_txt
        self.type = type
        self.max_datetime = max_datetime

    def __iter__(self):
        return self.parse_replace()

    def parse_replace(self):
        """
        :return:
        Logs prepared for convert to csv format
        """
        # re_line = re.compile(self.regexp)

        if self.type == 'white':
            with open(self.file_txt, 'r', encoding='latin1') as f:
                for line in f:
                    re_dateip = re.compile(
                        r'(.+\d+:\d+:\d+).+\[(.+)\].+?Client.*?(\d+\.\d+\.\d+\.\d+)')
                    eq_dateip = re_dateip.findall(line)
                    if eq_dateip:
                        white_date = eq_dateip[0][0]
                        white_id = eq_dateip[0][1]
                        white_ip = eq_dateip[0][2]
                        full_date = datetime.strptime(
                            time.strftime('%Y ') +
                            white_date, '%Y %b  %d %H:%M:%S')
                        full_date = str(full_date)
                        timestamp = time.mktime(time.strptime(
                            full_date, '%Y-%m-%d %H:%M:%S'))
                        if int(timestamp) > self.max_datetime:
                            yield int(timestamp), white_id, white_ip
                        else:
                            pass



        elif self.type == 'gray':
            with open(self.file_txt, 'r', encoding='latin1') as file:
                for line in file:
                    re_dateip = re.compile(
                        r'(.+\d+:\d+:\d+).+\[(.+)\].+?remote.*?(\d+\.\d+\.\d+\.\d+)')
                    eq_dateip = re_dateip.findall(line)
                    if eq_dateip:
                        gray_date = eq_dateip[0][0]
                        gray_id = int(eq_dateip[0][1]) - 1
                        gray_ip = eq_dateip[0][2]
                        full_date = datetime.strptime(
                            time.strftime('%Y ') +
                            gray_date, '%Y %b  %d %H:%M:%S')
                        full_date = str(full_date)
                        timestamp = time.mktime(time.strptime(
                            full_date, '%Y-%m-%d %H:%M:%S'))
                        if int(timestamp) > self.max_datetime:
                            yield int(timestamp), str(gray_id), gray_ip
                        else:
                            pass


        else:
            pass


    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(exc_type, exc_value, traceback)
        return self

    def __str__(self):
        return 'MessagesReadNew({}, {}, {})'.format(
            'file_txt', 'type', 'max_datetime')

    def __repr__(self):
        return "MessagesReadNew(file_txt='{}, type='{}', 'max_datetime='{}')".format(
            self.file_txt, self.type, self.max_datetime)
