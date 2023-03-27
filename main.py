import logging
import time

from video_checker import check_new_videos
from vk_post import post_to_group

CHECK_INTERVAL = 60

logging.basicConfig(level=logging.INFO)


def main():
    """Запускает бесконечный цикл для проверки наличия новых видео."""
    try:
        while True:
            post_to_group(check_new_videos())
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("Всего хорошего!")


if __name__ == "__main__":
    main()
