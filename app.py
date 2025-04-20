from flask import Flask, request, jsonify
from memory import PodcastMemory
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
memory = PodcastMemory()

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "endpoints": {
            "chat": "POST /api/chat",
            "memories": "POST /api/memories",
            "search": "POST /api/memories/search",
            "clear": "POST /api/clear"
        }
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' in request"}), 400
            
        # Store the message in memory
        memory.remember(content=data['message'])
        
        # Get relevant memories
        memories = memory.recall(query=data['message'])
        
        return jsonify({
            "status": "success",
            "response": f"Received your message about {data['message']}",
            "memories": memories
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/memories', methods=['POST'])
def add_memory():
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({"error": "Missing 'content' in request"}), 400
        
    memory_id = memory.remember(
        content=data['content'],
        metadata=data.get('metadata', {})
    )
    return jsonify({"status": "success", "memory_id": memory_id})

@app.route('/api/memories/search', methods=['POST'])
def search_memories():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request"}), 400
        
    results = memory.recall(
        query=data['query'],
        n_results=data.get('n_results', 3)
    )
    return jsonify(results)

@app.route('/api/clear', methods=['POST'])
def clear_memories():
    memory.index.delete(delete_all=True)
    return jsonify({"status": "All memories cleared"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)