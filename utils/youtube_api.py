import os

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from parse_url import parse_youtube_url

load_dotenv()

API_KEY = os.getenv("API_KEY")
YT = build("youtube", "v3", developerKey=API_KEY)


def get_channel_info(url: str) -> tuple[str, str] | None:
    data_type, data = parse_youtube_url(url)

    try:
        if data_type == "channel_id":
            response = YT.channels().list(part="snippet", id=data).execute()
            if response:
                channel_name = response["items"][0]["snippet"]["title"]
                return data, channel_name
            else:
                return None
        elif data_type == "user_name":
            response = YT.search().list(type="channel", part="snippet", maxResults=1, q=data).execute()
            if response and "items" in response and len(response["items"]) > 0:
                channel_id = response["items"][0]["id"]["channelId"]
                response = YT.channels().list(part="snippet", id=channel_id).execute()
                if response:
                    channel_name = response["items"][0]["snippet"]["title"]
                    return channel_id, channel_name
                else:
                    return None
            else:
                return None
        elif data_type == "video_id":
            response = YT.videos().list(part="snippet", id=data).execute()
            if response and "items" in response and len(response["items"]) > 0:
                channel_id = response["items"][0]["snippet"]["channelId"]
                response = YT.channels().list(part="snippet", id=channel_id).execute()
                if response:
                    channel_name = response["items"][0]["snippet"]["title"]
                    return channel_id, channel_name
                else:
                    return None
            else:
                return None
        else:
            return None
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    url = "https://www.youtube.com/@theextensional"
    url = "https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg"
    url = "https://youtu.be/dQw4w9WgXcQ"
    channel_info = get_channel_info(url)

    if channel_info:
        print(f"Канал: {channel_info}")
    else:
        print("Произошла ошибка при запросе.")
