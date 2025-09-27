#!/usr/bin/env python3
"""
Comprehensive Test Suite for Donation Platform
Tests all endpoints and features with detailed validation
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

class DonationPlatformTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        self.users_created = []
        self.donations_made = []
        
    def log_test(self, test_name, passed, details=""):
        """Log test results"""
        status = "✅ PASS" if passed else "❌ FAIL"
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details
        })
        print(f"{status}: {test_name}")
        if details:
            print(f"    Details: {details}")
        print()

    def test_server_health(self):
        """Test 1: Server Health Check"""
        try:
            response = requests.get(f"{self.base_url}/ping", timeout=5)
            expected = {"message": "pong"}
            
            if response.status_code == 200 and response.json() == expected:
                self.log_test("Server Health Check", True, f"Server responding on {self.base_url}")
                return True
            else:
                self.log_test("Server Health Check", False, f"Unexpected response: {response.json()}")
                return False
        except requests.exceptions.ConnectionError:
            self.log_test("Server Health Check", False, f"Cannot connect to {self.base_url}")
            return False
        except Exception as e:
            self.log_test("Server Health Check", False, f"Error: {str(e)}")
            return False

    def test_get_initial_needs(self):
        """Test 2: Get Pre-populated Needs"""
        try:
            response = requests.get(f"{self.base_url}/needs/")
            if response.status_code == 200:
                needs = response.json()
                expected_items = ["food", "clothing", "toys", "medical_supplies", "books", "electronics"]
                actual_items = [need["item_type"] for need in needs]
                
                if len(needs) == 6 and all(item in actual_items for item in expected_items):
                    details = f"Found {len(needs)} needs: {actual_items}"
                    self.log_test("Get Pre-populated Needs", True, details)
                    return True
                else:
                    self.log_test("Get Pre-populated Needs", False, f"Expected 6 needs, got {len(needs)}")
                    return False
            else:
                self.log_test("Get Pre-populated Needs", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get Pre-populated Needs", False, f"Error: {str(e)}")
            return False

    def test_create_users(self):
        """Test 3: Create Multiple Users"""
        test_users = [
            {"name": "Alice Johnson"},
            {"name": "Bob Smith"}, 
            {"name": "Charlie Brown"},
            {"name": "Diana Prince"}
        ]
        
        success_count = 0
        for user_data in test_users:
            try:
                response = requests.post(f"{self.base_url}/users/", json=user_data)
                if response.status_code == 200:
                    user = response.json()
                    expected_fields = ["id", "name", "points", "rank", "donations_count"]
                    
                    if all(field in user for field in expected_fields):
                        if (user["points"] == 0 and user["rank"] == "Bronze" and 
                            user["donations_count"] == 0 and user["name"] == user_data["name"]):
                            self.users_created.append(user)
                            success_count += 1
                        else:
                            self.log_test(f"Create User {user_data['name']}", False, 
                                        f"Incorrect default values: {user}")
                    else:
                        self.log_test(f"Create User {user_data['name']}", False, 
                                    f"Missing fields in response: {user}")
                else:
                    self.log_test(f"Create User {user_data['name']}", False, 
                                f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test(f"Create User {user_data['name']}", False, f"Error: {str(e)}")
        
        if success_count == len(test_users):
            self.log_test("Create Multiple Users", True, 
                        f"Created {success_count}/{len(test_users)} users successfully")
            return True
        else:
            self.log_test("Create Multiple Users", False, 
                        f"Only created {success_count}/{len(test_users)} users")
            return False

    def test_get_users(self):
        """Test 4: Get All Users"""
        try:
            response = requests.get(f"{self.base_url}/users/")
            if response.status_code == 200:
                users = response.json()
                if len(users) >= len(self.users_created):
                    self.log_test("Get All Users", True, f"Retrieved {len(users)} users")
                    return True
                else:
                    self.log_test("Get All Users", False, 
                                f"Expected at least {len(self.users_created)} users, got {len(users)}")
                    return False
            else:
                self.log_test("Get All Users", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Get All Users", False, f"Error: {str(e)}")
            return False

    def test_point_calculations(self):
        """Test 5: Point Calculation System"""
        if not self.users_created:
            self.log_test("Point Calculation Tests", False, "No users available for testing")
            return False
            
        user = self.users_created[0]  # Use first created user
        test_cases = [
            {"item": "food", "expected_base": 150, "description": "High urgency (1.5x multiplier)"},
            {"item": "medical_supplies", "expected_base": 200, "description": "Critical urgency (2.0x multiplier)"},
            {"item": "clothing", "expected_base": 120, "description": "Medium urgency (1.2x multiplier)"},
            {"item": "books", "expected_base": 110, "description": "Medium urgency (1.1x multiplier)"},
            {"item": "toys", "expected_base": 100, "description": "Low urgency (1.0x multiplier)"},
            {"item": "furniture", "expected_base": 100, "description": "Unknown item (1.0x default)"},
        ]
        
        passed_tests = 0
        for i, test_case in enumerate(test_cases):
            try:
                donation_data = {
                    "user_id": user["id"],
                    "item_type": test_case["item"],
                    "location": f"Test Location {i+1}"
                }
                
                response = requests.post(f"{self.base_url}/donate", json=donation_data)
                if response.status_code == 200:
                    result = response.json()
                    
                    # Calculate expected points (considering frequency bonus if any)
                    points_awarded = result["points_awarded"]
                    expected_points = test_case["expected_base"]
                    
                    # Allow for frequency bonus (donations after 5th get 1.1x bonus)
                    if len(self.donations_made) >= 5:
                        expected_points = int(expected_points * 1.1)
                    
                    if points_awarded == expected_points or points_awarded == test_case["expected_base"]:
                        self.donations_made.append(result)
                        self.log_test(f"Points: {test_case['item']}", True, 
                                    f"{points_awarded} points - {test_case['description']}")
                        passed_tests += 1
                    else:
                        self.log_test(f"Points: {test_case['item']}", False, 
                                    f"Expected ~{expected_points}, got {points_awarded}")
                else:
                    self.log_test(f"Points: {test_case['item']}", False, 
                                f"Status code: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Points: {test_case['item']}", False, f"Error: {str(e)}")
        
        success = passed_tests >= len(test_cases) * 0.8  # 80% pass rate
        self.log_test("Point Calculation System", success, 
                    f"Passed {passed_tests}/{len(test_cases)} point calculation tests")
        return success

    def test_frequency_bonus(self):
        """Test 6: Frequency Bonus System"""
        if not self.users_created:
            self.log_test("Frequency Bonus Test", False, "No users available")
            return False
            
        user = self.users_created[1]  # Use second user for clean slate
        
        # Make 5 donations to trigger frequency bonus
        for i in range(5):
            donation_data = {
                "user_id": user["id"],
                "item_type": "books",  # 110 base points
                "location": f"Frequency Test {i+1}"
            }
            try:
                response = requests.post(f"{self.base_url}/donate", json=donation_data)
                if response.status_code != 200:
                    self.log_test("Frequency Bonus Setup", False, 
                                f"Failed to make donation {i+1}")
                    return False
            except Exception as e:
                self.log_test("Frequency Bonus Setup", False, f"Error on donation {i+1}: {str(e)}")
                return False
        
        # 6th donation should have frequency bonus (1.1x)
        donation_data = {
            "user_id": user["id"],
            "item_type": "books",  # Should be 110 * 1.1 = 121 points
            "location": "Frequency Bonus Test"
        }
        
        try:
            response = requests.post(f"{self.base_url}/donate", json=donation_data)
            if response.status_code == 200:
                result = response.json()
                expected_points = 121  # 100 * 1.1 (books) * 1.1 (frequency)
                
                if result["points_awarded"] == expected_points:
                    self.log_test("Frequency Bonus System", True, 
                                f"Got {result['points_awarded']} points with 1.1x frequency bonus")
                    return True
                else:
                    self.log_test("Frequency Bonus System", False, 
                                f"Expected {expected_points} points, got {result['points_awarded']}")
                    return False
            else:
                self.log_test("Frequency Bonus System", False, 
                            f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Frequency Bonus System", False, f"Error: {str(e)}")
            return False

    def test_rank_progression(self):
        """Test 7: Rank Progression System"""
        if not self.users_created:
            self.log_test("Rank Progression Test", False, "No users available")
            return False
            
        user = self.users_created[2]  # Use third user
        
        # Test rank thresholds by making high-value donations
        rank_tests = [
            {"target_points": 400, "expected_rank": "Bronze"},
            {"target_points": 600, "expected_rank": "Silver"},
            {"target_points": 2100, "expected_rank": "Gold"},
        ]
        
        passed_tests = 0
        for rank_test in rank_tests:
            # Make medical supply donations (200 points each) to reach target
            donations_needed = (rank_test["target_points"] + 199) // 200  # Round up
            
            for i in range(donations_needed):
                donation_data = {
                    "user_id": user["id"],
                    "item_type": "medical_supplies",
                    "location": f"Rank Test {i+1}"
                }
                try:
                    requests.post(f"{self.base_url}/donate", json=donation_data)
                except:
                    pass  # Continue even if some fail
            
            # Check user's current rank
            try:
                response = requests.get(f"{self.base_url}/users/{user['id']}")
                if response.status_code == 200:
                    updated_user = response.json()
                    actual_rank = updated_user["rank"]
                    actual_points = updated_user["points"]
                    
                    if actual_points >= rank_test["target_points"] and actual_rank == rank_test["expected_rank"]:
                        self.log_test(f"Rank: {rank_test['expected_rank']}", True, 
                                    f"{actual_points} points → {actual_rank} rank")
                        passed_tests += 1
                    else:
                        self.log_test(f"Rank: {rank_test['expected_rank']}", False, 
                                    f"{actual_points} points → {actual_rank} (expected {rank_test['expected_rank']})")
                else:
                    self.log_test(f"Rank: {rank_test['expected_rank']}", False, "Failed to get user")
            except Exception as e:
                self.log_test(f"Rank: {rank_test['expected_rank']}", False, f"Error: {str(e)}")
        
        success = passed_tests >= 2  # At least 2 rank changes should work
        self.log_test("Rank Progression System", success, 
                    f"Verified {passed_tests}/{len(rank_tests)} rank changes")
        return success

    def test_donation_history(self):
        """Test 8: Donation History and Tracking"""
        try:
            # Test get all donations
            response = requests.get(f"{self.base_url}/donations/")
            if response.status_code == 200:
                donations = response.json()
                self.log_test("Get All Donations", True, f"Retrieved {len(donations)} donations")
            else:
                self.log_test("Get All Donations", False, f"Status code: {response.status_code}")
                return False
            
            # Test get donations for specific user
            if self.users_created:
                user = self.users_created[0]
                response = requests.get(f"{self.base_url}/donations/user/{user['id']}")
                if response.status_code == 200:
                    user_donations = response.json()
                    self.log_test("Get User Donations", True, 
                                f"User {user['name']} has {len(user_donations)} donations")
                    
                    # Verify donation structure
                    if user_donations:
                        donation = user_donations[0]
                        required_fields = ["id", "user_id", "item_type", "location", "timestamp", "points_awarded"]
                        if all(field in donation for field in required_fields):
                            self.log_test("Donation Data Structure", True, "All required fields present")
                            return True
                        else:
                            missing = [f for f in required_fields if f not in donation]
                            self.log_test("Donation Data Structure", False, f"Missing fields: {missing}")
                            return False
                    else:
                        self.log_test("Donation History Tracking", True, "No donations to verify structure")
                        return True
                else:
                    self.log_test("Get User Donations", False, f"Status code: {response.status_code}")
                    return False
            else:
                self.log_test("Donation History Test", False, "No users to test with")
                return False
                
        except Exception as e:
            self.log_test("Donation History Test", False, f"Error: {str(e)}")
            return False

    def test_error_handling(self):
        """Test 9: Error Handling"""
        error_tests = [
            {
                "name": "Invalid User ID",
                "request": lambda: requests.post(f"{self.base_url}/donate", 
                                                json={"user_id": 99999, "item_type": "food", "location": "Test"}),
                "expected_status": 404
            },
            {
                "name": "Get Nonexistent User", 
                "request": lambda: requests.get(f"{self.base_url}/users/99999"),
                "expected_status": 404
            },
            {
                "name": "Invalid JSON",
                "request": lambda: requests.post(f"{self.base_url}/users/", 
                                                json={"invalid": "data"}),
                "expected_status": 422
            }
        ]
        
        passed_tests = 0
        for test in error_tests:
            try:
                response = test["request"]()
                if response.status_code == test["expected_status"]:
                    self.log_test(f"Error: {test['name']}", True, 
                                f"Correctly returned status {response.status_code}")
                    passed_tests += 1
                else:
                    self.log_test(f"Error: {test['name']}", False, 
                                f"Expected {test['expected_status']}, got {response.status_code}")
            except Exception as e:
                self.log_test(f"Error: {test['name']}", False, f"Exception: {str(e)}")
        
        success = passed_tests >= len(error_tests) * 0.8
        self.log_test("Error Handling", success, f"Passed {passed_tests}/{len(error_tests)} error tests")
        return success

    def run_all_tests(self):
        """Run the complete test suite"""
        print("🧪 DONATION PLATFORM - COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        print(f"Testing against: {self.base_url}")
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all tests in sequence
        tests = [
            self.test_server_health,
            self.test_get_initial_needs,
            self.test_create_users,
            self.test_get_users,
            self.test_point_calculations,
            self.test_frequency_bonus,
            self.test_rank_progression,
            self.test_donation_history,
            self.test_error_handling
        ]
        
        passed_count = 0
        for test_func in tests:
            try:
                if test_func():
                    passed_count += 1
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                self.log_test(f"Test {test_func.__name__}", False, f"Unexpected error: {str(e)}")
        
        # Print summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len([r for r in self.test_results])
        passed_total = len([r for r in self.test_results if r["passed"]])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_total} ✅")
        print(f"Failed: {total_tests - passed_total} ❌")
        print(f"Success Rate: {(passed_total/total_tests)*100:.1f}%")
        print()
        
        if passed_total == total_tests:
            print("🎉 ALL TESTS PASSED! Your donation platform is working perfectly!")
        elif passed_total >= total_tests * 0.9:
            print("🔥 EXCELLENT! Almost all tests passed. Minor issues detected.")
        elif passed_total >= total_tests * 0.7:
            print("👍 GOOD! Most tests passed. Some features need attention.")
        else:
            print("⚠️  NEEDS WORK! Several tests failed. Check the details above.")
        
        print()
        print(f"Created {len(self.users_created)} test users")
        print(f"Made {len(self.donations_made)} test donations")
        print()
        
        return passed_total == total_tests

if __name__ == "__main__":
    print("🚀 Make sure your server is running first!")
    print("   Run: python main.py (or .\\run_server.bat)")
    print()
    
    # Allow custom URL
    url = input("Server URL (press Enter for http://localhost:8000): ").strip()
    if not url:
        url = "http://localhost:8000"
    
    tester = DonationPlatformTester(url)
    tester.run_all_tests()
