class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  # list of lists

    # Fungsi hash sederhana
    def hash_function(self, key):
        return hash(key) % self.size

    # Menambahkan data (insert)
    def insert(self, key, value):
        index = self.hash_function(key)
        
        # Cek apakah key sudah ada
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        
        # Jika belum ada, tambahkan
        self.table[index].append([key, value])

    # Mencari data (search)
    def search(self, key):
        index = self.hash_function(key)
        
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        
        return None

    # Menghapus data (delete)
    def delete(self, key):
        index = self.hash_function(key)
        
        for i, pair in enumerate(self.table[index]):
            if pair[0] == key:
                del self.table[index][i]
                return True
        
        return False

    # Menampilkan isi hash table
    def display(self):
        for i, bucket in enumerate(self.table):
            print(f"Index {i}: {bucket}")

ht = HashTable(5)

ht.insert("Alice", 85)
ht.insert("Bob", 90)
ht.insert("Charlie", 78)

print("Data Alice:", ht.search("Alice"))

ht.display()

ht.delete("Bob")
print("\nSetelah hapus Bob:")
ht.display()