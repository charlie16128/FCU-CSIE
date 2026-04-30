import cv2
import numpy as np

picPath = r'C:\Users\User\AppData\Roaming\Python\Python313\site-packages\cv2\data\haarcascade_frontalcatface.xml'
picPath_extended = r'C:\Users\User\AppData\Roaming\Python\Python313\site-packages\cv2\data\haarcascade_frontalcatface_extended.xml'

face_cascade =  cv2.CascadeClassifier(picPath)

img = cv2.imread("newFatcat.png")
img1 = cv2.imread("dogcat.jpg")
img2 = cv2.imread("dogcat1.jpg")

faces = face_cascade.detectMultiScale(img, scaleFactor=1.01, minNeighbors=10, minSize=(10,10))
faces1 = face_cascade.detectMultiScale(img1, scaleFactor=1.009, minNeighbors=10, minSize=(20,20))
faces2 = face_cascade.detectMultiScale(img2, scaleFactor=1.01, minNeighbors=15, minSize=(20,20))

cv2.rectangle(img, (img.shape[1]-140, img.shape[0]-20), (img.shape[1], img.shape[0]), (0, 255, 255), -1)
cv2.rectangle(img1, (img1.shape[1]-140, img1.shape[0]-20), (img1.shape[1], img1.shape[0]), (0, 255, 255), -1)
cv2.rectangle(img2, (img2.shape[1]-140, img2.shape[0]-20), (img2.shape[1], img2.shape[0]), (0, 255, 255), -1)


cv2.putText(img, "Finding " + str(len(faces)) + " Face", (img.shape[1]-135, img.shape[0]-5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
cv2.putText(img1, "Finding " + str(len(faces1)) + " Face", (img1.shape[1]-135, img1.shape[0]-5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)
cv2.putText(img2, "Finding " + str(len(faces2)) + " Face", (img2.shape[1]-135, img2.shape[0]-5), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
for (x,y,w,h) in faces1:
    cv2.rectangle(img1,(x,y),(x+w,y+h),(255,0,0),2)
for (x,y,w,h) in faces2:
    cv2.rectangle(img2,(x,y),(x+w,y+h),(255,0,0),2)
    
cv2.imshow("newFatcat", img)
cv2.imshow("dogcat", img1)
cv2.imshow("dogcat1", img2)

cv2.waitKey(0)
cv2.destroyAllWindows()
