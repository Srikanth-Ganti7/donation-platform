import requests
import json

def test_basic_phase2():
    base_url = "http://localhost:8000"
    
    print("🧪 Quick Phase 2 Test")
    print("=" * 40)
    
    try:
        # Test health check
        response = requests.get(f"{base_url}/ping", timeout=3)
        if response.status_code == 200:
            print("✅ Server is running")
        else:
            print("❌ Server health check failed")
            return
    except:
        print("❌ Cannot connect to server. Make sure it's running!")
        return
    
    # Test leaderboard endpoint
    try:
        response = requests.get(f"{base_url}/leaderboard/")
        if response.status_code == 200:
            leaderboard = response.json()
            print(f"✅ Leaderboard endpoint works - {len(leaderboard)} entries")
        else:
            print(f"❌ Leaderboard failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Leaderboard error: {e}")
    
    # Test user creation
    try:
        user_data = {"name": "Test User Phase2"}
        response = requests.post(f"{base_url}/users/", json=user_data)
        if response.status_code == 200:
            user = response.json()
            if "badges" in user and isinstance(user["badges"], list):
                print(f"✅ User creation with badges works - {user['name']} has {len(user['badges'])} badges")
            else:
                print(f"❌ User missing badges field: {user}")
        else:
            print(f"❌ User creation failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ User creation error: {e}")

if __name__ == "__main__":
    test_basic_phase2()
