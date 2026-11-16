from datetime import date, datetime, timedelta

KONDISI_BAIK = "baik"
KONDISI_RINGAN = "rusak ringan"
KONDISI_BERAT = "rusak berat"
KONDISI_VALID = (KONDISI_BAIK, KONDISI_RINGAN, KONDISI_BERAT)

class Mahasiswa:
    def __init__(self, nim, nama, no_hp):
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp
        self.status_mahasiswa = [] 

    @property
    def aktif_meminjam(self):
        return len(self.status_mahasiswa) > 0

    def __str__(self):
        status = "Aktif meminjam" if self.aktif_meminjam else "Tidak meminjam"
        return f"{self.nim} | {self.nama} | {self.no_hp} | {status}"


class Alat:
    def __init__(self, kode, nama, kategori, kondisi=KONDISI_BAIK):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.kondisi = kondisi
        self.status_alat = "tersedia" if kondisi == KONDISI_BAIK else "tidak tersedia"

    def __str__(self):
        return (f"{self.kode} | {self.nama} | {self.kategori} | "
                f"kondisi: {self.kondisi} | status: {self.status_alat}")


class Transaksi:
    """Superclass / Base class untuk seluruh transaksi laboratorium."""
    def __init__(self, id_transaksi, nim, tanggal):
        self.id = id_transaksi
        self.nim = nim
        self.tanggal = tanggal

    def __str__(self):
        return f"[{self.id}] NIM: {self.nim} | Tanggal: {self.tanggal}"


class Peminjaman(Transaksi):
    """Subclass Transaksi untuk peminjaman alat laboratorium."""
    def __init__(self, id_transaksi, nim, daftar_kode, tanggal_pinjam, batas_kembali):
        super().__init__(id_transaksi, nim, tanggal_pinjam)
        self.batas_kembali = batas_kembali
        self.items = {
            kode: {"dikembalikan": False, "kondisi": None,
                   "tanggal_kembali": None, "terlambat": False, "denda": 0}
            for kode in daftar_kode
        }

    @property
    def status(self):
        jumlah_kembali = sum(1 for i in self.items.values() if i["dikembalikan"])
        if jumlah_kembali == 0:
            return "dipinjam"
        if jumlah_kembali < len(self.items):
            return "sebagian dikembalikan"
        return "selesai"

    @property
    def aktif(self):
        return self.status != "selesai"

    def alat_belum_kembali(self):
        return [k for k, i in self.items.items() if not i["dikembalikan"]]

    def catat_pengembalian(self, kode, kondisi, tanggal, tarif_denda_telat=1000):
        item = self.items[kode]

        denda_telat = 0
        item["dikembalikan"] = True
        item["kondisi"] = kondisi
        item["tanggal_kembali"] = tanggal
        if tanggal > self.batas_kembali:
            item["terlambat"] = True
            hari_terlambat = (tanggal - self.batas_kembali).days
            denda_telat = hari_terlambat * tarif_denda_telat
        else:
            item["terlambat"] = False

        denda_kondisi = 0
        if kondisi == KONDISI_RINGAN:
            denda_kondisi = 25000
        elif kondisi == KONDISI_BERAT:
            denda_kondisi = 50000

        item["denda"] = denda_telat + denda_kondisi

    def __str__(self):
        baris = [f"Transaksi Peminjaman {self.id} | NIM: {self.nim} | Status: {self.status.upper()}",
                 f"  Pinjam: {self.tanggal} | Batas kembali: {self.batas_kembali}"]
        for kode, i in self.items.items():
            if i["dikembalikan"]:
                info_tambahan = []
                if i["terlambat"]:
                    info_tambahan.append("TERLAMBAT")
                if i["kondisi"] != KONDISI_BAIK:
                    info_tambahan.append(f"KONDISI {i['kondisi'].upper()}")

                if info_tambahan or i["denda"] > 0:
                    status_str = f" ({' & '.join(info_tambahan)} | TOTAL DENDA: Rp {i['denda']:,})"
                else:
                    status_str = " (Tepat Waktu & Kondisi Baik)"
                baris.append(
                    f"  - {kode}: dikembalikan {i['tanggal_kembali']}, "
                    f"kondisi {i['kondisi']}{status_str}")
            else:
                baris.append(f"  - {kode}: masih dipinjam")
        return "\n".join(baris)


class Pengembalian(Transaksi):
    """Subclass Transaksi untuk pencatatan berita acara pengembalian alat."""
    def __init__(self, id_kembali, id_peminjaman, nim, kode_alat, kondisi, tanggal_kembali, terlambat=False, denda=0):
        super().__init__(id_kembali, nim, tanggal_kembali)
        self.id_peminjaman = id_peminjaman
        self.kode_alat = kode_alat
        self.kondisi = kondisi
        self.terlambat = terlambat
        self.denda = denda

    def __str__(self):
        telat_info = f" | Terlambat: Ya (Denda: Rp {self.denda:,})" if self.terlambat else " | Tepat Waktu"
        return (f"Transaksi Pengembalian {self.id} (Ref Pinjam: {self.id_peminjaman}) | "
                f"NIM: {self.nim} | Alat: {self.kode_alat} | "
                f"Kondisi: {self.kondisi}{telat_info} | Tanggal: {self.tanggal}")

