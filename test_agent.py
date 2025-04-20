from agent import PodcastAssistant
import time

def run_tests():
    print("🚀 Starting PodcastPro Integration Tests")
    
    # Initialize with timing
    start_time = time.time()
    assistant = PodcastAssistant()
    init_time = time.time() - start_time
    print(f"✅ Assistant initialized in {init_time:.2f}s")
    
    # Test cases with timing
    tests = [
        ("Remember my podcast 'AI Today' focuses on machine learning applications in healthcare", "store"),
        ("What is my podcast about?", "recall"),
        ("Suggest topics for my next episode", "topics"),
        ("Create outline for episode about AI diagnostics", "outline"),
        ("", "error")
    ]
    
    for message, test_type in tests:
        print(f"\n🧪 {test_type.upper()} TEST")
        print(f"Input: {message}")
        
        start = time.time()
        response = assistant.chat(message)
        elapsed = time.time() - start
        
        print(f"\nResponse ({elapsed:.2f}s):")
        print(response)

if __name__ == "__main__":
    run_tests()