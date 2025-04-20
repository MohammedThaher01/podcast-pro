from memory import PodcastMemory
from tools import PodcastTools
from config import Config
import logging
from typing import List, Dict
from groq import Groq

class PodcastAssistant:
    def __init__(self):
        self.memory = PodcastMemory()
        self.tools = PodcastTools()
        self.logger = logging.getLogger(__name__)
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model_name = "llama3-8b-8192"
        self.podcast_name = "PodcastPro" 
        
    def chat(self, message: str) -> str:
        try:
            if not message.strip():
                return "Please provide a valid message"
            
            # First handle memory storage if needed
            if self._should_remember(message):
                return self._handle_memory_storage(message)
                
            # Then process the query
            context = self._get_context(message)
            return self._generate_response(message, context)
            
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return "I encountered an error processing your request"

    def _get_context(self, message: str) -> List[Dict]:
        """Enhanced context retrieval"""
        try:
            # Search with broader parameters
            return self.memory.recall(message, n_results=5)
        except Exception as e:
            self.logger.warning(f"Context error: {str(e)}")
            return []

    def _generate_response(self, message: str, context: List[Dict]) -> str:
        """Improved response generation with podcast name integration"""
        try:
            prompt = self._build_prompt(message, context)
            
            response = self.client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                model=self.model_name,
                temperature=0.7,
                max_tokens=1024
            )
            
            return self._format_response(response.choices[0].message.content)
            
        except Exception as e:
            self.logger.error(f"LLM error: {str(e)}")
            return "I couldn't generate a response to that."

    def _build_prompt(self, message: str, context: List[Dict]) -> str:
        """Prompt engineering with PodcastPro branding"""
        context_str = "\n".join(
            f"- {item['content']} (relevance: {item['score']:.2f})" 
            for item in context
        ) if context else "No relevant context found"
        
        return f"""**PodcastPro Assistant Instructions**
You are the AI assistant for the podcast "{self.podcast_name}". Use the following context to answer the query.

**Stored Context**:
{context_str}

**User Query**:
{message}

**Response Guidelines**:
1. Always mention the podcast name "{self.podcast_name}" when appropriate
2. Be specific and actionable
3. Reference the context when relevant
4. For suggestions, provide exactly 3 options
5. Use markdown formatting
6. Maintain a professional tone

**Response**:"""

    def _format_response(self, response: str) -> str:
        """Ensure consistent response formatting"""
        return response.strip()

    def _should_remember(self, message: str) -> bool:
        """More precise memory storage detection"""
        triggers = [
            "#remember", 
            "save this",
            "remember that",
            "store this"
        ]
        message_lower = message.lower()
        return (
            any(trigger in message_lower for trigger in triggers) 
            or message_lower.startswith("remember ")
        )

    def _handle_memory_storage(self, message: str) -> str:
        """Enhanced memory storage with confirmation"""
        clean_msg = message.replace("#remember", "").replace("remember that", "").strip()
        if not clean_msg:
            return "Please provide information to store"
            
        memory_id = self.memory.remember(
            content=clean_msg,
            metadata={"type": "podcast_info"}
        )
        return f"I've stored this in {self.podcast_name}'s memory: {clean_msg}"