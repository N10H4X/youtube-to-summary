#!/usr/bin/env python3
"""
Test client for YouTube to Summary API
Demonstrates how to use the REST API
"""

import requests
import json
import time

def test_api():
    """Test the YouTube to Summary API"""
    
    # API configuration
    base_url = "http://localhost:5000"
    
    print("🧪 Testing YouTube to Summary API")
    print("=" * 60)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    print("\n" + "-" * 40 + "\n")
    
    # Test 2: API status
    print("2. Testing API status...")
    try:
        response = requests.get(f"{base_url}/api/v1/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Status check failed: {e}")
    
    print("\n" + "-" * 40 + "\n")
    
    # Test 3: Invalid request (missing URL)
    print("3. Testing invalid request (missing URL)...")
    try:
        response = requests.post(
            f"{base_url}/api/v1/summarize",
            json={}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Invalid request test failed: {e}")
    
    print("\n" + "-" * 40 + "\n")
    
    # Test 4: Invalid YouTube URL
    print("4. Testing invalid YouTube URL...")
    try:
        response = requests.post(
            f"{base_url}/api/v1/summarize",
            json={"youtube_url": "https://example.com/not-youtube"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Invalid URL test failed: {e}")
    
    print("\n" + "-" * 40 + "\n")
    
    # Test 5: Valid YouTube URL (commented out by default to avoid long processing)
    print("5. Testing valid YouTube URL...")
    print("Note: This test is commented out to avoid long processing times.")
    print("To test with a real YouTube video, uncomment the code below and replace with a short video URL.")
    
    """
    # Uncomment this section to test with a real YouTube video
    # Replace with a short YouTube video URL for testing
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example URL
    
    try:
        print(f"Processing: {test_url}")
        print("This may take several minutes...")
        
        start_time = time.time()
        response = requests.post(
            f"{base_url}/api/v1/summarize",
            json={
                "youtube_url": test_url,
                # "api_key": "your_custom_api_key_here"  # Optional
            },
            timeout=600  # 10 minute timeout
        )
        end_time = time.time()
        
        print(f"Status: {response.status_code}")
        print(f"Processing time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print("✓ Success!")
            print(f"Summary: {result['data']['content'][:200]}...")  # First 200 chars
        else:
            print(f"Error: {json.dumps(response.json(), indent=2)}")
            
    except Exception as e:
        print(f"Valid URL test failed: {e}")
    """

def interactive_test():
    """Interactive test mode where user can input YouTube URLs"""
    
    base_url = "http://localhost:5000"
    
    print("🎥 Interactive YouTube to Summary API Test")
    print("=" * 60)
    print("Enter YouTube URLs to test the API (or 'quit' to exit)")
    print("")
    
    while True:
        try:
            url = input("YouTube URL: ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                break
            
            if not url:
                continue
            
            print(f"\n🔄 Processing: {url}")
            print("This may take several minutes...")
            
            start_time = time.time()
            response = requests.post(
                f"{base_url}/api/v1/summarize",
                json={"youtube_url": url},
                timeout=600  # 10 minute timeout
            )
            end_time = time.time()
            
            print(f"\n📊 Results:")
            print(f"Status Code: {response.status_code}")
            print(f"Processing Time: {end_time - start_time:.2f} seconds")
            
            if response.status_code == 200:
                result = response.json()
                print("✓ Success!")
                print(f"\n📝 Summary Report:")
                print("-" * 40)
                print(result['data']['content'])
                print("-" * 40)
            else:
                print("❌ Error occurred:")
                print(json.dumps(response.json(), indent=2))
            
            print("\n" + "=" * 60)
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_test()
    else:
        test_api()
        print("\n💡 Tip: Run 'python test_api.py interactive' for interactive testing")
