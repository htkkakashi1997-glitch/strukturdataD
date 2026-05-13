class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key):
        # Rumus: h(k) = k mod m
        return hash(key) % self.size

    def insert(self, key, value):
        hash_key = self._hash_function(key)
        # Cek jika key sudah ada, update value-nya
        for item in self.table[hash_key]:
            if item[0] == key:
                item[1] = value
                return
        # Jika belum ada, tambahkan (Chaining)
        self.table[hash_key].append([key, value])

    def get(self, key):
        hash_key = self._hash_function(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                return item[1]
        return "Not Found"

    def display(self):
        for i, bucket in enumerate(self.table):
            print(f"Index {i}: {bucket}")

# Demo Penggunaan
ht = HashTable(10)
ht.insert("nama", "Jouvan")
ht.insert("npm", "2023001")
ht.insert("aman", "Dosen") # Potensi collision jika hash sama

print("--- Isi Hash Table ---")
ht.display()
print(f"\nCari Nama: {ht.get('nama')}")