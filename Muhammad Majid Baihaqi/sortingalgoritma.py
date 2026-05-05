import streamlit as st
import time
import random
import pandas as pd

st.title("📊 Benchmark Sorting Algorithm (Rata-rata 3x Run)")

# Fungsi generate data
def generate_data(n):
    return [random.randint(1, 10000) for _ in range(n)]

# Bubble Sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Insertion Sort
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = key

# Quick Sort
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Fungsi hitung rata-rata waktu
def average_time(sort_func, data, runs=3):
    total = 0
    for _ in range(runs):
        arr = data.copy()
        start = time.time()
        if sort_func == quick_sort:
            sort_func(arr)
        else:
            sort_func(arr)
        total += (time.time() - start)
    return total / runs

# UI pilih ukuran data
sizes = st.multiselect(
    "Pilih ukuran data:",
    [100, 1000, 10000],
    default=[100, 1000]
)

if st.button("🚀 Jalankan Benchmark"):
    results = []

    for size in sizes:
        data = generate_data(size)

        bubble_avg = average_time(bubble_sort, data)
        insertion_avg = average_time(insertion_sort, data)
        quick_avg = average_time(quick_sort, data)

        results.append({
            "Data": size,
            "Bubble Sort (avg)": bubble_avg,
            "Insertion Sort (avg)": insertion_avg,
            "Quick Sort (avg)": quick_avg
        })

    df = pd.DataFrame(results)

    st.subheader("📋 Hasil Benchmark (Rata-rata 3x)")
    st.dataframe(df)

    st.subheader("📈 Grafik Perbandingan")
    st.line_chart(df.set_index("Data"))
