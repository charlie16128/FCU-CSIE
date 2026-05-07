import cv2
import numpy as np

# ==========================================
# 1. 準備辨識模型 (KNN 演算法)
# ==========================================
# KNN (K-Nearest Neighbors) 是一種「愛屋及烏」的分類法。
# 當丟入一個新數字，它會去資料庫找「最像的幾個鄰居」來投票決定這是哪個數字。
try:
    with np.load('knn_digit.npz') as data:
        train = data['train']          # 訓練集：電腦看過的數字特徵
        train_labels = data['train_labels']  # 標籤：這些特徵對應的是哪個數字
except FileNotFoundError:
    print("錯誤：找不到 knn_digit.npz 模型檔！")
    exit()

# 初始化 KNN 並將訓練數據載入記憶體
knn = cv2.ml.KNearest_create()
knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)

# ==========================================
# 2. 影像讀取與增強 (讓隱藏的數字顯現)
# ==========================================
img = cv2.imread('hiddendigits.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 【正規化 Normalize】：
# 原圖極暗 (像素值可能只有 0~10)，這步將其強行拉開到 0~255。
enhanced = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

# 【二值化 Threshold】：
# 設定門檻，讓影像只剩下「純黑」與「純白」。
# 這能去除背景雜訊，讓數字變成乾淨的白色塊，方便電腦抓取形狀。
_, thresh = cv2.threshold(enhanced, 50, 255, cv2.THRESH_BINARY)

# 用來畫結果的彩色背景圖
output_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

# ==========================================
# 3. 尋找輪廓 (鎖定每個數字的位置)
# ==========================================
# findContours：找出白色色塊的邊界。
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# boundingRect：用最小的矩形框住每個數字，取得座標 (x, y) 與 寬高 (w, h)。
bounding_boxes = [cv2.boundingRect(c) for c in contours]

# 排序：根據 x 座標由左至右排列，確保輸出順序符合人類閱讀習慣。
sorted_boxes = sorted(bounding_boxes, key=lambda b: b[0])

# ==========================================
# 4. 裁切與特徵正規化 (讓測試圖長得像訓練圖)
# ==========================================
# 這是辨識成功的關鍵！模型習慣看「置中、細筆畫」的手寫字，我們要去適應它。
found_numbers = []
count = 1

print("--- 辨識開始 ---")
for x, y, w, h in sorted_boxes:
    if w > 15 and h > 15:  # 過濾太小的雜訊
        
        # ROI (Region of Interest)：從大圖中裁切出單個數字小圖
        roi = thresh[y:y+h, x:x+w]
        
        # --- 處理置中與比例 (Padding) ---
        max_dim = max(w, h)
        
        # 【Padding 留白】：
        # 建立正方形畫布，並在數字周圍留出 30% 的黑邊。
        # 訓練集通常有大量留白，這步能讓數字比例更正確，避免縮放時變形。
        padding = int(max_dim * 0.3) 
        square_size = max_dim + padding * 2
        square_canvas = np.zeros((square_size, square_size), dtype=np.uint8)
        
        # 將數字置中貼入畫布
        start_x = (square_size - w) // 2
        start_y = (square_size - h) // 2
        square_canvas[start_y:start_y+h, start_x:start_x+w] = roi
        
        # --- 處理粗細 (Erosion 侵蝕) ---
        # 【Erosion 侵蝕】：
        # 使用形態學運算，把白色邊緣「削減」。
        # 電腦字型太粗，模型看不懂，這步是在幫粗體字「瘦身」成手寫細體。
        kernel = np.ones((3, 3), np.uint8)
        thinned_canvas = cv2.erode(square_canvas, kernel, iterations=2)
        
        # --- 縮放與拉平 ---
        # 統一縮放為 20x20，INTER_AREA 演算法在縮小時能保留最好的特徵。
        roi_resized = cv2.resize(thinned_canvas, (20, 20), interpolation=cv2.INTER_AREA)
        
        # 將 20x20 矩陣拉平成 1x400 的一維陣列，這是模型要求的輸入格式。
        test_data = roi_resized.reshape((1, 400)).astype(np.float32)
        
        # ==========================================
        # 5. KNN 預測與標註
        # ==========================================
        # 【K 值】：找最近的 3 個鄰居投票。
        # 如果 k=1 太草率，k=5 太保守容易被干擾，k=3 是目前的最佳平衡點。
        ret, result, neighbours, dist = knn.findNearest(test_data, k=3)
        digit = int(result[0, 0])
        
        found_numbers.append(digit)
        print(f"{count}. 數字={digit}, 鄰居投票結果={neighbours}")
        count += 1
        
        # 在畫面上繪製綠色方框與紅色的預測數值
        cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(output_img, str(digit), (x, y - 5), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

# ==========================================
# 6. 輸出最終結果
# ==========================================
print(f"\n依順序辨識結果： {found_numbers}")
print(f"辨識數字總合 = {sum(found_numbers)}")

cv2.imshow('Final Result (KNN Detection)', output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()