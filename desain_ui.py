import streamlit as st


def render_header():
    """Menampilkan judul dan pengantar aplikasi."""
    st.markdown(
        """
        <style>
        :root {
            color-scheme: dark;
        }
        body,
        [data-testid="stAppViewContainer"],
        .stApp {
            background: #0b1220;
            color: #e5e7eb;
        }
        [data-testid="stHeader"] {
            background: rgba(11, 18, 32, 0.92);
        }
        [data-testid="stMainBlockContainer"] {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3, h4 {
            color: #f3f4f6;
            letter-spacing: -0.02em;
        }
        h1 {
            font-size: clamp(1.75rem, 4vw, 2.75rem);
            line-height: 1.15;
            max-width: 100%;
            overflow-wrap: anywhere;
            white-space: normal !important;
        }
        [data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"],
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stCheckbox"] label {
            color: #d1d5db;
        }
        [data-testid="stExpander"],
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #111c2e;
            border: 1px solid #263449;
            border-radius: 12px;
        }
        [data-testid="stExpander"] summary {
            color: #e5e7eb;
        }
        [data-testid="stCheckbox"] {
            padding: 0.18rem 0;
        }
        div.stButton > button {
            background: #23834b;
            border: 1px solid #23834b;
            border-radius: 9px;
            color: #ffffff;
            font-weight: 600;
            min-height: 2.8rem;
        }
        div.stButton > button:hover {
            background: #1c6b3d;
            border-color: #1c6b3d;
            color: #ffffff;
        }
        [data-testid="stProgressBar"] > div > div {
            background-color: #34a853;
        }
        [data-testid="stProgressBar"] > div {
            background: #263449;
        }
        hr {
            border-color: #263449;
        }
        @media (max-width: 640px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1rem 1rem 2rem;
            }
            h1 {
                font-size: 1.75rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        '<div style="background:#142b20;border:1px solid #28543a;'
        'border-radius:6px;color:#a7f3d0 !important;display:inline-block;'
        'font-size:0.82rem;font-weight:700;letter-spacing:0.08em;'
        'margin-bottom:0.75rem;padding:0.38rem 0.6rem;">'
        'SISTEM PAKAR · TANAMAN TOMAT</div>',
        unsafe_allow_html=True
    )
    st.title("Diagnosis Penyakit dan Hama Tanaman Tomat")
    st.write(
        "Pilih gejala yang terlihat pada tanaman untuk mendapatkan "
        "perkiraan diagnosis beserta informasi penanganannya."
    )
    st.divider()


def render_symptom_selector(knowledge_base, data_gejala, nama_penyakit):
    """Menampilkan checklist gejala dan mengembalikan kode yang dipilih."""
    st.subheader("Pilih gejala")
    st.write("Pilih minimal 3 gejala yang sesuai dengan kondisi tanaman.")

    pilihan_gejala = []
    kolom_gejala = st.columns(2)

    for indeks, disease in enumerate(knowledge_base):
        with kolom_gejala[indeks % 2]:
            judul = nama_penyakit.get(disease, disease)

            with st.expander(judul):
                data_kategori = data_gejala[
                    data_gejala["Disease"] == disease
                ]

                for _, row in data_kategori.iterrows():
                    kode_gejala = row["Kode_Gejala"]
                    if st.checkbox(row["Gejala"], key=kode_gejala):
                        pilihan_gejala.append(kode_gejala)

    if pilihan_gejala:
        st.caption(f"{len(pilihan_gejala)} gejala dipilih")

    st.divider()
    return pilihan_gejala


def render_diagnosis_button():
    """Menampilkan tombol untuk memulai diagnosis."""
    return st.button("Mulai Diagnosis", type="primary")


def render_diagnosis_results(
    hasil,
    data_gejala,
    data_pengetahuan,
    nama_penyakit
):
    """Menampilkan hasil diagnosis yang sudah dihitung aplikasi utama."""
    st.subheader("Hasil diagnosis")

    if not hasil:
        st.error(
            "Belum ditemukan kategori yang cocok "
            "dengan gejala yang dipilih."
        )
        return

    for diagnosis in hasil:
        penyakit = nama_penyakit.get(
            diagnosis["penyakit"],
            diagnosis["penyakit"]
        )

        with st.container(border=True):
            st.markdown(f"#### {penyakit}")

            kolom_kecocokan, kolom_persen = st.columns(2)
            kolom_kecocokan.metric(
                "Gejala cocok",
                f"{diagnosis['jumlah_cocok']}/"
                f"{diagnosis['total_gejala']}"
            )
            kolom_persen.metric(
                "Persentase kecocokan",
                f"{diagnosis['persentase']}%"
            )
            st.progress(int(diagnosis["persentase"]))

            st.markdown("**Gejala yang cocok**")
            for kode in diagnosis["gejala_cocok"]:
                nama_gejala = data_gejala.loc[
                    data_gejala["Kode_Gejala"] == kode,
                    "Gejala"
                ]

                if not nama_gejala.empty:
                    st.write(f"- {nama_gejala.iloc[0]} ({kode})")

            with st.expander("Informasi dan penanganan"):
                data_penyakit = data_pengetahuan[
                    data_pengetahuan["Disease"] == diagnosis["penyakit"]
                ]
                fitur = {
                    "favourable_condition": "Kondisi yang Mendukung",
                    "physical_biological":
                        "Penanganan Fisik dan Biologis",
                    "preventive_measures": "Langkah Pencegahan"
                }

                for kode_fitur, judul in fitur.items():
                    st.markdown(f"**{judul}**")
                    informasi = data_penyakit.loc[
                        data_penyakit["Feature"]
                        .astype(str)
                        .str.strip()
                        .str.lower() == kode_fitur,
                        "Description"
                    ].dropna()

                    isi = [
                        str(teks).strip()
                        for teks in informasi
                        if str(teks).strip()
                    ]

                    if not isi:
                        st.info(
                            "Informasi belum tersedia "
                            "dalam basis pengetahuan."
                        )
                        continue

                    for teks in isi:
                        for item in teks.split("<br>"):
                            item = item.strip()
                            if item:
                                st.write(f"- {item}")