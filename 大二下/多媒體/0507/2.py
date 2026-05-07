import cv2
import numpy as np

# 1. 載入訓練好的數據
with np.load('knn_digit.npz') as data:
    train = data['train']
    train_labels = data['train_labels']

# 2. 初始化 KNN 並訓練數據
knn = cv2.ml.KNearest_create()
knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)

# 3. 定義要辨識的圖片列表
test_images = ['3.png', '8.png']

for img_name in test_images:
    # 讀取影像 (灰階)
    test_img = cv2.imread(img_name, cv2.IMREAD_GRAYSCALE)

    # 顯示影像
    cv2.imshow(f'Original - {img_name}', test_img)

    # 影像預處理：縮放成 20x20 並拉平成 1x400 的向量
    img_resized = cv2.resize(test_img, (20, 20))
    test_data = img_resized.reshape((1, 400)).astype(np.float32)

    # 4. 進行測試 (k=5)
    ret, result, neighbours, dist = knn.findNearest(test_data, k=5)
    
    # 5. 輸出辨識結果
    digit = int(result[0, 0])
    print(f"圖片 {img_name} 識別的數字是 = {digit}")

# 等待按鍵後關閉視窗
cv2.waitKey(0)
cv2.destroyAllWindows()