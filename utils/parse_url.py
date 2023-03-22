import re


def parse_youtube_url(url_or_id):
    # Определение шаблонов URL для каналов, видео и пользователей
    channel_id_pattern = re.compile(r"^[a-zA-Z0-9_-]{24}$")
    channel_url_pattern = re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/channel/([a-zA-Z0-9_-]+)")
    video_url_pattern = re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/watch\?v=([a-zA-Z0-9_-]+)")
    video_id_pattern = re.compile(r"^[a-zA-Z0-9_-]{11}$")
    channel_name_pattern = re.compile(r"(?:(?:https?:)?//)?(?:www\.)?youtube.com/c/([^/\s?]+)")
    user_pattern = re.compile(r"^(?:https?:\/\/(?:www\.)?youtube\.com\/)?(?:@)?([a-zA-Z0-9_-]+)$")

    # Поиск совпадений в URL-адресе или ID
    channel_id_match = channel_id_pattern.search(url_or_id)
    channel_url_match = channel_url_pattern.search(url_or_id)
    video_url_match = video_url_pattern.search(url_or_id)
    video_id_match = video_id_pattern.search(url_or_id)
    channel_name_match = channel_name_pattern.search(url_or_id)
    user_match = user_pattern.search(url_or_id)

    # Определение типа данных и вывод информации
    if channel_id_match:
        return "channel_id", url_or_id
    elif channel_url_match:
        channel_id = channel_url_match.group(1)
        return "channel", channel_id
    elif video_url_match:
        video_id = video_url_match.group(1)
        return "video", video_id
    elif video_id_match:
        return "video", url_or_id
    elif channel_name_match:
        channel_name = channel_name_match.group(1)
        return "channel_name", channel_name
    elif user_match:
        user_name = user_match.group(1)
        return "user_name", user_name
    else:
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