TransaksiPeminjaman = Peminjaman
TransaksiPengembalian = Pengembalian


# ======================================================================
# LOG AKTIVITAS (Tantangan D)
# ======================================================================

class ActivityLog:
    def __init__(self):
        self.entries = []  # list of {"waktu": str, "pesan": str}

    def catat(self, pesan):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.entries.append({"waktu": waktu, "pesan": pesan})

    def tampilkan(self):
        if not self.entries:
            print("Belum ada aktivitas.")
            return
        for e in self.entries:
            print(f"[{e['waktu']}] {e['pesan']}")


# ======================================================================
# SUB-MANAGERS (Domain-Specific Responsibilities)
# ======================================================================

class MahasiswaManager:
    """Mengelola penyimpanan dan operasi data mahasiswa."""
    def __init__(self, log=None):
        self.data = {}  # nim -> Mahasiswa
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


class AlatManager:
    """Mengelola inventaris peralatan dan kategori laboratorium."""
    def __init__(self, log=None):
        self.data = {}  # kode -> Alat
        self.kategori = {"perangkat komputasi", "perangkat jaringan",
                         "perangkat multimedia"}
        self.log = log

    def tambah(self, kode, nama, kategori, kondisi=KONDISI_BAIK):
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
        alat = Alat(kode, nama, kategori, kondisi)
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
        """Cari berdasarkan kode, sebagian nama, atau kategori."""
        kata = kata.lower()
        return [a for a in self.data.values()
                if kata in a.kode.lower() or kata in a.nama.lower()
                or kata in a.kategori.lower()]

    def get(self, kode):
        if kode not in self.data:
            raise ValueError(f"Alat dengan kode {kode} tidak ditemukan.")
        return self.data[kode]

    def alat_tersedia(self):
        return [a for a in self.data.values() if a.status_alat == "tersedia"]

    def alat_rusak(self):
        return [a for a in self.data.values() if a.kondisi != KONDISI_BAIK]


class TransaksiManager:
    """Mengelola riwayat transaksi peminjaman dan pengembalian."""
    def __init__(self):
        self.transaksi = {}      # id_trx -> Peminjaman
        self.pengembalian = []   # list of Pengembalian
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
        if tanggal < trx.tanggal:
            raise ValueError("Tanggal pengembalian tidak boleh sebelum tanggal pinjam.")

        # 1. Catat pengembalian item pada transaksi peminjaman (kalkulasi denda di dalam)
        trx.catat_pengembalian(kode, kondisi, tanggal)

        # 2. Buat objek transaksi pengembalian (Subclass Transaksi)
        self._no_pengembalian += 1
        id_kembali = f"R{self._no_pengembalian:03d}"
        item = trx.items[kode]
        terlambat = item["terlambat"]
        denda = item["denda"]

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

    def transaksi_mahasiswa(self, nim):
        return [t for t in self.transaksi.values() if t.nim == nim]

    def get_transaksi(self, id_trx):
        if id_trx not in self.transaksi:
            raise ValueError(f"Transaksi {id_trx} tidak ditemukan.")
        return self.transaksi[id_trx]


# ======================================================================
# LAB MANAGER (Koordinator Utama / Facade)
# ======================================================================

