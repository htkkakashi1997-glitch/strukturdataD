import streamlit as st
import time

st.title("🔍 Visualisasi Algoritma Searching")

# Sidebar Input
st.sidebar.header("Konfigurasi")
n = st.sidebar.slider("Jumlah Data", 10, 50, 20)
target = st.sidebar.number_input("Cari Angka:", value=15)
speed = st.sidebar.slider("Kecepatan (detik):", 0.1, 1.0, 0.3)

# Generate Data
data = list(range(1, n + 1))

# Pilihan Algoritma
algo = st.selectbox("Pilih Algoritma", ["Linear Search", "Binary Search"])

if st.button("Mulai Pencarian"):
    cols = st.columns(n)
    placeholders = [cols[i].empty() for i in range(n)]
    
    # Tampilan awal
    for i in range(n):
        placeholders[i].button(f"{data[i]}", key=f"init_{i}")

    found = False
    if algo == "Linear Search":
        for i in range(n):
            # Highlight yang sedang diperiksa
            placeholders[i].button(f"{data[i]}", type="primary", key=f"search_{i}")
            time.sleep(speed)
            
            if data[i] == target:
                st.success(f"Ketemu! {target} ada di indeks {i}")
                found = True
                break
            else:
                placeholders[i].button(f"{data[i]}", key=f"done_{i}", disabled=True)
                
    elif algo == "Binary Search":
        low, high = 0, n - 1
        while low <= high:
            mid = (low + high) // 2
            placeholders[mid].button(f"{data[mid]}", type="primary", key=f"mid_{mid}")
            time.sleep(speed)
            
            if data[mid] == target:
                st.success(f"Ketemu! {target} ada di indeks {mid}")
                found = True
                break
            elif data[mid] < target:
                for j in range(low, mid + 1):
                    placeholders[j].button(f"{data[j]}", key=f"fail_{j}", disabled=True)
                low = mid + 1
            else:
                for j in range(mid, high + 1):
                    placeholders[j].button(f"{data[j]}", key=f"fail_{j}", disabled=True)
                high = mid - 1

    if not found:
        st.error("Data tidak ditemukan.")