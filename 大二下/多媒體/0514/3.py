import cv2
import numpy as np

src = cv2.imread("hw15_1.jpg")
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# 注意這裡必須使用 cv2.RETR_LIST 或 cv2.RETR_TREE 才能同時找到內部與外部的所有輪廓
contours, hierarchy = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow("src", src)

for i in range(len(contours)):
    canvas = np.zeros_like(src)
    
    # 繪製黃色實心輪廓 (B=0, G=255, R=255)，厚度設為 -1 或 cv2.FILLED 表示填滿
    cv2.drawContours(canvas, contours, i, (0, 255, 255), -1)
    
    # 計算輪廓的影像矩 (Moments) 來找中心點
    M = cv2.moments(contours[i])
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        # 在中心點繪製藍色實心圓點 (B=255, G=0, R=0)
        cv2.circle(canvas, (cx, cy), 5, (255, 0, 0), -1)
        
    cv2.imshow(f"contours{i}", canvas)

cv2.waitKey(0)
cv2.destroyAllWindows()