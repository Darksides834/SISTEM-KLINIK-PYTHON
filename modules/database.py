DAFTAR_HARI = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu")
HARI_VALID = set(DAFTAR_HARI)

JAM_PRAKTIK = (
    ("08:00", "12:00"),
    ("13:00", "17:00"),
    ("18:00", "21:00")
)

KONDISI_ALAT = ("Baik", "Perawatan", "Rusak")
STATUS_AKTIF = {"Menunggu", "Dikonfirmasi"}
BATAS_STOK_OBAT = 20

dokter = {
    "DR01": {"nama": "dr. Andi Wijaya", "spesialis": "Umum", "biaya": 100000},
    "DR02": {"nama": "dr. Siti Rahma", "spesialis": "Anak", "biaya": 150000},
    "DR03": {"nama": "dr. Budi Santoso", "spesialis": "Gigi", "biaya": 175000},
    "DR04": {"nama": "dr. Maya Putri", "spesialis": "Kulit", "biaya": 200000}
}

layanan = {
    "LY01": {"nama": "Konsultasi Umum", "harga": 50000},
    "LY02": {"nama": "Pemeriksaan Gigi", "harga": 120000},
    "LY03": {"nama": "Imunisasi Anak", "harga": 90000},
    "LY04": {"nama": "Perawatan Kulit", "harga": 250000}
}

jadwal = {
    "JD01": {"dokter_id": "DR01", "hari": "Senin", "jam": ("08:00", "12:00"), "kuota": 10},
    "JD02": {"dokter_id": "DR02", "hari": "Selasa", "jam": ("13:00", "17:00"), "kuota": 8},
    "JD03": {"dokter_id": "DR03", "hari": "Rabu", "jam": ("08:00", "12:00"), "kuota": 6},
    "JD04": {"dokter_id": "DR04", "hari": "Kamis", "jam": ("18:00", "21:00"), "kuota": 5},
    "JD05": {"dokter_id": "DR01", "hari": "Jumat", "jam": ("13:00", "17:00"), "kuota": 10}
}

reservasi = [
    {"id": "RS01", "pasien": "Rina Lestari", "jadwal_id": "JD01", "layanan_id": "LY01", "status": "Selesai"},
    {"id": "RS02", "pasien": "Joko Prasetyo", "jadwal_id": "JD01", "layanan_id": "LY01", "status": "Selesai"},
    {"id": "RS03", "pasien": "Dewi Anggraini", "jadwal_id": "JD02", "layanan_id": "LY03", "status": "Selesai"},
    {"id": "RS04", "pasien": "Fajar Nugroho", "jadwal_id": "JD03", "layanan_id": "LY02", "status": "Selesai"},
    {"id": "RS05", "pasien": "Lilis Suryani", "jadwal_id": "JD04", "layanan_id": "LY04", "status": "Dikonfirmasi"},
    {"id": "RS06", "pasien": "Hendra Gunawan", "jadwal_id": "JD05", "layanan_id": "LY01", "status": "Menunggu"},
    {"id": "RS07", "pasien": "Putri Ayu", "jadwal_id": "JD02", "layanan_id": "LY03", "status": "Dikonfirmasi"},
    {"id": "RS08", "pasien": "Agus Salim", "jadwal_id": "JD03", "layanan_id": "LY02", "status": "Dibatalkan"}
]

transaksi = [
    ("TR01", "RS01", 50000),
    ("TR02", "RS02", 50000),
    ("TR03", "RS03", 90000),
    ("TR04", "RS04", 120000)
]

inventaris_alat = {
    "AL01": {"nama": "Stetoskop", "jumlah": 8, "kondisi": "Baik"},
    "AL02": {"nama": "Tensimeter Digital", "jumlah": 5, "kondisi": "Baik"},
    "AL03": {"nama": "Kursi Dental", "jumlah": 2, "kondisi": "Perawatan"},
    "AL04": {"nama": "Termometer Infrared", "jumlah": 6, "kondisi": "Baik"},
    "AL05": {"nama": "Autoclave", "jumlah": 1, "kondisi": "Rusak"}
}

obat = {
    "OB01": {"nama": "Paracetamol 500mg", "stok": 120, "harga": 5000},
    "OB02": {"nama": "Amoxicillin 500mg", "stok": 15, "harga": 12000},
    "OB03": {"nama": "Ibuprofen 400mg", "stok": 60, "harga": 8000},
    "OB04": {"nama": "Cetirizine 10mg", "stok": 10, "harga": 7000},
    "OB05": {"nama": "Vitamin C 500mg", "stok": 90, "harga": 4000}
}

users = {
    "admin": {"password": "admin123", "role": "admin"}
}

BATAS_LOGIN = 3
