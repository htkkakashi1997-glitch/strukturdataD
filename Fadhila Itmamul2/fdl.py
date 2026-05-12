import time
import random
import sys

# Menambah limit rekursi untuk Quick Sort pada data besar
sys.setrecursionlimit(100000)

# --- ALGORITMA SORTING ---

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# --- BENCHMARKING ENGINE ---

sizes = [100, 1000, 10000, 50000]
algorithms = {
    "Bubble Sort": bubble_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}

results = {alg: [] for alg in algorithms}

print(f"{'Algoritma':<15} | {'Size':<10} | {'Rata-rata Waktu (detik)':<20}")
print("-" * 50)

for size in sizes:
    data_original = [random.randint(0, 100000) for _ in range(size)]
    
    for name, func in algorithms.items():
        # Lewati Bubble Sort untuk 50.000 karena akan SANGAT lama (bisa berjam-jam)
        if name == "Bubble Sort" and size > 10000:
            results[name].append("N/A (Too Slow)")
            continue
            
        times = []
        for _ in range(3): # Jalankan minimal 3 kali
            data_copy = data_original.copy()
            start_time = time.time()
            func(data_copy)
            end_time = time.time()
            times.append(end_time - start_time)
        
        avg_time = sum(times) / len(times)
        results[name].append(round(avg_time, 6))
        print(f"{name:<15} | {size:<10} | {avg_time:<20.6f}")