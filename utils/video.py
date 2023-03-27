from dataclasses import dataclass


@dataclass
class Video:
    channel_id: str
    channel_name: str
    link: str
    title: str | None
    description: str | None
    published: str

    def __repr__(self) -> str:
        return (
            f"Video(channel_name={self.channel_name}, link={self.link}, title={self.title}, published={self.published})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Video):
            return False
        return (
            self.channel_name == other.channel_name
            and self.link == other.link
            and self.title == other.title
            and self.published == other.published
        )
