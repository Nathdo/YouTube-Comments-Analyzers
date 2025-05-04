import re
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
load_dotenv()

YOUTUBE_API_KEY = os.getenv('YouTube_API_KEY')

def extract_video_id(url):
    match = re.search(r"v=([^&]+)", url)
    if not match:
        match = re.search(r"youtu\.be/([^?&]+)", url)
    return match.group(1) if match else None

def get_comments_from_url(url):
    video_id = extract_video_id(url)
    if not video_id:
        return []

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=50,
        textFormat="plainText"
    )
    response = request.execute()
    return [item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response.get('items', [])]

def get_video_info(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()

    if response["items"]:
        snippet = response["items"][0]["snippet"]
        title = snippet.get("title", "Unknown Title")
        thumbnail_url = snippet.get("thumbnails", {}).get("default", {}).get("url", "")
        return title, thumbnail_url
    return "Unknown Title", ""
