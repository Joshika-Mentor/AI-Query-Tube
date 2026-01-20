import yt_dlp
import os
import re
from cache import get_transcript_cached, set_transcript_cached

TEMP_DIR = "/tmp"

def get_transcript(video_id: str):
    # 1️⃣ Check transcript cache first
    cached = get_transcript_cached(video_id)
    if cached:
        return cached

    try:
        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "vtt",
            "outtmpl": f"{TEMP_DIR}/{video_id}.%(ext)s",
            "quiet": True,
            "socket_timeout": 5
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(
                [f"https://www.youtube.com/watch?v={video_id}"]
            )

        vtt_file = f"{TEMP_DIR}/{video_id}.en.vtt"
        if not os.path.exists(vtt_file):
            return None

        with open(vtt_file, "r", encoding="utf-8") as f:
            text = f.read()

        # Clean transcript
        text = re.sub(r"\d+:\d+:\d+\.\d+ --> .*", "", text)
        text = re.sub(r"<.*?>|WEBVTT|Kind:.*|Language:.*", "", text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()

        os.remove(vtt_file)

        # 2️⃣ Save transcript to cache
        set_transcript_cached(video_id, text)

        return text

    except Exception:
        return None
