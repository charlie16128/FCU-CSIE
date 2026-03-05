import cv2
import numpy as np

img = np.zeros((160, 280),dtype = np.uint8)

for y in range(0, 160, 20):
    img[y: y+10, 0: 280] = 255
    
cv2.imwrite("D1349111_HW2_2.jpg", img)
cv2.imshow('D1349111_HW2_2.jpg',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
