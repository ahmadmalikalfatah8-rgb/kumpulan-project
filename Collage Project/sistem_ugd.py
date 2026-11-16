import time

# ====================================================================
# ENTITAS DATA
# ====================================================================

class Pasien:
    """Merepresentasikan satu pasien di sistem UGD."""

    LABEL_PRIORITAS = {
        1: "1 - KRITIS (mengancam nyawa)",
        2: "2 - GAWAT DARURAT",
        3: "3 - GAWAT TIDAK DARURAT",
        4: "4 - RINGAN",
        5: "5 - TIDAK GAWAT (rawat jalan)",
    }

    def __init__(self, no_rm, nama, keluhan, prioritas=None):
        self.no_rm = no_rm          # No. Rekam Medis -> kunci utama (unik, integer)
        self.nama = nama
        self.keluhan = keluhan
        self.prioritas = prioritas  # 1 (paling gawat) s.d. 5 (ringan), diisi saat triase

    def __str__(self):
        if self.prioritas is not None:
            label = self.LABEL_PRIORITAS.get(self.prioritas, str(self.prioritas))
            return f"[RM-{self.no_rm}] {self.nama} | Keluhan: {self.keluhan} | Prioritas: {label}"
        return f"[RM-{self.no_rm}] {self.nama} | Keluhan: {self.keluhan} | (belum ditriase)"


# ====================================================================
# 1. QUEUE  (Linked List, FIFO)
#    Digunakan untuk: antrian pendaftaran pasien sebelum ditriase.
# ====================================================================

class _NodeQueue:
    __slots__ = ("data", "next")

    def __init__(self, data):
        self.data = data
        self.next = None


class AntrianPendaftaran:
    """Queue (FIFO) berbasis singly linked list, diimplementasikan sendiri."""

    def __init__(self):
        self._front = None
        self._rear = None
        self._jumlah = 0

    def is_empty(self):
        return self._front is None

    def enqueue(self, pasien):
        """O(1) - menambahkan pasien baru ke akhir antrian."""
        node = _NodeQueue(pasien)
        if self.is_empty():
            self._front = node
            self._rear = node
        else:
            self._rear.next = node
            self._rear = node
        self._jumlah += 1

    def dequeue(self):
        """O(1) - mengambil & menghapus pasien paling depan antrian."""
        if self.is_empty():
            return None
        node = self._front
        self._front = self._front.next
        if self._front is None:
            self._rear = None
        self._jumlah -= 1
        return node.data

    def peek(self):
        """O(1) - melihat pasien paling depan tanpa menghapus."""
        return self._front.data if self._front else None

    def jumlah(self):
        return self._jumlah

    def display(self):
        print(f"\n--- ANTRIAN PENDAFTARAN (Queue) | Total: {self._jumlah} ---")
        if self.is_empty():
            print("  (kosong)")
            return
        print(f"  Depan antrian (peek): {self.peek()}")
        current = self._front
        i = 1
        while current:
            print(f"  {i}. {current.data}")
            current = current.next
            i += 1


# ====================================================================
# 2. STACK  (Linked List, LIFO)
#    Digunakan untuk: riwayat pemanggilan pasien & mekanisme undo.
# ====================================================================

class _NodeStack:
    __slots__ = ("data", "next")

    def __init__(self, data):
        self.data = data
        self.next = None


class RiwayatPemanggilan:
    """Stack (LIFO) berbasis singly linked list, diimplementasikan sendiri."""

    def __init__(self):
        self._top = None
        self._jumlah = 0

    def is_empty(self):
        return self._top is None

    def push(self, data):
        """O(1) - menyimpan satu transaksi (misal: hasil pemanggilan pasien)."""
        node = _NodeStack(data)
        node.next = self._top
        self._top = node
        self._jumlah += 1

    def pop(self):
        """O(1) - mengambil & menghapus transaksi paling terakhir (untuk undo)."""
        if self.is_empty():
            return None
        node = self._top
        self._top = self._top.next
        self._jumlah -= 1
        return node.data

    def peek(self):
        """O(1) - melihat transaksi teratas tanpa menghapus."""
        return self._top.data if self._top else None

    def jumlah(self):
        return self._jumlah

    def display(self):
        print(f"\n--- RIWAYAT PEMANGGILAN (Stack) | Total: {self._jumlah} ---")
        if self.is_empty():
            print("  (kosong)")
            return
        print(f"  Teratas / terakhir (peek): {self.peek()['pasien']} "
              f"(dipanggil {self.peek()['waktu']})")
        current = self._top
        i = 1
        while current:
            print(f"  {i}. {current.data['pasien']}  -- dipanggil pukul {current.data['waktu']}")
            current = current.next
            i += 1


