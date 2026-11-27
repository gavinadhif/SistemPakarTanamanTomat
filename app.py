
import streamlit as st
import pandas as pd

from aturan_diagnosis import load_knowledge_base, forward_chaining
from desain_ui import (
    render_header,
    render_symptom_selector,
    render_diagnosis_button,
    render_diagnosis_results
)

# Konfigurasi halaman
st.set_page_config(
    page_title="Sistem Pakar Tanaman Tomat",
    page_icon="🍅",
    layout="wide"
)

# Nama penyakit dalam bahasa Indonesia
nama_penyakit = {
    "Early Blight": "Hawar Awal",
    "Late Blight": "Hawar Daun Lanjut",
    "Leaf Miner": "Pengorok Daun",
    "Leaf Mold": "Kapang Daun",
    "Mosaic Virus": "Virus Mosaik",
    "Septoria": "Bercak Septoria",
    "Spider Mites": "Tungau Laba-laba",
    "Target Spot": "Bercak Sasaran",
    "Yellow Leaf Curl Virus": "Virus Keriting Kuning Daun"
}

# Memuat basis pengetahuan
knowledge_base = load_knowledge_base()

# Memuat daftar gejala
data_gejala = pd.read_csv(
    "dataset/Daftar_Gejala_Tomat_9_Kategori_ID.csv",
    encoding="utf-8-sig"
)

# Memuat informasi penyakit dan penanganan
data_pengetahuan = pd.read_csv(
    "dataset/Basis_Pengetahuan_Tomat_9_Kategori_ID.csv",
    encoding="utf-8-sig"
)

# Menampilkan header aplikasi
render_header()

# Menampilkan pilihan gejala
pilihan_gejala = render_symptom_selector(
    knowledge_base,
    data_gejala,
    nama_penyakit
)

# Tombol dan proses diagnosis
if render_diagnosis_button():

    if len(pilihan_gejala) < 3:

        st.warning(
            "Silakan pilih minimal 3 gejala terlebih dahulu."
        )

    else:

        # Menjalankan metode Forward Chaining
        hasil = forward_chaining(
            pilihan_gejala,
            knowledge_base
        )

        # Menampilkan hasil diagnosis
        render_diagnosis_results(
            hasil,
            data_gejala,
            data_pengetahuan,
            nama_penyakit
        )
