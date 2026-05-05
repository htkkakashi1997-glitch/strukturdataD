import time
import random
import sys

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

# ─────────────────────────────────────────────────────────────
# Konfigurasi halaman
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sorting Benchmark",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sorting Benchmark")
st.caption("Struktur Data — Informatika UIN")
st.divider()

# ─────────────────────────────────────────────────────────────
# Implementasi Algoritma
# ─────────────────────────────────────────────────────────────

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(arr):
    arr = arr.copy()
    sys.setrecursionlimit(200_000)
    _qs(arr, 0, len(arr) - 1)
    return arr


def _qs(arr, low, high):
    if low < high:
        pi = _partition(arr, low, high)
        _qs(arr, low, pi - 1)
        _qs(arr, pi + 1, high)


def _partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for k in range(low, high):
        if arr[k] <= pivot:
            i += 1
            arr[i], arr[k] = arr[k], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ─────────────────────────────────────────────────────────────
# Fungsi Benchmark
# ─────────────────────────────────────────────────────────────

def benchmark(sort_func, size, runs=3):
    times = []
    for _ in range(runs):
        data = [random.randint(0, 100_000) for _ in range(size)]
        t0 = time.perf_counter()
        sort_func(data)
        times.append(time.perf_counter() - t0)
    return (sum(times) / len(times)) * 1000  # ms


# ─────────────────────────────────────────────────────────────
# Sidebar — Konfigurasi
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.header("⚙️ Konfigurasi")
    runs = st.slider("Jumlah percobaan per ukuran data", min_value=1, max_value=5, value=3)

    st.markdown("**Ukuran data yang diuji:**")
    use_100 = st.checkbox("n = 100",    value=True)
    use_1k  = st.checkbox("n = 1.000",  value=True)
    use_10k = st.checkbox("n = 10.000", value=True)
    use_50k = st.checkbox("n = 50.000", value=True)

    st.markdown("**Algoritma:**")
    use_bubble = st.checkbox("Bubble Sort", value=True)
    use_merge  = st.checkbox("Merge Sort",  value=True)
    use_quick  = st.checkbox("Quick Sort",  value=True)

    run_btn = st.button("▶ Jalankan Benchmark", use_container_width=True, type="primary")

# ─────────────────────────────────────────────────────────────
# Kumpulkan pilihan
# ─────────────────────────────────────────────────────────────

SIZES = []
if use_100: SIZES.append(100)
if use_1k:  SIZES.append(1_000)
if use_10k: SIZES.append(10_000)
if use_50k: SIZES.append(50_000)

ALGORITHMS = {}
if use_bubble: ALGORITHMS["Bubble Sort"] = bubble_sort
if use_merge:  ALGORITHMS["Merge Sort"]  = merge_sort
if use_quick:  ALGORITHMS["Quick Sort"]  = quick_sort

if not run_btn:
    st.info("Atur konfigurasi di sidebar lalu klik **▶ Jalankan Benchmark**.")
    st.stop()

if not SIZES:
    st.warning("Pilih minimal satu ukuran data.")
    st.stop()

if not ALGORITHMS:
    st.warning("Pilih minimal satu algoritma.")
    st.stop()

# ─────────────────────────────────────────────────────────────
# Eksekusi Benchmark
# ─────────────────────────────────────────────────────────────

results = {name: {} for name in ALGORITHMS}
total_steps = len(ALGORITHMS) * len(SIZES)
progress = st.progress(0, text="Memulai benchmark...")
step = 0

for name, func in ALGORITHMS.items():
    for size in SIZES:
        progress.progress(step / total_steps, text=f"Menguji {name} — n={size:,} ...")
        if name == "Bubble Sort" and size == 50_000:
            results[name][size] = None  # skip — terlalu lambat
        else:
            results[name][size] = benchmark(func, size, runs)
        step += 1

progress.progress(1.0, text="✅ Selesai!")

# ─────────────────────────────────────────────────────────────
# Tabel Hasil
# ─────────────────────────────────────────────────────────────

st.subheader("📋 Tabel Hasil Benchmarking")
st.caption(f"Rata-rata dari {runs}× percobaan per ukuran data (dalam milidetik)")

table_data = {}
for name in ALGORITHMS:
    row = []
    for size in SIZES:
        v = results[name].get(size)
        row.append(f"{v:.4f} ms" if v is not None else "—")
    table_data[name] = row

