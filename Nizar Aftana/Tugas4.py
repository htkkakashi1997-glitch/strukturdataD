import streamlit as st

st.title("Visualisasi Circular Queue")

# Inisialisasi session state
if "queue" not in st.session_state:
    st.session_state.queue = []
    st.session_state.max_size = 5

# Input ukuran queue
max_size = st.number_input("Ukuran Queue", min_value=3, max_value=10, value=5)
st.session_state.max_size = max_size

# Input elemen
value = st.text_input("Masukkan nilai")

col1, col2 = st.columns(2)

# ENQUEUE
with col1:
    if st.button("Enqueue"):
        if len(st.session_state.queue) < st.session_state.max_size:
            st.session_state.queue.append(value)
        else:
            st.warning("Queue penuh!")

# DEQUEUE
with col2:
    if st.button("Dequeue"):
        if len(st.session_state.queue) > 0:
            st.session_state.queue.pop(0)
        else:
            st.warning("Queue kosong!")

# Tampilkan queue
st.subheader("Isi Circular Queue")

queue = st.session_state.queue

# Visualisasi kotak
cols = st.columns(st.session_state.max_size)

for i in range(st.session_state.max_size):
    if i < len(queue):
        cols[i].success(queue[i])
    else:
        cols[i].empty()

# Info front & rear
if queue:
    st.write(f"Front: {queue[0]}")
    st.write(f"Rear: {queue[-1]}")
else:
    st.write("Queue kosong")