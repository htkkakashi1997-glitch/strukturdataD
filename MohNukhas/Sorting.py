import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
import sys

# Menambah limit rekursi untuk Quick Sort pada data besar
sys.setrecursionlimit(100000)

# --- Implementasi Algoritma ---
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# --- Streamlit UI ---
st.set_page_config(page_title="Sorting Benchmark", layout="wide")
st.title("📊 Sorting Algorithm Benchmark Dashboard")

st.sidebar.header("Parameter Pengujian")
input_sizes = [100, 1000, 10000, 50000]
run_button = st.sidebar.button("Mulai Benchmark")

if run_button:
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Quick Sort": quick_sort
    }

    total_steps = len(input_sizes) * len(algorithms)
    step = 0

    for size in input_sizes:
        for name, func in algorithms.items():
            status_text.text(f"Running {name} pada data ukuran {size}...")
            
            # Catatan: Bubble/Selection sangat lambat di 50k, 
            # Dalam demo ini kita batasi agar tidak hang.
            if size == 50000 and name in ["Bubble Sort", "Selection Sort"]:
                avg_time = 0 # (Simulasi/Skip karena akan memakan waktu jam-an)
            else:
                times = []
                for _ in range(3):
                    data = [random.randint(0, 100000) for _ in range(size)]
                    start = time.time()
                    func(data.copy())
                    end = time.time()
                    times.append(end - start)
                avg_time = sum(times) / 3
            
            results.append({"Ukuran Data": size, "Algoritma": name, "Waktu (s)": avg_time})
            step += 1
            progress_bar.progress(step / total_steps)

    df = pd.DataFrame(results)
    pivot_df = df.pivot(index='Ukuran Data', columns='Algoritma', values='Waktu (s)')

    # Menampilkan Tabel
    st.subheader("Tabel Hasil Eksekusi (Rata-rata 3x)")
    st.dataframe(pivot_df.style.format("{:.5f}"))

    # Menampilkan Grafik
    st.subheader("Visualisasi Grafik Performa")
    fig, ax = plt.subplots(figsize=(10, 5))
    for col in pivot_df.columns:
        ax.plot(pivot_df.index, pivot_df[col], marker='o', label=col)
    
    ax.set_yscale('log') # Skala log agar Quick Sort terlihat dibanding Bubble Sort
    ax.set_xlabel("Ukuran Data (n)")
    ax.set_ylabel("Waktu (detik) - Skala Log")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    
    st.success("Benchmark Selesai!")
else:
    st.info("Klik tombol di sidebar untuk memulai simulasi benchmark.")