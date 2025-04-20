from agno.tools import tool
from typing import List, Dict
import requests
import os

class PodcastTools:
    
    @tool
    def research_topics(self, theme: str) -> List[Dict]:
        """Find trending topics matching podcast theme"""
        url = "https://listen-api.listennotes.com/api/v2/search"
        params = {
            "q": theme,
            "type": "episode",
            "sort_by_date": 1
        }
        headers = {"X-ListenAPI-Key": os.getenv("LISTENNOTES_API_KEY")}
        response = requests.get(url, headers=headers, params=params)
        return [{
            "title": e["title"],
            "description": e["description"],
            "link": e["link"]
        } for e in response.json()["results"][:3]]
    
    @tool
    def find_guests(self, topic: str) -> List[Dict]:
        """Find potential guests for a topic"""
        params = {
            "q": f"{topic} expert",
            "api_key": os.getenv("SERPER_API_KEY")
        }
        response = requests.get("https://google.serper.dev/search", params=params)
        return [{
            "name": r["title"],
            "credentials": r["snippet"],
            "link": r["link"]
        } for r in response.json()["organic"][:3]]
    
    @tool
    def generate_outline(self, topic: str) -> Dict:
        """Generate episode outline"""
        return {
            "structure": [
                "Hook (30s): Pose thought-provoking question",
                "Intro (1m): Context and importance",
                "Main Content (10m): 3 key points",
                "Guest Segment (5m): Q&A if applicable",
                "Conclusion (1m): Call-to-action"
            ],
            "prompts": [
                f"What's the most surprising thing about {topic}?",
                f"How does {topic} impact our daily lives?"
            ]
        }