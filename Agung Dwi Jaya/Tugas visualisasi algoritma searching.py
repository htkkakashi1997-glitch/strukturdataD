import streamlit as st
import time

def linear_search(arr, target):
    steps = []
    for i in range(len(arr)):
        steps.append((i, arr[i]))
        if arr[i] == target:
            return i, steps
    return -1, steps

def binary_search(arr, target):
    steps = []
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        steps.append((mid, arr[mid]))
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1, steps

st.title("Visualisasi Algoritma Searching")
st.write("Pilih algoritma dan lihat langkah pencarian.")

arr = st.text_input("Masukkan list angka (pisahkan dengan koma)", "1,3,5,7,9,11,13,15")
arr = [int(x.strip()) for x in arr.split(",")]
target = st.number_input("Masukkan angka yang dicari", value=7)

algo = st.selectbox("Pilih algoritma", ["Linear Search", "Binary Search"])

if st.button("Mulai Pencarian"):
    if algo == "Linear Search":
        idx, steps = linear_search(arr, target)
    else:
        arr.sort()  # Binary search perlu data terurut
        idx, steps = binary_search(arr, target)

    st.write("### Langkah-langkah pencarian:")
    for step in steps:
        st.write(f"Memeriksa indeks {step[0]} → nilai {step[1]}")
        time.sleep(0.5)

    if idx != -1:
        st.success(f"Target {target} ditemukan pada indeks {idx}.")
    else:
        st.error(f"Target {target} tidak ditemukan.")