class LabManager:
    """Koordinator utama sistem laboratorium untuk aturan bisnis lintas domain."""
    MAKS_TRANSAKSI_AKTIF = 2   # Aturan 2
    MAKS_HARI_PINJAM = 7

    def __init__(self):
        self.log = ActivityLog()
        self.mhs_mgr = MahasiswaManager(self.log)
        self.alat_mgr = AlatManager(self.log)
        self.trx_mgr = TransaksiManager()

    def hapus_mahasiswa(self, nim):
        mhs = self.mhs_mgr.get(nim)
        if mhs.aktif_meminjam:
            raise ValueError("Mahasiswa masih memiliki transaksi aktif, tidak dapat dihapus.")
        return self.mhs_mgr.hapus(nim)

    def hapus_alat(self, kode):
        if self.trx_mgr.is_alat_dipinjam(kode):
            raise ValueError("Alat masih tercatat dalam transaksi aktif, tidak dapat dihapus.")
        return self.alat_mgr.hapus(kode)

    def buat_transaksi(self, nim, daftar_kode, lama_hari=7):
        mhs = self.mhs_mgr.get(nim)
        if len(mhs.status_mahasiswa) >= self.MAKS_TRANSAKSI_AKTIF:
            raise ValueError("Mahasiswa sudah memiliki 2 transaksi aktif.")
        if not 1 <= lama_hari <= self.MAKS_HARI_PINJAM:
            raise ValueError("Lama peminjaman harus 1-7 hari.")
        daftar_kode = list(dict.fromkeys(daftar_kode))
        if not daftar_kode:
            raise ValueError("Pilih minimal satu alat.")

        for kode in daftar_kode:
            alat = self.alat_mgr.get(kode)
            if alat.status_alat != "tersedia":
                raise ValueError(f"Alat {kode} ({alat.nama}) tidak tersedia (status: {alat.status_alat}).")

        trx = self.trx_mgr.buat_peminjaman(nim, daftar_kode, lama_hari)
        mhs.status_mahasiswa.append(trx.id)
        for kode in daftar_kode:
            self.alat_mgr.get(kode).status_alat = "tidak tersedia"
            self.log.catat(f"{self.alat_mgr.get(kode).nama} ({kode}) dipinjam dalam {trx.id}")
        self.log.catat(f"Transaksi {trx.id} dibuat untuk {nim}")
        return trx

    def kembalikan_alat(self, id_trx, kode, kondisi, tanggal=None):
        trx, bukti_kembali = self.trx_mgr.catat_pengembalian(id_trx, kode, kondisi, tanggal)
        alat = self.alat_mgr.get(kode)
        alat.kondisi = kondisi    # Aturan 5: hanya 'baik' yang jadi tersedia
        alat.status_alat = "tersedia" if kondisi == KONDISI_BAIK else "tidak tersedia"
        self.log.catat(f"{alat.nama} ({kode}) dikembalikan, kondisi {kondisi} [{bukti_kembali.id}]")

        if not trx.aktif:
            self.mhs_mgr.get(trx.nim).status_mahasiswa.remove(id_trx)
            self.log.catat(f"Transaksi {id_trx} selesai")
        return trx

    # Laporan lintas domain: peralatan yang saat ini sedang dipinjam
    def alat_dipinjam(self):
        return [a for a in self.alat_mgr.data.values() if self.trx_mgr.is_alat_dipinjam(a.kode)]


# ======================================================================
# MENU INTERAKTIF
# ======================================================================

def input_angka(prompt, default=None):
    teks = input(prompt).strip()
    if not teks and default is not None:
        return default
    if not teks.isdigit():
        raise ValueError("Input harus berupa angka.")
    return int(teks)


def tampil_daftar(daftar, kosong="Data tidak ditemukan."):
    if not daftar:
        print(kosong)
    for item in daftar:
        print(item)


def data_awal(lab):
    """Data contoh agar program mudah diuji (Skenario 1)."""
    lab.mhs_mgr.tambah("M001", "Andi", "0811111111")
    lab.mhs_mgr.tambah("M002", "Budi", "0822222222")
    lab.alat_mgr.tambah("A001", "Kamera Digital", "perangkat multimedia")
    lab.alat_mgr.tambah("A002", "Tripod", "perangkat multimedia")
    lab.alat_mgr.tambah("A003", "Kabel LAN", "perangkat jaringan")
    lab.alat_mgr.tambah("A004", "Laptop", "perangkat komputasi")
    lab.alat_mgr.tambah("A005", "Multimeter", "elektronika")


def menu_mahasiswa(lab):
    print("\n[Kelola Mahasiswa] 1.Tambah 2.Edit 3.Hapus 4.Cari 5.Tampilkan semua")
    p = input("Pilih: ").strip()
    if p == "1":
        lab.mhs_mgr.tambah(input("NIM: ").strip(), input("Nama: ").strip(),
                           input("No HP: ").strip())
    elif p == "2":
        lab.mhs_mgr.edit(input("NIM: ").strip(),
                         input("Nama baru (kosong=tetap): ").strip(),
                         input("No HP baru (kosong=tetap): ").strip())
    elif p == "3":
        lab.hapus_mahasiswa(input("NIM: ").strip())
    elif p == "4":
        tampil_daftar(lab.mhs_mgr.cari(input("Kata kunci (NIM/nama): ").strip()))
    elif p == "5":
        tampil_daftar(lab.mhs_mgr.data.values(), "Belum ada mahasiswa.")
    else:
        print("Pilihan tidak valid.")
        return
    if p in ("1", "2", "3"):
        print("Berhasil.")


