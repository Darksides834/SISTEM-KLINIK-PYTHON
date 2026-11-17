import matplotlib.pyplot as plt
import pandas as pd

from modules import database
from modules.utils import (
    bersihkan_layar, jeda, format_rupiah, pilih_menu, tampilkan_tabel
)
from admin.dokter import menu_dokter
from admin.jadwal import menu_jadwal
from admin.layanan import menu_layanan
from admin.inventaris import menu_inventaris


def tampilkan_ringkasan():
    total_pendapatan = sum(isi[2] for isi in database.transaksi)
    reservasi_aktif = sum(
        1 for isi in database.reservasi if isi["status"] in database.STATUS_AKTIF
    )
    obat_menipis = sum(
        1 for isi in database.obat.values() if isi["stok"] < database.BATAS_STOK_OBAT
    )
    alat_bermasalah = sum(
        isi["jumlah"] for isi in database.inventaris_alat.values() if isi["kondisi"] != "Baik"
    )

    baris = (
        ("Jumlah Dokter", len(database.dokter)),
        ("Jumlah Jadwal", len(database.jadwal)),
        ("Jumlah Layanan", len(database.layanan)),
        ("Jenis Alat", len(database.inventaris_alat)),
        ("Alat Perlu Perhatian", alat_bermasalah),
        ("Jenis Obat", len(database.obat)),
        ("Obat Stok Menipis", obat_menipis),
        ("Reservasi Aktif", reservasi_aktif),
        ("Total Pendapatan", format_rupiah(total_pendapatan))
    )

    tampilkan_tabel("DASHBOARD ADMIN", ("Keterangan", "Nilai"), baris, kiri=("Keterangan",))


def tampilkan_grafik():
    plt.tight_layout()

    try:
        plt.show()
    except Exception:
        print("Grafik tidak dapat ditampilkan pada lingkungan ini")
    finally:
        plt.close("all")


def grafik_reservasi_dokter():
    if len(database.reservasi) == 0 or len(database.dokter) == 0:
        print("Data reservasi atau dokter masih kosong")
        return

    df_reservasi = pd.DataFrame(database.reservasi)
    df_jadwal = pd.DataFrame(
        [(kode, isi["dokter_id"]) for kode, isi in database.jadwal.items()],
        columns=["jadwal_id", "dokter_id"]
    )
    nama_dokter = pd.Series({kode: isi["nama"] for kode, isi in database.dokter.items()})

    gabungan = df_reservasi.merge(df_jadwal, on="jadwal_id")
    jumlah = gabungan.groupby("dokter_id").size().reindex(nama_dokter.index, fill_value=0)
    jumlah.index = nama_dokter[jumlah.index].values

    fig, sumbu = plt.subplots(figsize=(9, 5))
    jumlah.plot(kind="bar", ax=sumbu, color="steelblue")
    sumbu.set_title("Jumlah Reservasi per Dokter")
    sumbu.set_xlabel("Dokter")
    sumbu.set_ylabel("Jumlah Reservasi")
    sumbu.tick_params(axis="x", rotation=20)

    for posisi, nilai in enumerate(jumlah):
        sumbu.text(posisi, nilai, str(nilai), ha="center", va="bottom")

    tampilkan_grafik()


def grafik_stok_obat():
    if len(database.obat) == 0:
        print("Data obat masih kosong")
        return

    df_obat = pd.DataFrame.from_dict(database.obat, orient="index").sort_values("stok")
    warna = [
        "indianred" if stok < database.BATAS_STOK_OBAT else "seagreen"
        for stok in df_obat["stok"]
    ]

    fig, sumbu = plt.subplots(figsize=(9, 5))
    sumbu.barh(df_obat["nama"], df_obat["stok"], color=warna)
    sumbu.axvline(database.BATAS_STOK_OBAT, color="gray", linestyle="--", label="Batas stok menipis")
    sumbu.set_title("Stok Obat")
    sumbu.set_xlabel("Jumlah Stok")
    sumbu.legend()

    tampilkan_grafik()


def grafik_pendapatan_layanan():
    if len(database.transaksi) == 0:
        print("Data transaksi masih kosong")
        return

    df_transaksi = pd.DataFrame(database.transaksi, columns=["transaksi_id", "id", "total"])
    df_reservasi = pd.DataFrame(database.reservasi)
    nama_layanan = pd.Series({kode: isi["nama"] for kode, isi in database.layanan.items()})

    gabungan = df_transaksi.merge(df_reservasi, on="id")
    pendapatan = gabungan.groupby("layanan_id")["total"].sum()
    pendapatan.index = nama_layanan.reindex(pendapatan.index).fillna("Layanan Dihapus").values

    fig, sumbu = plt.subplots(figsize=(9, 5))
    pendapatan.plot(kind="bar", ax=sumbu, color="darkorange")
    sumbu.set_title("Pendapatan per Layanan")
    sumbu.set_xlabel("Layanan")
    sumbu.set_ylabel("Pendapatan (Rp)")
    sumbu.tick_params(axis="x", rotation=20)

    tampilkan_grafik()


def grafik_kondisi_alat():
    if len(database.inventaris_alat) == 0:
        print("Data alat masih kosong")
        return

    df_alat = pd.DataFrame.from_dict(database.inventaris_alat, orient="index")
    jumlah = df_alat.groupby("kondisi")["jumlah"].sum()
    jumlah = jumlah[jumlah > 0]

    if jumlah.empty:
        print("Jumlah alat masih kosong")
        return

    fig, sumbu = plt.subplots(figsize=(6, 6))
    sumbu.pie(jumlah, labels=jumlah.index, autopct="%1.1f%%", startangle=90)
    sumbu.set_title("Kondisi Alat Klinik")

    tampilkan_grafik()


def menu_visualisasi():
    daftar_menu = [
        "Reservasi per Dokter",
        "Stok Obat",
        "Pendapatan per Layanan",
        "Kondisi Alat",
        "Kembali"
    ]

    while True:
        bersihkan_layar()
        tampilkan_ringkasan()

        pilihan = pilih_menu("VISUALISASI DATA", daftar_menu)

        if pilihan == 5:
            return

        if pilihan == 1:
            grafik_reservasi_dokter()
        elif pilihan == 2:
            grafik_stok_obat()
        elif pilihan == 3:
            grafik_pendapatan_layanan()
        elif pilihan == 4:
            grafik_kondisi_alat()

        jeda()


def menu_admin():
    daftar_menu = [
        "Kelola Dokter",
        "Kelola Jadwal Dokter",
        "Kelola Layanan",
        "Kelola Inventaris",
        "Visualisasi Data",
        "Logout",
        "Keluar dari Program"
    ]

    while True:
        bersihkan_layar()
        tampilkan_ringkasan()

        pilihan = pilih_menu("MENU ADMIN", daftar_menu)

        if pilihan == 1:
            menu_dokter()
        elif pilihan == 2:
            menu_jadwal()
        elif pilihan == 3:
            menu_layanan()
        elif pilihan == 4:
            menu_inventaris()
        elif pilihan == 5:
            menu_visualisasi()
        elif pilihan == 6:
            bersihkan_layar()
            print("Logout berhasil")
            return "logout"
        elif pilihan == 7:
            bersihkan_layar()
            print("Program selesai. Terima kasih!")
            return "keluar"
