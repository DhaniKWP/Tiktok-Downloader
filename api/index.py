import re
import tempfile
import os
import requests
from flask import Flask, request, send_file, abort, send_from_directory
from moviepy import VideoFileClip

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(directory=os.getcwd(), path='index.html')

@app.route('/download')
def download():
    url = request.args.get('url', '').strip()
    format = request.args.get('format', 'mp4')  # default: mp4

    if not url:
        return abort(400, 'URL tidak boleh kosong.')

    try:
        # Hapus query param dari URL
        video_url = url.split("?")[0]

        # Request ke SnapTik/Tikmate API
        api_url = "https://api.tikmate.app/api/lookup"
        resp = requests.post(api_url, data={"url": video_url}, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        res_json = resp.json()

        if 'token' not in res_json or 'id' not in res_json:
            return abort(500, "Gagal mendapatkan respons yang valid dari SnapTik API.")

        download_link = f"https://tikmate.app/download/{res_json['token']}/{res_json['id']}.mp4"
        video_data = requests.get(download_link).content

    except Exception as e:
        return abort(500, f"Gagal mengambil video: {e}")

    # Simpan video ke file sementara
    tmp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tmp_video.write(video_data)
    tmp_video.flush()
    tmp_video.close()

    # Jika minta format mp3, konversi dulu
    if format == 'mp3':
        tmp_audio_path = tmp_video.name.replace('.mp4', '.mp3')
        try:
            clip = VideoFileClip(tmp_video.name)
            clip.audio.write_audiofile(tmp_audio_path)
            clip.close()
            return send_file(
                tmp_audio_path,
                as_attachment=True,
                download_name='tiktok_audio.mp3',
                mimetype='audio/mpeg'
            )
        except Exception as e:
            return abort(500, f"Gagal mengubah ke MP3: {e}")

    # Kalau formatnya tetap video
    return send_file(
        tmp_video.name,
        as_attachment=True,
        download_name='tiktok_no_wm.mp4',
        mimetype='video/mp4'
    )