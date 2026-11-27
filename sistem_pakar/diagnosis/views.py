from functools import lru_cache
from pathlib import Path
import sys

import pandas as pd
from django.shortcuts import render


PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from aturan_diagnosis import forward_chaining


NAMA_PENYAKIT = {
    "Early Blight": "Hawar Awal",
    "Late Blight": "Hawar Daun Lanjut",
    "Leaf Miner": "Pengorok Daun",
    "Leaf Mold": "Kapang Daun",
    "Mosaic Virus": "Virus Mosaik",
    "Septoria": "Bercak Septoria",
    "Spider Mites": "Tungau Laba-laba",
    "Target Spot": "Bercak Sasaran",
    "Yellow Leaf Curl Virus": "Virus Keriting Kuning Daun",
}

FITUR_PENANGANAN = {
    "favourable_condition": "Kondisi yang Mendukung",
    "physical_biological": "Penanganan Fisik dan Biologis",
    "preventive_measures": "Langkah Pencegahan",
}


@lru_cache(maxsize=1)
def load_diagnosis_data():
    data_gejala = pd.read_csv(
        PROJECT_ROOT / "dataset" / "Daftar_Gejala_Tomat_9_Kategori_ID.csv",
        encoding="utf-8-sig",
    )
    data_pengetahuan = pd.read_csv(
        PROJECT_ROOT / "dataset" / "Basis_Pengetahuan_Tomat_9_Kategori_ID.csv",
        encoding="utf-8-sig",
    )
    data_gejala["Kode_Gejala"] = data_gejala["Kode_Gejala"].astype(str)

    knowledge_base = {
        disease: data_gejala.loc[
            data_gejala["Disease"] == disease,
            "Kode_Gejala",
        ].tolist()
        for disease in data_gejala["Disease"].dropna().unique()
    }
    return knowledge_base, data_gejala, data_pengetahuan


def index(request):
    knowledge_base, data_gejala, data_pengetahuan = load_diagnosis_data()
    semua_kode_gejala = {
        kode
        for daftar_kode in knowledge_base.values()
        for kode in daftar_kode
    }
    kode_terpilih = list(dict.fromkeys(
        kode
        for kode in request.POST.getlist("gejala")
        if kode in semua_kode_gejala
    ))

    kelompok_gejala = []
    for disease in knowledge_base:
        rows = data_gejala.loc[
            data_gejala["Disease"] == disease,
            ["Kode_Gejala", "Gejala"],
        ].to_dict("records")
        kelompok_gejala.append({
            "nama": NAMA_PENYAKIT.get(disease, disease),
            "gejala": rows,
        })

    pesan_error = ""
    hasil_diagnosis = []
    if request.method == "POST":
        if len(kode_terpilih) < 3:
            pesan_error = "Silakan pilih minimal 3 gejala terlebih dahulu."
        else:
            hasil = forward_chaining(kode_terpilih, knowledge_base)
            nama_gejala = dict(zip(
                data_gejala["Kode_Gejala"],
                data_gejala["Gejala"],
            ))

            for diagnosis in hasil:
                data_penyakit = data_pengetahuan[
                    data_pengetahuan["Disease"] == diagnosis["penyakit"]
                ]
                penanganan = []
                for kode_fitur, judul in FITUR_PENANGANAN.items():
                    deskripsi = data_penyakit.loc[
                        data_penyakit["Feature"]
                        .astype(str)
                        .str.strip()
                        .str.lower() == kode_fitur,
                        "Description",
                    ].dropna()
                    daftar_item = [
                        item.strip()
                        for teks in deskripsi
                        for item in str(teks).split("<br>")
                        if item.strip()
                    ]
                    penanganan.append({
                        "judul": judul,
                        "informasi": daftar_item or [
                            "Informasi belum tersedia dalam basis pengetahuan."
                        ],
                    })

                hasil_diagnosis.append({
                    "nama": NAMA_PENYAKIT.get(
                        diagnosis["penyakit"],
                        diagnosis["penyakit"],
                    ),
                    "jumlah_cocok": diagnosis["jumlah_cocok"],
                    "total_gejala": diagnosis["total_gejala"],
                    "persentase": diagnosis["persentase"],
                    "gejala_cocok": [
                        {
                            "kode": kode,
                            "nama": nama_gejala[kode],
                        }
                        for kode in diagnosis["gejala_cocok"]
                        if kode in nama_gejala
                    ],
                    "penanganan": penanganan,
                })

    return render(request, "diagnosis/index.html", {
        "kelompok_gejala": kelompok_gejala,
        "kode_terpilih": kode_terpilih,
        "pesan_error": pesan_error,
        "hasil_diagnosis": hasil_diagnosis,
    })
