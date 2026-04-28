import sys
import os

# Add the src dir to the path so we can import llm_engine
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from llm_engine import LLMRecommendationEngine

def run_tests():
    print("Initializing LLMRecommendationEngine...")
    try:
        engine = LLMRecommendationEngine()
    except Exception as e:
        print(f"Failed to initialize engine: {e}")
        return
    
    # Generic context for testing
    test_context = '''Name: Mama Mia, Cuisine: Italian, Rating: 4.8, Cost: 1200, Location: Downtown
Name: Burger Bistro, Cuisine: American, Fast Food, Rating: 4.2, Cost: 400, Location: Uptown
Name: The Sushi Bar, Cuisine: Japanese, Sushi, Rating: 4.5, Cost: 1800, Location: Midtown
Name: Cheap Eats, Cuisine: Street Food, Rating: 3.9, Cost: 150, Location: Downtown
Name: Bella Napoli, Cuisine: Italian, Pizza, Rating: 4.6, Cost: 800, Location: Uptown'''

    test_cases = [
        {
            "name": "Test 1: Standard Query",
            "query": "I want a nice Italian place for a date in Uptown or Downtown.",
            "context": test_context
        },
        {
            "name": "Test 2: Vague Query",
            "query": "Just give me some good food.",
            "context": test_context
        },
        {
            "name": "Test 3: Empty Query",
            "query": "",
            "context": test_context
        },
        {
            "name": "Test 4: Conflicting Query (Asking for cuisine not in context)",
            "query": "I am dying for some authentic Mexican tacos.",
            "context": test_context
        },
        {
            "name": "Test 5: Cost Focused Query",
            "query": "I am a broke college student, I need something super cheap.",
            "context": test_context
        }
    ]

    success_count = 0
    print("=== Starting LLM Connectivity Tests ===\n")
    for tc in test_cases:
        print(f"Running {tc['name']}...")
        print(f"User Query: '{tc['query']}'")
        try:
            results = engine.generate_recommendations(tc['query'], tc['context'])
            print("Response Received!")
            print("Parsed Recommendations:")
            if not results:
                print("  [No recommendations returned]")
            else:
                for r in results:
                    print(f"  - {r.get('name')}: {r.get('explanation')}")
            success_count += 1
        except Exception as e:
            print(f"FAILED to get response. Error: {str(e)}")
        print("-" * 50)
        
    print(f"=== Tests Completed. {success_count}/{len(test_cases)} Passed. ===")

if __name__ == "__main__":
    run_tests()
