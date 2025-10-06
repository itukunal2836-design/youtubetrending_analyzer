from googleapiclient.discovery import build
import pandas as pd

API_KEY = "YOUR_API_KEY_HERE"

youtube = build('youtube', 'v3', developerKey=API_KEY)

# Request trending videos
request = youtube.videos().list(
    part="snippet,statistics,contentDetails",
    chart="mostPopular",
    regionCode="IN",   # Change this to your country code
    maxResults=50
)
response = request.execute()

# Extract data
videos = []
for item in response["items"]:
    video_data = {
        "title": item["snippet"]["title"],
        "channel": item["snippet"]["channelTitle"],
        "category_id": item["snippet"]["categoryId"],
        "publish_time": item["snippet"]["publishedAt"],
        "views": int(item["statistics"].get("viewCount", 0)),
        "likes": int(item["statistics"].get("likeCount", 0)),
        "comments": int(item["statistics"].get("commentCount", 0)),
        "duration": item["contentDetails"]["duration"],
    }
    videos.append(video_data)

# Save to CSV
df = pd.DataFrame(videos)
df.to_csv("youtube_trending.csv", index=False)
print("✅ Data saved to youtube_trending.csv")
print(df.head())
