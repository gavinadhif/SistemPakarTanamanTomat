# Sistem Pakar Diagnosis Penyakit dan Hama Tanaman Tomat

## Identitas Proyek

- Nama: Naufal Gavin Nadhif Annafi
- NIM: 253307050
- Kelas: 3B
- Mata Kuliah: Sistem Cerdas
- Program Studi: Teknologi Informasi
- Institusi: Politeknik Negeri Madiun

## Masalah yang Diselesaikan

Penyakit dan hama pada tanaman tomat dapat menimbulkan kerusakan serta menurunkan hasil panen. Namun, tidak semua orang dapat mengenali jenis penyakit atau hama berdasarkan gejala yang muncul pada tanaman.

Proyek ini bertujuan membuat aplikasi sistem pakar berbasis web untuk membantu pengguna mengidentifikasi kemungkinan penyakit dan hama tanaman tomat berdasarkan gejala yang dipilih.

Aplikasi memberikan hasil berupa daftar kemungkinan penyakit atau hama, jumlah gejala yang cocok, persentase kecocokan, serta informasi kondisi pendukung, penanganan, dan pencegahan.

## Dataset

Sumber: [Mendeley Data - A Comprehensive Dataset of Tomato Plant Diseases for National Predictive Analytics and Crop Health Management](https://data.mendeley.com/datasets/ztncd79yhk/1)

Penulis dataset: Omkar Shinde, Sahil Jagtap, Rugved Sawant, Mayuresh Marade, Nilesh Sable, dan Parikshit Mahalle.

Lisensi: CC BY 4.0.

Jumlah kategori: 9 kategori penyakit dan hama tanaman tomat.

Kategori yang digunakan:
1. Early Blight
2. Late Blight
3. Leaf Miner
4. Leaf Mold
5. Mosaic Virus
6. Septoria
7. Spider Mites
8. Target Spot
9. Yellow Leaf Curl Virus

Dataset diolah menjadi daftar 120 gejala dan basis pengetahuan yang digunakan dalam proses diagnosis.

File dataset yang digunakan:
- `Data.csv`: dataset asli.
- `Basis_Pengetahuan_Tomat_9_Kategori.csv`: basis pengetahuan asli.
- `Basis_Pengetahuan_Tomat_9_Kategori_ID.csv`: basis pengetahuan dalam bahasa Indonesia.
- `Daftar_Gejala_Tomat_9_Kategori.csv`: daftar gejala asli.
- `Daftar_Gejala_Tomat_9_Kategori_ID.csv`: daftar gejala dalam bahasa Indonesia.

## Metode

Metode yang digunakan adalah Sistem Pakar dengan teknik Forward Chaining.

Forward Chaining merupakan metode penalaran yang dimulai dari fakta yang diketahui, kemudian mencocokkannya dengan aturan untuk memperoleh kesimpulan.

Pada aplikasi ini, gejala yang dipilih pengguna menjadi fakta awal. Sistem kemudian mencocokkan kode gejala dengan aturan IF-THEN yang dibentuk dari basis pengetahuan.

Tahapan proses:
1. Pengguna memilih gejala yang sesuai dengan kondisi tanaman tomat.
2. Sistem membaca kode gejala yang dipilih.
3. Sistem mencocokkan gejala dengan aturan pada basis pengetahuan.
4. Kategori penyakit atau hama yang memiliki kecocokan dimasukkan sebagai kandidat diagnosis.
5. Sistem menghitung jumlah gejala yang cocok dan persentase kecocokan.
6. Hasil diagnosis beserta informasi penanganan ditampilkan kepada pengguna.

Jumlah aturan yang dibentuk adalah 120 aturan berdasarkan daftar gejala.

Persentase kecocokan dihitung menggunakan rumus:

`Persentase = (Jumlah gejala cocok / Total gejala kategori) x 100%`

Persentase tersebut menunjukkan tingkat kecocokan gejala terhadap suatu kategori, bukan probabilitas pasti atau akurasi diagnosis.

Teknologi yang digunakan:
- Python
- Django
- Pandas
- HTML dan CSS
- CSV sebagai penyimpanan data dan basis pengetahuan

## Hasil & Evaluasi

Aplikasi berhasil menjalankan proses diagnosis berdasarkan gejala yang dipilih pengguna dan menampilkan kategori penyakit atau hama berdasarkan hasil pencocokan.

Pengujian dilakukan terhadap sembilan kategori dengan menggunakan tiga gejala dari masing-masing kategori. Hasil pengujian menunjukkan bahwa kategori yang sesuai dengan gejala uji berhasil muncul sebagai hasil dengan kecocokan tertinggi.

### Tabel Pengujian Kasus

| No. | Kategori Uji | Gejala Cocok | Total Gejala | Persentase |
|---|---|---:|---:|---:|
| 1 | Early Blight | 3 | 7 | 42,86% |
| 2 | Late Blight | 3 | 9 | 33,33% |
| 3 | Leaf Miner | 3 | 18 | 16,67% |
| 4 | Leaf Mold | 3 | 8 | 37,50% |
| 5 | Mosaic Virus | 3 | 15 | 20,00% |
| 6 | Septoria | 3 | 12 | 25,00% |
| 7 | Spider Mites | 3 | 12 | 25,00% |
| 8 | Target Spot | 3 | 22 | 13,64% |
| 9 | Yellow Leaf Curl Virus | 3 | 17 | 17,65% |

Pengujian tersebut merupakan pengujian fungsional berdasarkan gejala yang telah diketahui pada masing-masing kategori. Pengujian ini belum dapat dianggap sebagai pengukuran akurasi diagnosis pada kondisi tanaman di lapangan.

## Cara Menjalankan

### Persyaratan

- Python
- Django
- Pandas
- Visual Studio Code atau editor kode lainnya

### Langkah menjalankan aplikasi

1. Buka folder proyek menggunakan Visual Studio Code.
2. Buka terminal pada folder utama proyek.
3. Aktifkan virtual environment:

   ```bash
   .venv\Scripts\activate
   ```

4. Masuk ke folder Django:

   ```bash
   cd sistem_pakar
   ```

5. Jalankan server Django:

   ```bash
   py manage.py runserver
   ```

6. Buka browser dan akses alamat:

   ```text
   http://127.0.0.1:8000/
   ```

7. Aplikasi siap digunakan untuk melakukan diagnosis penyakit dan hama tanaman tomat.

## Refleksi Singkat

Proyek ini berhasil menerapkan metode Forward Chaining untuk membantu proses identifikasi penyakit dan hama tanaman tomat berdasarkan gejala yang dipilih pengguna. Aplikasi juga dapat menampilkan informasi pendukung dan penanganan berdasarkan basis pengetahuan yang digunakan.

Keterbatasan aplikasi ini adalah hasil diagnosis masih bergantung pada kelengkapan dan ketepatan gejala yang dipilih pengguna. Persentase yang ditampilkan merupakan tingkat kecocokan gejala, bukan tingkat kepastian penyakit. Selain itu, pengujian masih menggunakan gejala dari basis pengetahuan dan belum diuji secara langsung oleh ahli pertanian pada tanaman di lapangan.

Pengembangan selanjutnya dapat dilakukan dengan menambahkan validasi dari ahli pertanian, memperluas basis pengetahuan, serta melakukan pengujian menggunakan kasus tanaman tomat yang diperoleh dari kondisi nyata.