import cv2
import numpy as np

img = cv2.imread("number.jpg")
img1 = cv2.imread("numbers.jpg")

maxval = 255 # 定義像素最大值

ret, dst1 = cv2.threshold(img, 127, maxval, cv2.THRESH_BINARY)
ret, dst2 = cv2.threshold(img1, 10, maxval, cv2.THRESH_BINARY)
ret, dst3 = cv2.threshold(img, 1, maxval, cv2.THRESH_BINARY_INV)
ret, dst4 = cv2.threshold(img, 1, maxval, cv2.THRESH_BINARY)

cv2.imshow("number", img)

cv2.imshow("pic1", dst1)
cv2.imshow("pic2", dst2)
cv2.imshow("pic3", dst3)
cv2.imshow("pic4", dst4)


cv2.waitKey(0)
cv2.destroyAllWindows()