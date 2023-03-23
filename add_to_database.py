import logging
import sqlite3

from utils.youtube_api import get_channel_id_and_name

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def check_channel_exists(db_conn: sqlite3.Connection, channel_id: str) -> bool:
    """
    Проверяет, существует ли уже запись с таким channel_id.

    Аргументы:
    db_conn (sqlite3.Connection): Объект подключения к базе данных.
    channel_id (str): ID YouTube-канала.

    Возвращает:
    bool: Флаг, указывающий, существует ли уже запись с таким channel_id.
    """
    cursor = db_conn.cursor()
    cursor.execute("SELECT channel_id FROM subscriptions WHERE channel_id = ?", (channel_id,))
    existing_record = cursor.fetchone()
    return bool(existing_record)


def add_to_database(db_conn: sqlite3.Connection, url: str) -> None:
    """
    Добавляет в базу данных новую строку с информацией о видео, канале или пользователе YouTube.

    Аргументы:
    db_conn (sqlite3.Connection): Объект подключения к базе данных.
    url (str): URL-адрес или ID YouTube-видео, канала или пользователя.
    """
    result = get_channel_id_and_name(url)
    if result is None:
        logging.warning(f'Не удалось получить информацию о канале для URL-адреса "{url}".')
        return
    channel_id, channel_name = result

    if check_channel_exists(db_conn, channel_id):
        logging.info(f'Запись с channel_id "{channel_id}" уже существует в базе данных.')
        return

    if not channel_id or not channel_name:
        logging.error(f'Не удалось получить ID или название канала для URL-адреса "{url}".')
        return

    cursor = db_conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO subscriptions (channel_id, channel_name) VALUES (?, ?)", (channel_id, channel_name)
    )
    db_conn.commit()
    logging.info(f'Данные для канала "{channel_name}" успешно добавлены в базу данных.')


def main():
    import os

    from dotenv import load_dotenv

    load_dotenv()
    DATABASE_URL = str(os.getenv("DATABASE_URL"))

    with sqlite3.connect(DATABASE_URL) as db_conn:
        db_conn.execute(
            "CREATE TABLE IF NOT EXISTS subscriptions ("
            "channel_id TEXT PRIMARY KEY,"
            "channel_name TEXT,"
            "last_video_date DATETIME DEFAULT (datetime('now'))"
            ")"
        )

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
            add_to_database(db_conn, url)


if __name__ == "__main__":
    main()
