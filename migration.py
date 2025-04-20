
## MongoDB → Pinecone Migration
from pymongo import MongoClient
import pinecone
from pinecone import Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os

load_dotenv()

mongo = MongoClient(os.getenv("MONGO_URI"))
pc = Pinecone(api_key="PINECONE_API_KEY",environment="us-west1-gcp")
index = pc.Index("podcastaiagent")

# Transfer data
for mem in mongo.db.memories.find():
    index.upsert([(
        str(mem["_id"]),
        mem["vector"],
        {**mem["metadata"], "content": mem["content"]}
    )])