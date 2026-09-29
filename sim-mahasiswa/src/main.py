"""
main.py - Program Utama Sistem Informasi Mahasiswa
Entry point aplikasi dengan menu interaktif berbasis console.
Mata Kuliah Pemrograman Python
"""

import sys
import os

# Tambah path src ke sys.path agar import models berjalan
sys.path.insert(0, os.path.dirname(__file__))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from models import Mahasiswa, DaftarMahasiswa

console = Console()
db = DaftarMahasiswa()


def tampilkan_menu():
    """Tampilkan menu utama."""
    menu_text = (
        "[bold cyan]╔══════════════════════════════════════╗[/]\n"
        "[bold cyan]║   SISTEM INFORMASI MAHASISWA (SIM)   ║[/]\n"
        "[bold cyan]╚══════════════════════════════════════╝[/]\n\n"
        "[bold white]  1.[/] [green]Tambah Mahasiswa[/]\n"
        "[bold white]  2.[/] [blue]Tampilkan Semua Mahasiswa[/]\n"
        "[bold white]  3.[/] [yellow]Cari Mahasiswa (NIM)[/]\n"
        "[bold white]  4.[/] [red]Hapus Mahasiswa[/]\n"
        "[bold white]  5.[/] [magenta]Edit IPK Mahasiswa[/]\n"
        "[bold white]  0.[/] [dim]Keluar[/]\n"
    )
    console.print(Panel(menu_text, border_style="cyan", padding=(1, 2)))
    console.print(f"  [dim]Total mahasiswa terdaftar: [bold]{db.jumlah}[/] orang[/]")


def tambah_mahasiswa():
    """Form tambah mahasiswa baru."""
    console.print("\n[bold cyan]━━━ Tambah Mahasiswa Baru ━━━[/]")
    try:
        nim       = Prompt.ask("  [cyan]NIM[/]")
        nama      = Prompt.ask("  [cyan]Nama Lengkap[/]")
        prodi     = Prompt.ask("  [cyan]Program Studi[/]")
        angkatan  = int(Prompt.ask("  [cyan]Angkatan[/]"))
        ipk       = float(Prompt.ask("  [cyan]IPK[/] [dim](0.0-4.0)[/]"))

        mhs = Mahasiswa(nim, nama, prodi, angkatan, ipk)
        db.tambah(mhs)
        console.print(f"\n  [bold green]✓ Berhasil![/] {nama} (NIM: {nim}) telah ditambahkan.\n")
    except ValueError as e:
        console.print(f"\n  [bold red]✗ Gagal:[/] {e}\n")


def tampilkan_semua():
    """Tampilkan seluruh data dalam tabel yang rapi."""
    console.print("\n[bold cyan]━━━ Daftar Semua Mahasiswa ━━━[/]")
    if not db.data:
        console.print("  [yellow]⚠  Belum ada data mahasiswa terdaftar.[/]\n")
        return

    table = Table(
        title=f"[bold]Daftar Mahasiswa — Total: {db.jumlah} orang[/]",
        border_style="cyan",
        header_style="bold magenta",
        show_lines=True,
    )
    table.add_column("No",           style="dim",    justify="center", width=4)
    table.add_column("NIM",          style="cyan",   justify="left",   min_width=12)
    table.add_column("Nama",         style="white",  justify="left",   min_width=25)
    table.add_column("Program Studi",style="green",  justify="left",   min_width=20)
    table.add_column("Angkatan",     style="yellow", justify="center", width=9)
    table.add_column("IPK",          style="bold",   justify="center", width=6)

    for i, m in enumerate(db.data, start=1):
        # Warnai IPK berdasarkan nilai
        if m.ipk >= 3.5:
            ipk_style = "bold green"
        elif m.ipk >= 3.0:
            ipk_style = "yellow"
        else:
            ipk_style = "red"
        table.add_row(
            str(i),
            m.nim,
            m.nama,
            m.program_studi,
            str(m.angkatan),
            Text(f"{m.ipk:.2f}", style=ipk_style),
        )
    console.print(table)
    console.print()


