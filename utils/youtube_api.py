import logging
import os
import sys

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.parse_url import parse_youtube_url  # noqa: 402

load_dotenv()

API_KEY = os.getenv("API_KEY")
YT = build("youtube", "v3", developerKey=API_KEY)


def get_channel_id_and_name(url: str) -> tuple[str, str] | None:
    """
    Возвращает информацию о канале YouTube по его URL.

    Аргументы:
    url -- URL канала YouTube в виде строки.

    Возвращает:
    В случае успеха, кортеж из двух элементов: название канала и его идентификатор.
    В случае ошибки, возвращает None.
    """
    data = parse_youtube_url(url)

    if data is None:
        logging.warning(f"Некорректный URL для YouTube: {url}")
        return None

    try:
        if data[0] == "channel_id":
            response = YT.channels().list(part="snippet", id=data[1]).execute()
            channel_id = data[1]
        elif data[0] == "user_name":
            response = YT.search().list(type="channel", part="snippet", maxResults=1, q=data[1]).execute()
            channel_id = response.get("items", [{}])[0].get("id", {}).get("channelId")
        elif data[0] == "video_id":
            response = YT.videos().list(part="snippet", id=data[1]).execute()
            channel_id = response.get("items", [{}])[0].get("snippet", {}).get("channelId")
        else:
            return None

        channel_data = (
            YT.channels().list(part="snippet", id=channel_id).execute().get("items", [{}])[0].get("snippet", {})
        )
        channel_name = channel_data.get("title", "")
        return channel_id, channel_name
    except HttpError as e:
        logging.error(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    urls = [
        "https://www.youtube.com/@theextensional",
        "https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg",
        "https://youtu.be/dQw4w9WgXcQ",
    ]

    for url in urls:
        channel_info = get_channel_id_and_name(url)

        if channel_info:
            logging.info(f"Канал: {channel_info[0]}, id: {channel_info[1]}")
        else:
            logging.warning("Произошла ошибка при запросе.")
