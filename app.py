import os
import re
import tempfile
import requests
from flask import Flask, request, send_file, abort, send_from_directory
from moviepy import VideoFileClip
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(directory=os.getcwd(), path='index.html')


# ===============================
# 🎬 TikTok Download (MP4 or MP3)
# ===============================
@app.route('/download')
def download():
    url = request.args.get('url', '').strip()
    format = request.args.get('format', 'mp4')

    if not url:
        return abort(400, 'URL tidak boleh kosong.')

    try:
        video_url = url.split("?")[0]
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

    tmp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tmp_video.write(video_data)
    tmp_video.flush()
    tmp_video.close()

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

    return send_file(
        tmp_video.name,
        as_attachment=True,
        download_name='tiktok_no_wm.mp4',
        mimetype='video/mp4'
    )


# ===============================
# 🖼️ Remove Background from Image
# ===============================
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return abort(400, 'File gambar tidak ditemukan.')

    image_file = request.files['image']

    try:
        input_image = Image.open(image_file.stream).convert("RGBA")
        output_image = remove(input_image)

        tmp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        output_image.save(tmp_output.name, format='PNG')

        return send_file(
            tmp_output.name,
            as_attachment=True,
            download_name='no-bg.png',
            mimetype='image/png'
        )

    except Exception as e:
        return abort(500, f'Gagal menghapus latar belakang: {e}')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8003))
    app.run(host="0.0.0.0", port=port)
