import numpy as np
import matplotlib.pyplot as plt 
import cv2

num = 150
# np.random.seed(5)

# 擴大座標範圍至 0~500，以包含 (200, 300) 的座標點
trains = np.random.randint(0, 500, size=(num,2)).astype(np.float32)

labels = np.array([0]*50 + [1]*50 + [2]*50).astype(np.float32)

blue_x = trains[labels.ravel() == 0]
plt.scatter(blue_x[:,0], blue_x[:,1], s=50, c='b', marker='x', label='Blue X')

yellow_o = trains[labels.ravel() == 1]
plt.scatter(yellow_o[:,0], yellow_o[:,1], s=50, c='y', marker='o', label='Yellow Circle')

black_v = trains[labels.ravel() == 2]
plt.scatter(black_v[:,0], black_v[:,1], s=50, c='k', marker='v', label='Black Down-Triangle')

test = np.array([[200, 300]]).astype(np.float32)
plt.scatter(test[:,0], test[:,1], s=100, c='r', marker='s', label='Test (Red Square)')

k = 7
knn = cv2.ml.KNearest_create()
knn.train(trains, cv2.ml.ROW_SAMPLE, labels)

ret, results, neighbours, dist = knn.findNearest(test, k=k)

class_names = {0.0: "Blue", 1.0: "Yellow", 2.0: "black"}
result_name = class_names[results[0][0]]

plt.title(f"KNN Classification Result:{result_name}")
plt.legend(loc='upper right')

print(f"鄰居標籤為: {neighbours.ravel()}")
print(f"最終判定為: {result_name}")

plt.show()