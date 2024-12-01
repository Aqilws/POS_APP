from abc import ABC, abstractmethod

# Base Class untuk Item Menu
class MenuItem:
    def __init__(self, id, nama, deskripsi, harga, foto):
        self.__id = id
        self.__nama = nama
        self.__deskripsi = deskripsi
        self.__harga = harga
        self.__foto = foto

    # Getter
    def get_id(self):
        return self.__id

    def get_nama(self):
        return self.__nama

    def get_deskripsi(self):
        return self.__deskripsi

    def get_harga(self):
        return self.__harga

    def get_foto(self):
        return self.__foto

    # Setter
    def set_harga(self, harga):
        self.__harga = harga


# Subclass untuk Makanan
class Makanan(MenuItem):
    def __init__(self, id, nama, deskripsi, harga, foto, kategori="Makanan"):
        super().__init__(id, nama, deskripsi, harga, foto)
        self.kategori = kategori


# Subclass untuk Minuman
class Minuman(MenuItem):
    def __init__(self, id, nama, deskripsi, harga, foto, dingin):
        super().__init__(id, nama, deskripsi, harga, foto)
        self.dingin = dingin


# Abstract Class untuk Kasir
class Kasir(ABC):
    @abstractmethod
    def hitung_total(self):
        pass


# Implementasi Kasir
class Transaksi(Kasir):
    def __init__(self):
        self.__pesanan = []

    def tambah_pesanan(self, item):
        self.__pesanan.append(item)

    def hitung_total(self):
        return sum(item.get_harga() for item in self.__pesanan)

    def tampilkan_pesanan(self):
        for item in self.__pesanan:
            print(f"{item.get_nama()} - Rp{item.get_harga()}")
