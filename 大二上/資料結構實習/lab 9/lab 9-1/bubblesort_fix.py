import random
import time

def bubble_sort(arr):
    """
    優化的 Bubble Sort 實作
    加入 no swap 判斷，如果某輪沒有發生交換則提前結束
    """
    n = len(arr)
    for i in range(n - 1):
        swapped = False  # 標記本輪是否發生交換
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True  # 發生交換
        # 如果本輪沒有發生交換，表示已經排序完成
        if not swapped:
            break

def generate_random(n):
    """生成隨機分布資料"""
    return [random.randint(0, 999999) for _ in range(n)]

def generate_good(n):
    """生成已排序但有1%資料未排序的資料"""
    arr = list(range(n))
    # 打亂1%的資料
    swap_count = n // 100
    for _ in range(swap_count):
        idx1 = random.randint(0, n - 1)
        idx2 = random.randint(0, n - 1)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr

def generate_worst(n):
    """生成最差情況資料（反向排序）"""
    return list(range(n - 1, -1, -1))

def test_sort(n, data_type, generate_func):
    """測試排序並計時"""
    arr = generate_func(n)
    
    # 使用 time.perf_counter_ns() 進行納秒級高精度計時
    start_time = time.perf_counter_ns()
    bubble_sort(arr)
    end_time = time.perf_counter_ns()
    
    elapsed_ns = end_time - start_time
    
    print(f"{n} {data_type}: {elapsed_ns} ns")

def main():
    sizes = [10000, 100000, 1000000]
    
    print("Python Bubble Sort 測試結果 (使用 time.perf_counter_ns()，加入 no swap 優化):")
    print("=========================================================")
    
    for n in sizes:
        print(f"\n資料量: {n}")
        test_sort(n, "random", generate_random)
        test_sort(n, "good", generate_good)
        test_sort(n, "worst", generate_worst)

if __name__ == "__main__":
    main()