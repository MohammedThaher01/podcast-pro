from agno.agent import Agent
from agno.models.groq import Groq
from memory import PodcastMemory
from tools import PodcastTools
import os

def process(self, message: str):
    # memory-aware processing
    if "#remember" in message:
        self.memory.remember(message.replace("#remember", "").strip())
        return "I've stored this in memory"
    
    context = self.memory.recall(message)
    return self.agent.run(f"Context: {context}\n\nQuery: {message}")

class PodcastAssistant:
    def __init__(self):
        self.memory = PodcastMemory()
        self.agent = Agent(
            name="PodcastPro",
            model=Groq(id="qwen-2.5-32b"),
            tools=[PodcastTools()],
            memory=self.memory,
            instructions=[
                "You are an expert podcast production assistant",
                "Remember the podcast's theme, style, and past episodes",
                "Combine historical context with fresh research",
                "Provide structured outlines with timing suggestions",
                "Suggest relevant guests and interview questions",
                "Always cite sources and include reference links"
            ],
            markdown=True
        )
    
    def chat(self, message: str) -> str:
        """Process message with memory recall"""
        # First recall relevant context
        context = self.memory.recall(message)
        
        # Generate response
        response = self.agent.print_response(
            f"Context: {context}\n\nUser: {message}"
        )
        
        # Remember important details
        if "my podcast" in message.lower():
            self.memory.remember(
                content=f"Podcast details: {message}",
                metadata={"type": "podcast_profile"}
            )
        
        return response.content