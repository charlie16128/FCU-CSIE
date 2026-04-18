import cv2
import numpy as np

drawing = False 
mode = 6        
mouse_x, mouse_y = -1, -1 
Window_Size = 1000
history = []   
redo_stack = []
window_name = "11402_4_D1349111"

def onChange(x):
    return

def CanvasInit():
    global canvas
    canvas = np.ones((Window_Size, Window_Size, 3), np.uint8) * 255

def save():
    global history, redo_stack
    history.append(canvas.copy())
    if len(history) > 1000: 
        history.pop(0)
    redo_stack.clear() 

def draw(event, x, y, flags, param):
    global mouse_x, mouse_y, drawing, canvas, mode

    r = cv2.getTrackbarPos('Red', window_name)
    g = cv2.getTrackbarPos('Green', window_name)
    b = cv2.getTrackbarPos('Blue', window_name)
    rad = cv2.getTrackbarPos('Radius', window_name)
    thick = cv2.getTrackbarPos('Thickness', window_name)
    color = (b, g, r)

    if event == cv2.EVENT_LBUTTONDOWN:
        save()
        drawing = True
        mouse_x, mouse_y = x, y
        
        if mode == 1: 
            cv2.circle(canvas, (x, y), rad, color, thick)
        elif mode == 2: 
            cv2.circle(canvas, (x, y), rad, color, -1)
        elif mode == 3: 
            cv2.rectangle(canvas, (x-rad, y-rad), (x+rad, y+rad), color, -1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            if mode == 4:
                cv2.circle(canvas, (x, y), rad, (255, 255, 255), -1)
            elif mode == 6: 
                cv2.line(canvas, (mouse_x, mouse_y), (x, y), color, thick)
                mouse_x, mouse_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            if mode == 5:
                cv2.line(canvas, (mouse_x, mouse_y), (x, y), color, thick)
            drawing = False

# main
cv2.namedWindow(window_name)

cv2.createTrackbar('Red', window_name, 0, 255, onChange)
cv2.createTrackbar('Green', window_name, 0, 255, onChange)
cv2.createTrackbar('Blue', window_name, 0, 255, onChange)
cv2.createTrackbar('Radius', window_name, 10, 60, onChange)
cv2.createTrackbar('Thickness', window_name, 2, 20, onChange)
cv2.setTrackbarMin('Thickness', window_name, 1)


CanvasInit()
cv2.setMouseCallback(window_name, draw)

while True:
    CanvasCopy = canvas.copy()
    mode_text = {1:"Circle", 2:"Filled Circle", 3:"Square", 4:"Eraser", 5:"Line", 6:"Free Draw"}
    
    info = f"Current Mode [{mode}] {mode_text[mode]} | Thick: {cv2.getTrackbarPos('Thickness', window_name)}"
    HowToUse = f"Switch mod: 1-6, U: Undo, R: Redo , C: Clear , Q: Quit"
    cv2.putText(CanvasCopy, info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (50, 50, 50), 2)
    cv2.putText(CanvasCopy, HowToUse, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 2)
    
    cv2.imshow(window_name, CanvasCopy)
    
    key = cv2.waitKey(1)
    
    if ord('1') <= key <= ord('6'):
        mode = key - ord('0')
    
    elif key == ord('u') or key == ord('U'):
        if history:
            redo_stack.append(canvas.copy())
            canvas = history.pop()
    
    elif key == ord('r') or key == ord('R'):
        if redo_stack:
            history.append(canvas.copy())
            canvas = redo_stack.pop()

    elif key == ord('c') or key == ord('C'):
        save()
        CanvasInit()
            
    elif key == ord('q') or key == ord('Q'):
        break

cv2.destroyAllWindows()