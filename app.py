import os
import tempfile
import requests
from flask import (Flask, request, abort, jsonify, send_file, send_from_directory, Response)
from moviepy import VideoFileClip

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

def get_video_tikwm(tiktok_url):
    r = requests.post(
        "https://tikwm.com/api/",
        data={"url": tiktok_url, "hd": 1},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20
    )
    r.raise_for_status()
    data = r.json()

    if not data.get("data") or not data["data"].get("play"):
        raise Exception("TikWM gagal")

    return {
        "title": data["data"].get("title", "tiktok_video_no_wm"),
        "video_url": data["data"]["play"]
    }

def get_video_ssstik(tiktok_url):
    from bs4 import BeautifulSoup

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://ssstik.io/"
    }

    session.get("https://ssstik.io/", headers=headers, timeout=10)

    r = session.post(
        "https://ssstik.io/abc?url=dl",
        data={"id": tiktok_url},
        headers=headers,
        timeout=20
    )

    soup = BeautifulSoup(r.text, "html.parser")
    a = soup.find("a", href=True, string=lambda x: x and "Download" in x)

    if not a:
        raise Exception("SSSTIK gagal")

    return {
        "title": "tiktok_video_no_wm",
        "video_url": a["href"]
    }

@app.route("/download-file")
def download_file():
    video_url = request.args.get("video_url")

    if not video_url:
        abort(400, "video_url required")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.tiktok.com/"
    }

    r = requests.get(video_url, headers=headers, stream=True, timeout=30)

    def stream():
        for chunk in r.iter_content(8192):
            if chunk:
                yield chunk

    return Response(
        stream(),
        headers={
            "Content-Disposition": "attachment; filename=tiktok_video.mp4",
            "Content-Type": "application/octet-stream"
        }
    )

@app.route("/download")
def download():
    url = request.args.get("url", "").strip()
    format = request.args.get("format", "mp4")

    if not url:
        abort(400, "URL tidak boleh kosong")

    try:
        try:
            result = get_video_tikwm(url)
        except:
            result = get_video_ssstik(url)

        video_url = result["video_url"]

        if format == "mp4":
            return jsonify({
                "status": "ok",
                "title": result["title"],
                "download_url": f"/download-file?video_url={video_url}"
            })

        tmp_mp4 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        r = requests.get(video_url, stream=True, timeout=30)

        for chunk in r.iter_content(8192):
            tmp_mp4.write(chunk)

        tmp_mp4.close()

        tmp_mp3 = tmp_mp4.name.replace(".mp4", ".mp3")

        clip = VideoFileClip(tmp_mp4.name)
        clip.audio.write_audiofile(tmp_mp3, logger=None)
        clip.close()

        return send_file(
            tmp_mp3,
            as_attachment=True,
            download_name="tiktok_audio.mp3",
            mimetype="audio/mpeg"
        )

    except Exception as e:
        abort(500, f"Gagal memproses video: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8003))
    app.run(host="0.0.0.0", port=port)
