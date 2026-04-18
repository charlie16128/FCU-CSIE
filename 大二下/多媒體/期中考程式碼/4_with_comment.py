import cv2
import numpy as np

# 初始化全域變數
drawing = False # 是否正在拖曳滑鼠
mode = 6        # 預設為自由曲線模式
ix, iy = -1, -1 # 滑鼠起始座標
Window_Size = 1000
history = []    # 儲存歷史紀錄用於 Undo
redo_stack = [] # 儲存被撤銷的動作用於 Redo
window_name = "11402_4_D1349111"

def onChange(x):
    return

def CanvasInit():
    global canvas
    canvas = np.ones((Window_Size, Window_Size, 3), np.uint8) * 255

def save():
    global history, redo_stack
    history.append(canvas.copy())
    if len(history) > 100: # 增加步數上限
        history.pop(0)
    redo_stack.clear() # 只要有新動作，就清空 Redo 堆疊

def draw_shape(event, x, y, flags, param):
    global ix, iy, drawing, canvas, mode

    # 取得滾動條數值
    r = cv2.getTrackbarPos('Red', window_name)
    g = cv2.getTrackbarPos('Green', window_name)
    b = cv2.getTrackbarPos('Blue', window_name)
    rad = cv2.getTrackbarPos('Radius', window_name)
    thick = cv2.getTrackbarPos('Thickness', window_name)
    color = (b, g, r)

    if event == cv2.EVENT_LBUTTONDOWN:
        # 動作開始前先存檔
        save()
        drawing = True
        ix, iy = x, y
        
        # 點擊即畫圖的模式
        if mode == 1: 
            cv2.circle(canvas, (x, y), rad, color, thick)
        elif mode == 2: 
            cv2.circle(canvas, (x, y), rad, color, -1)
        elif mode == 3: 
            cv2.rectangle(canvas, (x-rad, y-rad), (x+rad, y+rad), color, -1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode == 4: # 橡皮擦 (白色畫筆)
                cv2.circle(canvas, (x, y), rad, (255, 255, 255), -1)
            elif mode == 6: # 自由曲線
                cv2.line(canvas, (ix, iy), (x, y), color, thick)
                ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            if mode == 5: # 直線模式：放開時才確定位置
                cv2.line(canvas, (ix, iy), (x, y), color, thick)
            drawing = False
# main
# 建立視窗與滾動條
cv2.namedWindow(window_name)

cv2.createTrackbar('Red', window_name, 0, 255, onChange)
cv2.createTrackbar('Green', window_name, 0, 255, onChange)
cv2.createTrackbar('Blue', window_name, 0, 255, onChange)
cv2.createTrackbar('Radius', window_name, 10, 60, onChange)
cv2.createTrackbar('Thickness', window_name, 2, 20, onChange)

CanvasInit()
cv2.setMouseCallback(window_name, draw_shape)

while True:
    # 顯示畫布與目前資訊
    CanvasCopy = canvas.copy()
    mode_text = {1:"Circle", 2:"Filled Circle", 3:"Square", 4:"Eraser", 5:"Line", 6:"Free Draw"}
    
    # 顯示 UI 資訊
    info = f"Current Mode [{mode}] {mode_text[mode]} | Thick: {cv2.getTrackbarPos('Thickness', window_name)}"
    HowToUse = f"Switch mod: 1-6, U: Undo, R: Redo , C: Clear , Q: Quit"
    cv2.putText(CanvasCopy, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 50), 2)
    cv2.putText(CanvasCopy, HowToUse, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 2)
    
    
    cv2.imshow(window_name, CanvasCopy)
    
    key = cv2.waitKey(1)
    
    # 模式切換
    if ord('1') <= key <= ord('6'):
        mode = key - ord('0')
    
    # Undo 功能
    elif key == ord('u') or key == ord('U'):
        if history:
            # 將目前的畫面放進 Redo 堆疊
            redo_stack.append(canvas.copy())
            # 從歷史紀錄拿回上一個畫面
            canvas = history.pop()
    
    # Redo 功能
    elif key == ord('r') or key == ord('R'):
        if redo_stack:
            # 將目前畫面放進歷史紀錄
            history.append(canvas.copy())
            # 從 Redo 堆疊拿回畫面
            canvas = redo_stack.pop()

    # 清空畫布
    elif key == ord('c') or key == ord('C'):
        save()
        CanvasInit()
            
    # 結束程式
    elif key == ord('q') or key == ord('Q'):
        break

cv2.destroyAllWindows()