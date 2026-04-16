import cv2
import numpy as np

# 回呼函式 (Trackbar 必須要有，但我們可以讓它什麼都不做)
def nothing(x):
    pass

# 1. 基本畫面設定
cv2.namedWindow('edge_tool')

# 3. 建立四個滾動條
cv2.createTrackbar('Low', 'edge_tool', 50, 255, nothing)
cv2.createTrackbar('High', 'edge_tool', 150, 255, nothing)
cv2.createTrackbar('Blur', 'edge_tool', 1, 10, nothing)  # 模糊程度
cv2.createTrackbar('Method', 'edge_tool', 0, 2, nothing) # 0:Canny, 1:Sobel, 2:Laplacian

img = cv2.imread('lena.jpg') # 讀取彩色原圖

while True:
    # 讀取目前 Trackbar 的值
    low = cv2.getTrackbarPos('Low', 'edge_tool')
    high = cv2.getTrackbarPos('High', 'edge_tool')
    blur_val = cv2.getTrackbarPos('Blur', 'edge_tool')
    method = cv2.getTrackbarPos('Method', 'edge_tool')

    # 2. 影像前處理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 模糊處理: Blur size 必須是奇數
    k_size = blur_val * 2 + 1 
    blur_img = cv2.GaussianBlur(gray, (k_size, k_size), 0)

    # 4. 根據 Method 選擇邊緣偵測方法
    if method == 0:
        result = cv2.Canny(blur_img, low, high)
        method_name = "Canny Edge"
    elif method == 1:
        # Sobel 通常要取絕對值轉回 uint8
        sobelx = cv2.Sobel(blur_img, cv2.CV_64F, 1, 0, ksize=3)
        result = cv2.convertScaleAbs(sobelx)
        method_name = "Sobel Edge"
    else:
        # Laplacian 同樣要處理位元深度
        lap = cv2.Laplacian(blur_img, cv2.CV_64F)
        result = cv2.convertScaleAbs(lap)
        method_name = "Laplacian Edge"

    # 5. 畫面顯示 (拼圖)
    # 注意：拼圖前要把單通道(灰階)轉成三通道，才能跟彩色圖拼在一起
    gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    blur_3ch = cv2.cvtColor(blur_img, cv2.COLOR_GRAY2BGR)
    result_3ch = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    
    # 加上文字標籤 (題目要求的第 6 點)
    cv2.putText(result_3ch, f"Method: {method_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 合併四張圖
    top_row = np.hstack((img, gray_3ch))
    bottom_row = np.hstack((blur_3ch, result_3ch))
    final_view = np.vstack((top_row, bottom_row))

    cv2.imshow('edge_tool', final_view)

    # 7. 按鍵功能
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): # 結束程式
        break
    elif key == ord('s'): # 儲存結果
        cv2.imwrite('result.jpg', result)
    elif key == ord('r'): # 重設 (手動把 Trackbar 撥回預設)
        cv2.setTrackbarPos('Low', 'edge_tool', 50)
        # ...以此類推

cv2.destroyAllWindows()