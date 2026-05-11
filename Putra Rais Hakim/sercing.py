import streamlit as st
import time
import random

st.set_page_config(page_title="Searching Algorithm Visualizer", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Space+Grotesk:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00f5d4;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #aaa;
        margin-bottom: 2rem;
        font-size: 1rem;
    }
    .algo-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(0,245,212,0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
    }
    .step-log {
        font-family: 'Fira Code', monospace;
        font-size: 0.85rem;
        color: #ccc;
        background: rgba(0,0,0,0.3);
        border-radius: 8px;
        padding: 0.8rem;
        max-height: 200px;
        overflow-y: auto;
    }
    .highlight-found {
        color: #00f5d4;
        font-weight: 700;
    }
    .highlight-check {
        color: #f5a623;
    }
    .metric-card {
        background: rgba(0,245,212,0.1);
        border: 1px solid #00f5d4;
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🔍 Searching Algorithm Visualizer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Visualisasi Linear Search & Binary Search secara interaktif</div>', unsafe_allow_html=True)

# ── Sidebar Controls ──────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Pengaturan")
    algo = st.radio("Pilih Algoritma", ["Linear Search", "Binary Search"])
    array_size = st.slider("Ukuran Array", 5, 30, 15)
    
    if st.button("🎲 Generate Array Baru"):
        if algo == "Binary Search":
            arr = sorted(random.sample(range(1, 101), array_size))
        else:
            arr = random.sample(range(1, 101), array_size)
        st.session_state["array"] = arr

    if "array" not in st.session_state:
        if algo == "Binary Search":
            st.session_state["array"] = sorted(random.sample(range(1, 101), array_size))
        else:
            st.session_state["array"] = random.sample(range(1, 101), array_size)

    arr = st.session_state["array"]
    target = st.number_input("🎯 Cari Nilai", min_value=1, max_value=100, value=arr[array_size // 2])
    speed = st.slider("Kecepatan Animasi (detik)", 0.1, 1.5, 0.5, 0.1)
    start_btn = st.button("▶️ Mulai Visualisasi", use_container_width=True)

arr = st.session_state["array"]

# ── Array Display ──────────────────────────────────────────────────
def render_array(arr, highlight=None, found=None, low=None, high=None, mid=None):
    cols = st.columns(len(arr))
    for i, val in enumerate(arr):
        with cols[i]:
            if found is not None and i == found:
                color = "#00f5d4"
                border = "3px solid #00f5d4"
                text_color = "#000"
            elif highlight is not None and i == highlight:
                color = "#f5a623"
                border = "3px solid #f5a623"
                text_color = "#000"
            elif mid is not None and i == mid:
                color = "#e040fb"
                border = "3px solid #e040fb"
                text_color = "#fff"
            elif low is not None and high is not None and low <= i <= high:
                color = "rgba(0,245,212,0.15)"
                border = "1px solid #00f5d412"
                text_color = "#fff"
            else:
                color = "rgba(255,255,255,0.05)"
                border = "1px solid rgba(255,255,255,0.15)"
                text_color = "#aaa"

            st.markdown(
                f"""<div style="
                    background:{color};
                    border:{border};
                    border-radius:8px;
                    padding:0.5rem 0;
                    text-align:center;
                    font-family:'Fira Code',monospace;
                    font-weight:600;
                    color:{text_color};
                    transition: all 0.3s;
                ">
                    <div style="font-size:1.1rem">{val}</div>
                    <div style="font-size:0.65rem;color:#888">idx {i}</div>
                </div>""",
                unsafe_allow_html=True
            )

# ── Initial render ─────────────────────────────────────────────────
st.markdown("### 📊 Array")
arr_placeholder = st.empty()
with arr_placeholder.container():
    render_array(arr)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    steps_ph = st.empty()
with col2:
    result_ph = st.empty()

log_ph = st.empty()

# ── Algorithms ─────────────────────────────────────────────────────
def linear_search_visualize(arr, target, speed):
    steps = []
    result_ph.info("🔄 Mencari...")
    
    for i in range(len(arr)):
        with arr_placeholder.container():
            render_array(arr, highlight=i)
        
        steps.append(f"Step {i+1}: Memeriksa index {i} → nilai {arr[i]}")
        with log_ph.container():
            st.markdown('<div class="step-log">' + 
                       "<br>".join([f'<span class="highlight-check">{s}</span>' if j == len(steps)-1 else s 
                                    for j, s in enumerate(steps)]) + 
                       '</div>', unsafe_allow_html=True)
        
        with steps_ph.container():
            st.markdown(f'<div class="metric-card"><b style="color:#00f5d4;font-size:1.5rem">{i+1}</b><br><small>Langkah</small></div>', 
                       unsafe_allow_html=True)
        
        time.sleep(speed)
        
        if arr[i] == target:
            with arr_placeholder.container():
                render_array(arr, found=i)
            result_ph.success(f"✅ Ditemukan! Nilai {target} ada di index {i}")
            steps.append(f"✅ DITEMUKAN di index {i}!")
            with log_ph.container():
                st.markdown('<div class="step-log">' + "<br>".join(steps) + '</div>', unsafe_allow_html=True)
            return i, len(steps)
    
    result_ph.error(f"❌ Nilai {target} tidak ditemukan dalam array.")
    return -1, len(steps)


def binary_search_visualize(arr, target, speed):
    steps = []
    low, high = 0, len(arr) - 1
    step_count = 0
    result_ph.info("🔄 Mencari...")
    
    while low <= high:
        mid = (low + high) // 2
        step_count += 1
        
        with arr_placeholder.container():
            render_array(arr, mid=mid, low=low, high=high)
        
        steps.append(f"Step {step_count}: low={low}, high={high}, mid={mid} → nilai {arr[mid]}")
        with log_ph.container():
            st.markdown('<div class="step-log">' + 
                       "<br>".join([f'<span class="highlight-check">{s}</span>' if j == len(steps)-1 else s 
                                    for j, s in enumerate(steps)]) + 
                       '</div>', unsafe_allow_html=True)
        
        with steps_ph.container():
            st.markdown(f'<div class="metric-card"><b style="color:#00f5d4;font-size:1.5rem">{step_count}</b><br><small>Langkah</small></div>', 
                       unsafe_allow_html=True)
        
        time.sleep(speed)
        
        if arr[mid] == target:
            with arr_placeholder.container():
                render_array(arr, found=mid)
            result_ph.success(f"✅ Ditemukan! Nilai {target} ada di index {mid}")
            steps.append(f"✅ DITEMUKAN di index {mid}!")
            with log_ph.container():
                st.markdown('<div class="step-log">' + "<br>".join(steps) + '</div>', unsafe_allow_html=True)
            return mid, step_count
        elif arr[mid] < target:
            steps.append(f"   → {arr[mid]} < {target}, geser ke kanan (low = {mid+1})")
            low = mid + 1
        else:
            steps.append(f"   → {arr[mid]} > {target}, geser ke kiri (high = {mid-1})")
            high = mid - 1
    
    result_ph.error(f"❌ Nilai {target} tidak ditemukan dalam array.")
    return -1, step_count

# ── Info Panel ─────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📚 Penjelasan Algoritma"):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
**🔵 Linear Search**
- Memeriksa setiap elemen satu per satu dari kiri ke kanan
- **Time Complexity:** O(n)
- **Space Complexity:** O(1)
- Bekerja pada array **tidak terurut maupun terurut**
- Cocok untuk dataset kecil
        """)
    with c2:
        st.markdown("""
**🟣 Binary Search**
- Membagi array menjadi dua bagian setiap iterasi
- **Time Complexity:** O(log n)
- **Space Complexity:** O(1)
- Hanya bekerja pada array yang **sudah terurut**
- Jauh lebih efisien untuk dataset besar
        """)

# ── Run ────────────────────────────────────────────────────────────
if start_btn:
    if algo == "Binary Search" and sorted(arr) != arr:
        st.warning("⚠️ Binary Search memerlukan array terurut. Array akan diurutkan otomatis.")
        arr = sorted(arr)
        st.session_state["array"] = arr

    if algo == "Linear Search":
        idx, total_steps = linear_search_visualize(arr, target, speed)
    else:
        idx, total_steps = binary_search_visualize(arr, target, speed)