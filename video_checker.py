from datetime import datetime

from utils.database_utils import get_subscriptions, update_last_video_date
from utils.youtube_api import get_latest_video_data


def check_new_videos() -> None:
    """
    Проверяет наличие новых видео на каждом канале в базе данных подписок.
    Если есть новое видео, то выводит сообщение в консоль и обновляет дату последнего видео в базе данных.

    :return: None
    """
    for channel in get_subscriptions():
        channel_id, channel_name, last_video_date = channel
        latest_video = get_latest_video_data(channel_id)
        if not latest_video:
            continue

        publish_time_dt = datetime.strptime(latest_video["publish_time"], "%Y-%m-%dT%H:%M:%SZ")
        last_video_date_dt = datetime.strptime(last_video_date, "%Y-%m-%d %H:%M:%S")
        if publish_time_dt > last_video_date_dt:
            video_url = f"https://youtu.be/{latest_video['video_id']}"
            print(f"New video on {channel_name}: {video_url}")
            update_last_video_date(channel_id, publish_time_dt.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    check_new_videos()
