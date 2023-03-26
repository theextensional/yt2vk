from datetime import datetime, timezone

from utils.database_utils import get_subscriptions, update_last_video_date
from utils.youtube import get_latest_video_data


def check_new_videos() -> None:
    """
    Проверяет наличие новых видео на каждом канале в базе данных подписок.
    Если есть новое видео, то выводит сообщение в консоль и обновляет дату последнего видео в базе данных.

    :return: None
    """
    subscriptions = get_subscriptions()

    if not subscriptions:
        print("Запустите add_to_database.py, чтобы добавить первые записи в базу данных.")
        exit(1)

    for channel in subscriptions:
        channel_id, channel_name, last_video_date = channel
        latest_video = get_latest_video_data(channel_id)
        if not latest_video:
            continue

        publish_time_dt = (
            datetime.strptime(latest_video["published"], "%Y-%m-%dT%H:%M:%S%z")
            .astimezone(timezone.utc)
            .replace(tzinfo=None)
        )
        last_video_date_dt = datetime.strptime(last_video_date, "%Y-%m-%d %H:%M:%S")

        if publish_time_dt > last_video_date_dt:
            print(f"New video on {channel_name}: {latest_video['link']}")
            update_last_video_date(channel_id, publish_time_dt.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{nowtime}] No new video on {channel_name}")


if __name__ == "__main__":
    check_new_videos()