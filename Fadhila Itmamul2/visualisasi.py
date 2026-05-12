import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time
import sys

# Menaikkan limit rekursi
sys.setrecursionlimit(2000)

# 1. Implementasi Merge Sort
def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 2. Implementasi Quick Sort
def quick_sort(arr):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# 3. Implementasi Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

# --- UI Streamlit ---
st.set_page_config(page_title="Visualisasi Efisiensi Sorting", layout="wide")
st.title("📊 Perbandingan Performa: Merge, Quick, & Bubble Sort")

st.sidebar.header("Pengaturan Data")
# Batasi max_n ke 2000 agar Bubble Sort tidak membuat laptop hang/lama
max_n = st.sidebar.slider("Jumlah Data Maksimal", 100, 3000, 1000)
steps = st.sidebar.slider("Jumlah Titik Pengujian", 5, 15, 8)

if st.button("Mulai Simulasi 🚀"):
    sizes = np.linspace(10, max_n, steps, dtype=int)
    merge_times, quick_times, bubble_times = [], [], []

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, n in enumerate(sizes):
        data = np.random.randint(0, 10000, n).tolist()
        status_text.text(f"Menguji ukuran data: {n}...")

        # Test Merge Sort
        t1 = time.time()
        merge_sort(data.copy())
        merge_times.append(time.time() - t1)
        
        # Test Quick Sort
        t2 = time.time()
        quick_sort(data.copy())
        quick_times.append(time.time() - t2)

        # Test Bubble Sort
        t3 = time.time()
        bubble_sort(data.copy())
        bubble_times.append(time.time() - t3)
        
        progress_bar.progress((i + 1) / len(sizes))

    status_text.text("Simulasi Selesai!")

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sizes, merge_times, label='Merge Sort (O(n log n))', marker='o', color='#3498db')
    ax.plot(sizes, quick_times, label='Quick Sort (O(n log n))', marker='s', color='#e74c3c')
    ax.plot(sizes, bubble_times, label='Bubble Sort (O(n^2))', marker='^', color='#f1c40f')
    
    ax.set_xlabel('Ukuran Data (n)')
    ax.set_ylabel('Waktu Eksekusi (detik)')
    ax.set_title('Perbandingan Waktu Eksekusi')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    st.pyplot(fig)
    
    # Tabel Data
    st.subheader("📋 Detail Waktu (Detik)")
    st.table({
        "n": sizes,
        "Merge Sort": [f"{t:.5f}" for t in merge_times],
        "Quick Sort": [f"{t:.5f}" for t in quick_times],
        "Bubble Sort": [f"{t:.5f}" for t in bubble_times]
    })
else:
    st.info("Pilih jumlah data di sidebar dan klik tombol untuk memulai.")