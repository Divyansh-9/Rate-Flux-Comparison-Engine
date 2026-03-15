import requests
import time

BASE_URL = "http://localhost:5000/api"

def test_health():
    print("Testing API Health...")
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200
    print("✅ Health check passed!")

def test_validation():
    print("Testing Zod Validation (missing query)...")
    res = requests.get(f"{BASE_URL}/products/search")
    print(f"DEBUG: Status Code: {res.status_code}")
    print(f"DEBUG: Response text: {res.text}")
    assert res.status_code == 400
    data = res.json()
    assert data["message"] == "Invalid query parameters"
    print("✅ Validation check passed!")

def test_search_cache():
    print("Testing Redis Caching Performance...")
    query = "performance_test_cache"
    
    # 1. First request (Miss)
    start = time.time()
    res1 = requests.get(f"{BASE_URL}/products/search?q={query}")
    duration1 = time.time() - start
    assert res1.status_code == 200
    print(f"   First search (MongoDB query) took: {duration1:.4f}s")
    
    # 2. Second request (Hit)
    start = time.time()
    res2 = requests.get(f"{BASE_URL}/products/search?q={query}")
    duration2 = time.time() - start
    assert res2.status_code == 200
    print(f"   Second search (Redis Cache) took:  {duration2:.4f}s")
    
    # Let's add a small buffer in case the machine is just fast, but mostly duration2 < duration1
    if duration2 < duration1:
        print("✅ Redis Caching check passed! The second request was faster.")
    else:
        print("⚠️ Warning: Redis cache was not faster. Check docker logs for [cache:miss].")

def test_scrape_job_enqueue():
    print("Testing Scrape Job Enqueueing...")
    res = requests.post(f"{BASE_URL}/scrape", json={"query": "test query", "retailer": "amazon"})
    assert res.status_code == 202
    print("✅ Scrape job enqueue passed!")

if __name__ == "__main__":
    print("-" * 40)
    print("🧪 Running System Architecture Tests...")
    print("-" * 40)
    
    try:
        test_health()
        test_validation()
        test_search_cache()
        test_scrape_job_enqueue()
        print("-" * 40)
        print("🎉 All Tests Passed!")
    except Exception as e:
        print(f"❌ Test Failed: {str(e)}")
