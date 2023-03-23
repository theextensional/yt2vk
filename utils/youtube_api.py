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
    url (str): URL-адрес или ID YouTube-видео, канала или пользователя.

    Возвращает:
    В случае успеха, кортеж из двух элементов: название канала и его идентификатор.
    В случае ошибки, возвращает `None`.
    """
    data = parse_youtube_url(url)

    if data is None:
        logging.warning(f"Некорректный URL для YouTube: {url}")
        return None

    if data[0] == "channel_id":
        response = YT.channels().list(part="snippet", id=data[1]).execute()
        channel_id = data[1]
    elif data[0] == "user_name" or data[0] == "channel_name":
        response = YT.search().list(type="channel", part="snippet", maxResults=1, q=data[1]).execute()
        channel_id = response.get("items", [{}])[0].get("id", {}).get("channelId")
    elif data[0] == "video_id":
        response = YT.videos().list(part="snippet", id=data[1]).execute()
        channel_id = response.get("items", [{}])[0].get("snippet", {}).get("channelId")
    else:
        return None

    channel_data = YT.channels().list(part="snippet", id=channel_id).execute().get("items", [{}])[0].get("snippet", {})
    channel_name = channel_data.get("title", "")
    return channel_id, channel_name


def get_latest_video_data(channel_id: str) -> dict[str, str] | None:
    """
    Получает данные о последнем видео на канале YouTube по его идентификатору.

    Аргументы:
    channel_id (строка) - идентификатор канала на YouTube.

    Возвращает:
    Словарь с данными о последнем видео на канале, включающий:
        - "video_id" (строка) - идентификатор видео на YouTube.
        - "title" (строка) - название видео.
        - "description" (строка) - описание видео.
        - "publish_time" (строка) - дата и время публикации видео на YouTube.

    Если произошла ошибка, функция возвращает `None`.
    """
    request = YT.search().list(part="snippet", channelId=channel_id, type="video", order="date", maxResults=1)

    try:
        response = request.execute()
        video_data = response["items"][0]["snippet"]
        return {
            "video_id": response["items"][0]["id"]["videoId"],
            "title": video_data["title"],
            "description": video_data["description"],
            "publish_time": video_data["publishedAt"],
        }
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None


def _test_get_channel_id_and_name():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    urls = [
        "https://www.youtube.com/@theextensional",
        "https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg",
        "https://www.youtube.com/c/Экстенсиональный",
        "https://youtu.be/dQw4w9WgXcQ",
    ]

    for url in urls:
        channel_info = get_channel_id_and_name(url)

        if channel_info:
            logging.info(f"Канал: {channel_info[0]}, id: {channel_info[1]}")
        else:
            logging.warning("Произошла ошибка при запросе.")


def _test_get_latest_video_data():
    ids = ["UCrV_cFYbUwpjSOPVJOjTufg", "UCuAXFkgsw1L7xaCfnd5JJOw"]
    (print(data) for id in ids if (data := get_latest_video_data(id)))


if __name__ == "__main__":
    _test_get_channel_id_and_name()
    _test_get_latest_video_data()
