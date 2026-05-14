import cv2
import numpy as np

# 1. 讀取影像
src = cv2.imread("Lake.jpg")

# 將影像轉換為灰階，因為 threshold 必須在單通道（灰階）下運作
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

# 2. 二值化處理
# 規則：若灰階值 > 150 變成 255 (白色)，若灰階值 <= 150 變成 0 (黑色)
ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# 3. 製作 dst result：保留天空背景，燈塔以黑色顯示
# 原理：使用 bitwise_and，當 mask 為 255 (白色，即天空) 時保留原圖像素；mask 為 0 (黑色，即燈塔) 時輸出黑色。
dst_result = cv2.bitwise_and(src, src, mask=binary)

# 4. 製作 result (圖片最右側視窗)：保留燈塔，天空變白色
# 原理：複製原圖，並將 binary 遮罩中數值為 255 (也就是天空) 的位置，全部填上白色 (255, 255, 255)
result = src.copy()
result[binary == 255] = (255, 255, 255)

# 顯示所有視窗，名稱對應圖片上的標題
cv2.imshow("src", src)
cv2.imshow("binary", binary)
cv2.imshow("dst result", dst_result)
cv2.imshow("result", result)

cv2.waitKey(0)
cv2.destroyAllWindows()