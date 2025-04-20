from google.generativeai import embedding
from pinecone import Pinecone
from datetime import datetime
from typing import List, Dict, Optional  # Added Optional import
import os
from dotenv import load_dotenv

load_dotenv()

class PodcastMemory:
    def __init__(self):
        # Initialize Pinecone client (new v3+ syntax)
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        
        # Index configuration
        self.index_name = "podcast-memories"
        self.dimension = 768  # Gemini embedding size
        self._initialize_index()

    def _initialize_index(self):
        """Create or connect to Pinecone index"""
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=self.dimension,
                metric="cosine"
            )
        self.index = self.pc.Index(self.index_name)

    def _get_embedding(self, text: str) -> List[float]:
        """Generate embeddings using Gemini"""
        try:
            result = embedding.embed_content(
                model="models/embedding-001",
                content=text
            )
            return result["embedding"]
        except Exception as e:
            print(f"Embedding error: {str(e)}")
            return [0.0] * self.dimension  # Fallback

    def remember(self, content: str, metadata: Optional[Dict] = None) -> str:
        """Store memory with vector embedding"""
        if metadata is None:
            metadata = {}
        
        # Generate embedding and store
        memory_id = str(datetime.now().timestamp())
        vector = self._get_embedding(content)
        
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
        """Semantic search for relevant memories"""
        query_embedding = self._get_embedding(query)
        
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=n_results,
                include_metadata=True
            )
            
            return [{
                "id": match.id,
                "content": match.metadata["content"],
                "metadata": match.metadata,
                "score": match.score
            } for match in results.matches]
        
        except Exception as e:
            print(f"Vector search failed: {str(e)}")
            return []