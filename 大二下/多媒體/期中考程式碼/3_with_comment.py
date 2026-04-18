import cv2
import numpy as np
import random

# --- 1. 基本參數設定 ---
IMG_SIZE = 600
INFO_WIDTH = 300
BLOCK_SIZE = IMG_SIZE // 3  # 每個區塊 200x200

# 全域變數
selected = -1
moves = 0
success = False

# --- 2. 影像讀取與切割 ---
img = cv2.imread('lena.jpg')
img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

# 切割成 9 個區塊存入 List
blocks = []
for i in range(3):
    for j in range(3):
        block = img[i * BLOCK_SIZE : (i+1) * BLOCK_SIZE, j * BLOCK_SIZE : (j+1) * BLOCK_SIZE].copy()
        blocks.append(block)

# 順序控制
current_order = list(range(9))
correct_answer = list(range(9))

def init_puzzle():
    global current_order, moves, success, selected
    while True:
        random.shuffle(current_order)
        if current_order != correct_answer:
            break
    moves = 0
    success = False
    selected = -1
    

# --- 3. 滑鼠點擊邏輯 ---
def on_mouse(event, x, y, flags, param):
    global selected, moves, success, current_order
    if success: return # 成功後不允許再移動

    if event == cv2.EVENT_LBUTTONDOWN:
        # 判斷是否點在拼圖區 (x < 600)
        if x < IMG_SIZE:
            col = x // BLOCK_SIZE
            row = y // BLOCK_SIZE
            clicked_pos = row * 3 + col
            
            if selected == -1:
                selected = clicked_pos
            elif selected == clicked_pos:
                selected = -1 # 點同一個取消選取
            else:
                # 交換位置
                current_order[selected], current_order[clicked_pos] = current_order[clicked_pos], current_order[selected]
                moves += 1
                selected = -1
                print(current_order)
                # 檢查是否成功
                if current_order == correct_answer:
                    success = True


init_puzzle()
# --- 4. 主迴圈與畫面顯示 ---
cv2.namedWindow("11402_3_D1349111")
cv2.setMouseCallback("11402_3_D1349111", on_mouse)

while True:
    # 建立大畫布 (600x900)，並填滿白色
    canvas = np.full((IMG_SIZE, IMG_SIZE + INFO_WIDTH, 3), 255, dtype=np.uint8)
    
    # 繪製拼圖區 (左方 600x600)
    for i in range(9):
        target_row = i // 3
        target_col = i % 3
        block_to_draw = blocks[current_order[i]].copy()
        
        # 繪製格線
        cv2.rectangle(block_to_draw, (0,0), (BLOCK_SIZE, BLOCK_SIZE), (200, 200, 200), 1)
        
        # 如果是被選取的區塊，畫上紅色外框標示
        if i == selected:
            cv2.rectangle(block_to_draw, (5, 5), (BLOCK_SIZE-5, BLOCK_SIZE-5), (0, 0, 255), 5)
            
        canvas[target_row * BLOCK_SIZE : (target_row+1) * BLOCK_SIZE, target_col * BLOCK_SIZE : (target_col+1) * BLOCK_SIZE] = block_to_draw

    # --- 右側資訊欄 (白色背景上的黑色/彩色文字) ---
    # 5. 右上角參考圖 (150x150)
    ref_img = cv2.resize(img, (150, 150))
    canvas[20:170, 675:825] = ref_img
    cv2.putText(canvas, "Original", (710, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # 6. 資訊顯示
    cv2.putText(canvas, f"Moves: {moves}", (650, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    cv2.putText(canvas, "Click 2 blocks to swap", (620, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (50, 50, 50), 1)
    cv2.putText(canvas, "R: Restart", (650, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    cv2.putText(canvas, "Q: Quit", (650, 500), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    # 7. 完成條件
    if success:
        # 在拼圖中央顯示紅色的 SUCCESS 文字
        overlay = canvas.copy()
        cv2.putText(overlay, "SUCCESS!", (50, 350), cv2.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 255), 10)
        cv2.addWeighted(overlay, 0.7, canvas, 0.3, 0, canvas)

    cv2.imshow("11402_3_D1349111", canvas)

    # 8. 按鍵偵測
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):
        init_puzzle()

cv2.destroyAllWindows()