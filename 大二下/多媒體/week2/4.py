import cv2
import numpy as np

img = cv2.imread('flower1.jpg')

temp = np.vstack((img, img))
result = np.hstack((temp, temp))

cv2.imwrite('4.jpg', result)
cv2.imshow('4.jpg', result)

cv2.waitKey(5000)
cv2.destroyAllWindows()