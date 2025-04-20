from google.generativeai import embedding
from pinecone import Pinecone, ServerlessSpec
from datetime import datetime
from typing import List, Dict, Optional
import os
import time
from dotenv import load_dotenv

load_dotenv()

class PodcastMemory:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = "podcast-index"
        self.dimension = 768
        self._initialize_index()

    def _initialize_index(self):
        """Initialize with enhanced error handling"""
        try:
            if self.index_name not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
                time.sleep(10)  # Extended wait for index readiness
            self.index = self.pc.Index(self.index_name)
        except Exception as e:
            raise RuntimeError(f"Index init failed: {str(e)}")

    def _get_embedding(self, text: str) -> List[float]:
        """More reliable embedding generation"""
        try:
            result = embedding.embed_content(
                model="models/embedding-001",
                content=text
            )
            return result["embedding"]
        except Exception as e:
            print(f"Embedding error: {str(e)}")
            return [0.0] * self.dimension

    def remember(self, content: str, metadata: Optional[Dict] = None) -> str:
        """Enhanced memory storage"""
        metadata = metadata or {}
        vector = self._get_embedding(content)
        memory_id = f"mem_{int(time.time())}"
        
        self.index.upsert(
            vectors=[{
                "id": memory_id,
                "values": vector,
                "metadata": {
                    "content": content,
                    **metadata,
                    "timestamp": datetime.now().isoformat()
                }
            }]
        )
        return memory_id

    def recall(self, query: str, n_results: int = 3) -> List[Dict]:
        """Improved recall with better filtering"""
        try:
            results = self.index.query(
                vector=self._get_embedding(query),
                top_k=n_results,
                include_metadata=True,
                include_values=False
            )
            return sorted([
                {
                    "content": match.metadata["content"],
                    "score": match.score,
                    "timestamp": match.metadata.get("timestamp")
                }
                for match in results.matches
                if match.score > 0.6  # Quality threshold
            ], key=lambda x: x["score"], reverse=True)
        except Exception as e:
            print(f"Recall error: {str(e)}")
            return []