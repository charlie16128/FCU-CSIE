import cv2

picPath = r'C:\Users\User\AppData\Roaming\Python\Python313\site-packages\cv2\data\haarcascade_russian_plate_number.xml'
car_cascade =  cv2.CascadeClassifier(picPath)

img = cv2.imread("car1.jpg")
plates = car_cascade.detectMultiScale(img, scaleFactor=1.01, minNeighbors=40, minSize=(20,20))



for (x,y,w,h) in plates:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imshow("Car plate", img)

cv2.waitKey(0)
cv2.destroyAllWindows()
