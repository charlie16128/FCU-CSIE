import cv2
import numpy as np

def onChange(x):
    return

WindowName = 'edge_tool'
cv2.namedWindow(WindowName)

cv2.createTrackbar('Low', WindowName, 50, 255, onChange)
cv2.createTrackbar('High', WindowName, 150, 255, onChange)
cv2.createTrackbar('Blur_K', WindowName, 1, 15, onChange) 
cv2.createTrackbar('Method', WindowName, 0, 2, onChange) 
cv2.createTrackbar('Ksize', WindowName, 0, 5, onChange)

original_img = cv2.imread('lena.jpg') 
gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

while True:
    low = cv2.getTrackbarPos('Low', WindowName)
    high = cv2.getTrackbarPos('High', WindowName)
    blur_val = cv2.getTrackbarPos('Blur_K', WindowName)
    method = cv2.getTrackbarPos('Method', WindowName)
    
    ksize_sobel = 2 * cv2.getTrackbarPos('Ksize', WindowName) + 1
    
    ksize_blur = 2 * blur_val + 1 
    blur_img = cv2.GaussianBlur(gray, (ksize_blur, ksize_blur), 0)

    if method == 0:
        method_img = cv2.Canny(blur_img, low, high)
        method_name = "Canny Edge"
    elif method == 1:
        sobelx = cv2.Sobel(blur_img, cv2.CV_64F, 1, 0, ksize=ksize_sobel)
        sobely = cv2.Sobel(blur_img, cv2.CV_64F, 0, 1, ksize=ksize_sobel)
        abs_sx = cv2.convertScaleAbs(sobelx)
        abs_sy = cv2.convertScaleAbs(sobely)
        method_img = cv2.addWeighted(abs_sx, 0.5, abs_sy, 0.5, 0)        
        method_name = f"Sobel Edge(k={ksize_sobel})"
    else:
        lap = cv2.Laplacian(blur_img, cv2.CV_64F)
        method_img = cv2.convertScaleAbs(lap)
        method_name = "Laplacian Edge"

    gray_rainbow = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    blur_rainbow = cv2.cvtColor(blur_img, cv2.COLOR_GRAY2BGR)
    method_rainbow = cv2.cvtColor(method_img, cv2.COLOR_GRAY2BGR)

    cv2.putText(original_img, f"Original Img", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(gray_rainbow, f"Gray", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(blur_rainbow, f"Blur_K (k = {blur_val})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(method_rainbow, f"Method: {method_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    top = np.hstack((original_img, gray_rainbow))
    bottom = np.hstack((blur_rainbow, method_rainbow))
    result = np.vstack((top, bottom))

    cv2.imshow(WindowName, result)

    key = cv2.waitKey(1)
    if key == ord('q') or key == ord('Q'): 
        break
    elif key == ord('s') or key == ord('S'): 
        filename = f"Low({low})High({high})Blur({blur_val})Method({method_name})Ksize({ksize_sobel})"
        cv2.imwrite(f'{filename}.jpg', result)
        print(f"Saved Image as {filename}.jpg")
    elif key == ord('r') or key == ord('R'): 
        cv2.setTrackbarPos('Low', WindowName, 50)
        cv2.setTrackbarPos('High', WindowName, 150)
        cv2.setTrackbarPos('Blur_K', WindowName, 1)
        cv2.setTrackbarPos('Method', WindowName, 0)
        cv2.setTrackbarPos('Ksize', WindowName, 0)

cv2.destroyAllWindows()