from dataclasses import dataclass


@dataclass
class MediaPack:
    images: list[str]


class MediaService:

    def get_images(self, item_id: int) -> MediaPack:
        # заглушка под будущий CDN / AI images / backend
        return MediaPack(
            images=[
                f"https://picsum.photos/seed/{item_id}/600/400",
                f"https://picsum.photos/seed/{item_id+1}/600/400",
                f"https://picsum.photos/seed/{item_id+2}/600/400",
            ]
        )
