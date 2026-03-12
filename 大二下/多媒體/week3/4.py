import cv2

lena = cv2.imread('lena.jpg')
dollar = cv2.imread('dollar.jpg')

#face = lena[124:239, 135:215]
face = lena[150:240, 140:210]

face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
face_BGR = cv2.cvtColor(face_gray, cv2.COLOR_GRAY2BGR)

f_y, f_x = face_BGR.shape[:2]

x = 300
y = 110

dollar[y : y + f_y, x : x + f_x] = face_BGR

cv2.imshow('Lena in Dollar', dollar)

cv2.waitKey(0)
cv2.destroyAllWindows()