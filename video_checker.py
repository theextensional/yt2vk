import logging
from datetime import datetime, timezone

from utils.database_utils import get_subscriptions, update_last_video_date
from utils.video import Video
from utils.youtube import get_latest_video_data


def check_new_videos() -> list[Video]:
    """
    Проверяет базу данных подписок на наличие новых видео. Если есть новое видео, выводит сообщение в консоль и
    обновляет дату последнего видео в базе данных.

    Возвращает: Список объектов Video, содержащих информацию о новых видео.
    """
    new_videos = []
    logging.basicConfig(level=logging.INFO)

    for channel_id, channel_name, last_video_date in get_subscriptions():
        if latest_video := get_latest_video_data(channel_id):
            publish_time_dt = datetime.fromisoformat(latest_video.published).astimezone(timezone.utc)
            last_video_date_dt = datetime.fromisoformat(last_video_date).astimezone(timezone.utc)

            if publish_time_dt > last_video_date_dt:
                logging.info(
                    f"Новое видео на канале {channel_name}: {latest_video.title} {latest_video.link} "
                    f"({publish_time_dt:%d.%m.%Y %H:%M:%S} UTC)"
                )
                update_last_video_date(channel_id, publish_time_dt.isoformat())
                new_videos.append(latest_video)

    return new_videos


if __name__ == "__main__":
    check_new_videos()
