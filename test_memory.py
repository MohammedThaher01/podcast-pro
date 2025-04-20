from memory import PodcastMemory

def test_memory():
    print("🧪 Testing Memory System")
    
    try:
        # Initialize
        print("Initializing memory system...")
        mem = PodcastMemory()
        print("✅ Memory system initialized successfully!")
        
        # Test storage
        print("\nTesting memory storage...")
        memory_id = mem.remember("Test content about AI podcasting")
        print(f"Stored memory with ID: {memory_id}")
        
        # Test recall
        print("\nTesting memory recall...")
        results = mem.recall("AI podcast")
        print("Recall results:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['content']} (score: {result['score']:.2f})")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    test_memory()