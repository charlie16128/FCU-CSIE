import cv2
import numpy as np
import pandas as pd
import math

# ==========================================
# 步驟 1: 讀取編碼簿 (Codebook) 與原圖
# ==========================================
# 讀取 Excel 檔 (請確保 codebook 的格式是純數據，這裡假設每一列是一個 codeword)
# 如果 xlsx 包含 Header 或 Index 欄位，請在 pandas 讀取時透過 iloc 去除
data = pd.read_excel('codebook1.xlsx', header=None) 
codebook = data.values # 轉換成 numpy array，假設是形狀為 (K, 16) 的矩陣

# 讀取原圖 (轉為灰階)
img = cv2.imread('Lena.jpg', cv2.IMREAD_GRAYSCALE)
h, w = img.shape

# 準備兩個空的陣列：一個存壓縮後的索引，一個存解壓縮的圖片
index = np.zeros((h // 4, w // 4), dtype=np.uint8)
decompressed_img = np.zeros((h, w), dtype=np.uint8)

# ==========================================
# 步驟 2 & 3: 影像壓縮 (建立索引檔)
# ==========================================
print("開始壓縮影像...")
for i in range(0, h, 4):
    for j in range(0, w, 4):
        # 1. 抓取 4x4 區塊，並攤平成 16 1維向量
        block = img[i:i+4, j:j+4].flatten()
        
        # 2. 計算歐幾里德距離 (這裡利用 numpy 一次算完 block 對所有 codeword 的距離)
        #codebook (二維)：形狀是 (256, 16)。代表有 256 列，每列有 16 個數字。
        # block (一維)：形狀是 (16,)。代表只有 1 列，裡面有 16 個數字。
        d = np.linalg.norm(codebook - block, axis=1)
        
        # 3. 找出距離最小的那個 codeword 的 Index
        best_index = np.argmin(d)
        
        # 4. 把 Index 存入 index (這就是壓縮後的結果)
        index[i//4, j//4] = best_index

# ==========================================
# 步驟 4: 影像解壓縮 (還原影像)
# ==========================================    
print("開始解壓縮影像...")
for i in range(h // 4):
    for j in range(w // 4):
        # 1. 讀取索引值
        idx = index[i, j]
        
        # 2. 從編碼簿查出對應的 16 個像素值
        codeword = codebook[idx]
        
        # 3. 把 16 維向量折疊回 4x4 的區塊，並貼回原處
        decompressed_img[i*4:(i+1)*4, j*4:(j+1)*4] = codeword.reshape((4, 4))

# ==========================================
# 步驟 5: 計算 PSNR 與顯示結果
# ==========================================
# 手動撰寫 PSNR 計算公式 (對應配分要求)
# def calculate_psnr(img1, img2):
#     # 計算 MSE (均方誤差)
#     mse = np.mean((img1.astype(np.float64) - img2.astype(np.float64)) ** 2)
#     if mse == 0:
#         return float('inf')
#     # 計算 PSNR
#     max_pixel = 255.0
#     psnr = 10 * math.log10((max_pixel ** 2) / mse)
#     return psnr

# psnr_value = calculate_psnr(img, decompressed_img)

psnr = cv2.PSNR(img, decompressed_img)

print(f"原圖與解壓縮比較的影像品質 PSNR:{psnr:.2f} db")
# 註：你也可以用 OpenCV 內建的 cv2.PSNR(img, decompressed_img) 來驗證答案

# 為了讓「索引檔」視覺化可見，我們將其數值正規化到 0-255 範圍
# 否則索引值都很小，圖片看起來會是全黑的
index_img = cv2.normalize(index, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# 顯示配分要求的圖片
cv2.imshow('Original Image', img)
cv2.imshow('Compressed Index Image', index_img)
cv2.imshow('Decompressed Image', decompressed_img)

cv2.waitKey(0)
cv2.destroyAllWindows()