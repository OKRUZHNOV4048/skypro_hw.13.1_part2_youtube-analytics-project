import json
import os

from googleapiclient.discovery import build


class Channel:
    """
    Класс YouTube-канала
    """
    api_key: str = os.getenv('YT_API_KEY')  # Копирует YT_API_KEY из Google и добавляет к переменным окружения.
    youtube = build('youtube', 'v3', developerKey=api_key)  # Создает специальный объект для работы с YouTube API.

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с YouTube API
        """
        return cls.youtube

    def __init__(self, __channel_id: str) -> None:
        """
        Экземпляр инициализируется через передачу в аргумент __init__ id канала.
        Дальше все данные будут подтягиваться через API."""
        self.__channel_id = __channel_id
        channel = Channel.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = channel["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.subscriber_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.view_count = channel["items"][0]["statistics"]["viewCount"]

    @property
    def channel_id(self):
        """
        Геттер для атрибута channel_id
        """
        return self.__channel_id

    def print_info(self) -> None:
        """
        Выводит информацию о YouTube-канале
        """
        channel = Channel.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        info = json.dumps(channel, indent=2, ensure_ascii=False)
        print(info)

    def to_json(self, file_name):
        """
        Записывает в файл значения атрибутов экземпляра класса YouTube-канала Channel
        """
        youtube_channel_dict = {"id": self.channel_id, "title": self.title, "description": self.description,
                                "url": self.url, "subscriber_count": self.subscriber_count,
                                "video_count": self.video_count, "view_count": self.view_count}
        with open(file_name, 'w', encoding="UTF-8") as file:
            json.dump(youtube_channel_dict, file, indent=2, ensure_ascii=False)
