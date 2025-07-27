#!/usr/bin/env python3
"""
Test client for the Flask app
"""

import requests
import json

def test_flask_app():
    """Test the Flask app endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Flask App...")
    
    # Test home endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Home endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Home endpoint failed: {e}")
    
    # Test add endpoint
    try:
        data = {"num1": 10, "num2": 5}
        response = requests.post(f"{base_url}/add", json=data)
        print(f"✅ Add endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Add endpoint failed: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")

if __name__ == "__main__":
    test_flask_app() 