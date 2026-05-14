import cv2

src = cv2.imread("hw15-2.jpg")
gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

result = cv2.bitwise_not(binary)

cv2.imshow("src", src)
cv2.imshow("result", result)

cv2.waitKey(0)
cv2.destroyAllWindows()