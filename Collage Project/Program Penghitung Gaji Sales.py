# Super Class
class Sales:
    def __init__(self, nama, total_penjualan, target_penjualan, gaji_pokok):
        self.nama = nama
        self.total_penjualan = total_penjualan
        self.target_penjualan = target_penjualan
        self.gaji_pokok = gaji_pokok
        self.komisi_penjualan = 0.05
        self.bonus = 200000
        self.potongan_pajak = 0.05

    def hitung_total_gaji(self):
        if self.total_penjualan >= self.target_penjualan:
            total_gaji = self.gaji_pokok + self.hitung_komisi() + self.hitung_bonus()
        else:
            total_gaji = self.gaji_pokok + self.hitung_komisi() - self.hitung_potongan_pajak()
        return total_gaji

    def tampilkan_info(self):
        print(f"Nama: {self.nama}")
        print(f"Total Penjualan: {self.total_penjualan}")
        print(f"Target Penjualan: {self.target_penjualan}")
        print(f"Gaji Pokok: {self.gaji_pokok}")
        print(f"Komisi Penjualan: {self.hitung_komisi()}")
        print(f"Bonus: {self.hitung_bonus()}")
        print(f"Potongan Pajak: {self.hitung_potongan_pajak()}")
        print(f"Total Gaji: {self.hitung_total_gaji()}")

# Sub Class
class SalesJunior(Sales):
    def __init__(self, nama, total_penjualan, target_penjualan, gaji_pokok):
        super().__init__(nama, total_penjualan, target_penjualan, gaji_pokok)

    def hitung_komisi(self):
        komisi = self.komisi_penjualan * self.total_penjualan
        return komisi
    
    def hitung_bonus(self):
        if self.total_penjualan >= self.target_penjualan:
            bonus = self.bonus
        else:
            bonus = 0
        return bonus
    
    def hitung_potongan_pajak(self):
        if self.total_penjualan <= self.target_penjualan:
            potongan_pajak = self.potongan_pajak * (self.gaji_pokok + self.hitung_komisi())
        else:
            potongan_pajak = 0
        return potongan_pajak
    
    def hitung_total_gaji(self):
        return super().hitung_total_gaji()

    def tampilkan_info(self):
        super().tampilkan_info() 
    
class SalesSenior(Sales):
    def __init__(self, nama, total_penjualan, target_penjualan, gaji_pokok, komisi_tambahan):
        super().__init__(nama, total_penjualan, target_penjualan, gaji_pokok)
        self.komisi_tambahan = 0.02

    def hitung_komisi(self):
        komisi = (self.komisi_penjualan + self.komisi_tambahan) * self.total_penjualan
        return komisi
    
    def hitung_bonus(self):
        if self.total_penjualan >= self.target_penjualan:
            bonus = self.bonus
        else:
            bonus = 0
        return bonus
    
    def hitung_potongan_pajak(self):
        if self.total_penjualan <= self.target_penjualan:
            potongan_pajak = self.potongan_pajak * (self.gaji_pokok + self.hitung_komisi())
        else:
            potongan_pajak = 0
        return potongan_pajak
    
    def hitung_total_gaji(self):
        return super().hitung_total_gaji()
    
    def tampilkan_info(self):
        super().tampilkan_info()

class SalesManager(Sales):
    def __init__(self, nama, total_penjualan, target_penjualan, gaji_pokok, komisi_tambahan, bonus_tambahan):
        super().__init__(nama, total_penjualan, target_penjualan, gaji_pokok)
        self.komisi_tambahan = 0.03
        self.bonus_tambahan = 0.01 * self.hitung_komisi()

    def hitung_komisi(self):
        komisi = (self.komisi_penjualan + self.komisi_tambahan) * self.total_penjualan
        return komisi
    
    def hitung_bonus(self):
        if self.total_penjualan >= self.target_penjualan:
            bonus = self.bonus + self.bonus_tambahan
        else:
            bonus = 0
        return bonus
    
    def hitung_potongan_pajak(self):
        if self.total_penjualan <= self.target_penjualan:
            potongan_pajak = self.potongan_pajak * (self.gaji_pokok + self.hitung_komisi())
        else:
            potongan_pajak = 0
        return potongan_pajak
    
    def hitung_total_gaji(self):
        return super().hitung_total_gaji()

    def tampilkan_info(self):
        super().tampilkan_info()

# Contoh instansiasi
sales_junior = SalesJunior("Asepp", 1500000, 1000000, 3000000)
sales_senior = SalesSenior("Bagus", 1500000, 2000000, 5000000, 0.02)
sales_manager = SalesManager("Citra", 6000000, 4000000, 8000000, 0.03, 0.01)

sales_junior.tampilkan_info()
sales_senior.tampilkan_info()
sales_manager.tampilkan_info()