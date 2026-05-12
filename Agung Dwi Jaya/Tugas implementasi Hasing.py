import streamlit as st

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append((key, value))

    def search(self, key):
        index = self.hash_function(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None

    def display(self):
        return self.table
    
st.title("Visualisasi Hashing dengan Hash Table")

size = st.number_input("Masukkan ukuran hash table:", min_value=5, value=10)

ht = HashTable(size)

st.subheader("Masukkan data ke Hash Table")
key = st.number_input("Key (integer):", value=15)
value = st.text_input("Value:", "Data A")
if st.button("Insert"):
    ht.insert(key, value)
    st.success(f"Data ({key}, {value}) berhasil dimasukkan ke hash table.")
    
st.subheader("Cari data berdasarkan key")
search_key = st.number_input("Key yang dicari:", value=25)
if st.button("Search"):
    result = ht.search(search_key)
    if result:
        st.success(f"Data ditemukan: {result}")
    else:
        st.error("Data tidak ditemukan.")
        
st.subheader("Isi Hash Table")
table_data = ht.display()
for i, bucket in enumerate(table_data):
    st.write(f"Index {i}: {bucket}")