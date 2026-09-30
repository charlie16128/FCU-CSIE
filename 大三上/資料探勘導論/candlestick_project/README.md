# Candlestick Patterns Discovering

本專案依照 `作業一.md` 的建議方法，針對固定的臺灣 50 成分股完成 K 線型態探索、驗證期參數搜尋、Top 10 鎖定、2026 年樣本外測試、結果圖表與 Tkinter GUI。

目前儲存庫包含完整可執行程式與不需網路的合成資料測試；尚未執行正式 50 檔下載、完整 Grid Search 或正式績效計算，因此不含虛構的市場結果。

## 安裝

建議使用 Python 3.11 以上版本。在 `candlestick_project` 目錄執行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Tkinter 由 Windows 官方 Python 安裝程式提供，不是 pip 套件。

## 時間切分與資料洩漏防護

- 2018-01-01 至 2023-12-31：fit scaler、探索候選型態與聚類。
- 2024-01-01 至 2025-12-31：搜尋五組群組權重與相似度門檻，選出 bullish、bearish 各 10 個 Pattern。
- 2026-01-01 至 2026-12-31：只用鎖定模型進行最終樣本外測試。

2026 資料不會參與 scaler、候選探索、聚類、參數搜尋、資格門檻放寬、去重門檻或 Top 10 選取。

## 執行方式

每個階段都能獨立執行：

```powershell
python main.py --download
python main.py --prepare
python main.py --train
python main.py --validate
python main.py --test
python main.py --gui
python main.py --all
```

- `--download`：下載未調整 OHLCV 與 corporate actions。
- `--prepare`：清理資料、排除公司行動影響區間並計算 10 維特徵。
- `--train`：只用 2018–2023 資料建立 scaler、候選與聚類 centroid。
- `--validate`：只用 2024–2025 資料搜尋參數並鎖定 Top 10。
- `--test`：只用鎖定模型評估 2026 測試股票並產生五張圖。
- `--gui`：唯讀載入既有 Top 10 與測試結果，不會觸發訓練。
- `--all`：依序執行五個資料階段，不會自動開啟 GUI。

正式設定共有 `4^5 = 1024` 組權重與 11 個相似度門檻，也就是 11,264 組參數組合；在 50 檔股票上執行可能需要較長時間。

## 資料處理規則

原始未調整的 `Open/High/Low/Close/Volume`、`Adj Close`、`Dividends` 與 `Stock Splits` 儲存在 `data/raw`。程式不會對價格做 forward fill，並排除 corporate action 當日、前一交易日與後三交易日。

主要輸出位置：

- `data/processed/`：清理後資料與 10 維特徵。
- `data/results/`：候選、Pattern、Validation、Top 10 與 2026 統計。
- `models/`：scaler、最佳參數與鎖定的最終 Pattern。
- `outputs/figures/`：作業要求的五張 PNG。
- `logs/`：每次執行的記錄與放寬門檻警告。

單一股票下載或處理失敗時會記錄錯誤並繼續其他股票；缺少前置產物時會提示應先執行的階段。

## 測試

```powershell
python -m pytest -q
python -m compileall -q src main.py
python main.py --help
```

測試完全使用合成資料，不需要網路連線，也不會開啟 GUI 視窗。

## 投資結果限制

歷史表現不保證未來績效，型態可能過度擬合，市場狀態也可能改變。模擬結果未計入交易成本與滑價；bearish directional profit 是理論放空報酬，未模擬臺灣市場的借券可得性與放空限制。
