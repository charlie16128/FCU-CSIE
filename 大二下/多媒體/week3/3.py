import cv2
import numpy as np

image = cv2.imread('street.png', cv2.IMREAD_UNCHANGED)
bgra_image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)


b, g, r, a = cv2.split(bgra_image)

print("顯示資訊:")
print(f"修改前img[10,50] = {image[10,50]}")
print(f"修改前img[50,99] = {image[50,99]}")

a[0:200, 0:200] = 128
bgra_image = cv2.merge([b,g,r,a])

print(f"修改後img[10,50] = {bgra_image[10,50]}")
print(f"修改後img[50,99] = {bgra_image[50,99]}")

cv2.imwrite('street128.png', bgra_image)

cv2.waitKey(0)
cv2.destroyAllWindows()