import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "src"))

from backend_controller import BackendController

def run_tests():
    print("Initializing Backend Controller...")
    # Path to the parquet file from Phase 2
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "phase 2", "data", "cleaned_restaurants.parquet")
    
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Please ensure Phase 2 data ingestion ran.")
        return
        
    try:
        controller = BackendController(data_path)
    except Exception as e:
        print(f"Failed to initialize backend: {e}")
        return

    test_cases = [
        {
            "name": "Test 1: Normal Search with Query",
            "params": {
                "location": "Indiranagar",
                "budget": "Medium",
                "cuisines": ["Italian", "Cafe"],
                "min_rating": 4.0,
                "user_query": "I want a romantic place with good ambiance."
            }
        },
        {
            "name": "Test 2: Empty User Query (Auto-generation test)",
            "params": {
                "location": "Koramangala",
                "budget": "Low",
                "cuisines": ["Fast Food"],
                "min_rating": 3.5,
                "user_query": ""
            }
        },
        {
            "name": "Test 3: Impossible Constraints",
            "params": {
                "location": "NonExistentCity123",
                "budget": "Low",
                "cuisines": ["Martian Cuisine"],
                "min_rating": 5.0,
                "user_query": "Find me aliens."
            }
        }
    ]

    success_count = 0
    print("\n=== Starting Backend Controller Tests ===\n")
    for tc in test_cases:
        print(f"Running {tc['name']}...")
        print(f"Params: {tc['params']}")
        try:
            results = controller.get_recommendations(**tc['params'])
            print(f"Returned {len(results)} recommendations.")
            for i, r in enumerate(results, 1):
                print(f"  [{i}] {r.get('Name')} | Rating: {r.get('Rating')} | Cost: {r.get('Cost')}")
                print(f"      AI Reason: {r.get('Explanation')}")
            success_count += 1
        except Exception as e:
            print(f"FAILED to get response. Error: {str(e)}")
        print("-" * 60)
        
    print(f"=== Tests Completed. {success_count}/{len(test_cases)} Passed. ===")

if __name__ == "__main__":
    run_tests()
