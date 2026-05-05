import streamlit as st
import time

# =========================
# Node Circular Linked List
# =========================
class Node:
    def __init__(self, warna, durasi):
        self.warna = warna
        self.durasi = durasi
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, warna, durasi):
        new_node = Node(warna, durasi)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

# =========================
# Inisialisasi Lampu
# =========================
lampu = CircularLinkedList()
lampu.tambah("🔴", 40)
lampu.tambah("🟢", 20)
lampu.tambah("🟡", 5)

# =========================
# Streamlit UI
# =========================
st.title("🚦 Simulasi Lampu Lalu Lintas (Circular Linked List)")

start = st.button("Mulai Simulasi")

placeholder = st.empty()

if start:
    current = lampu.head
    
    while True:
        for i in range(current.durasi, 0, -1):
            if current.warna == "Merah":
                warna_bg = "red"
            elif current.warna == "Hijau":
                warna_bg = "green"
            else:
                warna_bg = "yellow"

            placeholder.markdown(
                f"""
                <div style='text-align:center'>
                    <h1 style='color:{warna_bg}'>{current.warna}</h1>
                    <h2>{i} detik</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(1)
        
        current = current.next