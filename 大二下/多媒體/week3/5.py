import cv2
import numpy as np

img = cv2.imread('jk.jpg')
h, w = img.shape[:2]
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h1, w1 = img_gray.shape[:2]

mask = np.zeros((h ,w), dtype="uint8")
mask1 = np.zeros((h1 ,w1), dtype="uint8")

cv2.rectangle(mask, (100, 80), (220, 250), 255, -1)
cv2.rectangle(mask1, (100, 80), (220, 250), 255, -1)

result = cv2.bitwise_and(img, img, mask = mask)
result_gray = cv2.bitwise_and(img_gray, img_gray, mask = mask1)

cv2.imshow("Original", img)
cv2.imshow("Mask", mask)
cv2.imshow("Result", result)
cv2.imshow("Gray Original", img_gray)
cv2.imshow("Result Gray", result_gray)

cv2.waitKey(0)
cv2.destroyAllWindows()