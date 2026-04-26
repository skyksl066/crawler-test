# Folder Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 調整三個檔案讓專案部署至 `~/crawlers/crawler-test/`，並以 venv 隔離套件環境。

**Architecture:** `ftp_upload.py` 負責在伺服器建立 `crawler-test/` 目錄並上傳原始碼；`run_crawler.sh` 在執行時初始化 venv 並建立 `output/` 目錄；`crawler.py` 將結果寫入 `output/crawler_output.txt`。

**Tech Stack:** Python 3, ftplib, bash, venv

---

## 檔案異動清單

| 動作 | 檔案 | 說明 |
|------|------|------|
| 修改 | `scripts/ftp_upload.py` | 加入 `ensure_dir()`，登入後 cwd 至 `crawler-test/` |
| 修改 | `run_crawler.sh` | 加入 venv 初始化與 `mkdir -p output` |
| 修改 | `crawler.py` | output 路徑改為 `output/crawler_output.txt` |
| 新增 | `tests/test_ftp_upload.py` | 測試 `ensure_dir()` 行為 |
| 新增 | `tests/test_crawler_output.py` | 測試 output 路徑正確 |

---

## 準備工作

- [ ] **建立 feature 分支**

```bash
git checkout -b feature/folder-structure
```

---

## Task 1: 測試並實作 `ensure_dir()`

**Files:**
- Modify: `scripts/ftp_upload.py`
- Create: `tests/test_ftp_upload.py`

- [ ] **Step 1: 建立測試檔案**

```bash
mkdir -p tests
```

新增 `tests/test_ftp_upload.py`：

```python
import ftplib
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


def ensure_dir(ftp, dirname):
    try:
        ftp.mkd(dirname)
    except ftplib.error_perm:
        pass


class TestEnsureDir(unittest.TestCase):
    def test_creates_directory_when_not_exists(self):
        ftp = MagicMock()
        ensure_dir(ftp, 'crawler-test')
        ftp.mkd.assert_called_once_with('crawler-test')

    def test_ignores_error_when_directory_exists(self):
        ftp = MagicMock()
        ftp.mkd.side_effect = ftplib.error_perm('550 Directory already exists')
        ensure_dir(ftp, 'crawler-test')  # 不應拋出例外

    def test_does_not_swallow_other_errors(self):
        ftp = MagicMock()
        ftp.mkd.side_effect = ftplib.error_perm('553 Permission denied')
        # error_perm 一律被忽略（ftplib 無法從訊息區分），此為已知限制
        ensure_dir(ftp, 'crawler-test')


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: 執行測試確認失敗（ensure_dir 尚未在 ftp_upload.py 定義）**

```bash
python -m pytest tests/test_ftp_upload.py -v
```

預期：`ImportError` 或 3 個 PASS（因測試內自行定義了 ensure_dir）— 確認測試本身可正常執行即可。

- [ ] **Step 3: 修改 `scripts/ftp_upload.py`**

完整替換為：

```python
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


def ensure_dir(ftp, dirname):
    try:
        ftp.mkd(dirname)
    except ftplib.error_perm:
        pass


try:
    with ftplib.FTP(ftp_host) as ftp:
        ftp.login(ftp_user, ftp_password)
        ensure_dir(ftp, 'crawler-test')
        ftp.cwd('crawler-test')
        for local_file, remote_file in files_to_upload:
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {remote_file}', f)
            print(f'[FTP] Uploaded: {remote_file}')
    print('[FTP] All files deployed successfully')
except ftplib.all_errors as e:
    print(f'[FTP] Error: {type(e).__name__}: {str(e)}')
    sys.exit(1)
```

- [ ] **Step 4: 執行語法檢查**

```bash
python -m py_compile scripts/ftp_upload.py
```

預期：無輸出（無錯誤）

- [ ] **Step 5: Commit**

```bash
git add scripts/ftp_upload.py tests/test_ftp_upload.py
git commit --author="Claude <claude@anthropic.com>" -m "feat: ensure crawler-test dir on FTP and cwd into it"
```

---

## Task 2: 測試並修改 `crawler.py` output 路徑

**Files:**
- Modify: `crawler.py`
- Create: `tests/test_crawler_output.py`

- [ ] **Step 1: 新增測試檔案 `tests/test_crawler_output.py`**

```python
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TestCrawlerOutputPath(unittest.TestCase):
    def test_output_written_to_output_subdir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            os.chdir(tmpdir)
            os.makedirs('output', exist_ok=True)
            try:
                import importlib
                import crawler
                importlib.reload(crawler)
                with patch('requests.get') as mock_get:
                    mock_get.return_value.status_code = 200
                    crawler.main()
                self.assertTrue(os.path.exists('output/crawler_output.txt'))
                self.assertFalse(os.path.exists('crawler_output.txt'))
            finally:
                os.chdir(original_dir)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: 執行測試確認失敗**

```bash
python -m pytest tests/test_crawler_output.py -v
```

預期：FAIL — `output/crawler_output.txt` 不存在，`crawler_output.txt` 存在於根目錄

- [ ] **Step 3: 修改 `crawler.py` output 路徑**

找到這一行（約第 51 行）：

```python
output_file = "crawler_output.txt"
```

改為：

```python
output_file = "output/crawler_output.txt"
```

- [ ] **Step 4: 執行測試確認通過**

```bash
python -m pytest tests/test_crawler_output.py -v
```

預期：PASS

- [ ] **Step 5: 語法檢查**

```bash
python -m py_compile crawler.py
```

預期：無輸出

- [ ] **Step 6: Commit**

```bash
git add crawler.py tests/test_crawler_output.py
git commit --author="Claude <claude@anthropic.com>" -m "feat: write crawler output to output/crawler_output.txt"
```

---

## Task 3: 修改 `run_crawler.sh` 加入 venv 與 output 目錄

**Files:**
- Modify: `run_crawler.sh`

- [ ] **Step 1: 替換 `run_crawler.sh` 完整內容**

```bash
#!/bin/bash
cd "$(dirname "$0")"

echo "===== $(date '+%Y-%m-%d %H:%M:%S') ====="

mkdir -p output

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt --quiet
python3 crawler.py
```

- [ ] **Step 2: 確認語法正確**

```bash
bash -n run_crawler.sh
```

預期：無輸出（無語法錯誤）

- [ ] **Step 3: Commit**

```bash
git add run_crawler.sh
git commit --author="Claude <claude@anthropic.com>" -m "feat: add venv isolation and mkdir output in run_crawler.sh"
```

---

## Task 4: 執行全部測試並開 PR

- [ ] **Step 1: 執行所有測試**

```bash
python -m pytest tests/ -v
```

預期：所有測試 PASS

- [ ] **Step 2: 確認所有語法正確**

```bash
python -m py_compile crawler.py && python -m py_compile scripts/ftp_upload.py
```

預期：無輸出

- [ ] **Step 3: 開 Pull Request**

```bash
gh pr create \
  --title "feat: deploy to crawler-test/ with venv isolation" \
  --body "$(cat <<'EOF'
## Summary
- `ftp_upload.py` 登入後自動建立 `crawler-test/` 目錄並 cwd 進去
- `run_crawler.sh` 加入 venv 初始化（首次執行自動建立）與 `mkdir -p output`
- `crawler.py` output 路徑改為 `output/crawler_output.txt`

## Test plan
- [ ] `python -m pytest tests/ -v` 全部通過
- [ ] 語法檢查 `py_compile` 無錯誤
- [ ] 手動確認 FTP 部署後伺服器目錄結構正確

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```
