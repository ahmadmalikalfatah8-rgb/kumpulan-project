# Super Class
class Sales:
    def __init__(self, nama, total_penjualan, target_penjualan, gaji_pokok, komisi_tambahan, bonus_tambahan):
        self.nama = nama
        self.total_penjualan = total_penjualan
        self.target_penjualan = target_penjualan
        self.gaji_pokok = gaji_pokok
        self.komisi_dasar = 0.05
        self.komisi_tambahan = komisi_tambahan
        self.bonus = bonus_tambahan
        self.bonus_tambahan = bonus_tambahan
        self.potongan_pajak = 0.05

    def hitung_gaji(self):
        if self.total_penjualan >= self.target_penjualan:
            total = self.gaji_pokok + (self.total_penjualan * (self.komisi_dasar + self.komisi_tambahan)) + self.bonus
        else:
            total = self.gaji_pokok + (self.total_penjualan * (self.komisi_dasar + self.komisi_tambahan)) - (self.potongan_pajak * (self.gaji_pokok + (self.total_penjualan * (self.komisi_dasar + self.komisi_tambahan))))
        return total

    def tampilkan_info(self):
        print(f"Nama: {self.nama}")
        print(f"Total Penjualan: {self.total_penjualan}")
        print(f"Target Penjualan: {self.target_penjualan}")
        print(f"Gaji Pokok: {self.gaji_pokok}")
        print(f"Komisi Penjualan: {self.komisi_dasar + self.komisi_tambahan}")
        print(f"Bonus: {self.bonus + self.bonus_tambahan}")
        print(f"Potongan Pajak: {self.potongan_pajak}")
        print(f"Total Gaji: {self.hitung_gaji()}")

# Sub Class
class SalesJunior(Sales):
    def __init__(self, nama, total_penjualan, target_penjualan, gaji_pokok, komisi_tambahan, bonus_tambahan):
        super().__init__(nama, total_penjualan, target_penjualan, gaji_pokok, komisi_tambahan, bonus_tambahan)

    def hitung_total_gaji(self):
        return super().hitung_total_gaji()

    def tampilkan_info(self):
        super().tampilkan_info() 
    
class SalesSenior(Sales):
    def __init__(self, nama, total_penjualan, target_penjualan, gaji_pokok, komisi_tambahan, bonus_tambahan):
        super().__init__(nama, total_penjualan, target_penjualan, gaji_pokok, komisi_tambahan, bonus_tambahan)
    
    def hitung_total_gaji(self):
        return super().hitung_total_gaji()
    
    def tampilkan_info(self):
        super().tampilkan_info()

class SalesManager(Sales):
    def __init__(self, nama, total_penjualan, target_penjualan, gaji_pokok, komisi_tambahan, bonus_tambahan):
        super().__init__(nama, total_penjualan, target_penjualan, gaji_pokok, komisi_tambahan, bonus_tambahan)
    
    def hitung_total_gaji(self):
        return super().hitung_total_gaji()

    def tampilkan_info(self):
        super().tampilkan_info()

# Contoh instansiasi
sales_junior = SalesJunior("Asepp", 1500000, 1000000, 3000000, 0, 0)
sales_senior = SalesSenior("Bagus", 1500000, 2000000, 5000000, 0.02, 0)
sales_manager = SalesManager("Citra", 6000000, 4000000, 8000000, 0.03, 0.01)

sales_junior.tampilkan_info()
sales_senior.tampilkan_info()
sales_manager.tampilkan_info()