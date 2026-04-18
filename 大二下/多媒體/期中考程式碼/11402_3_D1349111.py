import cv2
import numpy as np
import random

IMG_SIZE = 600
INFO_WIDTH = 300
BLOCK_SIZE = IMG_SIZE // 3  

selected_pos = -1
moves = 0
success = False

img = cv2.imread('lena.jpg')
img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

blocks = []
for i in range(3):
    for j in range(3):
        block = img[i * BLOCK_SIZE : (i+1) * BLOCK_SIZE, j * BLOCK_SIZE : (j+1) * BLOCK_SIZE].copy()
        blocks.append(block)

current_order = list(range(9))
correct_answer = list(range(9))

def init_puzzle():
    global current_order, moves, success, selected_pos
    while True:
        random.shuffle(current_order)
        if current_order != correct_answer:
            break
    moves = 0
    success = False
    selected_pos = -1
    
def on_mouse(event, x, y, flags, param):
    global selected_pos, moves, success, current_order
    if success: return 

    if event == cv2.EVENT_LBUTTONDOWN:
        if x < IMG_SIZE:
            col = x // BLOCK_SIZE
            row = y // BLOCK_SIZE
            clicked_pos = row * 3 + col
            
            if selected_pos == -1:
                selected_pos = clicked_pos
            elif selected_pos == clicked_pos:
                selected_pos = -1
            else:
                current_order[selected_pos], current_order[clicked_pos] = current_order[clicked_pos], current_order[selected_pos]
                moves += 1
                selected_pos = -1
                print(current_order)
                if current_order == correct_answer:
                    success = True


init_puzzle()
cv2.namedWindow("11402_3_D1349111")
cv2.setMouseCallback("11402_3_D1349111", on_mouse)


while True:
    canvas = np.full((IMG_SIZE, IMG_SIZE + INFO_WIDTH, 3), 255, dtype=np.uint8)
    
    for i in range(9):
        target_row = i // 3
        target_col = i % 3
        block_to_draw = blocks[current_order[i]].copy()
        
        cv2.rectangle(block_to_draw, (0,0), (BLOCK_SIZE, BLOCK_SIZE), (200, 200, 200), 1)
        
        if i == selected_pos:
            cv2.rectangle(block_to_draw, (5, 5), (BLOCK_SIZE-5, BLOCK_SIZE-5), (0, 0, 255), 5)
            
        canvas[target_row * BLOCK_SIZE : (target_row+1) * BLOCK_SIZE, target_col * BLOCK_SIZE : (target_col+1) * BLOCK_SIZE] = block_to_draw

    Thumbnail_img = cv2.resize(img, (150, 150))
    canvas[20:170, 675:825] = Thumbnail_img
    cv2.putText(canvas, "Original", (710, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    cv2.putText(canvas, f"Moves: {moves}", (650, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(canvas, "Click 2 blocks to swap", (620, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(canvas, "R: Restart", (650, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(canvas, "Q: Quit", (650, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    if success:
        overlay = canvas.copy()
        cv2.putText(overlay, "SUCCESS!", (50, 350), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 255), 10)
        cv2.addWeighted(overlay, 0.7, canvas, 0.3, 0, canvas)

    cv2.imshow("11402_3_D1349111", canvas)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):
        init_puzzle()

cv2.destroyAllWindows()