import logging
import os
import sqlite3

from dotenv import load_dotenv

from utils.database_utils import create_subscriptions_table
from utils.youtube import get_channel_info

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

load_dotenv()
DATABASE_URL = str(os.getenv("DATABASE_URL"))
if DATABASE_URL is None:
    raise ValueError("Not set DATABASE_URL в файле .env")


def check_channel_exists(db_conn: sqlite3.Connection, channel_id: str) -> bool:
    """
    Проверяет, существует ли уже запись с таким channel_id.

    Аргументы:
        `db_conn` (sqlite3.Connection): Объект подключения к базе данных.
        `channel_id` (str): ID YouTube-канала.

    Возвращает:
        `bool`: Флаг, указывающий, существует ли уже запись с таким `channel_id`.
    """
    cursor = db_conn.cursor()
    cursor.execute("SELECT channel_id FROM subscriptions WHERE channel_id = ?", (channel_id,))
    return bool(cursor.fetchone())


def add_to_database(db_conn: sqlite3.Connection, urls: str | list[str]) -> None:
    """
    Добавляет в базу данных новые строки с информацией о видео, канале или пользователе YouTube.

    Аргументы:
        `db_conn` (sqlite3.Connection): Объект подключения к базе данных.
        `urls` (str | list[str]): URL-адрес или список URL-адресов YouTube-видео, канала или пользователя.
    """
    urls = [urls] if isinstance(urls, str) else urls

    try:
        channel_info = [info for info in [get_channel_info(url) for url in urls] if info is not None]
        if not channel_info:
            logging.warning("Не удалось получить ID или название каналов.")
            return

        existing_channels = [channel_id for channel_id, _ in channel_info if check_channel_exists(db_conn, channel_id)]

        new_channel_info = [
            (channel_id, channel_name)
            for channel_id, channel_name in channel_info
            if channel_id not in existing_channels
        ]

        if not new_channel_info:
            logging.warning("Не удалось получить информацию о каналах.")
            return

        cursor = db_conn.cursor()
        cursor.executemany(
            "INSERT OR IGNORE INTO subscriptions (channel_id, channel_name) VALUES (?, ?)",
            new_channel_info,
        )
        db_conn.commit()

        for _, channel_name in new_channel_info:
            logging.info(f'Данные для канала "{channel_name}" успешно добавлены в базу данных.')

        for channel_id in existing_channels:
            logging.info(f'Запись с channel_id "{channel_id}" уже существует в базе данных.')
    except Exception as e:
        logging.error(f"Ошибка при добавлении данных: {e}")


def first_run():
    with sqlite3.connect(DATABASE_URL) as db_conn:
        create_subscriptions_table()

        with open("urls.txt", "r") as f:
            urls = f.readlines()

        add_to_database(db_conn, urls)


if __name__ == "__main__":
    first_run()
