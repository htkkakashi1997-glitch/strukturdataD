import streamlit as st
import random
import time
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sorting Benchmark", layout="wide")

st.title("📊 Sorting Benchmark")
st.write("Membandingkan performa **Bubble Sort**, **Merge Sort**, dan **Quick Sort** pada berbagai ukuran data.")

# ── Algoritma ────────────────────────────────────────────────────────────────

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Merge Sort":  merge_sort,
    "Quick Sort":  quick_sort,
}

DATA_SIZES = [100, 1_000, 10_000, 50_000]

# ── Sidebar ──────────────────────────────────────────────────────────────────

st.sidebar.header("⚙️ Pengaturan")
runs = st.sidebar.slider("Jumlah run per ukuran data", 1, 10, 3)
run_btn = st.sidebar.button("▶ Jalankan Benchmark", type="primary")

# ── Benchmark ────────────────────────────────────────────────────────────────

if run_btn:
    records = []
    progress = st.progress(0, text="Memulai...")
    total = len(ALGORITHMS) * len(DATA_SIZES)
    step = 0

    for algo_name, algo_fn in ALGORITHMS.items():
        for size in DATA_SIZES:
            times = []
            for _ in range(runs):
                data = [random.randint(0, 10_000_000) for _ in range(size)]
                t0 = time.perf_counter()
                algo_fn(data)
                times.append(time.perf_counter() - t0)

            avg_ms = (sum(times) / runs) * 1000
            records.append({
                "Algoritma":     algo_name,
                "Ukuran Data":   size,
                "Avg Time (ms)": round(avg_ms, 4),
                "Min (ms)":      round(min(times) * 1000, 4),
                "Max (ms)":      round(max(times) * 1000, 4),
            })
            step += 1
            progress.progress(step / total, text=f"{algo_name} | n={size:,}")

    progress.empty()
    st.session_state["df"] = pd.DataFrame(records)
    st.success("✅ Benchmark selesai!")

# ── Hasil ────────────────────────────────────────────────────────────────────

if "df" in st.session_state:
    df = st.session_state["df"]

    # Tabel pivot
    st.subheader("📋 Tabel Hasil Benchmarking (Avg Time dalam ms)")
    pivot = df.pivot(index="Algoritma", columns="Ukuran Data", values="Avg Time (ms)")
    pivot.columns = [f"n={c:,}" for c in pivot.columns]
    st.dataframe(pivot, use_container_width=True)

    # Tabel detail
    with st.expander("🔍 Lihat detail (Min / Max / Avg)"):
        st.dataframe(df, use_container_width=True, hide_index=True)

    # Grafik
    st.subheader("📈 Visualisasi Grafik")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Waktu Eksekusi per Ukuran Data (skala log)**")
        fig, ax = plt.subplots()
        for algo in ALGORITHMS:
            sub = df[df["Algoritma"] == algo].sort_values("Ukuran Data")
            ax.plot(sub["Ukuran Data"], sub["Avg Time (ms)"], marker="o", label=algo)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Ukuran Data (n)")
        ax.set_ylabel("Avg Time (ms)")
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

    with col2:
        st.write("**Perbandingan Algoritma pada n=50,000**")
        largest = df[df["Ukuran Data"] == 50_000]
        fig2, ax2 = plt.subplots()
        bars = ax2.bar(largest["Algoritma"], largest["Avg Time (ms)"],
                       color=["#ef4444", "#3b82f6", "#22c55e"])
        ax2.bar_label(bars, fmt="%.1f ms", padding=3)
        ax2.set_ylabel("Avg Time (ms)")
        ax2.grid(axis="y", linestyle="--", alpha=0.5)
        st.pyplot(fig2)

else:
    st.info("Klik **▶ Jalankan Benchmark** di sidebar untuk memulai.")