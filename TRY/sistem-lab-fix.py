from datetime import date, datetime, timedelta

KONDISI_VALID = ("baik", "rusak ringan", "rusak berat")

class Mahasiswa:

    def __init__(self, nim, nama, no_hp):
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp
        self.status_mahasiswa = [] 

    def aktif_meminjam(self):
        return len(self.status_mahasiswa) > 0

    def __str__(self):
        status = "Aktif meminjam" if self.aktif_meminjam else "Tidak meminjam"
        return f"{self.nim} | {self.nama} | {self.no_hp} | {status}"

class Peralatan:

    def __init__(self, kode, nama, kategori, kondisi="baik"):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.kondisi = kondisi
        self.status_alat = "tersedia" if kondisi == "baik" else "tidak tersedia"

    def __str__(self):
        return (f"{self.kode} | {self.nama} | {self.kategori} | "
                f"kondisi: {self.kondisi} | status: {self.status_alat}")

class Transaksi:

    def __init__(self, id_transaksi, nim, tanggal):
        self.id = id_transaksi
        self.nim = nim
        self.tanggal = tanggal

class Peminjaman(Transaksi):

    def __init__(self, id_transaksi, nim, daftar_kode, tanggal_pinjam, batas_kembali):
            super().__init__(id_transaksi, nim, tanggal_pinjam)
            self.batas_kembali = batas_kembali
            self.items = {
                kode: {"dikembalikan": False, "kondisi": None,
                       "tanggal_kembali": None, "terlambat": False}
                for kode in daftar_kode
            }

    def tanggal_pinjam(self):
            return self.tanggal

    def status(self):
            jumlah_kembali = sum(1 for i in self.items.values() if i["dikembalikan"])
            if jumlah_kembali == 0:
                return "belum dikembalikan"
            if jumlah_kembali < len(self.items):
                return "dikembalikan sebagian"
            return "selesai"

    def detail(self):
        baris = [f"Transaksi Peminjaman {self.id} | NIM: {self.nim} | Status: {self.status.upper()}",
                f"  Pinjam: {self.tanggal} | Batas kembali: {self.batas_kembali}"]
        for kode, i in self.items.items():
            if i["dikembalikan"]:
                telat = " (TERLAMBAT)" if i["terlambat"] else ""
                baris.append(f"  - {kode}: dikembalikan {i['tanggal_kembali']}, "
                                 f"kondisi {i['kondisi']}{telat}")
            else:
                baris.append(f"  - {kode}: masih dipinjam")
        return "\n".join(baris)

    def __str__(self):
        return self.detail()

class Pengembalian(Transaksi):

    def __init__(self, id_kembali, id_peminjaman, nim, kode_alat, kondisi, tanggal_kembali, terlambat=False, denda=0):
        super().__init__(id_kembali, nim, tanggal_kembali)
        self.id_peminjaman = id_peminjaman
        self.kode_alat = kode_alat
        self.kondisi = kondisi
        self.terlambat = terlambat
        self.denda = denda
  
    def alat_belum_kembali(self):
        return [k for k, i in self.items.items() if not i["dikembalikan"]]
    
    def catat_pengembalian(self, kode, kondisi, tanggal):
        item = self.items[kode]
        item["dikembalikan"] = True
        item["kondisi"] = kondisi
        item["tanggal_kembali"] = tanggal
        item["terlambat"] = tanggal > self.batas_kembali    

    def tanggal_kembali(self):
        return self.tanggal

    def detail(self):
        telat_info = f" | Terlambat: Ya (Denda: Rp {self.denda:,})" if self.terlambat else " | Tepat Waktu"
        return (f"Transaksi Pengembalian {self.id} (Ref Pinjam: {self.id_peminjaman}) | "
                f"NIM: {self.nim} | Alat: {self.kode_alat} | "
                f"Kondisi: {self.kondisi}{telat_info} | Tanggal: {self.tanggal}")

    def __str__(self):
        return self.detail()

class ActivityLog:
    def __init__(self):
        self.entries = []

    def catat(self, pesan):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.entries.append({"waktu": waktu, "pesan": pesan})

    def tampilkan(self):
        if not self.entries:
            print("Belum ada aktivitas.")
            return
        for e in self.entries:
            print(f"[{e['waktu']}] {e['pesan']}")

