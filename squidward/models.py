from django.db import models
from postgres_copy import CopyManager


class WhiteToDB(models.Model):
    """Модель для таблицы с белыми IP"""
    datetime = models.IntegerField(db_index=True)    # до 38 года :(
    pptp_id = models.IntegerField()
    pptp_ip = models.GenericIPAddressField(protocol='IPv4')
    objects = CopyManager()

    def __repr__(self):
        return 'WhiteToDB {0} {1} {2}'.format(
            self.datetime, self.pptpid, self.pptp_ip
        )


class GrayToDb(models.Model):
    """Модель для таблицы с серыми IP"""
    datetime = models.IntegerField(db_index=True)    # до 38 года :(
    pptp_id = models.IntegerField()
    pptp_ip = models.GenericIPAddressField(protocol='IPv4')
    objects = CopyManager()

    def __repr__(self):
        return 'GrayToDB {0} {1} {2}'.format(
            self.datetime, self.pptp_id, self.pptp_ip
        )


class SquidFullData(models.Model):
    """Модель для таблицы полного лога Squid"""
    datetime = models.IntegerField(db_index=True)    # до 38 года :(
    duration = models.IntegerField()
    pptpip = models.GenericIPAddressField(protocol='IPv4')
    size = models.BigIntegerField()
    resource = models.CharField(max_length=255, blank=True)
    objects = CopyManager()

    def __repr__(self):
        return 'SquidFullData {0} {1} {2} {3} {4}'.format(
            self.datetime, self.duration, self.ip, self.size, self.resource)


class HappinessState(models.Model):
    """Модель для таблицы состояний (ошибки, сакцессы)"""
    datetime = models.IntegerField()        # до 38 года :(
    section = models.CharField(max_length=24)
    message = models.CharField(max_length=50)
    state = models.SmallIntegerField()

    def __repr__(self):
        return 'Successes {0} {1} {2} {3}'.format(
            self.datetime, self.section, self.message, self.state)






