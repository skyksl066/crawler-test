#!/usr/bin/env python3
import os
import sys
import ftplib

ftp_host = os.getenv('FTP_HOST')
ftp_user = os.getenv('FTP_USER')
ftp_password = os.getenv('FTP_PASSWORD')

missing = [k for k, v in {'FTP_HOST': ftp_host, 'FTP_USER': ftp_user, 'FTP_PASSWORD': ftp_password}.items() if not v]
if missing:
    print(f'[FTP] Missing env vars: {", ".join(missing)}')
    sys.exit(1)

files_to_upload = [
    ('crawler.py', 'crawler.py'),
    ('requirements.txt', 'requirements.txt'),
    ('run_crawler.sh', 'run_crawler.sh'),
]

try:
    with ftplib.FTP(ftp_host) as ftp:
        ftp.login(ftp_user, ftp_password)
        for local_file, remote_file in files_to_upload:
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {remote_file}', f)
            print(f'[FTP] Uploaded: {remote_file}')
    print('[FTP] All files deployed successfully')
except ftplib.all_errors as e:
    print(f'[FTP] Error: {type(e).__name__}: {str(e)}')
    sys.exit(1)
