# Sistem Informasi Mahasiswa (SIM)

> Aplikasi console-based untuk mengelola data mahasiswa pada Program Studi Sistem Informasi.

---

## Identitas

| Field  | Keterangan           |
|--------|----------------------|
| Nama   | [Nama Lengkap Anda]  |
| NIM    | [NIM Anda]           |
| Kelas  | [Kelas Praktikum]    |

---

## Fitur

- ✅ **Tambah** data mahasiswa (NIM, nama, prodi, angkatan, IPK)
- ✅ **Tampilkan** seluruh data dalam tabel berwarna
- ✅ **Cari** mahasiswa berdasarkan NIM
- ✅ **Hapus** data mahasiswa dengan konfirmasi
- ✅ **Edit IPK** mahasiswa berdasarkan NIM
- ✅ **Validasi** data input (NIM minimal 6 karakter, IPK 0.0–4.0)

---

## Prasyarat

- Python 3.10+
- pip

---

## Instalasi

```bash
git clone https://github.com/USERNAME/sim-mahasiswa.git
cd sim-mahasiswa

# Buat dan aktifkan virtual environment
python -m venv venv

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Linux/macOS:
source venv/bin/activate

# Instal dependensi
pip install -r requirements.txt
```

---

## Penggunaan

```bash
# Aktifkan venv terlebih dahulu, lalu:
python -m src.main
```

---

## Pengujian

```bash
pytest tests/ -v
```

---

## Struktur Proyek

```
sim-mahasiswa/
├── src/
│   ├── __init__.py
│   ├── main.py        ← Program utama & menu interaktif
│   └── models.py      ← Model data Mahasiswa & DaftarMahasiswa
├── tests/
│   ├── __init__.py
│   └── test_main.py   ← 20 unit test (pytest)
├── docs/              ← Dokumentasi & screenshot
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup Checklist

- [x] Python 3.10+ terinstal (versi: _Python 3.14.5_)
- [x] Virtual environment dibuat & diaktivasi
- [x] Paket terinstal via `pip install -r requirements.txt`
- [x] Program berjalan tanpa error (`python -m src.main`)
- [x] Unit test lulus (`pytest tests/ -v`)
- [x] Repositori Git diinisiasi
- [x] Push ke GitHub berhasil
- [x] README.md lengkap

---

## Teknologi

| Alat      | Fungsi                          |
|-----------|---------------------------------|
| Python    | Bahasa pemrograman utama        |
| rich      | Output console yang terformat   |
| pytest    | Framework unit testing          |
| black     | Code formatter                  |
| ruff      | Linter cepat                    |
| git       | Version control                 |

---

*Mata Kuliah Pemrograman Python — Program Studi Sistem Informasi*
