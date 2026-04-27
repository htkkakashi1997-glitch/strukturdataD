"""
Sorting Algorithm Benchmark
Membandingkan performa Bubble Sort, Merge Sort, dan Quick Sort
pada ukuran data: 100, 1.000, 10.000, 50.000
Setiap algoritma dijalankan 3 kali dan dihitung rata-rata waktu eksekusi.
"""

import numpy as np
import time
import sys
import matplotlib.pyplot as plt

sys.setrecursionlimit(200000)

# ─────────────────────────────────────────────
# Dataset (sesuai soal)
# ─────────────────────────────────────────────
rng = np.random.default_rng(42)

def generate_data(size):
    if size == 100:
        return rng.integers(0, 100, size=(1, 100)).flatten().tolist()
    elif size == 1000:
        return rng.integers(0, 1999, size=(1, 1000)).flatten().tolist()
    elif size == 10000:
        return rng.integers(0, 97862, size=(1, 10000)).flatten().tolist()
    elif size == 50000:
        return rng.integers(0, 127000, size=(1, 50000)).flatten().tolist()


# ─────────────────────────────────────────────
# Algoritma Sorting
# ─────────────────────────────────────────────

def bubble_sort(arr):
    """Bubble Sort - O(n^2)"""
    a = list(arr)
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def merge_sort(arr):
    """Merge Sort - O(n log n)"""
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def _partition(a, lo, hi):
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def quick_sort(arr):
    """Quick Sort (iteratif) - O(n log n) rata-rata"""
    a = list(arr)
    stack = [(0, len(a) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo < hi:
            p = _partition(a, lo, hi)
            stack.append((lo, p - 1))
            stack.append((p + 1, hi))
    return a


# ─────────────────────────────────────────────
# Benchmark
# ─────────────────────────────────────────────

def benchmark(sort_fn, data, runs=3):
    times = []
    for _ in range(runs):
        arr = list(data)
        t0 = time.perf_counter()
        sort_fn(arr)
        times.append(time.perf_counter() - t0)
    return times, sum(times) / runs


SIZES = [100, 1000, 10000, 50000]
RUNS = 3

bubble_avg = []
merge_avg = []
quick_avg = []

print(f"{'Ukuran':>8} | {'Bubble Sort':>14} | {'Merge Sort':>14} | {'Quick Sort':>14}")
print("-" * 60)

for size in SIZES:
    data = generate_data(size)

    if size <= 10000:
        _, b_avg = benchmark(bubble_sort, data, RUNS)
        bubble_avg.append(b_avg)
    else:
        b_avg = None
        bubble_avg.append(None)

    _, m_avg = benchmark(merge_sort, data, RUNS)
    merge_avg.append(m_avg)

    _, q_avg = benchmark(quick_sort, data, RUNS)
    quick_avg.append(q_avg)

    b_str = f"{b_avg:.6f}s" if b_avg is not None else "N/A (skip)"
    print(f"{size:>8,} | {b_str:>14} | {m_avg:>13.6f}s | {q_avg:>13.6f}s")


# ─────────────────────────────────────────────
# Visualisasi
# ─────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Sorting Algorithm Benchmark", fontsize=16, fontweight="bold")

x_labels = ["100", "1.000", "10.000", "50.000"]
x = list(range(len(SIZES)))

# Log scale line chart
ax1.set_title("Waktu Eksekusi vs Ukuran Data")
b_vals = [t if t else float("nan") for t in bubble_avg]
ax1.plot(x[:3], b_vals[:3], "o-", color="#e74c3c", label="Bubble Sort", lw=2)
ax1.plot(x, merge_avg, "s-", color="#3498db", label="Merge Sort", lw=2)
ax1.plot(x, quick_avg, "^-", color="#2ecc71", label="Quick Sort", lw=2)
ax1.set_yscale("log")
ax1.set_xticks(x)
ax1.set_xticklabels(x_labels)
ax1.set_xlabel("Ukuran Data (n)")
ax1.set_ylabel("Waktu Rata-rata (detik, log scale)")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Bar chart perbandingan n=1000 & n=10000
ax2.set_title("Perbandingan pada n=1.000 dan n=10.000")
bar_x = np.array([0, 1, 2])
w = 0.35
b1 = [bubble_avg[1], merge_avg[1], quick_avg[1]]
b2 = [bubble_avg[2], merge_avg[2], quick_avg[2]]
ax2.bar(bar_x - w / 2, b1, w, label="n=1.000", color=["#e74c3c", "#3498db", "#2ecc71"], alpha=0.85)
ax2.bar(bar_x + w / 2, b2, w, label="n=10.000", color=["#e74c3c", "#3498db", "#2ecc71"], alpha=0.4)
ax2.set_xticks(bar_x)
ax2.set_xticklabels(["Bubble Sort", "Merge Sort", "Quick Sort"])
ax2.set_ylabel("Waktu (detik)")
ax2.set_yscale("log")
ax2.legend()
ax2.grid(True, alpha=0.3, axis="y")

plt.tight_layout()
plt.savefig("benchmark_chart.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nGrafik disimpan sebagai benchmark_chart.png")