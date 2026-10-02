# Java 多執行緒賽馬

這是一個只使用 JDK 與 Swing 的賽馬動畫程式。每匹馬由獨立的 Java `Thread` 執行，每場比賽會重新隨機產生不同速度與 1–3 點體力。第一匹馬完賽後，其他未完賽馬匹會自動消耗體力，每點提供 1 秒、20% 的加速。

## 功能

- 使用者可選擇 2–10 匹馬，預設 5 匹。
- 每匹馬使用不同名稱的獨立執行緒。
- GUI 約以 30 FPS 安全更新，不由背景執行緒直接修改 Swing 元件。
- 下方名次列依完賽順序即時更新。
- 全數完賽後可直接再賽一場，速度與體力會重新隨機。
- 不需要 Maven、圖片資源或第三方套件。

## 專案結構

```text
src/horserace/       程式原始碼
test/horserace/      純 JDK assert 測試
tools/horserace/     GUI 截圖產生工具
screenshots/         作業用 GUI 截圖
REPORT.md            多執行緒與非多執行緒流程討論
```

## 編譯

在專案根目錄以 PowerShell 執行：

```powershell
New-Item -ItemType Directory -Force out | Out-Null
$javaFiles = (Get-ChildItem -Recurse -File src,test,tools -Filter '*.java').FullName
javac -encoding UTF-8 -d out $javaFiles
```

## 執行程式

```powershell
java -cp out horserace.Main
```

操作方式：

1. 在「馬匹數量」選擇 2–10。
2. 按「開始比賽」。
3. 等待下方名次列顯示所有馬匹的完賽順序。
4. 按「再賽一場」開始新的隨機賽事。

## 執行測試

測試必須加上 `-ea` 啟用 Java assertions：

```powershell
java -ea -cp out horserace.HorseRaceTest
```

成功時會顯示：

```text
PASS: 6 horse-race tests
```

## 重新產生 GUI 截圖

以下指令會短暫開啟真正的 Swing 視窗、自動跑完一場比賽，並更新 `screenshots/` 中的三張 PNG：

```powershell
java -cp out horserace.ScreenshotGenerator
```

## 執行緒設計摘要

- `Horse`：每匹馬的 `Runnable`，只更新自己的位置、體力與加速狀態。
- `RaceController`：建立一馬一執行緒，同步保護排名，並保證首匹完賽事件只觸發一次。
- `RaceFrame`：接收賽事事件，使用 EDT 更新控制元件與名次。
- `RacePanel`：只讀取不可變的 `HorseSnapshot` 並用 Java2D 畫出畫面。