def menu_alat(lab):
    print("\n[Kelola Alat] 1.Tambah 2.Edit 3.Hapus 4.Cari 5.Tampilkan semua")
    p = input("Pilih: ").strip()
    if p == "1":
        print("Kategori yang ada:", ", ".join(sorted(lab.alat_mgr.kategori)))
        print("(Ketik kategori baru jika belum ada.)")
        lab.alat_mgr.tambah(input("Kode: ").strip(), input("Nama: ").strip(),
                            input("Kategori: ").strip())
    elif p == "2":
        lab.alat_mgr.edit(input("Kode: ").strip(),
                          input("Nama baru (kosong=tetap): ").strip(),
                          input("Kategori baru (kosong=tetap): ").strip())
    elif p == "3":
        lab.hapus_alat(input("Kode: ").strip())
    elif p == "4":
        tampil_daftar(lab.alat_mgr.cari(input("Kode / sebagian nama / kategori: ").strip()))
    elif p == "5":
        tampil_daftar(lab.alat_mgr.data.values(), "Belum ada alat.")
    else:
        print("Pilihan tidak valid.")
        return
    if p in ("1", "2", "3"):
        print("Berhasil.")


def buat_transaksi(lab):
    nim = input("NIM peminjam: ").strip()
    print("Alat tersedia:")
    tampil_daftar(lab.alat_mgr.alat_tersedia(), "(tidak ada alat tersedia)")
    kode = input("Kode alat (pisahkan dengan koma): ").split(",")
    kode = [k.strip() for k in kode if k.strip()]
    lama = input_angka("Lama pinjam (1-7 hari, default 7): ", default=7)
    trx = lab.buat_transaksi(nim, kode, lama)
    print("Transaksi berhasil dibuat:")
    print(trx)


def proses_pengembalian(lab):
    id_trx = input("ID transaksi: ").strip().upper()
    trx = lab.trx_mgr.get_transaksi(id_trx)
    belum = trx.alat_belum_kembali()
    if not belum:
        print("Semua alat pada transaksi ini sudah dikembalikan.")
        return
    print("Alat belum kembali:", ", ".join(belum))
    kode = input("Kode alat yang dikembalikan (pisahkan koma): ").split(",")
    for k in [x.strip() for x in kode if x.strip()]:
        kondisi = input(f"Kondisi {k} (baik/rusak ringan/rusak berat): ").strip().lower()
        tgl_str = input("Tanggal kembali (YYYY-MM-DD, kosong=hari ini): ").strip()
        tgl = date.fromisoformat(tgl_str) if tgl_str else None
        try:
            lab.kembalikan_alat(id_trx, k, kondisi, tgl)
            print(f"{k} berhasil dikembalikan.")
        except ValueError as e:
            print(f"Gagal untuk {k}: {e}")
    print(lab.trx_mgr.transaksi[id_trx])


MENU = """
===== SISTEM PEMINJAMAN PERALATAN LAB =====
 1. Kelola data mahasiswa
 2. Kelola data alat
 3. Buat transaksi peminjaman
 4. Tampilkan transaksi
 5. Proses pengembalian alat
 6. Cari transaksi berdasarkan mahasiswa
 7. Tampilkan alat yang tersedia
 8. Tampilkan alat yang sedang dipinjam
 9. Tampilkan alat yang rusak
10. Tampilkan riwayat peminjaman mahasiswa
11. Log aktivitas
 0. Keluar
"""


def main():
    lab = LabManager()
    if input("Muat data contoh? (y/n): ").strip().lower() == "y":
        data_awal(lab)

    while True:
        print(MENU)
        pilihan = input("Pilih menu: ").strip()
        try:
            if pilihan == "1":
                menu_mahasiswa(lab)
            elif pilihan == "2":
                menu_alat(lab)
            elif pilihan == "3":
                buat_transaksi(lab)
            elif pilihan == "4":
                print("\n--- DAFTAR TRANSAKSI PEMINJAMAN ---")
                tampil_daftar(lab.trx_mgr.transaksi.values(), "Belum ada transaksi peminjaman.")
                if lab.trx_mgr.pengembalian:
                    print("\n--- BUKTI TRANSAKSI PENGEMBALIAN ---")
                    tampil_daftar(lab.trx_mgr.pengembalian)
            elif pilihan in ("6", "10"):
                nim = input("NIM mahasiswa: ").strip()
                tampil_daftar(lab.trx_mgr.transaksi_mahasiswa(nim), "Mahasiswa belum pernah meminjam.")
            elif pilihan == "5":
                proses_pengembalian(lab)
            elif pilihan == "7":
                tampil_daftar(lab.alat_mgr.alat_tersedia(), "Tidak ada alat tersedia.")
            elif pilihan == "8":
                tampil_daftar(lab.alat_dipinjam(), "Tidak ada alat yang sedang dipinjam.")
            elif pilihan == "9":
                tampil_daftar(lab.alat_mgr.alat_rusak(), "Tidak ada alat rusak.")
            elif pilihan == "11":
                lab.log.tampilkan()
            elif pilihan == "0":
                print("Terima kasih.")
                break
            else:
                print("Menu tidak valid.")
        except ValueError as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()