# ====================================================================
# 3. BINARY SEARCH TREE (BST)
#    Digunakan untuk: basis data pasien aktif (sedang menunggu),
#    diindeks berdasarkan No. Rekam Medis (No. RM) agar pencarian,
#    penambahan, dan penghapusan efisien.
#
#    Traversal yang dipilih: INORDER.
#    Alasan: dengan kunci = No. RM (numerik), inorder traversal pada
#    BST menghasilkan daftar pasien terurut ASCENDING berdasarkan
#    No. RM secara alami -- cocok untuk kebutuhan rekap/administrasi
#    rekam medis yang rapi dan terurut, tanpa perlu proses sorting
#    tambahan di luar struktur data.
# ====================================================================

class _NodeBST:
    __slots__ = ("pasien", "left", "right")

    def __init__(self, pasien):
        self.pasien = pasien
        self.left = None
        self.right = None


class RekamMedisBST:
    """Binary Search Tree, diimplementasikan sendiri (node-based)."""

    def __init__(self):
        self.root = None
        self._jumlah_node = 0

    def is_empty(self):
        return self.root is None

    # ---------- INSERT ----------
    def insert(self, pasien):
        """Rata-rata O(log n), worst-case O(n) jika tidak seimbang."""
        self.root = self._insert(self.root, pasien)

    def _insert(self, node, pasien):
        if node is None:
            self._jumlah_node += 1
            return _NodeBST(pasien)
        if pasien.no_rm < node.pasien.no_rm:
            node.left = self._insert(node.left, pasien)
        elif pasien.no_rm > node.pasien.no_rm:
            node.right = self._insert(node.right, pasien)
        else:
            node.pasien = pasien  # No. RM sama -> update data
        return node

    # ---------- SEARCH ----------
    def search(self, no_rm):
        """Rata-rata O(log n) - mencari pasien berdasarkan No. RM."""
        return self._search(self.root, no_rm)

    def _search(self, node, no_rm):
        if node is None:
            return None
        if no_rm == node.pasien.no_rm:
            return node.pasien
        elif no_rm < node.pasien.no_rm:
            return self._search(node.left, no_rm)
        else:
            return self._search(node.right, no_rm)

    # ---------- DELETE ----------
    def delete(self, no_rm):
        """Rata-rata O(log n) - hapus pasien (3 kasus standar BST)."""
        self.root, dihapus = self._delete(self.root, no_rm)
        return dihapus

    def _delete(self, node, no_rm):
        if node is None:
            return node, False

        dihapus = False
        if no_rm < node.pasien.no_rm:
            node.left, dihapus = self._delete(node.left, no_rm)
        elif no_rm > node.pasien.no_rm:
            node.right, dihapus = self._delete(node.right, no_rm)
        else:
            dihapus = True
            # Kasus 1: tidak ada anak kiri
            if node.left is None:
                self._jumlah_node -= 1
                return node.right, dihapus
            # Kasus 2: tidak ada anak kanan
            if node.right is None:
                self._jumlah_node -= 1
                return node.left, dihapus
            # Kasus 3: punya dua anak -> cari successor (nilai terkecil di subtree kanan)
            successor = node.right
            while successor.left:
                successor = successor.left
            node.pasien = successor.pasien
            node.right, _ = self._delete(node.right, successor.pasien.no_rm)
        return node, dihapus

    # ---------- TRAVERSAL: INORDER ----------
    def inorder(self):
        """O(n) - menghasilkan daftar pasien terurut berdasarkan No. RM."""
        hasil = []
        self._inorder(self.root, hasil)
        return hasil

    def _inorder(self, node, hasil):
        if node:
            self._inorder(node.left, hasil)
            hasil.append(node.pasien)
            self._inorder(node.right, hasil)

    # ---------- HEIGHT ----------
    def height(self):
        """O(n). Konvensi: pohon kosong = -1, satu node = 0."""
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))

    # ---------- JUMLAH NODE ----------
    def jumlah_node(self):
        return self._jumlah_node

    def display_inorder(self):
        print(f"\n--- REKAM MEDIS PASIEN AKTIF (BST - Inorder by No. RM) ---")
        print(f"  Jumlah pasien aktif : {self.jumlah_node()}")
        print(f"  Tinggi pohon (BST)  : {self.height()}")
        if self.is_empty():
            print("  (tidak ada pasien aktif)")
            return
        for p in self.inorder():
            print(f"  - {p}")


