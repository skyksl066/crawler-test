#!/usr/bin/env python3
import os
import sys
import paramiko
from datetime import datetime

sftp_host = os.getenv('SFTP_HOST')
sftp_user = os.getenv('SFTP_USER')
sftp_password = os.getenv('SFTP_PASSWORD')
sftp_path = '/home/juicyhot/domains/juicyhothello.com/public_ftp'

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
remote_filename = f'crawler_output_{timestamp}.txt'
remote_path = f'{sftp_path}/{remote_filename}'

transport = paramiko.Transport((sftp_host, 22))
try:
    transport.connect(username=sftp_user, password=sftp_password)
    with paramiko.SFTPClient.from_transport(transport) as sftp:
        sftp.put('crawler_output.txt', remote_path)
        print(f'[SFTP] Upload Success: {remote_filename}')
except Exception as e:
    print(f'[SFTP] Error: {type(e).__name__}: {str(e)}')
    sys.exit(1)
finally:
    transport.close()
