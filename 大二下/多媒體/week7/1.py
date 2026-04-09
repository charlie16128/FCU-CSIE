import cv2
import numpy as np

src = cv2.imread("lena.jpg", cv2.IMREAD_GRAYSCALE)

src_bigger = cv2.copyMakeBorder(src, 1, 1, 1, 1, cv2.BORDER_REPLICATE)

rows, cols = src.shape

edge_manual = np.zeros((rows, cols), dtype=np.float64)

gx_mask = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
gy_mask = np.array([[-1, -2, -1], [ 0,  0,  0], [ 1,  2,  1]])

for i in range(rows):
    for j in range(cols):
        region = src_bigger[i : i+3, j : j+3]
        
        gx_val = np.sum(region * gx_mask)
        gy_val = np.sum(region * gy_mask)
        
        magnitude = np.sqrt(gx_val**2 + gy_val**2)
        
        edge_manual[i, j] = min(magnitude, 255)

edge_manual = edge_manual.astype(np.uint8)

cv2.imshow("Original", src)
cv2.imshow("Manual", edge_manual)
cv2.waitKey(0)
cv2.destroyAllWindows()




















# sobel_x = cv2.Sobel(src, cv2.CV_64F, 1, 0, ksize=3)
# sobel_y = cv2.Sobel(src, cv2.CV_64F, 0, 1, ksize=3)
# edge_opencv = cv2.magnitude(sobel_x, sobel_y)
# edge_opencv = np.uint8(np.clip(edge_opencv, 0, 255))