# ====================================================================
# 4. BINARY HEAP (Min-Heap berbasis array)
#    Digunakan untuk: menentukan urutan pemanggilan pasien
#    berdasarkan level kegawatan (semakin kecil angka = semakin gawat
#    = semakin diprioritaskan / akar heap).
# ====================================================================

class HeapPrioritas:
    """Min-Heap berbasis array (list Python sebagai representasi
    complete binary tree), diimplementasikan sendiri tanpa heapq."""

    def __init__(self):
        self._data = []  # index 0 = akar; anak dari i -> 2i+1, 2i+2; parent -> (i-1)//2

    def is_empty(self):
        return len(self._data) == 0

    def jumlah(self):
        return len(self._data)

    # ---------- INSERT ----------
    def insert(self, pasien):
        """O(log n) - tambahkan pasien lalu heapify up."""
        self._data.append(pasien)
        self._heapify_up(len(self._data) - 1)

    def _heapify_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._data[i].prioritas < self._data[parent].prioritas:
                self._data[i], self._data[parent] = self._data[parent], self._data[i]
                i = parent
            else:
                break

    # ---------- PEEK ----------
    def peek(self):
        """O(1) - lihat pasien dengan prioritas tertinggi (akar heap)."""
        return self._data[0] if self._data else None

    # ---------- DELETE ROOT ----------
    def delete_root(self):
        """O(log n) - ambil & hapus pasien dengan prioritas tertinggi."""
        if self.is_empty():
            return None
        akar = self._data[0]
        terakhir = self._data.pop()
        if self._data:
            self._data[0] = terakhir
            self._heapify_down(0)
        return akar

    def _heapify_down(self, i):
        n = len(self._data)
        while True:
            kiri = 2 * i + 1
            kanan = 2 * i + 2
            terkecil = i
            if kiri < n and self._data[kiri].prioritas < self._data[terkecil].prioritas:
                terkecil = kiri
            if kanan < n and self._data[kanan].prioritas < self._data[terkecil].prioritas:
                terkecil = kanan
            if terkecil != i:
                self._data[i], self._data[terkecil] = self._data[terkecil], self._data[i]
                i = terkecil
            else:
                break

    # ---------- DELETE BY ID (untuk fitur "batalkan pasien") ----------
    def delete_by_id(self, no_rm):
        """O(n) - cari index pasien (linear search, karena heap tidak
        terindeks oleh No. RM), lalu hapus & perbaiki struktur heap."""
        idx = None
        for i, p in enumerate(self._data):
            if p.no_rm == no_rm:
                idx = i
                break
        if idx is None:
            return None

        pasien = self._data[idx]
        terakhir = self._data.pop()
        if idx < len(self._data):
            self._data[idx] = terakhir
            parent = (idx - 1) // 2
            if idx > 0 and self._data[idx].prioritas < self._data[parent].prioritas:
                self._heapify_up(idx)
            else:
                self._heapify_down(idx)
        return pasien

    def display(self):
        print(f"\n--- HEAP PRIORITAS PEMANGGILAN (Binary Heap) | Total: {self.jumlah()} ---")
        if self.is_empty():
            print("  (kosong)")
            return
        print(f"  Prioritas tertinggi saat ini (peek/akar): {self.peek()}")
        print("  Representasi array heap:")
        for i, p in enumerate(self._data):
            print(f"  idx {i}: {p}")


# ====================================================================
# PROGRAM UTAMA (CLI / Console)
# ====================================================================

def cetak_menu():
    print("\n" + "=" * 65)
    print(" SISTEM MANAJEMEN UNIT GAWAT DARURAT (UGD) ")
    print("=" * 65)
    print(" 1. Pasien baru datang (daftar -> masuk Queue)")
    print(" 2. Lakukan Triase (Queue -> BST + Heap)")
    print(" 3. Panggil Pasien Prioritas Tertinggi (Heap -> Stack, hapus di BST)")
    print(" 4. Undo Pemanggilan Terakhir (Stack -> kembali ke Heap & BST)")
    print(" 5. Cari Pasien di Rekam Medis (BST search by No. RM)")
    print(" 6. Batalkan Pasien yang Masih Menunggu (hapus dari BST & Heap)")
    print(" ---------------------------------------------------------")
    print(" 7. Tampilkan Antrian Pendaftaran (Queue)")
    print(" 8. Tampilkan Rekam Medis Pasien Aktif (BST - Inorder)")
    print(" 9. Tampilkan Heap Prioritas")
    print("10. Tampilkan Riwayat Pemanggilan (Stack)")
    print(" 0. Keluar")
    print("=" * 65)


