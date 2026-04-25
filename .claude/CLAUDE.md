# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

Python Web 爬蟲 + GitHub Actions 自動部署系統。Push 到 main 分支後，GitHub Actions 自動將原始碼部署至 FTP 服務器；服務器端使用 `run_crawler.sh` 執行爬蟲。

### 核心架構

**crawler.py**
- 主爬蟲程式，執行 HTTP 測試並將結果寫入 `crawler_output.txt`（JSON 格式）
- 測試邏輯新增在 `main()` 中

**scripts/ftp_upload.py**
- 讀取環境變數 `FTP_HOST / FTP_USER / FTP_PASSWORD`，使用標準庫 `ftplib` 上傳原始碼
- 上傳清單：`crawler.py`、`requirements.txt`、`run_crawler.sh`
- 任一環境變數缺失則立即 `sys.exit(1)`

**run_crawler.sh**
- 服務器端執行腳本：`pip3 install -r requirements.txt --quiet` → `python3 crawler.py`
- 執行前自動 `cd` 至腳本所在目錄，日誌含時間戳標頭

**GitHub Actions Workflow** (`.github/workflows/crawler.yml`)
- 觸發條件：push 到 main 分支
- 職責：執行 `scripts/ftp_upload.py`，將原始碼部署到 FTP 服務器
- **不在 CI 中執行爬蟲**，爬蟲由服務器端自行排程呼叫 `run_crawler.sh`

### 依賴

```
requests==2.32.3
```

FTP 上傳使用 Python 標準庫 `ftplib`，無需額外安裝。

## 常用命令

**本地執行爬蟲**
```bash
python crawler.py
```

**語法檢查**
```bash
python -m py_compile crawler.py && python -m py_compile scripts/ftp_upload.py
```

**手動觸發部署（需設定 FTP 環境變數）**
```bash
FTP_HOST=... FTP_USER=... FTP_PASSWORD=... python scripts/ftp_upload.py
```

**手動觸發 GitHub Actions**
```bash
gh workflow run crawler.yml
```

**查看最近執行記錄**
```bash
gh run view --log
```

## 環境配置

GitHub Secrets 需設定：

| 變數 | 說明 |
|------|------|
| `FTP_HOST` | FTP 服務器位址 |
| `FTP_USER` | FTP 帳號 |
| `FTP_PASSWORD` | FTP 密碼 |

本地測試可建立 `.env`（不要提交），搭配 `export` 或 `python-dotenv` 載入。

## 程式碼修改指南

- 新增爬蟲邏輯：在 `crawler.py` 的 `main()` 中新增測試段，並將結果 append 至 `test_results["data"]`
- 輸出格式維持 JSON，欄位包含 `test`（測試名稱）、`result`（PASS/FAIL）、`error`（可選）
- HTTP 請求一律設定 `timeout=10`
- 若需在服務器部署新檔案，更新 `scripts/ftp_upload.py` 的 `files_to_upload` 清單
