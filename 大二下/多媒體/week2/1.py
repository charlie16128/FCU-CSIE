import cv2

img = cv2.imread('jk.jpg') # 灰階讀取 flag= cv2.IMREAD_GRAYSCALE
cv2.imshow('jk.jpg', img)

h, w, c= img.shape 
img[h-50: h, w-50: w] = [255, 255, 255]
cv2.imwrite('JK_white.jpg', img)
cv2.imshow('JK_white.jpg', img)

img[h-50: h, 0: w] = [0, 255, 255]
cv2.imwrite('JK_Yellow.jpg', img)
cv2.imshow('JK_Yellow.jpg', img)

cv2.waitKey(5000)
cv2.destroyAllWindows()