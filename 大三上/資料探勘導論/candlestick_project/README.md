# K 線型態探索作業

本專案使用 `yfinance` 下載固定 50 檔臺灣股票資料，依老師指定的 10 個特徵找出看漲與看跌 K 線型態，再以 2026 年資料進行樣本外測試。

程式刻意維持精簡，主要只有五個 Python 檔案：

- `config.py`：股票、日期與少量參數。
- `data_loader.py`：下載與清理資料。
- `kline_analysis.py`：特徵、相似度、回測與圖表。
- `gui.py`：顯示已產生的結果。
- `main.py`：執行入口。

## 安裝

建議使用 Python 3.11 以上版本。在 `candlestick_project` 目錄執行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Tkinter 由 Windows 官方 Python 安裝程式提供，不是 pip 套件。

## 執行方式

依序執行：

```powershell
python main.py --download
python main.py --analyze
python main.py --test
python main.py --gui
```

也可以一次完成前三個資料階段：

```powershell
python main.py --all
```

- `--download`：下載 50 檔未調整 OHLCV、股利與股票分割資料。
- `--analyze`：清理資料、計算特徵、選參數並輸出看漲/看跌 Top 10。
- `--test`：使用鎖定結果測試固定 10 檔股票的 2026 資料。
- `--gui`：唯讀顯示既有結果，不會重新下載或分析。

## 分析流程

```text
yfinance 下載
→ 清理資料與排除除權息日期
→ 計算老師指定的 10 維特徵
→ 2018–2023 找候選並聚類
→ 2024–2025 比較少量權重與門檻
→ 選出看漲與看跌 Top 10
→ 2026 固定 10 檔股票測試
→ CSV、JSON、圖表與 GUI
```

時間切分如下：

- 2018-01-01 至 2023-12-31：fit scaler、探索候選型態與聚類。
- 2024-01-01 至 2025-12-31：比較三組容易解釋的權重與三個相似度門檻，選出 bullish、bearish 各 10 個 Pattern。
- 2026-01-01 至 2026-12-31：只用鎖定模型進行最終樣本外測試。

2026 資料不會參與 scaler、候選探索、聚類、權重或門檻選擇，也不會影響 Top 10。

## 資料處理規則

原始未調整的 `Open/High/Low/Close/Volume`、`Adj Close`、`Dividends` 與 `Stock Splits` 儲存在 `data/raw`。程式不會對價格做 forward fill，並排除 corporate action 當日、前一交易日與後三交易日。

主要輸出：

- `data/raw/`：每檔股票一個原始 CSV。
- `data/results/final_patterns.json`：鎖定的 scaler、權重、門檻與 Top 10。
- `data/results/top10_bullish.csv`、`top10_bearish.csv`。
- `data/results/test_2026_*.csv/json`：2026 測試結果。
- `outputs/figures/`：Top 10 與 2026 比較圖。
- `logs/latest.log`：下載、資料不足與分析訊息。

單一股票下載或處理失敗時會記錄錯誤並繼續其他股票；缺少前置產物時會提示應先執行的階段。

## 測試

```powershell
python -m pytest -q
python -m compileall -q main.py config.py data_loader.py kline_analysis.py gui.py
python main.py --help
```

測試不需要網路連線，也不會開啟 GUI 視窗。

## 投資結果限制

歷史表現不保證未來績效，型態可能過度擬合，市場狀態也可能改變。模擬結果未計入交易成本與滑價；bearish directional profit 是理論放空報酬，未模擬臺灣市場的借券可得性與放空限制。
