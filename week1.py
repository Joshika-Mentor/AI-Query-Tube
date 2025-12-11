!pip install requests pandas #panda library installations


#importing pandas with api key and channel id
import requests
import pandas as pd

API_KEY = "AIzaSyAUueJtpbgNovyq-7oQsFWJ64zWJPc2z2w"
CHANNEL_ID = "UCWv7vMbMWH4-V0ZXdmDpPBA"

url = "https://www.googleapis.com/youtube/v3/search"
params = {
    "key": "AIzaSyAUueJtpbgNovyq-7oQsFWJ64zWJPc2z2w",
    "channelId":"UCWv7vMbMWH4-V0ZXdmDpPBA" ,
    "part": "snippet,id",
    "order": "date",
    "maxResults": 50
}

response = requests.get(url, params=params).json()

videos = []
for item in response["items"]:
    if "videoId" in item["id"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        published = item["snippet"]["publishedAt"]
        videos.append([video_id, title, published])

df = pd.DataFrame(videos, columns=["video_id", "title", "published_date"])
df.head()

#csv 
df.to_csv("youtube_metadata.csv", index=False)

