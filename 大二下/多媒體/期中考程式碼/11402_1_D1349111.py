import cv2
import numpy as np
import pandas as pd
import math

data = pd.read_excel('codebook1.xlsx', header=None) 
codebook = data.values 

img = cv2.imread('Lena.jpg', cv2.IMREAD_GRAYSCALE)
h, w = img.shape

index = np.zeros((h // 4, w // 4), dtype=np.uint8)
decompressed_img = np.zeros((h, w), dtype=np.uint8)

print("開始壓縮影像...")
for i in range(0, h, 4):
    for j in range(0, w, 4):
        block = img[i:i+4, j:j+4].flatten()
        
        d = np.linalg.norm(codebook - block, axis=1)
        
        best_index = np.argmin(d)
        
        index[i//4, j//4] = best_index

print("開始解壓縮影像...")
for i in range(h // 4):
    for j in range(w // 4):
        idx = index[i, j]
        
        codeword = codebook[idx]
        
        decompressed_img[i*4:(i+1)*4, j*4:(j+1)*4] = codeword.reshape((4, 4))

psnr = cv2.PSNR(img, decompressed_img)

print(f"原圖與解壓縮比較的影像品質 PSNR:{psnr:.2f} db")

index_img = cv2.normalize(index, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

cv2.imshow('Original Image', img)
cv2.imshow('Compressed Index Image', index_img)
cv2.imshow('Decompressed Image', decompressed_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
