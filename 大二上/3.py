import cv2
import numpy as np

img = np.zeros((160, 280, 3), dtype = np.uint8)
img1 = np.zeros((160, 280),dtype = np.uint8)

for i in range(0, 160):
    for k in range(0, 280):
        b = np.random.randint(0, 255)
        g = np.random.randint(0, 255)
        r = np.random.randint(0, 255)
        
        img[i, k] = [b, g, r]
        img1[i, k] = b
    
cv2.imwrite('D1349111_HW2_3.jpg', img)
cv2.imshow('D1349111_HW2_3.jpg', img)

cv2.imwrite('D1349111_HW2_3(1).jpg', img1)
cv2.imshow('D1349111_HW2_3(1).jpg', img1)

cv2.waitKey(0)
cv2.destroyAllWindows()