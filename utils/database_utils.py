import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = str(os.getenv("DATABASE_URL"))


def update_last_video_date(channel_id, new_date) -> None:
    """
    Обновляет дату последнего видео для заданного канала.

    Аргументы:
    - `channel_id` - идентификатор YouTube-канала (строка)
    - `new_date` - новая дата последнего видео в формате "YYYY-MM-DD HH:MM:SS" (строка)
    """
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        query = "UPDATE subscriptions SET last_video_date = ? WHERE channel_id = ?"
        cursor.execute(query, (new_date, channel_id))
        conn.commit()


def get_subscriptions() -> list[tuple[str, str, str]]:
    """
    Возвращает список подписок в базе данных.

    Результатом является список кортежей, содержащих следующие поля:
    - `channel_id` - идентификатор YouTube-канала (строка)
    - `channel_name` - название канала (строка)
    - `last_video_date` - дата последнего видео в формате "YYYY-MM-DD HH:MM:SS" (строка)
    """
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        query = "SELECT channel_id, channel_name, last_video_date FROM subscriptions"
        cursor.execute(query)
        return cursor.fetchall()


if __name__ == "__main__":
    # Обновляем дату последнего видео
    update_last_video_date("UCrV_cFYbUwpjSOPVJOjTufg", "2023-03-19 21:31:10")
