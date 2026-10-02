# K 線型態探索 Word 報告 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 依已核准規格建立一份可編輯、數值正確、版面經逐頁驗證的 `K線型態探索報告.docx`。

**Architecture:** 使用一支暫存的 Python 產生器讀取既有 CSV、JSON、程式設定與圖表，產生報告專用圖表與 Word 文件。所有圖表與表格都由相同輸入資料生成，完成後以結構檢查與 DOCX 轉 PNG 的方式驗證內容及版面。

**Tech Stack:** Codex bundled Python、python-docx、pandas、NumPy、matplotlib、Pillow、LibreOffice 文件渲染器

---

## 檔案配置

- Create: `tmp/report/build_candlestick_report.py`
  - 讀取專案資料、建立報告專用圖表、產生 DOCX、執行數值與結構檢查。
- Create: `tmp/report/assets/program_flow.png`
  - 程式資料流程圖。
- Create: `tmp/report/assets/top10_bullish_report.png`
  - 適合直式頁面的看漲 Top 10 型態圖。
- Create: `tmp/report/assets/top10_bearish_report.png`
  - 適合直式頁面的看跌 Top 10 型態圖。
- Create: `tmp/report/assets/test_2026_report.png`
  - 2026 年有訊號之型態與股票結果圖。
- Create: `K線型態探索報告.docx`
  - 最終交付文件。
- Create: `tmp/report/render/page-*.png`
  - 逐頁版面驗證檔，不交付。

### Task 1: 建立輸入資料與產生器骨架

**Files:**
- Create: `tmp/report/build_candlestick_report.py`

- [ ] **Step 1: 標記 DOCX 建立作業**

Run:

```powershell
& 'C:\Users\ctugm\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe' 'C:\Users\ctugm\.cache\codex-runtimes\codex-primary-runtime\plugins\openai-primary-runtime\plugins\documents\skills\documents\container_tools\mark_artifact_operation_started.mjs' --operation-kind create --expected-output-count 1 --output-format docx
```

Expected: exit code 0. This command must run exactly once immediately before the first authoring command.

- [ ] **Step 2: 建立產生器骨架**

使用 `apply_patch` 建立 Python 檔，定義以下固定路徑與輸入：

```python
ROOT = Path(r"E:\逢甲大學\FCU Git\大三上\資料探勘導論")
PROJECT = ROOT / "candlestick_project"
RESULTS = PROJECT / "data" / "results"
ASSETS = ROOT / "tmp" / "report" / "assets"
OUTPUT = ROOT / "K線型態探索報告.docx"

TOP_BULLISH = RESULTS / "top10_bullish.csv"
TOP_BEARISH = RESULTS / "top10_bearish.csv"
FINAL_MODEL = RESULTS / "final_patterns.json"
TEST_OVERALL = RESULTS / "test_2026_overall_metrics.json"
TEST_SIGNALS = RESULTS / "test_2026_signals.csv"
TEST_PATTERN = RESULTS / "test_2026_pattern_metrics.csv"
TEST_STOCK = RESULTS / "test_2026_stock_metrics.csv"
VALIDATION = RESULTS / "validation_results.csv"
```

產生器須在任何輸入不存在時停止，錯誤訊息列出缺少的絕對路徑。

- [ ] **Step 3: 加入資料一致性檢查**

檢查條件：

```python
assert len(bullish) == 10
assert len(bearish) == 10
assert final_model["weight_preset"] == "shape_first"
assert final_model["cluster_distance_threshold"] == 1.0
assert final_model["similarity_threshold"] == 1.6
assert overall["total_signals"] == 2
assert overall["successful_signals"] == 0
assert overall["overall_accuracy"] == 0.0
```

另檢查 `all_patterns.csv` 為 7,661 列、bullish 為 4,319 列、bearish 為 3,342 列，且 `cluster_size` 合計為 9,246。

- [ ] **Step 4: 執行輸入檢查**

Run:

```powershell
& 'C:\Users\ctugm\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 'E:\逢甲大學\FCU Git\大三上\資料探勘導論\tmp\report\build_candlestick_report.py' --check-inputs
```

Expected: 輸出 `Input validation passed`，exit code 0。

### Task 2: 建立報告專用圖表

**Files:**
- Modify: `tmp/report/build_candlestick_report.py`
- Create: `tmp/report/assets/program_flow.png`
- Create: `tmp/report/assets/top10_bullish_report.png`
- Create: `tmp/report/assets/top10_bearish_report.png`
- Create: `tmp/report/assets/test_2026_report.png`

- [ ] **Step 1: 建立流程圖函式**

以 matplotlib 建立直向流程圖，依序呈現：

```text
yfinance 下載 50 檔股票
資料清理與 corporate action 排除
計算 10 維 K 線特徵
2018 至 2023 候選探索與聚類
2024 至 2025 權重和門檻驗證
選出看漲與看跌各 Top 10
鎖定模型
2026 固定 10 檔樣本外測試
輸出 CSV 圖表與 GUI
```

使用白底、深綠框線、黑字與箭頭，輸出至少 220 dpi。

- [ ] **Step 2: 建立 Top 10 型態圖函式**

讀取 `centroid_raw`，重建前一日與當日兩根相對 K 棒。看漲與看跌分開建立 5 列 2 欄圖，每個子圖顯示型態編號與驗證期平均方向性報酬。避免沿用原始寬圖中標籤過密或遭裁切的版面。

- [ ] **Step 3: 建立 2026 測試圖函式**

