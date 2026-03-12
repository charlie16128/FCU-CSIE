import cv2

image = cv2.imread('view.jpg')

blue, green, red = cv2.split(image)
rgb_image = cv2.merge([red, green, blue])
bgr_image = cv2.merge([blue, green, red])

cv2.imshow('view.jpg', image)
cv2.imshow('RGB.jpg', rgb_image)
cv2.imshow('BGR.jpg', bgr_image)

cv2.waitKey(0)
cv2.destroyAllWindows()