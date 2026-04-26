# crawler-test 資料夾結構調整設計

**日期：** 2026-04-26
**狀態：** 已確認

## 背景

伺服器 `~/crawlers/` 下目前只有 `logs/` 資料夾。每個爬蟲專案需自行負責建立並管理自己的子目錄。此設計將 `crawler-test` 專案調整為符合此架構。

## 目標伺服器結構

```
~/crawlers/
├── logs/
└── crawler-test/
    ├── crawler.py
    ├── requirements.txt
    ├── run_crawler.sh
    ├── venv/               ← 伺服器本地，不上傳
    └── output/
        └── crawler_output.txt
```

## 變更範圍

### 1. `scripts/ftp_upload.py`

- 登入後呼叫 `ensure_dir(ftp, 'crawler-test')` 嘗試建立目錄（若已存在則忽略 `ftplib.error_perm`）
- 執行 `ftp.cwd('crawler-test')` 切換工作目錄
- 上傳的檔案清單不變（`crawler.py`、`requirements.txt`、`run_crawler.sh`）
- `output/` 目錄由 `run_crawler.sh` 在執行時建立，FTP 不處理

### 2. `run_crawler.sh`

- 加入 `mkdir -p output` 確保輸出目錄存在
- 加入 venv 初始化邏輯：若 `venv/` 不存在則執行 `python3 -m venv venv`
- 透過 `source venv/bin/activate` 啟用虛擬環境後再執行 `pip install` 與 `python3 crawler.py`
- 每個專案各自維護自己的 `venv/`，套件完全隔離

### 3. `crawler.py`

- output 路徑從 `crawler_output.txt` 改為 `output/crawler_output.txt`

## Git 工作流程

- `main` 分支觸發 GitHub Actions 部署，不直接 commit
- 所有新功能開 `feature/xxx` 分支，完成後開 PR 給使用者審核後合併
- Claude 所做的 commit 使用 `--author="Claude <claude@anthropic.com>"` 以便區分

## 不在範圍內

- `logs/` 目錄管理（由使用者或 cron 自行處理）
- 新爬蟲邏輯
- GitHub Actions workflow 變更
