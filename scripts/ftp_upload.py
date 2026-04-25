#!/usr/bin/env python3
import os
import sys
import ftplib
from datetime import datetime

ftp_host = os.getenv('FTP_HOST')
ftp_user = os.getenv('FTP_USER')
ftp_password = os.getenv('FTP_PASSWORD')

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f'crawler_output_{timestamp}.txt'

try:
    ftp = ftplib.FTP(ftp_host)
    ftp.login(ftp_user, ftp_password)
    with open('crawler_output.txt', 'rb') as f:
        ftp.storbinary(f'STOR {filename}', f)
    print(f'[FTP] Upload Success: {filename}')
    ftp.quit()
except Exception as e:
    print(f'[FTP] Error: {type(e).__name__}: {str(e)}')
    sys.exit(1)
