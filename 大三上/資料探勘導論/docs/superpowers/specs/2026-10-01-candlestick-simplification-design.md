# K 線型態專案精簡設計

## 目標

將既有 `candlestick_project/` 從多模組、完整參數搜尋的版本，重整為適合作業展示與說明的精簡版本。保留老師要求的資料下載、10 維特徵、相似度回測、看漲與看跌 Top 10、2026 測試及 GUI；移除不必要的細分模組、龐大 Grid Search、複雜設定層與大量細碎測試。

## 專案結構

手寫程式集中成五個主要 Python 檔案：

- `main.py`：命令列入口與流程控制。
- `config.py`：股票清單、日期範圍、門檻與少量權重方案。
- `data_loader.py`：使用 `yfinance` 下載資料、檢查 OHLCV、排除除權息影響區間。
- `kline_analysis.py`：10 維特徵、候選型態、標準化、聚類去重、相似度、回測、排名與 2026 測試。
- `gui.py`：唯讀顯示 Top 10 與測試結果。

另保留 `requirements.txt`、`README.md` 與一個集中式 `tests/test_core.py`。產生的原始資料、結果 CSV/JSON、圖片與 log 不計入手寫程式檔案數。

## 執行介面

`main.py` 支援以下操作：

- `--download`：下載固定 50 檔股票資料。
- `--analyze`：清理、建立特徵、探索型態、驗證並選出 Top 10。
- `--test`：用鎖定結果測試固定至少 10 檔股票的 2026 資料。
- `--gui`：開啟既有結果，不重新分析。
- `--all`：依序執行下載、分析與測試，不自動開啟 GUI。

## 資料流程

1. 以 `yfinance` 下載 2018 年起的未調整 OHLCV、股利與股票分割資料，每檔股票存成一個 CSV。
2. 排序、去重並移除缺失或非法 OHLCV；除權息當日、前一交易日與後三交易日不可成為 Pattern。
3. 完全依作業公式計算 10 維特徵與三個交易日後報酬。
4. 以 2018–2023 找出三日後上漲超過 5% 或下跌超過 5% 的候選型態，並 fit Z-score 統計值。
5. 分開處理 bullish 與 bearish 候選；使用固定距離門檻的階層式聚類建立代表 centroid，避免大量近似候選重複回測。
6. 以 2024–2025 比較三組可解釋的預設權重：等權重、K 線形狀優先、位置與趨勢優先。每組搭配固定的一小組相似度門檻，不執行 11,264 組完整 Grid Search。
7. 依出現次數、預測正確率與平均方向獲利篩選，再依平均方向獲利排序，選出看漲及看跌各 10 個型態。
8. 將 scaler 統計值、最佳權重、相似度門檻及 Top 10 centroid 存入單一 `final_patterns.json`。
9. 2026 階段只讀取鎖定結果，對固定至少 10 檔股票進行樣本外測試，不重新調整參數。

## 輸出

- `data/results/top10_bullish.csv`
- `data/results/top10_bearish.csv`
- `data/results/test_2026_signals.csv`
- `data/results/test_2026_pattern_metrics.csv`
- `data/results/test_2026_stock_metrics.csv`
- `data/results/test_2026_overall_metrics.json`
- `data/results/final_patterns.json`
- `outputs/figures/top10_bullish.png`
- `outputs/figures/top10_bearish.png`
- `outputs/figures/2026_pattern_performance.png`
- `outputs/figures/2026_stock_performance.png`

GUI 直接讀取上述輸出，顯示兩個 Top 10 清單、代表性兩日 K 線、Validation 指標與可用的 2026 指標。

## 錯誤處理

- 單一股票下載或處理失敗時記錄錯誤並繼續其他股票。
- 正式分析若有效股票少於 50 檔，輸出明確警告。
- 缺少前置資料時，錯誤訊息指出應先執行哪個命令。
- 若符合門檻的型態不足 10 個，依分數補足並記錄警告，不建立多層門檻放寬機制。
- 2026 測試若不足 10 檔有效股票則停止，避免產生不符合題目的結果。

## 測試

`tests/test_core.py` 集中驗證：

- 10 維特徵及三日後報酬公式。
- 除權息影響區間排除。
- 相同向量距離為零、權重影響距離、門檻包含等號。
- Discovery、Validation、2026 三段日期互不洩漏。
- 使用假下載函式驗證一檔失敗不會中斷其餘股票。
- 使用小型合成資料跑完分析與 2026 評估。

GUI 不做自動開窗測試，只測試資料合併與代表 K 線重建函式。

## 移除範圍

新結構驗證通過後，刪除被取代的 `src/` 細分模組、舊 `tests/`、`config/settings.yaml`、舊計畫產生但不再被程式引用的模型檔，以及舊 README 內完整 Grid Search 說明。固定股票清單、使用者資料與可沿用的正式輸出不主動刪除。

## 完成條件

- 五個主要 Python 檔案能完成下載、分析、2026 測試與 GUI 展示。
- `yfinance` 僅負責資料取得，分析可從本地 CSV 重跑。
- 核心測試全部通過。
- `python main.py --help` 可正常執行。
- README 能讓同學用最少步驟安裝與執行。
