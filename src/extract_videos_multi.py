import requests
import pandas as pd
import os

print("SCRIPT STARTED (MILESTONE 1 – DATA EXTRACTION)")

# ======================
# CONFIGURATION
# ======================
API_KEY = "AIzaSyBcYjFGX8DCaR8k98LVQqqI1FwQvqfRm6M"

CHANNELS = {
    "Error Makes Clever": "UCwr-evhuzGZgDFrq_1pLt_A",

    # Food
    "Village Cooking Channel": "UCk3JZr7eS3pg5AGEvBdEvFg",

    # Songs
    "Lyrics Channel": "UCrh2CBMFVPhjT404_8z2vQw",

    # Movies
    "CineFix": "UCKy1dAqELo0zrOtPkf0eTMw"
}


BASE_URL = "https://www.googleapis.com/youtube/v3/search"

# ======================
# SAFE DATA PATH
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(DATA_DIR, "videos_multi_raw.csv")

# ======================
# DATA COLLECTION
# ======================
all_videos = []

def fetch_channel_videos(channel_name, channel_id):
    print(f"\n📡 Fetching videos from: {channel_name}")
    next_page_token = None

    while True:
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": 50,
            "order": "date",
            "type": "video",
            "key": API_KEY,
            "pageToken": next_page_token
        }

        response = requests.get(BASE_URL, params=params).json()

        # -------- DEBUG --------
        print("API response keys:", response.keys())

        if "error" in response:
            print("❌ API ERROR:", response["error"])
            break

        if "items" not in response:
            print("❌ No items found in response")
            break

        for item in response["items"]:
            all_videos.append({
                "video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "publishedAt": item["snippet"]["publishedAt"],
                "channel_name": channel_name
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break


# ======================
# RUN EXTRACTION
# ======================
for name, cid in CHANNELS.items():
    fetch_channel_videos(name, cid)

print("\nTotal videos collected:", len(all_videos))

# ======================
# SAVE TO CSV
# ======================
if len(all_videos) == 0:
    print("❌ No videos collected. CSV will not be created.")
else:
    df = pd.DataFrame(all_videos)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Data saved to: {OUTPUT_PATH}")
    print("✅ Milestone 1 Completed Successfully")
