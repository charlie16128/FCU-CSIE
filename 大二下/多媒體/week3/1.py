import cv2
import numpy as np

image = cv2.imread('colorbar.jpg')
cv2.imshow('bgr', image)


blue, green, red = cv2.split(image)

cv2.imshow('blue', blue)
cv2.imshow('green', green)
cv2.imshow('red', red)

zeros = np.zeros(image.shape[:2], dtype='uint8') #image.shape[:2] 取前兩個通道
blue_colored = cv2.merge([blue, zeros, zeros])
green_colored = cv2.merge([zeros, green, zeros])
red_colored = cv2.merge([zeros, zeros, red])

cv2.imshow('blue_colored', blue_colored)
cv2.imshow('green_colored', green_colored)
cv2.imshow('red_colored', red_colored)

cv2.waitKey(0)
cv2.destroyAllWindows()