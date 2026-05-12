import time
import random
import sys

# Menambah limit rekursi untuk Quick Sort pada data besar
sys.setrecursionlimit(200000)

# --- Algoritma Sorting ---

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
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

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# --- Fungsi Benchmarking ---

def benchmark():
    sizes = [100, 1000, 10000, 50000]
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort)
    ]
    
    results = {}

    for size in sizes:
        print(f"Testing size: {size}...")
        results[size] = {}
        for name, func in algorithms:
            # Skip Bubble Sort untuk 50.000 karena akan sangat lama (>30 menit)
            if name == "Bubble Sort" and size > 10000:
                results[size][name] = "N/A (Too Slow)"
                continue
                
            times = []
            for _ in range(3):
                data = [random.randint(0, 100000) for _ in range(size)]
                start_time = time.time()
                func(data.copy())
                end_time = time.time()
                times.append(end_time - start_time)
            
            avg_time = sum(times) / 3
            results[size][name] = round(avg_time, 6)
            
    return results

# Menjalankan Benchmark
results = benchmark()

# Menampilkan Tabel Hasil
print("\n--- Tabel Hasil Benchmarking (detik) ---")
header = f"{'Ukuran Data':<15} | {'Bubble Sort':<15} | {'Merge Sort':<15} | {'Quick Sort':<15}"
print(header)
print("-" * len(header))
for size, algos in results.items():
    print(f"{size:<15} | {str(algos['Bubble Sort']):<15} | {str(algos['Merge Sort']):<15} | {str(algos['Quick Sort']):<15}")