def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Input harus berupa angka. Coba lagi.")


def main():
    queue = AntrianPendaftaran()
    bst = RekamMedisBST()
    heap = HeapPrioritas()
    stack = RiwayatPemanggilan()

    counter_rm = [1000]  # list agar bisa di-mutate di dalam fungsi lokal

    def rm_baru():
        counter_rm[0] += 1
        return counter_rm[0]

    while True:
        cetak_menu()
        pilihan = input("Pilih menu: ").strip()

        # ---------------- 1. PASIEN DATANG -> QUEUE ----------------
        if pilihan == "1":
            nama = input("  Nama pasien       : ").strip()
            keluhan = input("  Keluhan utama     : ").strip()
            pasien = Pasien(rm_baru(), nama, keluhan)
            queue.enqueue(pasien)
            print(f"  -> Pasien {pasien.nama} (RM-{pasien.no_rm}) masuk antrian pendaftaran.")

        # ---------------- 2. TRIASE: QUEUE -> BST + HEAP ----------------
        elif pilihan == "2":
            if queue.is_empty():
                print("  Antrian pendaftaran kosong, tidak ada pasien untuk ditriase.")
                continue
            pasien = queue.dequeue()
            print(f"  Mentriase: {pasien}")
            level = input_int("  Masukkan level kegawatan (1=Kritis ... 5=Ringan): ")
            while level not in range(1, 6):
                print("  Level harus 1-5.")
                level = input_int("  Masukkan level kegawatan (1=Kritis ... 5=Ringan): ")
            pasien.prioritas = level
            bst.insert(pasien)     # simpan ke rekam medis aktif
            heap.insert(pasien)    # masukkan ke antrian prioritas
            print(f"  -> {pasien.nama} (RM-{pasien.no_rm}) tercatat di BST & Heap "
                  f"dengan prioritas {level}.")

        # ---------------- 3. PANGGIL PASIEN: HEAP -> STACK, DELETE DI BST ----------------
        elif pilihan == "3":
            if heap.is_empty():
                print("  Tidak ada pasien dalam antrian prioritas (Heap kosong).")
                continue
            pasien = heap.delete_root()
            bst.delete(pasien.no_rm)  # pasien sudah dipanggil -> tidak aktif menunggu lagi
            waktu = time.strftime("%H:%M:%S")
            stack.push({"pasien": pasien, "waktu": waktu})
            print(f"  -> DIPANGGIL: {pasien} pada pukul {waktu}")
            print("     (otomatis dihapus dari Heap & BST, dicatat ke Stack)")

        # ---------------- 4. UNDO: STACK -> HEAP & BST ----------------
        elif pilihan == "4":
            if stack.is_empty():
                print("  Tidak ada riwayat pemanggilan untuk di-undo.")
                continue
            transaksi = stack.pop()
            pasien = transaksi["pasien"]
            heap.insert(pasien)
            bst.insert(pasien)
            print(f"  -> UNDO berhasil: {pasien} dikembalikan ke Heap & BST.")

        # ---------------- 5. SEARCH DI BST ----------------
        elif pilihan == "5":
            no_rm = input_int("  Masukkan No. RM yang dicari: ")
            hasil = bst.search(no_rm)
            if hasil:
                print(f"  Ditemukan: {hasil}")
            else:
                print("  Pasien dengan No. RM tersebut tidak ditemukan (atau sudah dipanggil).")

        # ---------------- 6. BATALKAN PASIEN: HAPUS DI BST & HEAP ----------------
        elif pilihan == "6":
            no_rm = input_int("  Masukkan No. RM pasien yang akan dibatalkan: ")
            pasien_bst = bst.search(no_rm)
            if pasien_bst is None:
                print("  Pasien tidak ditemukan di rekam medis aktif.")
                continue
            bst.delete(no_rm)
            heap.delete_by_id(no_rm)
            print(f"  -> Pasien {pasien_bst.nama} (RM-{no_rm}) dibatalkan & dihapus dari BST & Heap.")

        # ---------------- 7-10. DISPLAY ----------------
        elif pilihan == "7":
            queue.display()
        elif pilihan == "8":
            bst.display_inorder()
        elif pilihan == "9":
            heap.display()
        elif pilihan == "10":
            stack.display()

        elif pilihan == "0":
            print("  Keluar dari sistem. Sampai jumpa!")
            break
        else:
            print("  Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()
