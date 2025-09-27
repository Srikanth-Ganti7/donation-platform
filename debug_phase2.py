import requests
import json

def test_specific_phase2_issue():
    base_url = "http://localhost:8000"
    
    print("🔍 Debugging Phase 2 Test Issue")
    print("=" * 50)
    
    try:
        # Test 1: Create a user
        print("1. Creating test user...")
        user_data = {"name": "Debug Test User"}
        response = requests.post(f"{base_url}/users/", json=user_data)
        
        if response.status_code != 200:
            print(f"❌ User creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        user = response.json()
        print(f"✅ User created: {user['name']} with badges: {user['badges']}")
        
        # Test 2: Make first donation for First Blood badge
        print("\n2. Making first donation (food)...")
        donation_data = {
            "user_id": user["id"],
            "item_type": "food",
            "location": "Debug Test"
        }
        
        response = requests.post(f"{base_url}/donate", json=donation_data)
        if response.status_code != 200:
            print(f"❌ Donation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        donation_result = response.json()
        print(f"✅ Donation successful: {donation_result['points_awarded']} points")
        
        # Test 3: Check user badges after first donation
        print("\n3. Checking user badges...")
        response = requests.get(f"{base_url}/users/{user['id']}")
        updated_user = response.json()
        
        print(f"User stats: {updated_user['points']} points, {updated_user['donations_count']} donations")
        print(f"Badges: {updated_user['badges']}")
        
        if "First Blood" not in updated_user["badges"]:
            print("❌ ISSUE FOUND: First Blood badge not awarded!")
            print(f"Expected: ['First Blood'], Got: {updated_user['badges']}")
        else:
            print("✅ First Blood badge correctly awarded")
        
        # Test 4: Make medical donation for Lifesaver badge
        print("\n4. Making medical supplies donation...")
        medical_donation = {
            "user_id": user["id"],
            "item_type": "medical_supplies",
            "location": "Hospital Debug"
        }
        
        response = requests.post(f"{base_url}/donate", json=medical_donation)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Medical donation: {result['points_awarded']} points")
            
            # Check badges again
            response = requests.get(f"{base_url}/users/{user['id']}")
            updated_user = response.json()
            print(f"Updated badges: {updated_user['badges']}")
            
            expected_badges = ["First Blood", "Lifesaver"]
            missing_badges = [b for b in expected_badges if b not in updated_user["badges"]]
            
            if missing_badges:
                print(f"❌ ISSUE FOUND: Missing badges: {missing_badges}")
                print(f"Expected: {expected_badges}, Got: {updated_user['badges']}")
            else:
                print("✅ Lifesaver badge correctly awarded")
        
        # Test 5: Check leaderboard
        print("\n5. Testing leaderboard...")
        response = requests.get(f"{base_url}/leaderboard/")
        if response.status_code == 200:
            leaderboard = response.json()
            print(f"✅ Leaderboard working: {len(leaderboard)} entries")
            
            # Check if our user is in leaderboard with badges
            our_user = next((u for u in leaderboard if u["user_id"] == user["id"]), None)
            if our_user:
                print(f"User in leaderboard with badges: {our_user['badges']}")
            else:
                print("❌ User not found in leaderboard")
        else:
            print(f"❌ Leaderboard failed: {response.status_code}")
        
        print(f"\n🎯 Debug complete for user ID: {user['id']}")
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")

if __name__ == "__main__":
    test_specific_phase2_issue()
