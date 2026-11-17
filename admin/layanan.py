from modules import database
from modules.utils import (
    bersihkan_layar, jeda, format_rupiah, buat_id, input_teks,
    input_angka, konfirmasi, pilih_menu, pilih_kunci, tampilkan_tabel
)


def tampilkan_layanan():
    baris = [
        (nomor, kode, data["nama"], format_rupiah(data["harga"]))
        for nomor, (kode, data) in enumerate(database.layanan.items(), 1)
    ]

    tampilkan_tabel(
        "DAFTAR LAYANAN",
        ("No", "ID", "Nama Layanan", "Harga"),
        baris,
        kiri=("Nama Layanan",),
        kanan=("Harga",)
    )


def tambah_layanan():
    nama = input_teks("Masukkan nama layanan: ")
    nama_terdaftar = {data["nama"].lower() for data in database.layanan.values()}

    if nama.lower() in nama_terdaftar:
        print("Nama layanan sudah terdaftar")
        return

    harga = input_angka("Masukkan harga layanan: ", 0)
    kode = buat_id("LY", database.layanan)

    database.layanan[kode] = {"nama": nama, "harga": harga}

    print("Layanan berhasil ditambahkan dengan ID", kode)


def edit_layanan():
    kode = pilih_kunci(database.layanan, "Masukkan nomor layanan yang ingin diedit: ")

    if kode is None:
        return

    data = database.layanan[kode]
    print("Kosongkan input jika tidak ingin mengubah data")

    nama = input_teks("Masukkan nama layanan baru: ", data["nama"])
    nama_lain = {
        isi["nama"].lower()
        for kode_lain, isi in database.layanan.items()
        if kode_lain != kode
    }

    if nama.lower() in nama_lain:
        print("Nama layanan sudah terdaftar")
        return

    data["nama"] = nama
    data["harga"] = input_angka("Masukkan harga layanan baru: ", 0, data["harga"])

    print("Layanan berhasil diedit")


def hapus_layanan():
    kode = pilih_kunci(database.layanan, "Masukkan nomor layanan yang ingin dihapus: ")

    if kode is None:
        return

    if any(isi["layanan_id"] == kode for isi in database.reservasi):
        print("Layanan tidak bisa dihapus karena sudah digunakan pada reservasi")
        return

    if konfirmasi("Yakin menghapus " + database.layanan[kode]["nama"]):
        del database.layanan[kode]
        print("Layanan berhasil dihapus")
    else:
        print("Penghapusan dibatalkan")


def menu_layanan():
    daftar_menu = [
        "Tambah Layanan",
        "Edit Layanan",
        "Hapus Layanan",
        "Kembali"
    ]

    while True:
        bersihkan_layar()
        tampilkan_layanan()

        pilihan = pilih_menu("KELOLA LAYANAN", daftar_menu)

        if pilihan == 4:
            return

        if pilihan == 1:
            tambah_layanan()
        elif pilihan == 2:
            edit_layanan()
        elif pilihan == 3:
            hapus_layanan()

        jeda()
