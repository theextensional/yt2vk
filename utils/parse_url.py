import re


class InvalidYoutubeUrlException(Exception):
    pass


REGEX_PATTERNS = {
    "channel_id": re.compile(r"^[a-zA-Z0-9_-]{24}$"),
    "channel_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/channel/([a-zA-Z0-9_-]+)"),
    "video_url": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/watch\?v=([a-zA-Z0-9_-]+)"),
    "video_id": re.compile(r"^[a-zA-Z0-9_-]{11}$"),
    "channel_name": re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/c/([^/\s?]+)"),
    "user_name": re.compile(r"^(?:https?:\/\/(?:www\.)?youtube\.com\/)?(?:@)?([a-zA-Z0-9_-]+)$"),
}


def parse_youtube_url(url_or_id):
    for data_type, pattern in REGEX_PATTERNS.items():
        if match := pattern.search(url_or_id):
            if data_type == "channel_url":
                return "channel_id", match.group(1)
            elif data_type == "channel_id":
                return data_type, url_or_id
            else:
                return data_type, match.group(1)
    raise InvalidYoutubeUrlException("Некорректный URL для YouTube")


if __name__ == "__main__":
    urls = [
        "https://www.youtube.com/@theextensional",  # пользователь
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # видео
        "https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg",  # канал ID
        "https://www.youtube.com/c/Экстенсиональный",  # название канала
        "UCrV_cFYbUwpjSOPVJOjTufg",  # канал ID
        "@theextensional",  # пользователь
        "https://www.google.com/",  # некорректный URL
    ]

    for url in urls:
        try:
            data_type, data = parse_youtube_url(url)
            print(f"URL: {url}, Тип данных: {data_type}, Данные: {data}")
        except InvalidYoutubeUrlException as e:
            print(f"URL: {url}, Ошибка: {e}")
