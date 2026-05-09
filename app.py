"""
URL Shortener API + UI
Tugas Mandiri PaaS - Komputasi Awan
Muhammad Raihan Fadhilah - 1202220335
"""

import os
import string
import random
from datetime import datetime
from flask import Flask, jsonify, request, redirect, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Konfigurasi database dari environment variable
database_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
# Railway/Heroku kadang kasih postgres:// (deprecated), SQLAlchemy butuh postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-jangan-pakai-di-produksi')

db = SQLAlchemy(app)


# Model database
class ShortURL(db.Model):
    __tablename__ = 'short_urls'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    original_url = db.Column(db.String(2048), nullable=False)
    click_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            'code': self.code,
            'original_url': self.original_url,
            'click_count': self.click_count,
            'created_at': self.created_at.isoformat()
        }


def generate_code(length=6):
    """Generate kode pendek acak yang belum dipakai."""
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not ShortURL.query.filter_by(code=code).first():
            return code


# Endpoint 1: Beranda - tampilkan UI atau JSON tergantung Accept header
@app.route('/')
def beranda():
    # Kalau request dari browser, tampilkan UI
    if 'text/html' in request.headers.get('Accept', ''):
        return render_template('index.html')

    # Kalau dari API client (curl, Thunder Client tanpa Accept), kasih JSON
    return jsonify({
        'aplikasi': 'URL Shortener API',
        'pengembang': 'Muhammad Raihan Fadhilah (1202220335)',
        'matkul': 'Komputasi Awan - BBK3CAB3',
        'versi': '1.0.0',
        'endpoints': {
            'POST /shorten': 'Buat short URL dari URL panjang',
            'GET /<code>': 'Redirect ke URL asli',
            'GET /stats/<code>': 'Lihat statistik klik',
            'GET /health': 'Health check'
        }
    })


# Endpoint untuk akses API info eksplisit (alternatif ke GET /)
@app.route('/api')
def api_info():
    return jsonify({
        'aplikasi': 'URL Shortener API',
        'pengembang': 'Muhammad Raihan Fadhilah (1202220335)',
        'matkul': 'Komputasi Awan - BBK3CAB3',
        'versi': '1.0.0',
        'endpoints': {
            'POST /shorten': 'Buat short URL dari URL panjang',
            'GET /<code>': 'Redirect ke URL asli',
            'GET /stats/<code>': 'Lihat statistik klik',
            'GET /health': 'Health check'
        }
    })


# Endpoint 2: Bikin short URL
@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json(silent=True)
    if not data or 'url' not in data:
        return jsonify({'error': 'Body JSON harus berisi field "url"'}), 400

    original_url = data['url'].strip()
    if not original_url.startswith(('http://', 'https://')):
        return jsonify({'error': 'URL harus diawali http:// atau https://'}), 400

    # Cek apakah URL ini sudah pernah di-shorten
    existing = ShortURL.query.filter_by(original_url=original_url).first()
    if existing:
        return jsonify({
            'pesan': 'URL ini sudah pernah dipendekkan',
            'data': existing.to_dict(),
            'short_url': request.host_url + existing.code
        }), 200

    code = generate_code()
    new_url = ShortURL(code=code, original_url=original_url)
    db.session.add(new_url)
    db.session.commit()

    return jsonify({
        'pesan': 'URL berhasil dipendekkan',
        'data': new_url.to_dict(),
        'short_url': request.host_url + code
    }), 201


# Endpoint 3: Redirect
@app.route('/<code>')
def redirect_url(code):
    # Hindari konflik dengan endpoint lain
    if code in ('shorten', 'health', 'stats', 'api', 'static'):
        abort(404)

    short_url = ShortURL.query.filter_by(code=code).first()
    if not short_url:
        return jsonify({'error': 'Kode tidak ditemukan'}), 404

    short_url.click_count += 1
    db.session.commit()

    return redirect(short_url.original_url, code=302)


# Endpoint 4: Statistik
@app.route('/stats/<code>')
def stats(code):
    short_url = ShortURL.query.filter_by(code=code).first()
    if not short_url:
        return jsonify({'error': 'Kode tidak ditemukan'}), 404

    return jsonify({
        'pesan': 'Statistik URL',
        'data': short_url.to_dict()
    })


# Endpoint 5: Health check
@app.route('/health')
def health():
    try:
        # Cek koneksi database
        db.session.execute(db.text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'

    return jsonify({
        'status': 'sehat',
        'database': db_status,
        'timestamp': datetime.utcnow().isoformat()
    })


# Inisialisasi database saat aplikasi start
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