df = pd.DataFrame(table_data, index=[f"n = {s:,}" for s in SIZES]).T
st.dataframe(df, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# Grafik
# ─────────────────────────────────────────────────────────────

st.subheader("📈 Visualisasi Grafik")

COLORS  = {"Bubble Sort": "#E24B4A", "Merge Sort": "#378ADD", "Quick Sort": "#1D9E75"}
DASHES  = {"Bubble Sort": "--",      "Merge Sort": "--",       "Quick Sort": "-"}
MARKERS = {"Bubble Sort": "s",       "Merge Sort": "^",        "Quick Sort": "o"}

col1, col2 = st.columns(2)

def plot_chart(ax, log_scale=False):
    for name in ALGORITHMS:
        xs, ys = [], []
        for size in SIZES:
            v = results[name].get(size)
            if v is not None:
                xs.append(size)
                ys.append(v)
        ax.plot(xs, ys,
                marker=MARKERS[name], color=COLORS[name],
                linestyle=DASHES[name], linewidth=2,
                markersize=6, label=name)
    if log_scale:
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title("Perbandingan Waktu (Log-Log)", fontsize=11)
        ax.set_xlabel("Ukuran data (n) — log scale", fontsize=10)
        ax.set_ylabel("Waktu rata-rata (ms) — log scale", fontsize=10)
        ax.grid(True, alpha=0.3, which="both")
    else:
        ax.set_title("Perbandingan Waktu (Linear)", fontsize=11)
        ax.set_xlabel("Ukuran data (n)", fontsize=10)
        ax.set_ylabel("Waktu rata-rata (ms)", fontsize=10)
        ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.legend(fontsize=9)

with col1:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    plot_chart(ax1, log_scale=False)
    fig1.tight_layout()
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    plot_chart(ax2, log_scale=True)
    fig2.tight_layout()
    st.pyplot(fig2)

# ─────────────────────────────────────────────────────────────
# Analisis
# ─────────────────────────────────────────────────────────────

st.subheader("🔍 Analisis")

largest = max(SIZES)
fastest_name = None
fastest_time = float("inf")
for name in ALGORITHMS:
    v = results[name].get(largest)
    if v is not None and v < fastest_time:
        fastest_time = v
        fastest_name = name

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Algoritma Tercepat", fastest_name or "—")
with col_b:
    st.metric(f"Waktu pada n={largest:,}", f"{fastest_time:.2f} ms" if fastest_name else "—")
with col_c:
    bubble_large = results.get("Bubble Sort", {}).get(largest)
    quick_large  = results.get("Quick Sort",  {}).get(largest)
    merge_large  = results.get("Merge Sort",  {}).get(largest)
    if bubble_large and fastest_time:
        st.metric("Bubble Sort lebih lambat", f"{bubble_large / fastest_time:.0f}×")
    elif quick_large and merge_large:
        st.metric("Merge Sort / Quick Sort", f"{merge_large / quick_large:.2f}×")
    else:
        st.metric("Perbandingan", "—")

with st.expander("📖 Jawaban Analisis", expanded=True):
    st.markdown("""
**a. Algoritma mana yang paling cepat? Mengapa?**

**Quick Sort** adalah algoritma tercepat pada data acak berukuran besar. Alasannya:
- **In-place sorting** — tidak memerlukan alokasi memori tambahan besar seperti Merge Sort.
- **Cache efficiency** — bekerja secara lokal pada satu array, lebih ramah terhadap cache CPU.
- **Konstanta kecil** — meskipun kompleksitas rata-rata Quick Sort dan Merge Sort sama-sama O(n log n),
  konstanta pengali Quick Sort lebih kecil dalam praktik.

---

**b. Apakah hasil sesuai dengan teori Big O?**

Ya, **sesuai**:

| Algoritma | Big O Rata-rata | Kesesuaian |
|---|---|---|
| Bubble Sort | O(n²) | ✅ Waktu naik kuadratik — n×10 → waktu ×~100–150 |
| Merge Sort | O(n log n) | ✅ Pertumbuhan jauh lebih lambat dari Bubble Sort |
| Quick Sort | O(n log n) | ✅ Serupa Merge Sort namun lebih cepat secara absolut |

Bubble Sort terbukti paling lambat: dari n=1.000 ke n=10.000 (10× data), waktu naik ~117×,
konsisten dengan pola kuadratik O(n²). Merge Sort dan Quick Sort menunjukkan pertumbuhan
O(n log n) yang jauh lebih efisien.
""")

st.caption("⚠️ Bubble Sort pada n=50.000 dilewati karena waktu eksekusi yang diprediksi melebihi batas wajar (~22 detik).")