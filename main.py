import os
import csv
import base64
import requests
import json
from cer import calculate_cer
from PIL import Image

# KONFIGURASI
LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"  # Ubah jika perlu
MODEL = "llava-1.6-mistral-7b"  # Atau "bakllava", sesuai model kamu

# PROMPT UNTUK MODEL
PROMPT = "What is the license plate number shown in this image? Respond only with the plate number."

# HEADER request
headers = {
    "Content-Type": "application/json"
}

# Fungsi membaca data ground truth dari CSV
def load_ground_truth(csv_path):
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

# Fungsi konversi gambar ke base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_f:
        return base64.b64encode(img_f.read()).decode('utf-8')

def query_lmstudio(image_path, prompt):
    base64_img = image_to_base64(image_path)
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]
            }
        ],
        "temperature": 0.2,
        "max_tokens": 100
    }
    response = requests.post(LMSTUDIO_URL, headers=headers, json=payload)
    
    try:
        result = response.json()
        print(json.dumps(result, indent=2))  # Lihat isi respon

        # Ambil konten teksnya
        raw_text = result['choices'][0]['message']['content'].strip()
        print("Raw prediction:", raw_text)

        # Ekstrak plate number saja
        import re
        match = re.search(r"[A-Z0-9]{1,3}\s?[0-9]{1,4}\s?[A-Z]{1,3}", raw_text)
        if match:
            prediction = match.group(0).replace(" ", "")
        else:
            prediction = ""

        print("Hasil prediksi (bersih):", prediction)
        return prediction

    except Exception as e:
        print("Gagal mengambil prediksi:", e)
        return ""

# Fungsi utama
def run_ocr():
    dataset = load_ground_truth("ground_truth.csv")
    output = []

    for row in dataset:
        image_file = row["image"]
        gt = row["ground_truth"]
        image_path = os.path.join("test", image_file)

        print(f"Processing {image_file}...")

        try:
            pred = query_lmstudio(image_path, PROMPT)
        except Exception as e:
            print(f"Error processing {image_file}: {e}")
            pred = ""

        cer_score = calculate_cer(gt, pred)
        output.append({
            "image": image_file,
            "ground_truth": gt,
            "prediction": pred,
            "CER_score": cer_score
        })

    # Simpan hasil ke result.csv
    with open("result.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["image", "ground_truth", "prediction", "CER_score"])
        writer.writeheader()
        writer.writerows(output)

    print("Selesai. Hasil disimpan di result.csv")

# Eksekusi jika dijalankan langsung
if __name__ == "__main__":
    run_ocr()
