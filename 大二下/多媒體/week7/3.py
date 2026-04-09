import cv2
import numpy as np

src = cv2.imread("bw_noise.jpg")

kernel = np.ones((4, 4), np.uint8)

dst = cv2.erode(src, kernel)

cv2.imshow("dst", dst)
cv2.imshow("original", src)

cv2.waitKey(0)
cv2.destroyAllWindows()