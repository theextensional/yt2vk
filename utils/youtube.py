import logging
import os
import sys

import feedparser
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.parse_url import parse_youtube_url  # noqa: 402
from utils.video import Video  # noqa: 402

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_channel_info(url: str) -> tuple[str, str] | None:
    """
    Функция получает URL-адрес канала на YouTube в виде строки и возвращает
    кортеж с идентификатором и именем канала в виде строк, если информация была
    успешно получена из HTML-кода страницы канала. В противном случае
    возвращается None.

    Аргументы:
    - url (str): URL-адрес канала на YouTube.

    Возвращает:
    - tuple[str, str] | None: кортеж из двух строк - идентификатор и имя канала,
    если информация была успешно получена, или None, если произошла ошибка при
    получении информации.
    """
    parsed_url = parse_youtube_url(url)
    if not parsed_url:
        return None

    response = requests.get(parsed_url)
    if not response.ok:
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    channel_id = soup.find("meta", {"itemprop": "channelId"})["content"]
    channel_name = soup.find("link", {"itemprop": "name"})["content"]

    return str(channel_id), str(channel_name)


def get_latest_video_data(channel_id: str) -> Video | None:
    """
    Получает идентификатор канала на YouTube в виде строки и возвращает информацию о последнем
    загруженном на канал видео в виде объекта Video, если информация была успешно получена из
    RSS-канала канала. Если произошла ошибка при получении информации или канал не содержит видео,
    функция возвращает None.

    Аргументы:
    - channel_id (str): Идентификатор канала на YouTube.

    Возвращает:
    - Video | None: Объект Video, содержащий информацию о последнем видео канала, если информация была успешно получена,
    или None, если произошла ошибка при получении информации или канал не содержит видео.
    """
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(url)

    if latest_video := feed.entries[0] if feed.entries else None:
        return Video(
            channel_id,
            latest_video["author"],
            latest_video["link"],
            latest_video["title"],
            latest_video["summary"],
            latest_video["published"],
        )
    return None


if __name__ == "__main__":
    with open("urls.txt", "r") as f:
        urls = f.readlines()

    for url in urls:
        channel_info = get_channel_info(url)
        if channel_info:
            channel_id, channel_name = channel_info
            latest_video = get_latest_video_data(channel_id)
            if latest_video:
                logging.info(f"Канал: {channel_name}, id: {channel_id}. Последнее видео: {latest_video.title}")
            else:
                logging.warning("Не удалось получить информацию о последнем видео.")
        else:
            logging.warning(f"Произошла ошибка при запросе {url}")
