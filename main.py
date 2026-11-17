from modules import database
from modules.utils import bersihkan_layar, pilih_menu, tampilkan_tabel
from admin.dashboard import menu_admin


def proses_login():
    sisa_kesempatan = database.BATAS_LOGIN

    while sisa_kesempatan > 0:
        print("\n========== LOGIN ==========")
        nama = input("Masukkan username: ").strip()
        password = input("Masukkan password: ").strip()

        sisa_kesempatan -= 1

        if nama in database.users and database.users[nama]["password"] == password:
            role = database.users[nama]["role"]
            tampilkan_tabel(
                "LOGIN BERHASIL",
                ("Keterangan", "Nilai"),
                (("Selamat datang", nama), ("Role anda", role)),
                kiri=("Keterangan", "Nilai")
            )
            input("\nTekan Enter untuk melanjutkan...")
            return nama, role

        print("Username atau password salah")
        if sisa_kesempatan > 0:
            print("Login tersisa:", sisa_kesempatan, "kali")

    return None


def main():
    daftar_menu = [
        "Login",
        "Keluar dari Program"
    ]

    while True:
        bersihkan_layar()
        pilihan = pilih_menu("SELAMAT DATANG DI SISTEM KLINIK", daftar_menu)

        if pilihan == 1:
            hasil_login = proses_login()

            if hasil_login is None:
                print("\nKesempatan login habis")
                input("Tekan Enter untuk kembali...")
                continue

            nama, role = hasil_login

            if role == "admin":
                status = menu_admin()
            else:
                print("Menu untuk role", role, "belum tersedia")
                input("Tekan Enter untuk kembali...")
                continue

            if status == "keluar":
                return

        elif pilihan == 2:
            bersihkan_layar()
            print("Program selesai. Terima kasih!")
            return


if __name__ == "__main__":
    main()
