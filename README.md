# URL Shortener API

Tugas Mandiri Mata Kuliah Komputasi Awan (BBK3CAB3) - Platform as a Service.

**Pengembang:** Muhammad Raihan Fadhilah (1202220335)
**Program Studi:** S1 Sistem Informasi - Universitas Telkom

## Deskripsi

Aplikasi web sederhana untuk memendekkan URL panjang menjadi kode unik, sekaligus mencatat statistik klik. Dideploy ke platform PaaS Railway dengan add-on PostgreSQL.

## Stack Teknologi

- **Bahasa:** Python 3.12
- **Framework:** Flask + Flask-SQLAlchemy
- **Database:** PostgreSQL (Railway add-on)
- **WSGI Server:** Gunicorn
- **Platform PaaS:** Railway

## Endpoint

| Method | Endpoint        | Fungsi                          |
|--------|-----------------|---------------------------------|
| GET    | `/`             | Info aplikasi dan daftar endpoint |
| POST   | `/shorten`      | Buat short URL dari URL panjang |
| GET    | `/<code>`       | Redirect ke URL asli            |
| GET    | `/stats/<code>` | Lihat statistik klik            |
| GET    | `/health`       | Health check                    |

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
curl -X POST https://<app>.up.railway.app/shorten \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://telkomuniversity.ac.id\"}"
```

**Cek statistik:**
```bash
curl https://<app>.up.railway.app/stats/<code>
```

## Lisensi

Tugas akademik. Bebas digunakan untuk pembelajaran.
