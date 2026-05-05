import streamlit as st
import time

# 1. Struktur Data Circular Linked List
class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

def create_traffic_light():
    merah = Node("MERAH", 40)
    hijau = Node("HIJAU", 20)
    kuning = Node("KUNING", 5)

    # Urutan: Merah -> Hijau -> Kuning -> Merah
    merah.next = hijau
    hijau.next = kuning
    kuning.next = merah
    return merah

# 2. Setup Halaman
st.set_page_config(page_title="Lampu Lalu Lintas", layout="centered")
st.title("🚦 Simulasi Lampu Lalu Lintas Asli")

if 'current_node' not in st.session_state:
    st.session_state.current_node = create_traffic_light()

placeholder = st.empty()

# 3. Loop Visualisasi
while True:
    node = st.session_state.current_node
    
    with placeholder.container():
        # Membuat layout agar lampu berada di tengah
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            # FRAME LAMPU (Atas ke Bawah)
            
            # Lampu MERAH
            if node.warna == "MERAH":
                st.error("### ● MERAH")
            else:
                st.write("⚪ (mati)")

            st.write("---") # Pembatas antar lampu

            # Lampu KUNING
            if node.warna == "KUNING":
                st.warning("### ● KUNING")
            else:
                st.write("⚪ (mati)")

            st.write("---")

            # Lampu HIJAU
            if node.warna == "HIJAU":
                st.success("### ● HIJAU")
            else:
                st.write("⚪ (mati)")

        # Bagian Durasi di bawah lampu
        st.divider()
        st.write(f"**Status Sekarang:** {node.warna}")
        
        progress_bar = st.progress(0)
        status_timer = st.empty()

        for i in range(node.durasi):
            detik_sisa = node.durasi - i
            status_timer.text(f"Berubah dalam {detik_sisa} detik...")
            progress_bar.progress((i + 1) / node.durasi)
            time.sleep(1)

    # Logika Circular Linked List pindah ke Node berikutnya
    st.session_state.current_node = node.next
    st.rerun()