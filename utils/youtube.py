import logging
import os
import sys

import feedparser
import requests
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.parse_url import parse_youtube_url  # noqa: 402

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def get_channel_info(url: str) -> tuple[str, str] | None:
    channel_id = None
    channel_name = None

    # Parse the YouTube URL
    parsed_url = parse_youtube_url(url)
    if not parsed_url:
        return None

    # Send a request to get HTML code of channel page
    response = requests.get(parsed_url)

    # Check if the response is a success
    if not response.ok:
        return None

    # Create a Beautiful Soup object for parsing HTML code
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the element with the channel ID in the HTML code
    channel_id = soup.find("meta", {"itemprop": "channelId"})["content"]

    # Find the element with the channel name in the HTML code
    channel_name = soup.find("link", {"itemprop": "name"})["content"]

    # Return the channel ID and name as a tuple
    return str(channel_id), str(channel_name)


def get_latest_video_data(channel_id: str) -> dict[str, str] | None:
    url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + channel_id
    feed = feedparser.parse(url)
    # Извлечение информации о новых видео
    if feed.entries:
        latest_video = feed.entries[0]
        return {
            "title": latest_video.get("title", ""),
            "link": latest_video.get("link", ""),
            "published": latest_video.get("published", ""),
            "description": latest_video.get("description", ""),
        }


if __name__ == "__main__":
    urls = [
        "https://www.youtube.com/@theextensional",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg",
        "https://www.youtube.com/c/Экстенсиональный",
        "UCrV_cFYbUwpjSOPVJOjTufg",
        "@theextensional",
        "https://www.google.com/",
    ]
    for url in urls:
        channel_info = get_channel_info(url)
        if channel_info:
            channel_id, channel_name = channel_info
            latest_video = get_latest_video_data(channel_id)
            if latest_video:
                logging.info(f"Канал: {channel_name}, id: {channel_id}. Последнее видео: {latest_video['title']}")
            else:
                logging.warning("Не удалось получить информацию о последнем видео.")
        else:
            logging.warning("Произошла ошибка при запросе.")
