from django.db.models import base
import requests
from django.conf import settings
from django.core.cache import cache


class APIKeyHelper:
    def fetch_api_key():
        key = cache.get("api_key")
        return key

    def set_api_key(key: str):
        cache.set("api_key", key)

    def set_initial_key():
        base_key = settings.GOOGLE_KEY
        if base_key:
            cache.set("api_key", base_key)


class GoogleYoutubeAPI:
    def __init__(self) -> None:
        self.api_url = settings.YT_API_URL
        self.keyword = settings.SEARCH_KEY

    def fetch_data(self):
        query_dict = {
            "part": "snippet",
            "maxResults": 25,
            "type": "video",
            "key": APIKeyHelper.fetch_api_key(),
            "q": self.keyword,
        }
        data = requests.get(url=self.api_url, params=query_dict)
        if data.status_code != 200:
            return []
        api_data = data.json()
        api_data = [api_data_point["snippet"] for api_data_point in api_data["items"]]
        return api_data
