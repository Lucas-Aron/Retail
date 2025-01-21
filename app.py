import sqlite3
import streamlit as st
from datetime import datetime
import pandas as pd

# Koneksi ke database
conn = sqlite3.connect("store_management.db", check_same_thread=False)
cursor = conn.cursor()

# Pastikan tabel Product sudah ada
def ensure_product_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            ProductID TEXT PRIMARY KEY,
            Merek TEXT NOT NULL,
            Model TEXT NOT NULL,
            Type TEXT NOT NULL,
            Color TEXT,
            Size TEXT,
            Stok INTEGER NOT NULL,
            HargaBeli REAL NOT NULL,
            HargaJual REAL NOT NULL,
            KodeSupplier TEXT NOT NULL
        )
    ''')
    conn.commit()

# Pastikan tabel Supplier sudah ada
def ensure_supplier_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierID TEXT PRIMARY KEY,
            NamaSupplier TEXT NOT NULL,
            AlamatSupplier TEXT NOT NULL,
            Email TEXT NOT NULL,
            NomorTelepon TEXT NOT NULL
        )
    ''')
    conn.commit()

# Pastikan tabel EmployeeAccess sudah ada
def ensure_employee_access_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EmployeeAccess (
            AccessID TEXT PRIMARY KEY,
            EmployeeName TEXT NOT NULL,
            AccessTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

# Panggil fungsi untuk memastikan tabel
ensure_product_table()
ensure_supplier_table()
ensure_employee_access_table()

# Fungsi untuk mencatat akses karyawan
def log_employee_access(employee_name):
    access_id = f"EMP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    cursor.execute('''
        INSERT INTO EmployeeAccess (AccessID, EmployeeName)
        VALUES (?, ?)
    ''', (access_id, employee_name))
    conn.commit()

# Fungsi untuk mendapatkan riwayat akses karyawan
def get_employee_access_log():
    cursor.execute("SELECT * FROM EmployeeAccess ORDER BY AccessTime DESC")
    return cursor.fetchall()

# Fungsi untuk menambahkan data ke tabel Supplier
def add_supplier(nama, alamat, email, telepon):
    supplier_id = f"SUP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    cursor.execute('''
        INSERT INTO Supplier (SupplierID, NamaSupplier, AlamatSupplier, Email, NomorTelepon)
        VALUES (?, ?, ?, ?, ?)
    ''', (supplier_id, nama, alamat, email, telepon))
    conn.commit()

# Fungsi untuk mendapatkan daftar supplier
def get_suppliers():
    cursor.execute("SELECT SupplierID, NamaSupplier FROM Supplier")
    return cursor.fetchall()

# Fungsi untuk menambahkan data ke tabel Product
def add_product(merek, model, tipe, color, size, stok, harga_beli, harga_jual, kode_supplier):
    product_id = f"PROD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    cursor.execute('''
        INSERT INTO Product (ProductID, Merek, Model, Type, Color, Size, Stok, HargaBeli, HargaJual, KodeSupplier)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (product_id, merek, model, tipe, color, size, stok, harga_beli, harga_jual, kode_supplier))
    conn.commit()

# Streamlit Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Menu", ["Akses Karyawan", "Tambah Produk", "Lihat Produk", "Tambah Supplier", "Lihat Supplier", "Riwayat Akses Karyawan"])

# Halaman Akses Karyawan
if menu == "Akses Karyawan":
    st.title("Akses Karyawan")

    with st.form("form_employee_access"):
        employee_name = st.text_input("Nama Karyawan")
        submitted = st.form_submit_button("Catat Akses")

        if submitted:
            log_employee_access(employee_name)
            st.success(f"Akses berhasil dicatat untuk karyawan: {employee_name}")

# Halaman Riwayat Akses Karyawan
elif menu == "Riwayat Akses Karyawan":
    st.title("Riwayat Akses Karyawan")

    access_logs = get_employee_access_log()

    if access_logs:
        df = pd.DataFrame(access_logs, columns=["ID", "Nama Karyawan", "Waktu Akses"])
        st.table(df)
    else:
        st.warning("Belum ada riwayat akses karyawan.")

# Halaman Tambah Supplier
elif menu == "Tambah Supplier":
    st.title("Tambah Supplier Baru")

    with st.form("form_supplier"):
        nama = st.text_input("Nama Supplier")
        alamat = st.text_input("Alamat Supplier")
        email = st.text_input("Email")
        telepon = st.text_input("Nomor Telepon")

        submitted = st.form_submit_button("Tambah")

        if submitted:
            add_supplier(nama, alamat, email, telepon)
            st.success("Supplier berhasil ditambahkan!")

# Halaman Lihat Supplier
elif menu == "Lihat Supplier":
    st.title("Daftar Supplier")

    cursor.execute("SELECT * FROM Supplier")
    rows = cursor.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Nama", "Alamat", "Email", "Telepon"])
        st.table(df)
    else:
        st.warning("Tidak ada data supplier.")

# Halaman Tambah Produk
elif menu == "Tambah Produk":
    st.title("Tambah Produk Baru")

    suppliers = get_suppliers()
    supplier_options = {f"{s[1]} (ID: {s[0]})": s[0] for s in suppliers}

    with st.form("form_product"):
        merek = st.text_input("Merek")
        model = st.text_input("Model")
        tipe = st.text_input("Tipe")
        color = st.text_input("Warna")
        size = st.text_input("Ukuran")
        stok = st.number_input("Stok", min_value=0, step=1)
        harga_beli = st.number_input("Harga Beli", min_value=0.0, step=0.1)
        harga_jual = st.number_input("Harga Jual", min_value=0.0, step=0.1)
        kode_supplier = st.selectbox("Supplier", options=list(supplier_options.keys()))

        submitted = st.form_submit_button("Tambah")

        if submitted:
            selected_supplier_id = supplier_options[kode_supplier]
            add_product(merek, model, tipe, color, size, stok, harga_beli, harga_jual, selected_supplier_id)
            st.success("Produk berhasil ditambahkan!")

# Halaman Lihat Produk
elif menu == "Lihat Produk":
    st.title("Daftar Produk")

    cursor.execute("SELECT * FROM Product")
    rows = cursor.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["ID", "Merek", "Model", "Tipe", "Warna", "Ukuran", "Stok", "Harga Beli", "Harga Jual", "Kode Supplier"])
        st.table(df)
    else:
        st.warning("Tidak ada data produk.")

# Tutup koneksi database secara manual
if st.sidebar.button("Tutup Aplikasi"):
    conn.close()
    st.sidebar.success("Koneksi database ditutup.")
