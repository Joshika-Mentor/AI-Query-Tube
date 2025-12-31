from youtube_transcript_api import YouTubeTranscriptApi
import sys

vid = "n_MVhE63ZQQ" # Karpathy GPT
try:
    print(f"Fetching {vid}...")
    api = YouTubeTranscriptApi()
    # Try .fetch()
    transcript_obj = api.fetch(vid, languages=['en', 'en-US'])
    print(f"Type: {type(transcript_obj)}")
    if hasattr(transcript_obj, 'fetch'):
       # It might be a Transcript object?
       data = transcript_obj.fetch()
    else:
       # Maybe it IS the data?
       # The doc said "fetch(...) -> FetchedTranscript"
       # Let's inspect it
       print(f"Dir: {dir(transcript_obj)}")
       data = transcript_obj # Placeholder
       
    # If it is iterable/list-like?
    try:
        print(f"First item: {transcript_obj[0]}")
        data = transcript_obj
    except:
        pass

    print("Success!")
except Exception as e:
    print(f"Error: {e}")
