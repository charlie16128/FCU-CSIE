import cv2
import numpy as np

height, width = 300, 400

blue_img = np.zeros((height,width,3),np.uint8) # 建立藍色blue底的彩色影像陣列

blue_img[:,:,0] = 255                   # 填滿藍色

cv2.imshow("blue_image", blue_img)    # 顯示blue_img影像陣列

green_img = np.zeros((height,width,3),np.uint8) # 建立綠色green底的彩色影像陣列

green_img[:,:,1] = 255                  # 填滿綠色

cv2.imshow("green_image", green_img)    # 顯示blue_img影像陣列   # 顯示green_img影像陣列

red_img = np.zeros((height,width,3),np.uint8) # 建立紅色red底的彩色影像陣列

red_img[:,:,2] = 255                    # 填滿紅色

cv2.imshow("red_image", red_img)    # 顯示blue_img影像陣列

cv2.waitKey(0)
cv2.destroyAllWindows()