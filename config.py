import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Core Services
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV", "us-west1-gcp")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # External APIs
    LISTENNOTES_API_KEY = os.getenv("LISTENNOTES_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    
    # Database
    MONGO_URI = os.getenv("MONGO_URI")
    
    # Index Names
    INDEX_NAME = "podcast-index"