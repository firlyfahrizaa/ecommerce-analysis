# 🛍️ Proyek Analisis Data: E-Commerce Public Dataset

Proyek Akhir Belajar Fundamental Analisis Data - Dicoding Indonesia.

Dashboard interaktif ini dibangun menggunakan **Streamlit** untuk menganalisis performa penjualan kategori produk, pengaruh ketepatan waktu pengiriman terhadap kepuasan ulasan pelanggan, serta segmentasi pelanggan menggunakan teknik **RFM Analysis (Recency, Frequency, Monetary)**.

---

## 📁 Struktur Direktori

```text
submission/
├── dashboard/
│   ├── dashboard.py           # Skrip utama aplikasi dashboard Streamlit
│   └── main_data.csv          # Dataset siap saji yang telah dibersihkan
├── data/
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── notebook.ipynb             # Jupyter Notebook analisis lengkap
├── README.md                  # Dokumentasi panduan setup dan eksekusi
├── requirements.txt           # Berkas dependensi pustaka Python
└── url.txt                    # Tautan live dashboard di Streamlit Community Cloud
```

---

## 🚀 Panduan Menjalankan Dashboard di Komputer Lokal

### 1. Masuk ke Direktori Proyek
Buka Terminal atau Command Prompt, lalu arahkan ke folder utama proyek:
```bash
cd submission
```

### 2. Setup Virtual Environment
Gunakan virtual environment agar dependensi pustaka terisolasi dengan rapi.

**Untuk Windows (Command Prompt / PowerShell):**
```cmd
python -m venv venv
.\venv\Scripts\activate
```

**Untuk macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalasi Dependensi
Pasang seluruh library yang dibutuhkan menggunakan berkas `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard
Jalankan file `dashboard.py` sesuai struktur folder proyek:
```bash
streamlit run dashboard/dashboard.py
```

> **Catatan (Pengguna Windows):** Jika perintah `streamlit` tidak terbaca di terminal, jalankan perintah alternatif berikut:
> ```cmd
> python -m streamlit run dashboard/dashboard.py
> ```

---

## 🌐 Tautan Live Deployment

Aplikasi dashboard ini telah dideploy ke **Streamlit Community Cloud** dan dapat diakses secara daring melalui tautan yang tercantum pada berkas [`url.txt`](url.txt).
