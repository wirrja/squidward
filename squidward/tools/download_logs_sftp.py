import paramiko
from django.conf import settings



remotepath = settings.SQUID_LOGDIR_REMOTE
remotepath_messages = settings.PPTP_LOGDIR_REMOTE
username = settings.SQUID_USERNAME
password = settings.SQUID_PASSWORD
# local path for both log types and programs
localpath = settings.SQUID_LOGDIR
log_filename = settings.LOG_FILENAME





def download_logs_sftp():
    """

    :return:
    """
    # download squid access.log
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('10.87.250.12', username=username, password=password)
    stdin, stdout, stderr = client.exec_command('cd {} && ls'.format(remotepath))
    sftp = client.open_sftp()
    for line in stdout:
        for logfile in log_filename:
            if logfile in line:
                remote = remotepath + line.rstrip()
                local = localpath + line.rstrip()
                sftp.get(remote, local)




    # download poptop messages.log
    stdin, stdout, stderr = client.exec_command('cd {} && ls'.format(remotepath_messages))
    sftp = client.open_sftp()
    for line in stdout:
        for logfile in log_filename:
            if logfile in line:
                remote = remotepath_messages + line.rstrip()
                local = localpath + line.rstrip()
                sftp.get(remote, local)

    sftp.close()
    client.close()