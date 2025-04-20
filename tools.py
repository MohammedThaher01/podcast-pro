import requests
from config import Config
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential

class PodcastTools:
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _safe_api_call(self, url: str, params: dict, headers: dict = None) -> dict:
        response = requests.get(
            url,
            params=params,
            headers=headers or {},
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    # def research_topics(self, theme: str) -> List[Dict]:
    #     try:
    #         data = self._safe_api_call(
    #             url="https://listen-api.listennotes.com/api/v2/search",
    #             params={"q": theme, "type": "episode"},
    #             headers={"X-ListenAPI-Key": Config.LISTENNOTES_API_KEY}
    #         )
    #         return [{
    #             "title": e["title"],
    #             "link": e["link"]
    #         } for e in data.get("results", [])[:3]]
    #     except Exception as e:
    #         return [{"error": str(e)}]

    def find_guests(self, topic: str) -> List[Dict]:
        try:
            data = self._safe_api_call(
                url="https://google.serper.dev/search",
                params={"q": f"{topic} expert"},
                headers={"X-API-KEY": Config.SERPER_API_KEY}
            )
            return [{
                "name": r["title"],
                "link": r["link"]
            } for r in data.get("organic", [])[:3]]
        except Exception as e:
            return [{"error": str(e)}]