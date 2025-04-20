from flask import Flask, request, jsonify
from memory import PodcastMemory
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
memory = PodcastMemory()

@app.route('/api/memories', methods=['POST'])
def add_memory():
    data = request.json
    memory.remember(
        content=data['content'],
        metadata=data.get('metadata', {})
    )
    return jsonify({"status": "success"})

@app.route('/api/memories/search', methods=['POST'])
def search_memories():
    data = request.json
    results = memory.recall(
        query=data['query'],
        n_results=data.get('n_results', 3)
    )
    return jsonify(results)

# Error handling
@app.errorhandler(500)
def handle_error(e):
    return jsonify({
        "error": str(e),
        "solution": "Check MIGRATION.md for Pinecone setup"
    }), 500

if __name__ == '__main__':
    app.run(port=5000)