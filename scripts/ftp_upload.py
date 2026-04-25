#!/usr/bin/env python3
import os
import sys
import ftplib

ftp_host = os.getenv('FTP_HOST')
ftp_user = os.getenv('FTP_USER')
ftp_password = os.getenv('FTP_PASSWORD')
remote_path = '/home/juicyhot/scripts'

files_to_upload = [
    ('crawler.py', 'crawler.py'),
    ('requirements.txt', 'requirements.txt'),
    ('run_crawler.sh', 'run_crawler.sh'),
]

try:
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_password)

    for local_file, remote_file in files_to_upload:
        with open(local_file, 'rb') as f:
            ftp.storbinary(f'STOR {remote_file}', f)
        print(f'[FTP] Uploaded: {remote_file}')

    ftp.quit()
    print('[FTP] All files deployed successfully')
except Exception as e:
    print(f'[FTP] Error: {type(e).__name__}: {str(e)}')
    sys.exit(1)
