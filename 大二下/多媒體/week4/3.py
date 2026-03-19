import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def cv2_chinese(img, text, left, top, textcolor, fontsize):
    if(isinstance(img, np.ndarray)):
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    
    fontText = ImageFont.truetype("C:\Windows\Fonts\mingliu.ttc", fontsize, encoding='utf-8')
    
    draw.text((left, top), text, textcolor, font=fontText)
    
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


img = cv2.imread("antarctic.jpg")
img = cv2_chinese(img, "逢甲大學多媒體系統", 50, 100, (0, 0, 255), 50)

cv2.imshow("Antarctic.jpg",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
