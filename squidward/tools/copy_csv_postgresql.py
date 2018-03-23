from django.conf import settings
from ..models import SquidFullData, WhiteToDB, GrayToDb


def copy_csv_postgresql():
    data = settings.CSV_FILE
    # SquidFullDataCopy.objects.from_csv(data)
    SquidFullData.objects.from_csv(
        data,
        dict(datetime='datetime',
             duration='duration',
             pptpip='pptpip',
             size='size',
             resource='resource'
        )
    )

def copy_csv_messages_postgresql():
    data = settings.CSV_FILE_MESSAGES_WHITE
    WhiteToDB.objects.from_csv(
        data,
        dict(datetime='datetime',
             pptp_id='pptp_id',
             pptp_ip='pptp_ip'
        )
    )
    data = settings.CSV_FILE_MESSAGES_GRAY
    GrayToDb.objects.from_csv(
        data,
        dict(datetime='datetime',
             pptp_id='pptp_id',
             pptp_ip='pptp_ip'
             )
    )