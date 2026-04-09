import cv2 
import numpy as np

src = cv2.imread("snowman.jpg")

kernel = np.ones((5,5), np.uint8)

dst = cv2.morphologyEx(src, cv2.MORPH_GRADIENT, kernel)

cv2.imshow("src", src)
cv2.imshow("After", dst)

cv2.waitKey(0)
cv2.destroyAllWindows()
