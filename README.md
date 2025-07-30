# OCR Plat Nomor Kendaraan dengan Visual Language Model (VLM)

Proyek ini melakukan Optical Character Recognition (OCR) pada gambar plat nomor kendaraan menggunakan **Visual Language Model (VLM)** seperti `llava-1.6-mistral-7b` yang dijalankan melalui **LMStudio** dan diintegrasikan dengan bahasa pemrograman Python.

##  Fitur Utama

- Kirim gambar plat nomor ke LMStudio via API
- Gunakan prompt untuk mengekstrak nomor plat
- Evaluasi akurasi prediksi menggunakan metrik **Character Error Rate (CER)**
- Simpan hasil evaluasi ke file `result.csv`

---

##  Model yang Digunakan

- **Model:** `llava-1.6-mistral-7b` (bisa diganti ke model multimodal lain seperti `bakllava`)
- **Server VLM:** [LMStudio](https://lmstudio.ai)

---

## 📂 Struktur Folder

ocr-vlm-platnomor/
├── main.py # Program utama
├── cer.py # Fungsi untuk menghitung CER
├── ground_truth.csv # Ground truth plat nomor
├── result.csv # Hasil prediksi dan CER
├── test/ # Folder berisi gambar
│ ├── test001_1.jpg
│ └── ...
└── README.md # Dokumentasi


---

##  Cara Menjalankan

### 1. Jalankan LMStudio

- Unduh dan jalankan LMStudio (https://lmstudio.ai)
- Pilih model `llava-1.6-mistral-7b` dan jalankan local server di `http://localhost:1234`

### 2. Siapkan Lingkungan Python

```bash
pip install requests pillow

### 3. Jalankan Program
python main.py

### 4. Hasil
Hasil prediksi disimpan dalam file result.csv dengan format:
image,ground_truth,prediction,CER_score
test001_1.jpg,B9140BCD,B914OBCD,0.125
test001_2.jpg,B2407UZO,B2407UZO,0.0
...

📏 Metode Evaluasi
Menggunakan Character Error Rate (CER):
CER = (S + D + I) / N
S = Substitusi

D = Deletion (karakter yang hilang)

I = Insertion (karakter yang salah ditambah)

N = Jumlah karakter pada ground truth

Fungsi perhitungan CER ada di cer.py.
