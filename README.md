# 🎨 TikTok Downloader – MP4/MP3

[![Deploy on Railway](https://img.shields.io/badge/Railway-Live-blueviolet?logo=railway)](https://tiktok-downloader-mp4-mp3.up.railway.app/)

Downloader simpel dan powerful untuk video TikTok tanpa watermark – tersedia dalam format MP4 (video) dan MP3 (audio). Dibangun menggunakan **Python Flask** dan **SnapTik API**, aplikasi ini siap digunakan langsung lewat web.

🌐 **Akses langsung**: [tiktok-downloader-mp4-mp3.up.railway.app](https://tiktok-downloader-mp4-mp3.up.railway.app)

---

## 🚀 Fitur Utama

* ✅ Unduh video TikTok **tanpa watermark**
* 🎵 Ekspor sebagai **MP3** (audio saja) atau **MP4** (video)
* ⚡ Antarmuka clean, responsif & mobile-friendly
* 🔒 Semua proses dijalankan langsung di server — tidak menyimpan data pengguna
* 🧠 API pihak ketiga (SnapTik/Tikmate) untuk scraping cepat & stabil

---

## 🖼️ Tampilan

![Preview](https://user-images.githubusercontent.com/your-screenshot-url.png)

> *UI minimalis dengan tampilan smooth dan animasi modern*

---

## 🧑‍💻 Teknologi yang Digunakan

* **Backend**: [Flask](https://flask.palletsprojects.com/)
* **Frontend**: HTML5 + Vanilla JS + CSS animasi
* **Video processing**: [moviepy](https://zulko.github.io/moviepy/)
* **Deployment**: [Railway](https://railway.app/)
* **API pihak ketiga**: [SnapTik](https://snaptik.app/) (unofficial via `tikmate.app`)

---

## 📦 Cara Install Lokal

```bash
git clone https://github.com/username/tiktok-downloader.git
cd tiktok-downloader
python3 -m venv venv
source venv/bin/activate  # atau venv\Scripts\activate di Windows
pip install -r requirements.txt
python app.py
```

Akses di browser: [http://localhost:8003](http://localhost:8003)

---

## ⚙️ Struktur Proyek

```bash
.
├── app.py               # Backend Flask logic
├── index.html           # Tampilan frontend
├── requirements.txt     # Dependencies Python
└── README.md            # Dokumentasi (file ini)
```

---

## ⚙️ Deployment

Proyek ini siap untuk deploy ke Railway:

1. Klik **Deploy to Railway**
2. Set environment variable `PORT=8003`
3. Done!

---

## 📌 Catatan Tambahan

* Pastikan format URL TikTok valid dan publik
* API SnapTik bisa memiliki rate-limit atau error sesekali — cek log server jika terjadi kegagalan unduh

---

## ❤️ Dibuat oleh

**Dhani Kusuma**

> Made with passion and a few cups of ☕
> ✨ GitHub: [@DhaniKWP](https://github.com/Dhanikwp)

---

## 📄 Lisensi

MIT License
