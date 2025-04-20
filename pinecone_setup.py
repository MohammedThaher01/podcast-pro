from pinecone import pinecone

# Initialize Pinecone with your API key and the environment
pc= pinecone(api_key="PINECONE_API_KEY", environment="us-east-1")  # Make sure to replace with your actual API key
index = pinecone.Index("podcast-index")

# Create the index with the specified name, dimension, and metric
pinecone.create_index(
    name="podcast-index",  # Your index name
    dimension=1536,        # Dimension size (based on your model)
    metric="cosine"        # Cosine similarity metric
)

# Connect to your Pinecone index
index = pinecone.Index("podcast-index")

# Upsert example vectors (replace with your actual data)
index.upsert(
    vectors=[
        {"id": "vec1", "values": [1.0, 1.5], "metadata": {"genre": "drama"}},
        {"id": "vec2", "values": [2.0, 1.0], "metadata": {"genre": "action"}},
        {"id": "vec3", "values": [0.1, 0.3], "metadata": {"genre": "drama"}},
        {"id": "vec4", "values": [1.0, -2.5], "metadata": {"genre": "action"}}
    ],
    namespace="ns1"  # Replace with your namespace, or leave it if not required
)

# Query example for the most similar vectors
response = index.query(
    namespace="ns1",  # Replace with your namespace if needed
    vector=[0.1, 0.3],  # Example query vector
    top_k=2,  # Number of top results to return
    include_values=True,
    include_metadata=True,
    filter={"genre": {"$eq": "action"}}  # Optional filter
)

print(response)
