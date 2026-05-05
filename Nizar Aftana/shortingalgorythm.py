import random
import time
import matplotlib.pyplot as plt

# =========================
# ALGORITMA SORTING
# =========================

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a

def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr)//2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# =========================
# BENCHMARK
# =========================

sizes = [100, 1000, 10000, 50000]

bubble_times = []
insertion_times = []
merge_times = []

for size in sizes:
    data = [random.randint(1, 100000) for _ in range(size)]
    
    # Bubble Sort
    total = 0
    for _ in range(3):
        start = time.time()
        bubble_sort(data)
        end = time.time()
        total += (end - start)
    bubble_times.append(total / 3)
    
    # Insertion Sort
    total = 0
    for _ in range(3):
        start = time.time()
        insertion_sort(data)
        end = time.time()
        total += (end - start)
    insertion_times.append(total / 3)
    
    # Merge Sort
    total = 0
    for _ in range(3):
        start = time.time()
        merge_sort(data)
        end = time.time()
        total += (end - start)
    merge_times.append(total / 3)

# =========================
# TABEL OUTPUT
# =========================

print("Ukuran | Bubble | Insertion | Merge")
for i in range(len(sizes)):
    print(f"{sizes[i]} | {bubble_times[i]:.5f} | {insertion_times[i]:.5f} | {merge_times[i]:.5f}")

# =========================
# GRAFIK
# =========================

plt.plot(sizes, bubble_times, label="Bubble Sort")
plt.plot(sizes, insertion_times, label="Insertion Sort")
plt.plot(sizes, merge_times, label="Merge Sort")

plt.xlabel("Ukuran Data")
plt.ylabel("Waktu (detik)")
plt.title("Perbandingan Sorting")
plt.legend()
plt.show()