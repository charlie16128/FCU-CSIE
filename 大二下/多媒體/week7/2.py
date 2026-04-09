import cv2

src = cv2.imread("geneva.jpg") # 彩色讀取

# Scharr()函數
dstx = cv2.Scharr(src, cv2.CV_32F, 1, 0) # 計算 x 軸影像梯度
dsty = cv2.Scharr(src, cv2.CV_32F, 0, 1) # 計算 y 軸影像梯度
dstx = cv2.convertScaleAbs(dstx) # 將負值轉正值
dsty = cv2.convertScaleAbs(dsty) # 將負值轉正值
dst_scharr = cv2.addWeighted(dstx, 0.5,dsty, 0.5, 0) # 影像融合


dst_laplacian = cv2.Laplacian(src, cv2.CV_32F, ksize=3, scale=0.5)
dst_laplacian = cv2.convertScaleAbs(dst_laplacian)


# 輸出影像梯度
# cv2.imshow("Src", src) 
cv2.imshow("Scharr", dst_scharr) 
cv2.imshow("Laplacian", dst_laplacian) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 