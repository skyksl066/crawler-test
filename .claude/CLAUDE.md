# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

Python Web 爬蟲 + GitHub Actions 自動化執行系統。爬蟲定期抓取網頁資料、進行測試驗證，並將結果上傳至 FTP 服務器。

### 核心架構

**crawler.py**
- 主要爬蟲程式，單一入口點
- 功能：HTTP 請求測試、資料處理、結果輸出到本地檔案
- 運行方式：直接執行 `python crawler.py` 或由 GitHub Actions 排程觸發

**GitHub Actions Workflow** (.github/workflows/crawler.yml)
- 排程執行：每 30 分鐘自動運行
- 環境：Ubuntu 最新版 + Python 3.11
- 流程：
  1. 安裝依賴 (requests, paramiko)
  2. 執行 crawler.py
  3. 將結果上傳到 FTP 服務器

### 依賴

核心依賴在 GitHub Actions 中安裝：
- **requests**：HTTP 請求庫
- **paramiko**（FTP 上傳用）

開發時需提前安裝：
```bash
pip install requests paramiko
```

## 常用命令

### 本地開發

**運行爬蟲**
```bash
python crawler.py
```

輸出結果到 `crawler_output.txt`。

**檢查語法**
```bash
python -m py_compile crawler.py
```

### GitHub Actions

**手動觸發工作流程**
在 GitHub Actions 頁面點選「Run workflow」按鈕，或使用 gh CLI：
```bash
gh workflow run crawler.yml
```

## 環境配置

### FTP 上傳設定

爬蟲執行結果會自動上傳至 FTP 服務器。需在 GitHub Secrets 設定以下變數：

| 變數名稱 | 說明 |
|---------|------|
| `FTP_HOST` | FTP 服務器位址 |
| `FTP_USER` | FTP 帳號 |
| `FTP_PASSWORD` | FTP 密碼 |

**設定方式**：
1. GitHub 專案設定 → Secrets and variables → Actions
2. 新增 Repository secrets

### 本地測試 FTP 功能

若需在本地測試 FTP 上傳，建立 `.env` 檔案（不要提交）：
```
FTP_HOST=your_ftp_host
FTP_USER=your_user
FTP_PASSWORD=your_password
```

## 程式碼修改指南

- 新增爬蟲邏輯時，在 `main()` 函式中的相應測試段添加
- 結果輸出格式維持 JSON，便於解析和存檔
- HTTP 請求需設置 timeout（預設 10 秒），防止長時間掛起
- 例外處理：捕捉可預期的錯誤（網路、檔案 I/O），將詳細訊息記錄至輸出結果

## 調試

執行爬蟲並查看詳細輸出：
```bash
python crawler.py 2>&1 | tee debug_output.txt
```

觀察 GitHub Actions 工作流程日誌：
```bash
gh run view --log
```
