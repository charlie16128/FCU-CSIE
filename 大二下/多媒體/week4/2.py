import cv2
import numpy as np

img = cv2.imread("antarctic.jpg")

font = cv2.FONT_HERSHEY_SIMPLEX

cv2.putText(img, 'FCU Student', (0, 150), font, 3, (255, 0, 0), 12, cv2.LINE_8, False)

cv2.imshow("Fcu CSIE Student",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