只繪製實際出現訊號的兩個型態與兩檔股票，以百分比顯示平均方向性報酬；圖下注明另外 18 個型態與 8 檔測試股票沒有訊號。

- [ ] **Step 4: 產生並檢查圖檔**

Run:

```powershell
& 'C:\Users\ctugm\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 'E:\逢甲大學\FCU Git\大三上\資料探勘導論\tmp\report\build_candlestick_report.py' --assets-only
```

Expected: 四個 PNG 均存在、寬度至少 1,600 px、檔案大小大於 20 KB。

### Task 3: 建立 Word 報告

**Files:**
- Modify: `tmp/report/build_candlestick_report.py`
- Create: `K線型態探索報告.docx`

- [ ] **Step 1: 設定文件樣式**

使用 Letter 直式、0.8 至 0.85 吋邊界。設定：

```text
Title       24 pt 微軟正黑體 黑色
Subtitle    13 pt 微軟正黑體 黑色
Heading 1   16 pt 微軟正黑體 黑色
Heading 2   13 pt 微軟正黑體 黑色
Normal      11 pt 微軟正黑體 黑色 1.25 倍行距
Caption      9 pt 微軟正黑體 深灰色
```

表格使用深綠色表頭、白字、淡綠交錯列、`#D9D9D9` 內外框線，所有儲存格保留足夠內距且不設定固定列高。

- [ ] **Step 2: 建立封面與分節**

封面內容：

```text
K 線型態探索與相似度比對
資料探勘導論作業一

姓名  ____________________
學號  ____________________
日期  2026 年 10 月
```

封面不顯示頁碼。後續頁面從 1 開始顯示置中頁碼。

- [ ] **Step 3: 寫入正文**

依設計規格建立摘要、資料集與處理、10 維特徵、相似度演算法、程式流程、驗證結果、Top 10、2026 測試、投資討論、心得及附錄。公式使用 Word 方程式元素或 Cambria Math 的獨立數學段落，不保留 LaTeX 原文。

- [ ] **Step 4: 加入表格與圖表**

加入：

```text
表 1  資料切分
表 2  十維 K 線特徵
表 3  最終參數
表 4  看漲 Top 10
表 5  看跌 Top 10
表 6  2026 年訊號
圖 1  程式流程
圖 2  看漲 Top 10 K 線型態
圖 3  看跌 Top 10 K 線型態
圖 4  2026 年樣本外績效
```

圖與圖說維持同頁；表格欄寬依資料類型分配，不平均分欄。

- [ ] **Step 5: 儲存並執行內容檢查**

Run:

```powershell
& 'C:\Users\ctugm\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 'E:\逢甲大學\FCU Git\大三上\資料探勘導論\tmp\report\build_candlestick_report.py'
```

Expected: `K線型態探索報告.docx` 存在且大於 250 KB，產生器輸出 `Document validation passed`。

### Task 4: 程式化驗證 Word 內容

**Files:**
- Verify: `K線型態探索報告.docx`

- [ ] **Step 1: 重新開啟 DOCX**

使用 `python-docx` 重新讀取文件，確認可解析且沒有損壞。

- [ ] **Step 2: 核對必要內容**

檢查文件文字包含：

```text
50 檔
104,542
7,661
shape_first
1.6
2 次
0%
-2.82%
```

檢查表 4 與表 5 各有 10 筆資料，表 6 有 2 筆訊號；文件內至少有 4 張圖片。

- [ ] **Step 3: 檢查 OOXML**

開啟 DOCX zip，確認沒有未完成標記、工具引用 token 或空白圖片關係。確認第一節與正文節的頁碼設定不同，且正文節包含頁碼欄位。

### Task 5: 渲染並逐頁檢查

**Files:**
- Verify: `K線型態探索報告.docx`
- Create: `tmp/report/render/page-*.png`

- [ ] **Step 1: 渲染 Word 文件**

Run:

```powershell
& 'C:\Users\ctugm\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' 'C:\Users\ctugm\.codex\plugins\cache\openai-primary-runtime\documents\26.930.11008\skills\documents\render_docx.py' 'E:\逢甲大學\FCU Git\大三上\資料探勘導論\K線型態探索報告.docx' --output_dir 'E:\逢甲大學\FCU Git\大三上\資料探勘導論\tmp\report\render' --emit_pdf
```

Expected: 每頁均產生 `page-N.png`，並產生非空 PDF。

- [ ] **Step 2: 逐頁視覺檢查**

逐頁確認：

- 中文字型正常，無方框或缺字。
- 標題、表格、方程式及圖說沒有截斷或重疊。
- Top 10 圖中的型態編號與報酬可讀。
- 表格沒有擠壓、斷裂或貼邊。
- 頁碼從正文開始，封面無頁碼。
- 沒有因分頁形成大片空白。

- [ ] **Step 3: 修正並重新渲染**

若任何頁面不符合條件，使用 `apply_patch` 修改產生器，重新產生 DOCX，再執行相同渲染命令。最後一次檢查必須涵蓋所有頁面。

### Task 6: 最終交付

**Files:**
- Deliver: `K線型態探索報告.docx`

- [ ] **Step 1: 最終檔案檢查**

確認 DOCX 的完整路徑、檔案大小及最後修改時間，並重新執行產生器的驗證模式。

- [ ] **Step 2: 在 Codex 中開啟文件**

使用 `open_in_codex` 開啟最終 DOCX，方便使用者直接檢視與編輯。

- [ ] **Step 3: 回覆交付結果**

只引用最終 DOCX 一次，不連結中間 PNG 或 PDF。簡要說明已包含作業要求、個人欄位留白及 2026 結果限制。
