# URL Shortener API

Tugas Mandiri Mata Kuliah Komputasi Awan (BBK3CAB3) - Platform as a Service.

**Pengembang:** Muhammad Raihan Fadhilah (1202220335)
**Program Studi:** S1 Sistem Informasi - Universitas Telkom

## Deskripsi

Aplikasi web sederhana untuk memendekkan URL panjang menjadi kode unik, sekaligus mencatat statistik klik. Dideploy ke platform PaaS Render dengan PostgreSQL sebagai database.

## Stack Teknologi

- **Bahasa:** Python 3.12
- **Framework:** Flask + Flask-SQLAlchemy
- **Database:** PostgreSQL 16
- **WSGI Server:** Gunicorn
- **Platform PaaS:** Render

## Aplikasi Live

🌐 **https://url-shortener-paas.onrender.com**

## Endpoint

| Method | Endpoint        | Fungsi                            |
|--------|-----------------|-----------------------------------|
| GET    | `/`             | Halaman utama (UI URL Shortener)  |
| POST   | `/shorten`      | Buat short URL dari URL panjang   |
| GET    | `/<code>`       | Redirect ke URL asli              |
| GET    | `/stats/<code>` | Lihat statistik klik              |
| GET    | `/health`       | Health check                      |

## Menjalankan Secara Lokal

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # lalu edit sesuai kebutuhan
python app.py
```

Buka `http://localhost:5000`.

## Contoh Penggunaan

**Memendekkan URL:**
```bash
curl -X POST https://url-shortener-paas.onrender.com/shorten \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://telkomuniversity.ac.id\"}"
```

**Cek statistik:**
```bash
curl https://url-shortener-paas.onrender.com/stats/<code>
```

**Cek kesehatan aplikasi:**
```bash
curl https://url-shortener-paas.onrender.com/health
```

## Lisensi

Tugas akademik. Bebas digunakan untuk pembelajaran.
