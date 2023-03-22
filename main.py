import os
import time
from datetime import datetime, timedelta

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables from .env file
load_dotenv()

# Set API key and channel ID from environment variables
DEVELOPER_KEY = os.getenv("API_KEY")
CHANNEL_ID = "user/theextensional"

# установка параметров запроса к API
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# количество секунд между проверками наличия нового видео
CHECK_INTERVAL = 60

# создание объекта YouTube API
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# определение даты, начиная с которой будем проверять новые видео
today = datetime.utcnow()
start_date = (today - timedelta(days=70)).strftime("%Y-%m-%dT%H:%M:%SZ")
print(start_date)

try:
    # отправка запроса на получение списка новых видео на канале
    search_response = youtube.search().list(type="channel", part="snippet", maxResults=1, q="@theextensional").execute()

    # проверка наличия новых видео
    if len(search_response.get("items", [])) > 0:
        print(search_response["items"][0]["id"]["channelId"])
    #     print("New video found!")
    #     video_id = search_response["items"][0]["id"]["videoId"]
    #     video_url = f"https://www.youtube.com/watch?v={video_id}"
    #     print(video_url)

    # # обновление даты начала проверки наличия новых видео
    # today = datetime.utcnow()
    # start_date = today.strftime("%Y-%m-%dT%H:%M:%SZ")

except HttpError as error:
    print(f"An error occurred: {error}")

# # определение и проверка новых видео
# while True:
#     try:
#         # отправка запроса на получение списка новых видео на канале
#         search_response = youtube.search().list(
#             channelId=CHANNEL_ID,
#             type='video',
#             part='id,snippet',
#             maxResults=1,
#             publishedAfter=start_date
#         ).execute()

#         # проверка наличия новых видео
#         if len(search_response.get("items", [])) > 0:
#             print("New video found!")
#             video_id = search_response["items"][0]["id"]["videoId"]
#             video_url = f"https://www.youtube.com/watch?v={video_id}"
#             print(video_url)

#         # обновление даты начала проверки наличия новых видео
#         today = datetime.utcnow()
#         start_date = today.strftime('%Y-%m-%dT%H:%M:%SZ')

#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         break

#     # задержка перед следующей проверкой наличия новых видео
#     time.sleep(CHECK_INTERVAL)
