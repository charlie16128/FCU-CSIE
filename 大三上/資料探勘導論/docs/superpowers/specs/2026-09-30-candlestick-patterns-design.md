# Candlestick Patterns Discovering 實作設計

## 目標與本輪範圍

依 `作業一.md` 從零建立 `candlestick_project/` Python 專案，完成可執行的資料下載、清理、特徵工程、候選探索、聚類、Validation 參數搜尋、Top 10 選取、2026 out-of-sample 測試、圖表輸出、Tkinter GUI 與自動化測試。

本輪不下載完整 50 檔正式資料、不執行耗時的正式訓練，也不撰寫作業報告。程式不得偽造正式結果；缺少前置資料或模型時，應明確提示使用者執行正確的前置命令。

## 專案架構

專案放在目前工作目錄下的 `candlestick_project/`。採模組化 CLI pipeline，入口為 `main.py`，支援：

- `--download`：下載並保存原始 OHLCV 與 corporate actions。
- `--prepare`：清理資料並建立 10 維特徵。
- `--train`：以 2018–2023 發現候選並聚類。
- `--validate`：以 2024–2025 搜尋參數並選出 Top 10。
- `--test`：使用鎖定模型評估固定股票的 2026 資料。
- `--gui`：只載入既有模型與結果，顯示 Top 10。
- `--all`：依序執行以上資料探勘階段，不自動啟動 GUI。

實作依 `作業一.md` 建議拆分為設定、資料存取、清理、特徵、候選、聚類、相似度、回測、參數搜尋、Top 10 選擇、2026 測試、視覺化、GUI 與共用工具等單一責任模組。

## 資料與模型流程

1. 下載層保留未調整的 `Open/High/Low/Close/Volume`、`Adj Close`、`Dividends` 與 `Stock Splits`，每檔股票獨立儲存。
2. 清理層排序並去重日期，移除缺失或非法 OHLCV，且排除 corporate action 當日、前一交易日與後三交易日。
3. 特徵層集中實作規格中的 10 維公式與三交易日後報酬，不以未來資料建立任何輸入特徵。
4. 訓練層只用 2018–2023 的有效資料 fit scaler，分別尋找 bullish/bearish candidates，並以 Agglomerative Clustering 建立 centroid。
5. Validation 層只用 2024–2025，搜尋 5 組 group weight 與 0.4–1.4 threshold。距離計算採 NumPy 向量化與分批處理，避免建立不必要的大型三維陣列。
6. 最佳參數決定後，依 occurrence、accuracy、average directional profit 與加權距離去重規則鎖定 bullish/bearish 各 10 個 Pattern。
7. Final test 只讀取鎖定的 scaler、weights、threshold、資格條件與 centroids；2026 不得影響任何模型選擇。

## 輸出與可重現性

- 固定台灣 50 股票清單與至少 10 檔測試清單置於 `config/`。
- 所有重要參數置於 `config/settings.yaml`。
- 中間資料、結果 CSV、模型 JSON/joblib、PNG 與 log 依規格固定路徑保存。
- CSV 使用 UTF-8，日期統一為 `YYYY-MM-DD`，內部報酬使用小數。
- Pattern JSON 保存 standardized centroid、raw centroid、來源日期與 validation metrics。
- GUI 不訓練模型；缺少結果時顯示可採取的前置步驟。

## 錯誤處理

- 單一股票下載或處理失敗時記錄錯誤並繼續其他股票。
- 下載提供有限次 retry；資料欄位缺失、資料量不足、模型檔缺失與輸出不完整都使用具體錯誤訊息。
- cluster 數過少或過多、資格門檻放寬、去重門檻放寬、有效股票不足 50 檔等情形必須記錄 warning。
- 寫入模型與結果前驗證欄位、方向與日期範圍，避免不完整輸出和 data leakage。

## GUI 與圖表

Tkinter 主畫面分為 Bullish Top 10 與 Bearish Top 10。選取 Pattern 後顯示前一日與當日的重建 K 線、10 維特徵、validation metrics 與可用的 2026 metrics。Matplotlib 負責 GUI 嵌入圖與規格要求的 PNG 輸出。

centroid_raw 的 K 線重建只用於相對形狀展示，明確標示為代表性重建圖，不宣稱可還原真實價格。

## 測試策略

- 以人工 OHLCV 驗證 `upper`、`lower`、`body`、`open_style`、`close_style`、`volume_feature`、`trend` 與 `return_3d`。
- 驗證 corporate-action 前一日、當日與後三交易日都被排除。
- 驗證相同向量距離為零、提高特徵權重會增加對應距離、邊界 `distance <= threshold` 可匹配。
- 驗證 scaler 僅 fit 2018–2023，training API 拒絕含 2026 的 discovery 範圍，validation 與 test 時段互斥。
- 以合成資料測試 candidate discovery、聚類、回測統計、資格放寬、排名去重與主要 CLI 串接。

## 完成判準

本輪完成時，專案骨架、所有核心模組、設定檔、固定股票清單、README、requirements、Tkinter GUI 與基本測試都已建立；測試可在不下載正式市場資料的情況下執行。正式 50 檔下載、長時間 Grid Search、2026 實際結果與報告留待後續執行。
