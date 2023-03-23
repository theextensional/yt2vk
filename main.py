import time

from video_checker import check_new_videos

CHECK_INTERVAL = 300


def main():
    """
    Запускает бесконечный цикл для проверки наличия новых видео.
    Вызывает функцию check_new_videos() в теле цикла и задерживается на CHECK_INTERVAL секунд.

    :return: None
    """
    while True:
        check_new_videos()
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
