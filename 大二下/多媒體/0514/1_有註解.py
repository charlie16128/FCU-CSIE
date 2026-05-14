import cv2
import numpy as np

# 1. 讀取影像
src = cv2.imread("easy.jpg")
src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
ret, dst_binary = cv2.threshold(src_gray, 127, 255, cv2.THRESH_BINARY)

# 2. 尋找輪廓
contours, hierarchy = cv2.findContours(dst_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 遍歷每一個輪廓進行處理
for i in range(len(contours)):
    # 建立一個全黑的底圖
    canvas = np.zeros_like(src)
    
    # 繪製白色輪廓 (不塗滿)
    cv2.drawContours(canvas, contours, contourIdx=i, color=(255, 255, 255), thickness=2)

    # 計算外接矩形
    x, y, w, h = cv2.boundingRect(contours[i])
    
    # 繪製綠色外接矩形
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # 在個別視窗的矩形上方顯示紅色索引值
    cv2.putText(canvas, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # 顯示個別視窗
    cv2.imshow(f"contours{i}", canvas)

    # --- 處理原始圖 (src) ---
    # 在原圖的對應位置也繪製上相同的索引編號 (紅色)
    cv2.putText(src, str(i), (x + (w//2) - 10, y + (h//2) + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# 顯示標註了編號的原圖
cv2.imshow("src", src)

cv2.waitKey(0)
cv2.destroyAllWindows()