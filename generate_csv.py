import os
import csv

# Nama folder tempat gambar-gambar test berada
folder = "test"
# Nama file output CSV
output_csv = "ground_truth.csv"

# Cek apakah folder ada
if not os.path.exists(folder):
    print(f"Folder '{folder}' tidak ditemukan.")
    exit()

# Ambil semua file JPG dari folder test
image_files = sorted([f for f in os.listdir(folder) if f.lower().endswith(".jpg")])

# Tulis ke ground_truth.csv dengan kolom kosong untuk diisi manual
with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["image", "ground_truth"])  # Header
    for image in image_files:
        writer.writerow([image, ""])  # Ground truth dikosongkan untuk diisi manual

print(f"{len(image_files)} file telah ditambahkan ke {output_csv}. Silakan isi kolom ground_truth secara manual.")
