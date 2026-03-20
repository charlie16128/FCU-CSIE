import cv2
import numpy as np
import random

img = cv2.imread("antarctic.jpg")

cy = int(img.shape[0] / 2)
cx = int(img.shape[1] / 2)

min_r = 30               
max_r = min(cx, cy)      

radius = min_r
direction = 1           
is_paused = False

while True:
    if is_paused == False:
        canvas = img.copy() #set canvas clean
        

        cv2.circle(canvas, (cx, cy), min_r, (0, 0, 255), -1)
        
        for r in range(min_r + 20, radius + 1, 25):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # color = (0, 255, 255)
            cv2.circle(canvas, (cx, cy), r, color, 2)

        radius += (10 * direction)
        
        if radius >= max_r:
            direction = -1
        elif radius <= min_r:
            direction = 1
            
        cv2.imshow("My Draw", canvas)

    key = cv2.waitKey(50)
    
    if key == ord('q') or key == ord('Q'):
        break
    elif key == ord(' '):  
        is_paused = True
    elif key == ord('r') or key == ord('R'): 
        is_paused = False

cv2.destroyAllWindows()