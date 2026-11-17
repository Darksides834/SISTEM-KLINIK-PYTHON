from modules import database
from modules.utils import (
    bersihkan_layar, jeda, buat_id, input_angka, konfirmasi,
    pilih_menu, pilih_kunci, tampilkan_tabel
)
from admin.dokter import tampilkan_dokter


def format_jam(jam):
    return jam[0] + " - " + jam[1]


def hitung_terisi(kode_jadwal):
    return sum(
        1 for isi in database.reservasi
        if isi["jadwal_id"] == kode_jadwal and isi["status"] in database.STATUS_AKTIF
    )


def cek_bentrok(kode_dokter, hari, jam, abaikan=None):
    return any(
        kode != abaikan
        and isi["dokter_id"] == kode_dokter
        and isi["hari"] == hari
        and isi["jam"] == jam
        for kode, isi in database.jadwal.items()
    )


def pilih_hari():
    daftar_hari = list(database.DAFTAR_HARI)
    return daftar_hari[pilih_menu("Pilih hari praktik", daftar_hari) - 1]


def pilih_jam():
    daftar_jam = [format_jam(jam) for jam in database.JAM_PRAKTIK]
    return database.JAM_PRAKTIK[pilih_menu("Pilih jam praktik", daftar_jam) - 1]


def tampilkan_jadwal():
    baris = [
        (
            nomor,
            kode,
            database.dokter[data["dokter_id"]]["nama"],
            data["hari"],
            format_jam(data["jam"]),
            data["kuota"],
            hitung_terisi(kode)
        )
        for nomor, (kode, data) in enumerate(database.jadwal.items(), 1)
    ]

    tampilkan_tabel(
        "JADWAL DOKTER",
        ("No", "ID", "Dokter", "Hari", "Jam", "Kuota", "Terisi"),
        baris,
        kiri=("Dokter",)
    )


def tambah_jadwal():
    if len(database.dokter) == 0:
        print("Data dokter masih kosong, tambahkan dokter terlebih dahulu")
        return

    tampilkan_dokter()
    kode_dokter = pilih_kunci(database.dokter, "Pilih nomor dokter: ")

    if kode_dokter is None:
        return

    hari = pilih_hari()
    jam = pilih_jam()

    if cek_bentrok(kode_dokter, hari, jam):
        print("Jadwal dokter pada hari dan jam tersebut sudah ada")
        return

    kuota = input_angka("Masukkan kuota pasien: ", 1)
    kode = buat_id("JD", database.jadwal)

    database.jadwal[kode] = {
        "dokter_id": kode_dokter,
        "hari": hari,
        "jam": jam,
        "kuota": kuota
    }

    print("Jadwal berhasil ditambahkan dengan ID", kode)


def edit_jadwal():
    kode = pilih_kunci(database.jadwal, "Masukkan nomor jadwal yang ingin diedit: ")

    if kode is None:
        return

    data = database.jadwal[kode]
    print("Dokter pada jadwal:", database.dokter[data["dokter_id"]]["nama"])

    hari = pilih_hari()
    jam = pilih_jam()

    if cek_bentrok(data["dokter_id"], hari, jam, kode):
        print("Jadwal dokter pada hari dan jam tersebut sudah ada")
        return

    terisi = hitung_terisi(kode)
    kuota = input_angka("Masukkan kuota baru: ", 1, data["kuota"])

    if kuota < terisi:
        print("Kuota tidak boleh kurang dari jumlah reservasi aktif:", terisi)
        return

    data["hari"] = hari
    data["jam"] = jam
    data["kuota"] = kuota

    print("Jadwal berhasil diedit")


def hapus_jadwal():
    kode = pilih_kunci(database.jadwal, "Masukkan nomor jadwal yang ingin dihapus: ")

    if kode is None:
        return

    if any(isi["jadwal_id"] == kode for isi in database.reservasi):
        print("Jadwal tidak bisa dihapus karena sudah terhubung dengan reservasi")
        return

    if konfirmasi("Yakin menghapus jadwal " + kode):
        del database.jadwal[kode]
        print("Jadwal berhasil dihapus")
    else:
        print("Penghapusan dibatalkan")


def menu_jadwal():
    daftar_menu = [
        "Tambah Jadwal",
        "Edit Jadwal",
        "Hapus Jadwal",
        "Kembali"
    ]

    while True:
        bersihkan_layar()
        tampilkan_jadwal()

        pilihan = pilih_menu("KELOLA JADWAL DOKTER", daftar_menu)

        if pilihan == 4:
            return

        if pilihan == 1:
            tambah_jadwal()
        elif pilihan == 2:
            edit_jadwal()
        elif pilihan == 3:
            hapus_jadwal()

        jeda()
