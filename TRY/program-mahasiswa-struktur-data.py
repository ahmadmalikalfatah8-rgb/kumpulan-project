class Mahasiswa:
    
    def __init__(self, nama, nim, jurusan):
        self.nama = nama
        self.nim = nim
        self.jurusan = jurusan

    def tampilkan_info(self):
        print(f"Nama: {self.nama}")
        print(f"NIM: {self.nim}")
        print(f"Jurusan: {self.jurusan}")

class System:
    def __init__(self):
        self.mahasiswa_list = []

    def tambah_mahasiswa(self, mahasiswa):
        self.mahasiswa_list.append(mahasiswa)

    def tampilkan_semua_mahasiswa(self):
        for mahasiswa in self.mahasiswa_list:
            mahasiswa.tampilkan_info()
            print("--------------------")