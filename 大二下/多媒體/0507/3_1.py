import cv2
import numpy as np

try:
    with np.load('knn_digit.npz') as data:
        train = data['train']
        train_labels = data['train_labels']
except FileNotFoundError:
    print("Error: knn_digit.npz not found.")
    exit()

knn = cv2.ml.KNearest_create()
knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)

img = cv2.imread('hiddendigits.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
enhanced = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
_, thresh = cv2.threshold(enhanced, 50, 255, cv2.THRESH_BINARY)

output_img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
bounding_boxes = [cv2.boundingRect(c) for c in contours]
sorted_boxes = sorted(bounding_boxes, key=lambda b: b[0])

found_numbers = []

print(f"{'順序':<5} | {'預測值':<6} | {'鄰居投票結果':<15}")
print("-" * 30)

for i, (x, y, w, h) in enumerate(sorted_boxes, 1):
    if w > 15 and h > 15:
        roi = thresh[y:y+h, x:x+w]
        
        max_dim = max(w, h)
        padding = int(max_dim * 0.3) 
        square_size = max_dim + padding * 2
        
        square_canvas = np.zeros((square_size, square_size), dtype=np.uint8)
        start_x = (square_size - w) // 2
        start_y = (square_size - h) // 2
        square_canvas[start_y:start_y+h, start_x:start_x+w] = roi
        
        kernel = np.ones((3, 3), np.uint8)
        thinned_canvas = cv2.erode(square_canvas, kernel, iterations=2)
        
        roi_resized = cv2.resize(thinned_canvas, (20, 20), interpolation=cv2.INTER_AREA)
        test_data = roi_resized.reshape((1, 400)).astype(np.float32)
        
        # k=3 代表取最近的三個鄰居
        ret, result, neighbours, dist = knn.findNearest(test_data, k=3)
        digit = int(result[0, 0])
        found_numbers.append(digit)
        
        # 印出詳細投票資訊
        print(f"{i:<7} | {digit:<9} | {str(neighbours[0]):<15}")
        
        cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(output_img, str(digit), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

print(f"辨識結果： {found_numbers}")
print(f"總合 = {sum(found_numbers)}")

cv2.imshow('Result', output_img)
cv2.waitKey(0)
cv2.destroyAllWindows()