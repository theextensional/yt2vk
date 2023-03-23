import re

REGEX_PATTERNS = {
    "channel_id": re.compile(r"^[a-zA-Z0-9_-]{24}$"),
    "channel_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/channel/([a-zA-Z0-9_-]+)"),
    "video_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)"),
    "video_id": re.compile(r"^[a-zA-Z0-9_-]{11}$"),
    "short_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtu.be/([a-zA-Z0-9_-]+)"),
    "channel_name": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/c/([^/\s?]+)"),
    "user_name": re.compile(r"^(?:https?:\/\/(?:www\.)?youtube\.com\/)?(?:@)?([a-zA-Z0-9_-]+)$"),
}


def parse_youtube_url(url_or_id: str) -> tuple[str, str] | None:
    """
    Функция для извлечения информации из URL-адреса YouTube.

    Аргументы:
    url_or_id (str): URL-адрес или ID YouTube-видео, канала или пользователя.

    Возвращает:
    tuple: Кортеж с типом данных и соответствующим значением. Возможные типы данных:
        - "video_id" (ID видео);
        - "channel_id" (ID канала);
        - "user_name" (имя пользователя);
        - "channel_name" (название канала).

    Возвращает `None`, если переданный URL-адрес не соответствует шаблонам.

    Пример использования:
    >>> parse_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    ('video_id', 'dQw4w9WgXcQ')
    >>> parse_youtube_url("https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg")
    ('channel_id', 'UCrV_cFYbUwpjSOPVJOjTufg')
    >>> parse_youtube_url("@theextensional")
    ('user_name', 'theextensional')
    """
    for data_type, pattern in REGEX_PATTERNS.items():
        if match := pattern.match(url_or_id):
            if data_type == "channel_url":
                return "channel_id", match.group(1)
            elif data_type == "channel_id":
                return data_type, url_or_id
            elif data_type == "video_url" or data_type == "short_url":
                return "video_id", match.group(1)
            else:
                return data_type, match.group(1)
    return None


if __name__ == "__main__":
    urls = [
        "https://www.youtube.com/@theextensional",  # пользователь
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # видео ID
        "https://youtu.be/dQw4w9WgXcQ",  # видео ID
        "https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg",  # канал ID
        "https://www.youtube.com/c/Экстенсиональный",  # название канала
        "UCrV_cFYbUwpjSOPVJOjTufg",  # канал ID
        "@theextensional",  # пользователь
        "https://www.google.com/",  # некорректный URL
    ]

    for url in urls:
        parsed_data = parse_youtube_url(url)
        if parsed_data is None:
            print(f"URL: {url}, Ошибка: некорректный URL")
        else:
            data_type, data = parsed_data
            print(f"URL: {url}, Тип данных: {data_type}, Данные: {data}")
