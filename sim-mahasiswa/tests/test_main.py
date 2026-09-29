"""
test_main.py - Unit Test untuk Sistem Informasi Mahasiswa
Menggunakan pytest framework.
Mata Kuliah Pemrograman Python
"""

import pytest
import sys
import os

# Tambah path src ke sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models import Mahasiswa, DaftarMahasiswa


# ============================================================
# TEST CLASS: TestMahasiswa
# ============================================================

class TestMahasiswa:
    """Unit test untuk model Mahasiswa."""

    def test_buat_mahasiswa_valid(self):
        """C1: Mahasiswa dengan data lengkap dan valid harus terbuat."""
        mhs = Mahasiswa("2024SI001", "Andi Pratama", "Sistem Informasi", 2024, 3.50)
        assert mhs.nim == "2024SI001"
        assert mhs.nama == "Andi Pratama"
        assert mhs.program_studi == "Sistem Informasi"
        assert mhs.angkatan == 2024
        assert mhs.ipk == 3.50

    def test_ipk_default_nol(self):
        """C2: IPK default harus 0.0 jika tidak diisi."""
        mhs = Mahasiswa("2024SI002", "Budi", "Sistem Informasi", 2024)
        assert mhs.ipk == 0.0

    def test_nim_terlalu_pendek(self):
        """C3: NIM dengan kurang dari 6 karakter harus raise ValueError."""
        with pytest.raises(ValueError, match="NIM tidak valid"):
            Mahasiswa("abc", "Test", "SI", 2024, 3.0)

    def test_nim_kosong(self):
        """C4: NIM kosong harus raise ValueError."""
        with pytest.raises(ValueError):
            Mahasiswa("", "Test", "SI", 2024, 3.0)

    def test_nama_kosong(self):
        """C5: Nama kosong harus raise ValueError."""
        with pytest.raises(ValueError, match="Nama tidak boleh kosong"):
            Mahasiswa("2024SI003", "", "SI", 2024, 3.0)

    def test_ipk_di_atas_4(self):
        """C6: IPK lebih dari 4.0 harus raise ValueError."""
        with pytest.raises(ValueError, match="IPK harus antara 0.0-4.0"):
            Mahasiswa("2024SI004", "Test", "SI", 2024, 5.0)

    def test_ipk_negatif(self):
        """C7: IPK negatif harus raise ValueError."""
        with pytest.raises(ValueError, match="IPK harus antara 0.0-4.0"):
            Mahasiswa("2024SI005", "Test", "SI", 2024, -1.0)

    def test_ipk_boundary_nol(self):
        """C8: IPK boundary bawah (0.0) harus valid."""
        mhs = Mahasiswa("2024SI006", "Citra", "SI", 2024, 0.0)
        assert mhs.ipk == 0.0

    def test_ipk_boundary_empat(self):
        """C9: IPK boundary atas (4.0) harus valid."""
        mhs = Mahasiswa("2024SI007", "Dewi", "SI", 2024, 4.0)
        assert mhs.ipk == 4.0

    def test_str_representation(self):
        """C10: __str__ harus mengembalikan format yang benar."""
        mhs = Mahasiswa("2024SI001", "Andi", "SI", 2024, 3.5)
        result = str(mhs)
        assert "2024SI001" in result
        assert "Andi" in result
        assert "3.50" in result


# ============================================================
# TEST CLASS: TestDaftarMahasiswa
# ============================================================

class TestDaftarMahasiswa:
    """Unit test untuk model DaftarMahasiswa (CRUD)."""

    def setup_method(self):
        """Setup: buat DaftarMahasiswa baru sebelum setiap test."""
        self.db = DaftarMahasiswa()
        self.mhs1 = Mahasiswa("2024SI001", "Andi Pratama", "Sistem Informasi", 2024, 3.50)
        self.mhs2 = Mahasiswa("2024SI002", "Budi Santoso", "Sistem Informasi", 2024, 3.20)

    def test_tambah_dan_cari(self):
        """D1: Tambah mahasiswa lalu cari berdasarkan NIM."""
        self.db.tambah(self.mhs1)
        result = self.db.cari("2024SI001")
        assert result == self.mhs1
        assert self.db.jumlah == 1

    def test_nim_duplikat_raise_error(self):
        """D2: Menambah NIM yang sudah ada harus raise ValueError."""
        m1 = Mahasiswa("2024SI001", "Andi", "SI", 2024, 3.0)
        m2 = Mahasiswa("2024SI001", "Budi", "SI", 2024, 3.5)
        self.db.tambah(m1)
        with pytest.raises(ValueError, match="sudah terdaftar"):
            self.db.tambah(m2)

    def test_cari_nim_tidak_ada(self):
        """D3: Cari NIM yang tidak ada harus mengembalikan None."""
        result = self.db.cari("TIDAK_ADA")
        assert result is None

    def test_hapus_mahasiswa(self):
        """D4: Hapus mahasiswa berdasarkan NIM harus berhasil."""
        self.db.tambah(self.mhs1)
        hasil = self.db.hapus("2024SI001")
        assert hasil is True
        assert self.db.jumlah == 0
        assert self.db.cari("2024SI001") is None

    def test_hapus_nim_tidak_ada(self):
        """D5: Hapus NIM yang tidak ada harus mengembalikan False."""
        hasil = self.db.hapus("TIDAK_ADA")
        assert hasil is False

    def test_jumlah_setelah_tambah_banyak(self):
        """D6: Jumlah mahasiswa harus tepat setelah beberapa tambah."""
        self.db.tambah(self.mhs1)
        self.db.tambah(self.mhs2)
        assert self.db.jumlah == 2

    def test_update_ipk_berhasil(self):
        """D7: Update IPK mahasiswa yang ada harus berhasil."""
        self.db.tambah(self.mhs1)
        hasil = self.db.update_ipk("2024SI001", 3.75)
        assert hasil is True
        assert self.db.cari("2024SI001").ipk == 3.75

    def test_update_ipk_tidak_valid(self):
        """D8: Update IPK di luar range harus raise ValueError."""
        self.db.tambah(self.mhs1)
        with pytest.raises(ValueError, match="IPK harus antara"):
            self.db.update_ipk("2024SI001", 4.5)

    def test_update_ipk_nim_tidak_ada(self):
        """D9: Update IPK untuk NIM tidak ada harus mengembalikan False."""
        hasil = self.db.update_ipk("TIDAK_ADA", 3.5)
        assert hasil is False

    def test_daftar_kosong_awal(self):
        """D10: DaftarMahasiswa baru harus kosong."""
        assert self.db.jumlah == 0
        assert self.db.data == []
