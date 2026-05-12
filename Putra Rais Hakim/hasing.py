"""
Implementasi Hashing dengan Python
====================================
Fitur:
- Hash Table dengan Chaining (untuk collision handling)
- Hash Table dengan Open Addressing (Linear Probing)
- Custom hash function
- Operasi: insert, search, delete, display
"""


# ══════════════════════════════════════════════════
# 1. HASH TABLE - CHAINING (Separate Chaining)
# ══════════════════════════════════════════════════

class Node:
    """Node untuk Linked List dalam chaining."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTableChaining:
    """
    Hash Table menggunakan Separate Chaining untuk menangani collision.
    Setiap bucket adalah Linked List.
    """

    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def _hash(self, key):
        """Hash function: modulo division."""
        if isinstance(key, str):
            # Polynomial rolling hash untuk string
            h = 0
            for ch in key:
                h = (h * 31 + ord(ch)) % self.size
            return h
        return hash(key) % self.size

    def insert(self, key, value):
        """Masukkan key-value pair ke hash table."""
        index = self._hash(key)
        node = self.table[index]

        # Cek apakah key sudah ada (update value)
        while node:
            if node.key == key:
                node.value = value
                print(f"[UPDATE] key='{key}' diperbarui → value='{value}' (index {index})")
                return
            node = node.next

        # Tambah node baru di awal chain
        new_node = Node(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.count += 1
        print(f"[INSERT] key='{key}' → value='{value}' (index {index})")

    def search(self, key):
        """Cari nilai berdasarkan key. Return value atau None."""
        index = self._hash(key)
        node = self.table[index]

        while node:
            if node.key == key:
                print(f"[FOUND ] key='{key}' → value='{node.value}' (index {index})")
                return node.value
            node = node.next

        print(f"[NOT FOUND] key='{key}' tidak ada dalam tabel.")
        return None

    def delete(self, key):
        """Hapus entry berdasarkan key."""
        index = self._hash(key)
        node = self.table[index]
        prev = None

        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.table[index] = node.next
                self.count -= 1
                print(f"[DELETE] key='{key}' dihapus dari index {index}")
                return True
            prev = node
            node = node.next

        print(f"[DELETE] key='{key}' tidak ditemukan.")
        return False

    def display(self):
        """Tampilkan isi hash table."""
        print("\n" + "═" * 45)
        print("   HASH TABLE (Chaining)")
        print("═" * 45)
        for i, node in enumerate(self.table):
            chain = []
            curr = node
            while curr:
                chain.append(f"({curr.key}: {curr.value})")
                curr = curr.next
            status = " → ".join(chain) if chain else "[ kosong ]"
            print(f"  [{i:2d}] {status}")
        print(f"\n  Total entries: {self.count}")
        print("═" * 45 + "\n")

    @property
    def load_factor(self):
        return self.count / self.size


# ══════════════════════════════════════════════════
# 2. HASH TABLE - OPEN ADDRESSING (Linear Probing)
# ══════════════════════════════════════════════════

class HashTableLinearProbing:
    """
    Hash Table menggunakan Open Addressing dengan Linear Probing.
    Saat collision, cari slot kosong berikutnya secara linear.
    """

    DELETED = "__DELETED__"  # Sentinel untuk slot yang dihapus

    def __init__(self, size=10):
        self.size = size
        self.keys = [None] * self.size
        self.values = [None] * self.size
        self.count = 0

    def _hash(self, key):
        if isinstance(key, str):
            h = 0
            for ch in key:
                h = (h * 31 + ord(ch)) % self.size
            return h
        return hash(key) % self.size

    def _probe(self, index, i):
        """Linear probing: geser satu slot."""
        return (index + i) % self.size

    def insert(self, key, value):
        if self.load_factor >= 0.7:
            print("[WARNING] Load factor tinggi, pertimbangkan resize!")

        index = self._hash(key)
        for i in range(self.size):
            slot = self._probe(index, i)
            if self.keys[slot] is None or self.keys[slot] == self.DELETED:
                self.keys[slot] = key
                self.values[slot] = value
                self.count += 1
                print(f"[INSERT] key='{key}' → value='{value}' (slot {slot}, probe={i})")
                return
            elif self.keys[slot] == key:
                self.values[slot] = value
                print(f"[UPDATE] key='{key}' diperbarui → value='{value}' (slot {slot})")
                return

        print("[ERROR] Hash table penuh!")

    def search(self, key):
        index = self._hash(key)
        for i in range(self.size):
            slot = self._probe(index, i)
            if self.keys[slot] is None:
                break
            if self.keys[slot] == key:
                print(f"[FOUND ] key='{key}' → value='{self.values[slot]}' (slot {slot})")
                return self.values[slot]

        print(f"[NOT FOUND] key='{key}' tidak ditemukan.")
        return None

    def delete(self, key):
        index = self._hash(key)
        for i in range(self.size):
            slot = self._probe(index, i)
            if self.keys[slot] is None:
                break
            if self.keys[slot] == key:
                self.keys[slot] = self.DELETED
                self.values[slot] = None
                self.count -= 1
                print(f"[DELETE] key='{key}' dihapus dari slot {slot}")
                return True

        print(f"[DELETE] key='{key}' tidak ditemukan.")
        return False

    def display(self):
        print("\n" + "═" * 45)
        print("   HASH TABLE (Linear Probing)")
        print("═" * 45)
        for i in range(self.size):
            if self.keys[i] is None:
                print(f"  [{i:2d}] [ kosong ]")
            elif self.keys[i] == self.DELETED:
                print(f"  [{i:2d}] [ DELETED ]")
            else:
                print(f"  [{i:2d}] ({self.keys[i]}: {self.values[i]})")
        print(f"\n  Total entries : {self.count}")
        print(f"  Load factor   : {self.load_factor:.2f}")
        print("═" * 45 + "\n")

    @property
    def load_factor(self):
        return self.count / self.size


# ══════════════════════════════════════════════════
# 3. SIMPLE HASH FUNCTION DEMO
# ══════════════════════════════════════════════════

def demo_hash_functions():
    print("\n" + "═" * 45)
    print("   DEMO HASH FUNCTIONS")
    print("═" * 45)

    words = ["apple", "banana", "cherry", "date", "elderberry"]
    size = 10

    print(f"\n{'Kata':<15} {'ASCII Sum':>10} {'Hash (mod 10)':>15}")
    print("-" * 42)
    for word in words:
        ascii_sum = sum(ord(c) for c in word)
        h = ascii_sum % size
        print(f"{word:<15} {ascii_sum:>10} {h:>15}")
    print()


# ══════════════════════════════════════════════════
# MAIN - Demo
# ══════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 50)
    print("   IMPLEMENTASI HASHING - Python")
    print("=" * 50)

    # ── Demo Hash Functions ──
    demo_hash_functions()

    # ── Demo Chaining ──────────────────────────────
    print("\n>>> Hash Table dengan CHAINING <<<\n")
    ht_chain = HashTableChaining(size=7)

    data = [
        ("nama", "Budi"),
        ("usia", 21),
        ("kota", "Bandung"),
        ("jurusan", "Informatika"),
        ("nim", "123456789"),
        ("semester", 4),
        ("nama", "Siti"),   # collision key → update
    ]

    for k, v in data:
        ht_chain.insert(k, v)

    ht_chain.display()

    print("--- Operasi Search ---")
    ht_chain.search("kota")
    ht_chain.search("hobby")   # tidak ada

    print("\n--- Operasi Delete ---")
    ht_chain.delete("usia")
    ht_chain.delete("hobi")    # tidak ada

    ht_chain.display()

    # ── Demo Linear Probing ────────────────────────
    print("\n>>> Hash Table dengan LINEAR PROBING <<<\n")
    ht_lp = HashTableLinearProbing(size=10)

    mahasiswa = [
        ("Alice", 85),
        ("Bob", 92),
        ("Charlie", 78),
        ("Diana", 95),
        ("Eve", 88),
    ]

    for nama, nilai in mahasiswa:
        ht_lp.insert(nama, nilai)

    ht_lp.display()

    print("--- Operasi Search ---")
    ht_lp.search("Bob")
    ht_lp.search("Frank")

    print("\n--- Operasi Delete ---")
    ht_lp.delete("Charlie")

    print("\n--- Setelah Delete ---")
    ht_lp.display()

    print("\n--- Insert setelah Delete ---")
    ht_lp.insert("Grace", 91)
    ht_lp.display()

    print("\n✅ Semua operasi hashing selesai!")