import logging
import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = str(os.getenv("DATABASE_URL"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


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

    logging.info(f"Обновлена дата последнего видео для канала {channel_id}: {new_date}")


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
        try:
            query = "SELECT channel_id, channel_name, last_video_date FROM subscriptions"
            cursor.execute(query)
        except sqlite3.OperationalError:
            print("Запустите add_to_database.py, чтобы добавить первые записи в базу данных.")
            exit(1)
        return cursor.fetchall()


def create_subscriptions_table() -> None:
    """
    Создает таблицу подписок в базе данных, если она не существует.
    """
    print("Создание таблицы подписок...")
    with sqlite3.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS subscriptions ("
            "channel_id TEXT PRIMARY KEY,"
            "channel_name TEXT,"
            "last_video_date DATETIME DEFAULT (datetime('now'))"
            ")"
        )
        conn.commit()


if __name__ == "__main__":
    # Создаем таблицу подписок, если она не существует
    create_subscriptions_table()
    # Обновляем дату последнего видео
    update_last_video_date("UCrV_cFYbUwpjSOPVJOjTufg", "2023-03-19 21:31:10")
