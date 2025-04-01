import requests


class ImageProviderClient:
    def __init__(self, provider_url: str):
        self.provider_url = provider_url.rstrip("/")

    def get_image(self, img_id: int, timeout_secs: float = 5.0) -> bytes | str:
        url = f"{self.provider_url}/{img_id}"
        try:
            response = requests.get(url, timeout=timeout_secs)
            response.raise_for_status()
            return response.content
        except requests.exceptions.Timeout as ex:
            return f"Error while getting image with image_id={img_id}: Timeout error ({timeout_secs} secs)"
        except requests.RequestException as ex:
            return f"Error while getting image with image_id={img_id}: {ex}"
