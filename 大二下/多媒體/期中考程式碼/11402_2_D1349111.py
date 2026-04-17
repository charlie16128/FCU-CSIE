import cv2
import numpy as np

def onChange(x):
    return

cv2.namedWindow('edge_tool_demo')

cv2.createTrackbar('Low', 'edge_tool_demo', 50, 255, onChange)
cv2.createTrackbar('High', 'edge_tool_demo', 150, 255, onChange)
cv2.createTrackbar('Blur', 'edge_tool_demo', 1, 10, onChange) 
cv2.createTrackbar('Method', 'edge_tool_demo', 0, 2, onChange) 

original_img = cv2.imread('lena.jpg') 
gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

while True:
    low = cv2.getTrackbarPos('Low', 'edge_tool_demo')
    high = cv2.getTrackbarPos('High', 'edge_tool_demo')
    blur_val = cv2.getTrackbarPos('Blur', 'edge_tool_demo')
    method = cv2.getTrackbarPos('Method', 'edge_tool_demo')

    k_size = blur_val * 2 + 1 
    blur_img = cv2.GaussianBlur(gray, (k_size, k_size), 0)

    if method == 0:
        method_img = cv2.Canny(blur_img, low, high)
        method_name = "Canny Edge"
    elif method == 1:
        sobelx = cv2.Sobel(blur_img, cv2.CV_64F, 1, 0, ksize=3)
        method_img = cv2.convertScaleAbs(sobelx)
        method_name = "Sobel Edge"
    else:
        lap = cv2.Laplacian(blur_img, cv2.CV_64F)
        method_img = cv2.convertScaleAbs(lap)
        method_name = "Laplacian Edge"

    gray_rainbow = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    blur_rainbow = cv2.cvtColor(blur_img, cv2.COLOR_GRAY2BGR)
    method_rainbow = cv2.cvtColor(method_img, cv2.COLOR_GRAY2BGR)

    cv2.putText(original_img, f"Original Img", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(gray_rainbow, f"Gray", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(blur_rainbow, f"Blur", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(method_rainbow, f"Method: {method_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    top = np.hstack((original_img, gray_rainbow))
    bottom = np.hstack((blur_rainbow, method_rainbow))
    result = np.vstack((top, bottom))

    cv2.imshow('edge_tool_demo', result)

    key = cv2.waitKey(1)
    if key == ord('q'): 
        break
    elif key == ord('s'): 
        cv2.imwrite('result.jpg', result)
    elif key == ord('r'): 
        cv2.setTrackbarPos('Low', 'edge_tool_demo', 50)
        cv2.setTrackbarPos('High', 'edge_tool_demo', 150)
        cv2.setTrackbarPos('Blur', 'edge_tool_demo', 1)
        cv2.setTrackbarPos('Method', 'edge_tool_demo', 0)

cv2.destroyAllWindows()