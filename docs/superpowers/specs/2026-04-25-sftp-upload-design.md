# SFTP Upload Migration Design

**Date:** 2026-04-25
**Status:** Approved

## Problem

The current GitHub Actions workflow uses FTP (`ftplib`) to upload crawler results. FTP transmits credentials and data in plaintext, making it less secure. The goal is to migrate to SFTP (SSH File Transfer Protocol) for encrypted transfer.

## Decision

Migrate the "Upload to FTP" step in `.github/workflows/crawler.yml` to use SFTP via `paramiko`, with **password authentication**.

Chosen approach: reuse the already-installed `paramiko` dependency with password-based authentication — the least disruptive change while gaining the security of SSH-encrypted transport.

## Architecture

### What Changes

| Component | Before | After |
|-----------|--------|-------|
| Protocol | FTP (plaintext) | SFTP (SSH-encrypted) |
| Library | `ftplib` (stdlib) | `paramiko` (already installed) |
| Auth | Password | Password (same credential) |
| GitHub Secrets | `FTP_HOST`, `FTP_USER`, `FTP_PASSWORD` | `SFTP_HOST`, `SFTP_USER`, `SFTP_PASSWORD` |

### What Stays the Same

- Crawler logic in `crawler.py` — no changes
- File output format (`crawler_output.txt`)
- Timestamped remote filename (`crawler_output_YYYYMMDD_HHMMSS.txt`)
- Schedule: every 30 minutes via cron

### Target Server

- **Host:** `ftp.juicyhothello.com`
- **User:** `crawler+juicyhothello.com`
- **Port:** 22
- **Remote path:** `/home/juicyhot/domains/juicyhothello.com/public_ftp/`

## Implementation

### GitHub Secrets

Remove old FTP secrets, add:

| Secret | Value |
|--------|-------|
| `SFTP_HOST` | `ftp.juicyhothello.com` |
| `SFTP_USER` | `crawler+juicyhothello.com` |
| `SFTP_PASSWORD` | (your password) |

### Workflow Change

Replace the "Upload to FTP" step in `.github/workflows/crawler.yml`:

```python
import os
import paramiko
from datetime import datetime

sftp_host = os.getenv('SFTP_HOST')
sftp_user = os.getenv('SFTP_USER')
sftp_password = os.getenv('SFTP_PASSWORD')
sftp_path = '/home/juicyhot/domains/juicyhothello.com/public_ftp'

try:
    transport = paramiko.Transport((sftp_host, 22))
    transport.connect(username=sftp_user, password=sftp_password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    remote_filename = f'crawler_output_{timestamp}.txt'
    remote_path = f'{sftp_path}/{remote_filename}'

    sftp.put('crawler_output.txt', remote_path)
    print(f'[SFTP] Upload Success: {remote_filename}')

    sftp.close()
    transport.close()

except Exception as e:
    print(f'[SFTP] Error: {str(e)}')
```

### Step env block

```yaml
- name: Upload via SFTP
  env:
    SFTP_HOST: ${{ secrets.SFTP_HOST }}
    SFTP_USER: ${{ secrets.SFTP_USER }}
    SFTP_PASSWORD: ${{ secrets.SFTP_PASSWORD }}
```

## Error Handling

- Connection failures and upload errors are caught and printed — same pattern as the existing FTP step
- Workflow does not fail-fast on upload errors (non-critical, crawler still ran successfully)

## Out of Scope

- SSH key authentication (selected password auth for simplicity)
- Changes to `crawler.py`
- Changes to the crawl or scheduling logic