class SistemMahasiswa:

    def __init__(self, log=None):
        self.data = {}
        self.log = log

    def tambah(self, nim, nama, no_hp):
        if not nim or not nama:
            raise ValueError("NIM dan nama tidak boleh kosong.")
        if nim in self.data:
            raise ValueError(f"NIM {nim} sudah terdaftar.")
        mhs = Mahasiswa(nim, nama, no_hp)
        self.data[nim] = mhs
        if self.log:
            self.log.catat(f"Mahasiswa {nim} ditambahkan")
        return mhs

    def edit(self, nim, nama=None, no_hp=None):
        mhs = self.get(nim)
        if nama:
            mhs.nama = nama
        if no_hp:
            mhs.no_hp = no_hp
        if self.log:
            self.log.catat(f"Mahasiswa {nim} diubah")
        return mhs

    def hapus(self, nim):
        mhs = self.get(nim)
        del self.data[nim]
        if self.log:
            self.log.catat(f"Mahasiswa {nim} dihapus")
        return mhs

    def cari(self, kata):
        kata = kata.lower()
        return [m for m in self.data.values()
                if kata in m.nim.lower() or kata in m.nama.lower()]

    def get(self, nim):
        if nim not in self.data:
            raise ValueError(f"Mahasiswa dengan NIM {nim} tidak ditemukan.")
        return self.data[nim]

class SistemAlat:

    def __init__(self, log=None):
        self.data = {}
        self.kategori = {"perangkat komputasi", "perangkat jaringan",
                         "perangkat multimedia"}
        self.log = log

    def tambah(self, kode, nama, kategori, kondisi="baik"):
        if not kode or not nama or not kategori:
            raise ValueError("Kode, nama, dan kategori tidak boleh kosong.")
        if kode in self.data:
            raise ValueError(f"Kode alat {kode} sudah ada.")
        if kondisi not in KONDISI_VALID:
            raise ValueError("Kondisi tidak valid.")
        kategori = kategori.lower()
        if kategori not in self.kategori:
            self.kategori.add(kategori)
            if self.log:
                self.log.catat(f"Kategori baru '{kategori}' ditambahkan")
        alat = Peralatan(kode, nama, kategori, kondisi)
        self.data[kode] = alat
        if self.log:
            self.log.catat(f"Alat {kode} ({nama}) ditambahkan")
        return alat

    def edit(self, kode, nama=None, kategori=None):
        alat = self.get(kode)
        if nama:
            alat.nama = nama
        if kategori:
            alat.kategori = kategori.lower()
            self.kategori.add(alat.kategori)
        if self.log:
            self.log.catat(f"Alat {kode} diubah")
        return alat

    def hapus(self, kode):
        alat = self.get(kode)
        del self.data[kode]
        if self.log:
            self.log.catat(f"Alat {kode} dihapus")
        return alat

    def cari(self, kata):
        kata = kata.lower()
        return [a for a in self.data.values()
                if kata in a.kode.lower() or kata in a.nama.lower()
                or kata in a.kategori.lower()]

    def get(self, kode):
        if kode not in self.data:
            raise ValueError(f"Alat dengan kode {kode} tidak ditemukan.")
        return self.data[kode]

class TransaksiManager:

    def __init__(self):
        self.transaksi = {}      
        self.pengembalian = []   
        self._no_transaksi = 0
        self._no_pengembalian = 0

    def buat_peminjaman(self, nim, daftar_kode, lama_hari=7):
        self._no_transaksi += 1
        id_trx = f"T{self._no_transaksi:03d}"
        hari_ini = date.today()
        trx = Peminjaman(id_trx, nim, daftar_kode, hari_ini,
                         hari_ini + timedelta(days=lama_hari))
        self.transaksi[id_trx] = trx
        return trx

    def catat_pengembalian(self, id_trx, kode, kondisi, tanggal=None):
        trx = self.get_transaksi(id_trx)
        if kondisi not in KONDISI_VALID:
            raise ValueError("Kondisi harus: baik / rusak ringan / rusak berat.")
        if kode not in trx.items:
            raise ValueError(f"Alat {kode} tidak ada di transaksi {id_trx}.")
        if trx.items[kode]["dikembalikan"]:
            raise ValueError(f"Alat {kode} sudah dikembalikan.")
        tanggal = tanggal or date.today()
        if tanggal < trx.tanggal_pinjam:
            raise ValueError("Tanggal pengembalian tidak boleh sebelum tanggal pinjam.")

        trx.catat_pengembalian(kode, kondisi, tanggal)

        self._no_pengembalian += 1
        id_kembali = f"R{self._no_pengembalian:03d}"
        terlambat = tanggal > trx.batas_kembali
        hari_terlambat = (tanggal - trx.batas_kembali).days if terlambat else 0
        denda = max(0, hari_terlambat * 5000)

        bukti_kembali = Pengembalian(
            id_kembali, id_trx, trx.nim, kode, kondisi, tanggal, terlambat, denda
        )
        self.pengembalian.append(bukti_kembali)
        return trx, bukti_kembali

    def is_alat_dipinjam(self, kode):
        for trx in self.transaksi.values():
            if trx.aktif and kode in trx.alat_belum_kembali():
                return True
        return False

    def get_transaksi(self, id_trx):
        if id_trx not in self.transaksi:
            raise ValueError(f"Transaksi {id_trx} tidak ditemukan.")
        return self.transaksi[id_trx]