import logging
import sqlite3

from utils.youtube_api import get_channel_id_and_name

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def add_to_database(db_conn: sqlite3.Connection, url: str):
    """
    Добавляет в базу данных новую строку с информацией о видео, канале или пользователе YouTube.

    Аргументы:
    db_conn (sqlite3.Connection): Объект подключения к базе данных.
    url (str): URL-адрес или ID YouTube-видео, канала или пользователя.
    """
    # Извлекаем ID и название канала или видео ID
    result = get_channel_id_and_name(url)
    if result is None:
        logging.warning(f'Не удалось получить информацию о канале для URL-адреса "{url}".')
        return
    channel_id, channel_name = result

    # Проверяем, существует ли уже запись с таким channel_id
    cursor = db_conn.cursor()
    cursor.execute("SELECT channel_id FROM youtube_data WHERE channel_id = ?", (channel_id,))
    existing_record = cursor.fetchone()
    if existing_record:
        logging.info(f'Запись с channel_id "{channel_id}" уже существует в базе данных.')
        return

    # Проверяем, что значения channel_id и channel_name не пустые
    if not channel_id or not channel_name:
        logging.error(f'Не удалось получить ID или название канала для URL-адреса "{url}".')
        return

    # Сохраняем данные в базу данных
    cursor.execute("INSERT INTO youtube_data (channel_id, channel_name) VALUES (?, ?)", (channel_id, channel_name))
    db_conn.commit()
    logging.info(f'Данные для канала "{channel_name}" успешно добавлены в базу данных.')


if __name__ == "__main__":
    # Создаем подключение к базе данных
    db_conn = sqlite3.connect("db.sqlite3")

    # Список URL-адресов для добавления в базу данных
    urls = [
        "https://www.youtube.com/@theextensional",  # пользователь
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # видео
        "https://youtu.be/dQw4w9WgXcQ",  # видео
        "https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg",  # канал ID
        "https://www.youtube.com/c/Экстенсиональный",  # название канала
        "UCrV_cFYbUwpjSOPVJOjTufg",  # канал ID
        "@theextensional",  # пользователь
        "https://www.google.com/",  # некорректный URL
    ]

    with db_conn:
        # Создаем таблицу, если она не существует
        db_conn.execute(
            "CREATE TABLE IF NOT EXISTS youtube_data ("
            "channel_id TEXT PRIMARY KEY,"
            "channel_name TEXT,"
            "last_video_date DATETIME DEFAULT NULL"
            ")"
        )

        # Обрабатываем каждый URL и добавляем его в базу данных
        for url in urls:
            add_to_database(db_conn, url)

    # Закрываем подключение к базе данных
    db_conn.close()