def cari_mahasiswa():
    """Cari mahasiswa berdasarkan NIM."""
    console.print("\n[bold cyan]━━━ Cari Mahasiswa ━━━[/]")
    nim = Prompt.ask("  [cyan]Masukkan NIM yang dicari[/]")
    mhs = db.cari(nim)
    if mhs:
        table = Table(title="[bold green]✓ Mahasiswa Ditemukan[/]", border_style="green")
        table.add_column("Field",  style="bold cyan")
        table.add_column("Data",   style="white")
        table.add_row("NIM",           mhs.nim)
        table.add_row("Nama",          mhs.nama)
        table.add_row("Program Studi", mhs.program_studi)
        table.add_row("Angkatan",      str(mhs.angkatan))
        table.add_row("IPK",           f"{mhs.ipk:.2f}")
        console.print(table)
    else:
        console.print(f"\n  [bold red]✗ Mahasiswa dengan NIM '{nim}' tidak ditemukan.[/]\n")


def hapus_mahasiswa():
    """Hapus mahasiswa berdasarkan NIM."""
    console.print("\n[bold cyan]━━━ Hapus Mahasiswa ━━━[/]")
    nim = Prompt.ask("  [cyan]Masukkan NIM yang akan dihapus[/]")
    mhs = db.cari(nim)
    if mhs:
        konfirmasi = Prompt.ask(
            f"  [yellow]Yakin hapus [bold]{mhs.nama}[/] (NIM: {nim})?[/] [dim][y/n][/]"
        )
        if konfirmasi.lower() == "y":
            db.hapus(nim)
            console.print(f"\n  [bold green]✓ Berhasil![/] Data {mhs.nama} telah dihapus.\n")
        else:
            console.print("  [dim]Penghapusan dibatalkan.[/]\n")
    else:
        console.print(f"\n  [bold red]✗ NIM '{nim}' tidak ditemukan.[/]\n")


def edit_ipk():
    """Edit IPK mahasiswa berdasarkan NIM."""
    console.print("\n[bold cyan]━━━ Edit IPK Mahasiswa ━━━[/]")
    nim = Prompt.ask("  [cyan]Masukkan NIM mahasiswa[/]")
    mhs = db.cari(nim)
    if mhs:
        console.print(f"  IPK saat ini: [bold yellow]{mhs.ipk:.2f}[/]")
        try:
            ipk_baru = float(Prompt.ask("  [cyan]IPK baru[/] [dim](0.0-4.0)[/]"))
            db.update_ipk(nim, ipk_baru)
            console.print(f"\n  [bold green]✓ Berhasil![/] IPK {mhs.nama} diperbarui menjadi [bold]{ipk_baru:.2f}[/]\n")
        except ValueError as e:
            console.print(f"\n  [bold red]✗ Gagal:[/] {e}\n")
    else:
        console.print(f"\n  [bold red]✗ NIM '{nim}' tidak ditemukan.[/]\n")


def main():
    """Loop utama aplikasi SIM Mahasiswa."""
    console.clear()
    console.print("\n[bold cyan]  Selamat datang di Sistem Informasi Mahasiswa![/]\n")

    while True:
        tampilkan_menu()
        pilihan = Prompt.ask("\n  [bold]Pilih menu[/]", choices=["0", "1", "2", "3", "4", "5"])

        if pilihan == "1":
            tambah_mahasiswa()
        elif pilihan == "2":
            tampilkan_semua()
        elif pilihan == "3":
            cari_mahasiswa()
        elif pilihan == "4":
            hapus_mahasiswa()
        elif pilihan == "5":
            edit_ipk()
        elif pilihan == "0":
            console.print("\n  [bold cyan]Sampai jumpa! Terima kasih telah menggunakan SIM.[/]\n")
            break


if __name__ == "__main__":
    main()
