import sqlite3
import streamlit as st

# Koneksi ke database
conn = sqlite3.connect("store_management.db", check_same_thread=False)
cursor = conn.cursor()

# Pastikan tabel Product sudah ada
def ensure_product_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
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
            SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
            NamaSupplier TEXT NOT NULL,
            AlamatSupplier TEXT NOT NULL,
            Email TEXT NOT NULL,
            NomorTelepon TEXT NOT NULL
        )
    ''')
    conn.commit()

# Panggil fungsi untuk memastikan tabel
ensure_product_table()
ensure_supplier_table()

# Fungsi untuk menambahkan data ke tabel Supplier
def add_supplier(nama, alamat, email, telepon):
    cursor.execute('''
        INSERT INTO Supplier (NamaSupplier, AlamatSupplier, Email, NomorTelepon)
        VALUES (?, ?, ?, ?)
    ''', (nama, alamat, email, telepon))
    conn.commit()

# Fungsi untuk mendapatkan daftar supplier
def get_suppliers():
    cursor.execute("SELECT SupplierID, NamaSupplier FROM Supplier")
    return cursor.fetchall()

# Fungsi untuk menambahkan data ke tabel Product
def add_product(merek, model, tipe, color, size, stok, harga_beli, harga_jual, kode_supplier):
    cursor.execute('''
        INSERT INTO Product (Merek, Model, Type, Color, Size, Stok, HargaBeli, HargaJual, KodeSupplier)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (merek, model, tipe, color, size, stok, harga_beli, harga_jual, kode_supplier))
    conn.commit()

# Streamlit Sidebar
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Menu", ["Tambah Produk", "Lihat Produk", "Tambah Supplier", "Lihat Supplier"])

# Halaman Tambah Supplier
if menu == "Tambah Supplier":
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
        for row in rows:
            st.write(f"**ID**: {row[0]} | **Nama**: {row[1]} | **Alamat**: {row[2]} | **Email**: {row[3]} | **Telepon**: {row[4]}")
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
        for row in rows:
            st.write(f"**ID**: {row[0]} | **Merek**: {row[1]} | **Model**: {row[2]} | **Tipe**: {row[3]} | **Warna**: {row[4]} | **Ukuran**: {row[5]} | **Stok**: {row[6]} | **Harga Beli**: {row[7]} | **Harga Jual**: {row[8]} | **Kode Supplier**: {row[9]}")
    else:
        st.warning("Tidak ada data produk.")

# Tutup koneksi database secara manual
if st.sidebar.button("Tutup Aplikasi"):
    conn.close()
    st.sidebar.success("Koneksi database ditutup.")
