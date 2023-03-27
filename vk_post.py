import logging
import os

import requests
import vk_api
from dotenv import load_dotenv

from utils.video import Video

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

load_dotenv()
VK_ACCESS_TOKEN: str | None = os.getenv("VK_ACCESS_TOKEN")
if VK_ACCESS_TOKEN is None:
    raise ValueError("Не задан токен VK_ACCESS_TOKEN в файле .env")
VK_GROUP_ID: str | int | None = os.getenv("VK_GROUP_ID")
if VK_GROUP_ID is None:
    raise ValueError("Не задан ID группы VK_GROUP_ID в файле .env")

vk_session = vk_api.VkApi(token=VK_ACCESS_TOKEN)
vk = vk_session.get_api()


def post_to_group(videos: list[Video], group_id: str | int = VK_GROUP_ID) -> None:
    """
    Публикует сообщение на стене группы ВКонтакте.

    Аргументы:
        - `videos` (List[Video]): список объектов Video, которые нужно опубликовать на стене группы.
        - `group_id` (str | int): идентификатор группы, на стене которой будет опубликовано сообщение.
                По умолчанию используется значение `VK_GROUP_ID` из файла `.env`.

    Результат:
        `None`.

    Если список видео пустой, функция ничего не делает.
    """
    if not videos:
        return

    for video in videos:
        message = f"Новое видео на канале {video.channel_name}:"
        message = f"{message}\n\n{video.description}" if video.description else message
        uploaded_video = vk.video.save(wallpost=1, description=message, link=video.link, group_id=group_id)
        requests.post(uploaded_video["upload_url"])
        logging.info("Сообщение опубликовано на стене группы")


if __name__ == "__main__":
    new_video = Video(
        channel_id="UCrV_cFYbUwpjSOPVJOjTufg",
        channel_name="Экстенсиональный",
        description=(
            "Заинтересованы найти друзей, которые будут работать над "
            "достижением общих целей и миссии? Присоединяйтесь к нам и вместе мы определим наши приоритеты и способы "
            "реализации. Мы будем использовать наши ресурсы и силы для достижения конкретных результатов. "
            "Присоединяйтесь к нашему сообществу, чтобы сделать наш мир лучше!"
            "\n\nПрисоединяйтесь в Discord: https://discord.gg/sYEGrjz6Fp"
        ),
        link="https://www.youtube.com/watch?v=2N20P3Kfgso",
        published="2023-03-27 11:15:44",
        title="",
    )
    post_to_group([new_video])
