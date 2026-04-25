# SFTP Upload Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the FTP upload step in GitHub Actions with SFTP via paramiko password authentication.

**Architecture:** Only `.github/workflows/crawler.yml` changes — the FTP step is replaced with a SFTP step using `paramiko.Transport` + `SFTPClient`. The env variables are renamed from `FTP_*` to `SFTP_*` and must also be updated in GitHub Secrets.

**Tech Stack:** Python 3.11, paramiko, GitHub Actions

---

### Task 1: Update workflow — replace FTP step with SFTP

**Files:**
- Modify: `.github/workflows/crawler.yml:30-66`

- [ ] **Step 1: Replace the "Upload to FTP" step**

Open `.github/workflows/crawler.yml` and replace lines 30–66 (the entire "Upload to FTP" step) with:

```yaml
      - name: Upload via SFTP
        env:
          SFTP_HOST: ${{ secrets.SFTP_HOST }}
          SFTP_USER: ${{ secrets.SFTP_USER }}
          SFTP_PASSWORD: ${{ secrets.SFTP_PASSWORD }}
        run: |
          pip install paramiko
          python << 'EOF'
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
EOF
```

- [ ] **Step 2: Verify YAML syntax**

```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/crawler.yml'))" && echo "YAML OK"
```

Expected output:
```
YAML OK
```

- [ ] **Step 3: Verify the embedded Python syntax**

```bash
python -c "
import os
import paramiko
from datetime import datetime
print('Python syntax OK')
"
```

Expected output:
```
Python syntax OK
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/crawler.yml
git commit -m "Migrate upload from FTP to SFTP via paramiko"
git push
```

---

### Task 2: Update GitHub Secrets

> This step is done in the GitHub web UI — not in code.

- [ ] **Step 1: Remove old FTP secrets**

Go to: `GitHub repo → Settings → Secrets and variables → Actions`

Delete these three secrets:
- `FTP_HOST`
- `FTP_USER`
- `FTP_PASSWORD`

- [ ] **Step 2: Add new SFTP secrets**

In the same page, add:

| Name | Value |
|------|-------|
| `SFTP_HOST` | `ftp.juicyhothello.com` |
| `SFTP_USER` | `crawler+juicyhothello.com` |
| `SFTP_PASSWORD` | (your FTP/SFTP password) |

---

### Task 3: Trigger and verify

- [ ] **Step 1: Manually trigger the workflow**

In GitHub: `Actions → Python Crawler Automation → Run workflow`

Or via CLI:
```bash
gh workflow run crawler.yml
```

- [ ] **Step 2: Watch the run**

```bash
gh run watch
```

- [ ] **Step 3: Confirm SFTP upload success in the logs**

In the "Upload via SFTP" step log, you should see:
```
[SFTP] Upload Success: crawler_output_YYYYMMDD_HHMMSS.txt
```

If you see `[SFTP] Error: ...`, check:
- SFTP_PASSWORD is correct
- Port 22 is open on `ftp.juicyhothello.com`
- The remote path `/home/juicyhot/domains/juicyhothello.com/public_ftp` exists and is writable
