import cv2
import numpy as np
import random

IMG_SIZE = 600
INFO_WIDTH = 300
BLOCK_SIZE = IMG_SIZE // 3  

success_times = 0
best_move = -1
selected_pos = -1
moves = 0
success = False
cheat = False

img = cv2.imread('lena.jpg')
img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

blocks = []
cheat_blocks = []

k = 1
for i in range(3):
    for j in range(3):
        block = img[i * BLOCK_SIZE : (i+1) * BLOCK_SIZE, j * BLOCK_SIZE : (j+1) * BLOCK_SIZE].copy()
        cheat_block = img[i * BLOCK_SIZE : (i+1) * BLOCK_SIZE, j * BLOCK_SIZE : (j+1) * BLOCK_SIZE].copy()
        
        cv2.putText(cheat_block, f"{k}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
        
        blocks.append(block)
        cheat_blocks.append(cheat_block)
        k += 1

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
    
def OnMouse(event, x, y, flags, param):
    global selected_pos, moves, success, current_order,success_times
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
                if current_order == correct_answer:
                    success = True
                    success_times += 1

def draw():
    for i in range(9):
        target_row = i // 3
        target_col = i % 3
        
        if cheat: 
            block_to_draw = cheat_blocks[current_order[i]].copy()
        else:
            block_to_draw = blocks[current_order[i]].copy()
        
        cv2.rectangle(block_to_draw, (0,0), (BLOCK_SIZE, BLOCK_SIZE), (200, 200, 200), 1)
        
        if i == selected_pos:
            cv2.rectangle(block_to_draw, (5, 5), (BLOCK_SIZE-5, BLOCK_SIZE-5), (0, 0, 255), 5)
            
        canvas[target_row * BLOCK_SIZE : (target_row+1) * BLOCK_SIZE, target_col * BLOCK_SIZE : (target_col+1) * BLOCK_SIZE] = block_to_draw

# main
init_puzzle()
WindowName = "11402_3_D1349111"
cv2.namedWindow(WindowName)
cv2.setMouseCallback(WindowName, OnMouse)

while True:
    canvas = np.full((IMG_SIZE, IMG_SIZE + INFO_WIDTH, 3), 255, dtype=np.uint8)
    
    draw()
    
    Thumbnail_img = cv2.resize(img, (150, 150))
    canvas[20:170, 675:825] = Thumbnail_img
    cv2.putText(canvas, "Original", (710, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 0, 0), 2)
    
    cv2.putText(canvas, f"Moves: {moves} | Best: {best_move}", (620, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)
    cv2.putText(canvas, f"Success times: {success_times}", (620, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 0), 2)
    cv2.putText(canvas, "Click 2 blocks to swap", (620, 375), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(canvas, "R: Restart", (620, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 180, 0), 2)
    cv2.putText(canvas, "Q: Quit", (620, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 180, 0), 2)
    cv2.putText(canvas, "C: Open Cheat", (620, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 180, 0), 2)

    if success:
        cv2.putText(canvas, "SUCCESS! Press 'R' to retry", (50, 350), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 255), 5)
        if moves < best_move or best_move == -1:
            best_move = moves

    cv2.imshow(WindowName, canvas)

    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'):
        break
    elif key == ord('r') or key == ord('R'):
        init_puzzle()
    elif key == ord('c') or key == ord('C'):
        cheat = not cheat

cv2.destroyAllWindows()