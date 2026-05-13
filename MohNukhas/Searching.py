import streamlit as st
import time
import pandas as pd

# Judul Aplikasi
st.set_page_config(page_title="Tugas Struktur Data - Searching & Hashing", layout="wide")
st.title("🔍 Visualisasi Searching & Implementasi Hashing")
st.write("Dibuat untuk memenuhi tugas Informatika UINSSC")

# Sidebar untuk Navigasi
menu = st.sidebar.selectbox("Pilih Menu:", ["Searching Visualization", "Hashing Implementation"])

# --- BAGIAN 1: SEARCHING VISUALIZATION ---
if menu == "Searching Visualization":
    st.header("1. Visualisasi Algoritma Searching")
    
    # Input data
    raw_input = st.text_input("Masukkan angka (pisahkan dengan koma):", "10, 50, 30, 70, 80, 60, 20, 90, 40")
    data = [int(x.strip()) for x in raw_input.split(",")]
    key = st.number_input("Cari angka:", value=30)
    
    algo = st.radio("Pilih Algoritma:", ["Sequential Search", "Binary Search"])
    
    if st.button("Mulai Cari"):
        if algo == "Sequential Search":
            st.subheader("Proses Sequential Search")
            st.info("Algoritma ini membandingkan data satu per satu dari awal. [cite: 203]")
            found = False
            cols = st.columns(len(data))
            
            for i in range(len(data)):
                # Visualisasi
                with cols[i]:
                    if data[i] == key:
                        st.success(f"[{data[i]}]")
                        st.write(f"Index {i}: Match!")
                        found = True
                    else:
                        st.warning(f"{data[i]}")
                        st.write(f"Index {i}")
                time.sleep(0.5)
                if found: break
            
            if found: st.balloons()
            else: st.error("Data tidak ditemukan.")

        else: # Binary Search
            st.subheader("Proses Binary Search")
            st.info("Data harus terurut terlebih dahulu! [cite: 267]")
            data.sort()
            st.write("Data terurut:", data)
            
            low = 0
            high = len(data) - 1
            found = False
            
            placeholder = st.empty()
            
            while low <= high:
                mid = (low + high) // 2 # Rumus sesuai slide [cite: 274]
                
                with placeholder.container():
                    st.write(f"Low: {low}, Mid: {mid}, High: {high}")
                    display_data = []
                    for idx, val in enumerate(data):
                        if idx == mid: display_data.append(f"🎯 {val}")
                        elif low <= idx <= high: display_data.append(f"{val}")
                        else: display_data.append(f"~~{val}~~")
                    st.write(" | ".join(display_data))
                
                time.sleep(1)
                
                if data[mid] == key:
                    st.success(f"Data {key} ditemukan di indeks {mid}!")
                    found = True
                    break
                elif data[mid] < key:
                    low = mid + 1
                else:
                    high = mid - 1
            
            if not found: st.error("Data tidak ditemukan.")

