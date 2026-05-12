import streamlit as st
import time

st.title("🔍 Visualisasi Algoritma Searching")

# Input data
data_input = st.text_input("Masukkan angka (pisahkan dengan koma)", "5,2,8,1,9,3")
key = st.number_input("Masukkan angka yang dicari", step=1)

algoritma = st.selectbox("Pilih Algoritma", ["Linear Search", "Binary Search"])

# Konversi input ke list integer
try:
    data = list(map(int, data_input.split(",")))
except:
    st.error("Input harus berupa angka dipisahkan koma!")
    st.stop()

if st.button("Mulai Pencarian"):

    if algoritma == "Linear Search":
        st.subheader("Proses Linear Search")
        found = False
        
        for i in range(len(data)):
            st.write(f"Mengecek index {i} → {data[i]}")
            time.sleep(0.7)

            if data[i] == key:
                st.success(f"✅ Data ditemukan di index {i}")
                found = True
                break
        
        if not found:
            st.error("❌ Data tidak ditemukan")

    else:
        st.subheader("Proses Binary Search")
        data.sort()
        st.write("Data setelah diurutkan:", data)
        time.sleep(1)

        low = 0
        high = len(data) - 1
        found = False

        while low <= high:
            mid = (low + high) // 2
            st.write(f"Low={low}, High={high}, Mid={mid}")
            st.write(f"Mengecek nilai tengah → {data[mid]}")
            time.sleep(1)

            if data[mid] == key:
                st.success(f"✅ Data ditemukan di index {mid}")
                found = True
                break
            elif data[mid] < key:
                low = mid + 1
            else:
                high = mid - 1

        if not found:
            st.error("❌ Data tidak ditemukan")