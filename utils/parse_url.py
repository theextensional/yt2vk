import re


def parse_youtube_url(url_or_id):
    # Определение шаблонов URL для каналов, видео и пользователей
    patterns = [
        (re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/channel/([a-zA-Z0-9_-]+)"), "channel"),
        (re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/watch\?v=([a-zA-Z0-9_-]+)"), "video"),
        (re.compile(r"^[a-zA-Z0-9_-]{11}$"), "video"),
        (re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/c/([^/\s?]+)"), "channel_name"),
        (re.compile(r"^(?:https?:\/\/(?:www\.)?youtube\.com\/)?(?:@)?([a-zA-Z0-9_-]+)$"), "user_name"),
        (re.compile(r"^[a-zA-Z0-9_-]{24}$"), "channel_id"),
    ]

    # Поиск совпадений в URL-адресе или ID
    for pattern, data_type in patterns:
        match = pattern.search(url_or_id)
        if match:
            return data_type, match.group(1)

    return None, None


if __name__ == "__main__":
    # Пример использования
    url = "https://www.youtube.com/@theextensional"
    data_type, data = parse_youtube_url(url)
    print(data_type, data)

    url = "https://www.youtube.com/channel/UCrV_cFYbUwpjSOPVJOjTufg"
    data_type, data = parse_youtube_url(url)
    print(data_type, data)

    url = "https://www.youtube.com/c/Экстенсиональный"
    data_type, data = parse_youtube_url(url)
    print(data_type, data)

    url = "UCrV_cFYbUwpjSOPVJOjTufg"
    data_type, data = parse_youtube_url(url)
    print(data_type, data)

    url = "@theextensional"
    data_type, data = parse_youtube_url(url)
    print(data_type, data)
