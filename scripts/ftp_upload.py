#!/usr/bin/env python3
import os
import sys
import ftplib

files_to_upload = [
    ('app.py', 'app.py'),
    ('requirements.txt', 'requirements.txt'),
    ('run_app.sh', 'run_app.sh'),
]


def ensure_dir(ftp, dirname):
    try:
        ftp.mkd(dirname)
    except ftplib.error_perm as e:
        if not str(e).startswith('550'):
            raise


def main():
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_password = os.getenv('FTP_PASSWORD')
    project_name = os.getenv('GITHUB_REPOSITORY', 'crawler-test').split('/')[-1]

    missing = [k for k, v in {'FTP_HOST': ftp_host, 'FTP_USER': ftp_user, 'FTP_PASSWORD': ftp_password}.items() if not v]
    if missing:
        print(f'[FTP] Missing env vars: {", ".join(missing)}')
        sys.exit(1)

    try:
        with ftplib.FTP(ftp_host) as ftp:
            ftp.login(ftp_user, ftp_password)
            ensure_dir(ftp, project_name)
            ftp.cwd(project_name)
            for local_file, remote_file in files_to_upload:
                with open(local_file, 'rb') as f:
                    ftp.storbinary(f'STOR {remote_file}', f)
                print(f'[FTP] Uploaded: {remote_file}')
        print('[FTP] All files deployed successfully')
    except ftplib.all_errors as e:
        print(f'[FTP] Error: {type(e).__name__}: {str(e)}')
        sys.exit(1)


if __name__ == '__main__':
    main()
