import cv2
import numpy as np
import random 
width = 640
height = 480
r = 15

bx = int(width / 2)
by = 50
b_dx = 2
b_dy = 2

paddle_w = 120
paddle_h = 15
px = int((width - paddle_w) / 2)
py = height - 40
paddle_speed = 30

score = 0
state = 0
color = (255, 0, 0)
color_p = (0, 200, 0)

def change_color(color):
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    return color


while True:
    img = np.ones((height, width, 3), np.uint8) * 255
    key = cv2.waitKey(5) 
    
    if key == 27: #esc
        break

    if key == ord('r') or key == ord('R'):
        score = 0
        bx, by = int(width / 2), 50
        b_dx, b_dy = 5, 5
        px = int((width - paddle_w) / 2)
        state = 0

    if state == 0:
        if key == ord('a') or key == ord('A'):
            px -= paddle_speed
            if px < 0: px = 0
        elif key == ord('d') or key == ord('D'):
            px += paddle_speed
            if px + paddle_w > width: px = width - paddle_w
        elif key == ord(' '):
            state = 1

        bx += b_dx
        by += b_dy

        if bx <= r or bx >= width - r:
            b_dx = -b_dx
            color = change_color(color)
            color_p = change_color(color)
            
        if by <= r:
            b_dy = -b_dy
            color = change_color(color)
            color_p = change_color(color)

        if b_dy > 0: # 方向向下
            if py <= by + r <= py + paddle_h: # 高度介於paddle
                if px <= bx <= px + paddle_w: # x介於 paddle
                    b_dy = -b_dy
                    score += 1
                    color = change_color(color)
                    color_p = change_color(color)  

        if by >= height - r:
            state = 2

    elif state == 1:
        if key == ord(' '): 
            state = 0

    cv2.putText(img, "A: Left   D: Right   SPACE: Pause   R: Restart   ESC: Exit", 
                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 100, 100), 1, cv2.LINE_8)
    cv2.putText(img, f"Score: {score}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3, cv2.LINE_8)

    cv2.circle(img, (bx, by), r, color, -1)
    cv2.rectangle(img, (px, py), (px + paddle_w, py + paddle_h), color_p, -1)

    if state == 1:
        cv2.putText(img, "Paused", (int(width/2)-100, int(height/2)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4, cv2.LINE_8)
        
    elif state == 2:
        cv2.putText(img, "Game OVER", (int(width/2)-160, int(height/2)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4, cv2.LINE_8)

    cv2.imshow("Bouncing Ball Game", img)

cv2.destroyAllWindows()
