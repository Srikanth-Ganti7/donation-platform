#!/usr/bin/env python3
"""
Comprehensive Test Suite for Donation Platform - Phase 2
Tests all endpoints including new leaderboard and badge features
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

    def test_create_users(self):
        """Test 2: User Creation with Badges"""
        test_users = [
            {"name": "Alice Smith"},
            {"name": "Bob Johnson"},
            {"name": "Carol Williams"},
            {"name": "David Brown"}
        ]
        
        for user_data in test_users:
            try:
                response = requests.post(f"{self.base_url}/users/", json=user_data)
                if response.status_code == 200:
                    user = response.json()
                    required_fields = ["id", "name", "points", "rank", "donations_count", "badges"]
                    
                    if all(field in user for field in required_fields):
                        # Check initial values
                        if (user["points"] == 0 and user["rank"] == "Bronze" and 
                            user["donations_count"] == 0 and user["badges"] == []):
                            self.users_created.append(user)
                        else:
                            self.log_test("User Creation", False, 
                                        f"Incorrect initial values for {user['name']}")
                            return False
                    else:
                        self.log_test("User Creation", False, f"Missing fields in response")
                        return False
                else:
                    self.log_test("User Creation", False, f"Status code: {response.status_code}")
                    return False
            except Exception as e:
                self.log_test("User Creation", False, f"Error creating user: {str(e)}")
                return False
        
        self.log_test("User Creation with Badges", True, f"Created {len(self.users_created)} users with badge support")
        return True

    def test_leaderboard_empty(self):
        """Test 3: Initial Empty Leaderboard"""
        try:
            response = requests.get(f"{self.base_url}/leaderboard/")
            if response.status_code == 200:
                leaderboard = response.json()
                if isinstance(leaderboard, list):
                    # Check structure of leaderboard entries
                    required_fields = ["user_id", "name", "points", "rank", "donations_count", "badges"]
                    valid_structure = True
                    
                    for entry in leaderboard:
                        if not all(field in entry for field in required_fields):
                            valid_structure = False
                            break
                        if not isinstance(entry["badges"], list):
                            valid_structure = False
                            break
                    
                    if valid_structure:
                        self.log_test("Initial Leaderboard", True, 
                                    f"Leaderboard with {len(leaderboard)} entries, proper structure")
                        return True
                    else:
                        self.log_test("Initial Leaderboard", False, "Invalid leaderboard structure")
                        return False
                else:
                    self.log_test("Initial Leaderboard", False, "Leaderboard not a list")
                    return False
            else:
                self.log_test("Initial Leaderboard", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Initial Leaderboard", False, f"Error: {str(e)}")
            return False

    def test_first_donation_and_badges(self):
        """Test 4: First Donation and First Blood Badge"""
        if not self.users_created:
            self.log_test("First Donation Badge", False, "No users available")
            return False
        
        user = self.users_created[0]
        
        # Make first donation
        donation_data = {
            "user_id": user["id"],
            "item_type": "food",  # 150 points (100 * 1.5)
            "location": "First Donation Test"
        }
        
        try:
            response = requests.post(f"{self.base_url}/donate", json=donation_data)
            if response.status_code == 200:
                result = response.json()
                expected_points = 150
                
                if result["points_awarded"] == expected_points:
                    # Check if user got "First Blood" badge
                    user_response = requests.get(f"{self.base_url}/users/{user['id']}")
                    if user_response.status_code == 200:
                        updated_user = user_response.json()
                        
                        if "First Blood" in updated_user["badges"]:
                            self.log_test("First Donation Badge", True, 
                                        f"User earned First Blood badge with {result['points_awarded']} points")
                            return True
                        else:
                            self.log_test("First Donation Badge", False, 
                                        f"First Blood badge not awarded. Badges: {updated_user['badges']}")
                            return False
                    else:
                        self.log_test("First Donation Badge", False, "Could not retrieve updated user")
                        return False
                else:
                    self.log_test("First Donation Badge", False, 
                                f"Expected {expected_points} points, got {result['points_awarded']}")
                    return False
            else:
                self.log_test("First Donation Badge", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("First Donation Badge", False, f"Error: {str(e)}")
            return False

    def test_medical_lifesaver_badge(self):
        """Test 5: Medical Supplies Donation for Lifesaver Badge"""
        if not self.users_created:
            self.log_test("Lifesaver Badge", False, "No users available")
            return False
        
        user = self.users_created[1]  # Use second user
        
        # Make medical supplies donation
        donation_data = {
            "user_id": user["id"],
            "item_type": "medical_supplies",  # 200 points (100 * 2.0)
            "location": "Hospital"
        }
        
        try:
            response = requests.post(f"{self.base_url}/donate", json=donation_data)
            if response.status_code == 200:
                result = response.json()
                expected_points = 200
                
                if result["points_awarded"] == expected_points:
                    # Check if user got both badges
                    user_response = requests.get(f"{self.base_url}/users/{user['id']}")
                    if user_response.status_code == 200:
                        updated_user = user_response.json()
                        expected_badges = ["First Blood", "Lifesaver"]
                        
                        has_both = all(badge in updated_user["badges"] for badge in expected_badges)
                        
                        if has_both:
                            self.log_test("Lifesaver Badge", True, 
                                        f"User earned both First Blood and Lifesaver badges")
                            return True
                        else:
                            missing_badges = [b for b in expected_badges if b not in updated_user["badges"]]
                            self.log_test("Lifesaver Badge", False, 
                                        f"Missing badges: {missing_badges}. Has: {updated_user['badges']}")
                            return False
                    else:
                        self.log_test("Lifesaver Badge", False, "Could not retrieve updated user")
                        return False
                else:
                    self.log_test("Lifesaver Badge", False, 
                                f"Expected {expected_points} points, got {result['points_awarded']}")
                    return False
            else:
                self.log_test("Lifesaver Badge", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Lifesaver Badge", False, f"Error: {str(e)}")
            return False

    def test_rank_progression_and_badges(self):
        """Test 6: Rank Progression with Rank Badges"""
        if not self.users_created:
            self.log_test("Rank Progression Badges", False, "No users available")
            return False
        
        user = self.users_created[2]  # Use third user
        
        # Make enough donations to reach Silver (500+ points)
        # 3 medical donations = 3 * 200 = 600 points
        for i in range(3):
            donation_data = {
                "user_id": user["id"],
                "item_type": "medical_supplies",
                "location": f"Rank Test {i+1}"
            }
            
            try:
                response = requests.post(f"{self.base_url}/donate", json=donation_data)
                if response.status_code != 200:
                    self.log_test("Rank Progression Badges", False, f"Donation {i+1} failed")
                    return False
            except Exception as e:
                self.log_test("Rank Progression Badges", False, f"Error on donation {i+1}: {str(e)}")
                return False
        
        # Check final rank and badges
        try:
            response = requests.get(f"{self.base_url}/users/{user['id']}")
            if response.status_code == 200:
                updated_user = response.json()
                
                # Should be Silver rank with 600 points
                if updated_user["rank"] == "Silver":
                    expected_badges = ["First Blood", "Lifesaver", "Silver Star"]
                    
                    # Check for rank badge
                    has_rank_badge = "Silver Star" in updated_user["badges"]
                    
                    if has_rank_badge:
                        self.log_test("Rank Progression Badges", True, 
                                    f"User reached Silver rank with Silver Star badge. Total points: {updated_user['points']}")
                        return True
                    else:
                        self.log_test("Rank Progression Badges", False, 
                                    f"Silver Star badge missing. Has: {updated_user['badges']}")
                        return False
                else:
                    self.log_test("Rank Progression Badges", False, 
                                f"Expected Silver rank, got {updated_user['rank']} with {updated_user['points']} points")
                    return False
            else:
                self.log_test("Rank Progression Badges", False, "Could not retrieve updated user")
                return False
        except Exception as e:
            self.log_test("Rank Progression Badges", False, f"Error: {str(e)}")
            return False

    def test_leaderboard_populated(self):
        """Test 7: Populated Leaderboard Sorting"""
        try:
            response = requests.get(f"{self.base_url}/leaderboard/")
            if response.status_code == 200:
                leaderboard = response.json()
                
                if len(leaderboard) >= 3:  # Should have at least our test users
                    # Check if sorted by points (descending)
                    points_sorted = True
                    for i in range(len(leaderboard) - 1):
                        if leaderboard[i]["points"] < leaderboard[i + 1]["points"]:
                            points_sorted = False
                            break
                    
                    if points_sorted:
                        top_user = leaderboard[0]
                        self.log_test("Populated Leaderboard", True, 
                                    f"Leaderboard sorted correctly. Top user: {top_user['name']} ({top_user['points']} points, {top_user['rank']})")
                        return True
                    else:
                        self.log_test("Populated Leaderboard", False, "Leaderboard not sorted by points")
                        return False
                else:
                    self.log_test("Populated Leaderboard", False, f"Expected at least 3 users, got {len(leaderboard)}")
                    return False
            else:
                self.log_test("Populated Leaderboard", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Populated Leaderboard", False, f"Error: {str(e)}")
            return False

    def test_generous_giver_badge(self):
        """Test 8: Generous Giver Badge (10 donations)"""
        if not self.users_created:
            self.log_test("Generous Giver Badge", False, "No users available")
            return False
        
        user = self.users_created[3]  # Use fourth user
        
        # Make 10 donations to trigger Generous Giver badge
        for i in range(10):
            donation_data = {
                "user_id": user["id"],
                "item_type": "books",  # 110 points each
                "location": f"Generous Test {i+1}"
            }
            
            try:
                response = requests.post(f"{self.base_url}/donate", json=donation_data)
                if response.status_code != 200:
                    self.log_test("Generous Giver Badge", False, f"Donation {i+1} failed")
                    return False
            except Exception as e:
                self.log_test("Generous Giver Badge", False, f"Error on donation {i+1}: {str(e)}")
                return False
        
        # Check for Generous Giver badge
        try:
            response = requests.get(f"{self.base_url}/users/{user['id']}")
            if response.status_code == 200:
                updated_user = response.json()
                
                expected_badges = ["First Blood", "Generous Giver"]
                has_generous_badge = "Generous Giver" in updated_user["badges"]
                
                if has_generous_badge and updated_user["donations_count"] == 10:
                    self.log_test("Generous Giver Badge", True, 
                                f"User earned Generous Giver badge after 10 donations. Total points: {updated_user['points']}")
                    return True
                else:
                    self.log_test("Generous Giver Badge", False, 
                                f"Badge: {has_generous_badge}, Donations: {updated_user['donations_count']}, Badges: {updated_user['badges']}")
                    return False
            else:
                self.log_test("Generous Giver Badge", False, "Could not retrieve updated user")
                return False
        except Exception as e:
            self.log_test("Generous Giver Badge", False, f"Error: {str(e)}")
            return False

    def test_point_master_badge(self):
        """Test 9: Point Master Badge (1000+ points)"""
        if not self.users_created:
            self.log_test("Point Master Badge", False, "No users available")
            return False
        
        # Check if any user has 1000+ points and Point Master badge
        for user in self.users_created:
            try:
                response = requests.get(f"{self.base_url}/users/{user['id']}")
                if response.status_code == 200:
                    updated_user = response.json()
                    
                    if updated_user["points"] >= 1000:
                        has_point_master = "Point Master" in updated_user["badges"]
                        
                        if has_point_master:
                            self.log_test("Point Master Badge", True, 
                                        f"User {updated_user['name']} has Point Master badge with {updated_user['points']} points")
                            return True
            except:
                continue
        
        # If no user has 1000+ points, create more donations
        user = self.users_created[0]  # Use first user
        
        # Make enough medical donations to reach 1000+ points
        for i in range(3):  # 3 * 200 = 600, plus previous 150 = 750, need 2 more
            donation_data = {
                "user_id": user["id"],
                "item_type": "medical_supplies",
                "location": f"Point Master Test {i+1}"
            }
            
            try:
                requests.post(f"{self.base_url}/donate", json=donation_data)
            except:
                pass
        
        # Check again
        try:
            response = requests.get(f"{self.base_url}/users/{user['id']}")
            if response.status_code == 200:
                updated_user = response.json()
                
                if updated_user["points"] >= 1000:
                    has_point_master = "Point Master" in updated_user["badges"]
                    
                    if has_point_master:
                        self.log_test("Point Master Badge", True, 
                                    f"User earned Point Master badge with {updated_user['points']} points")
                        return True
                    else:
                        self.log_test("Point Master Badge", False, 
                                    f"User has {updated_user['points']} points but no Point Master badge. Badges: {updated_user['badges']}")
                        return False
                else:
                    self.log_test("Point Master Badge", False, 
                                f"User only has {updated_user['points']} points, need 1000+")
                    return False
        except Exception as e:
            self.log_test("Point Master Badge", False, f"Error: {str(e)}")
            return False

    def test_error_handling(self):
        """Test 10: Error Handling"""
        try:
            # Test invalid user donation
            invalid_donation = {
                "user_id": 99999,
                "item_type": "food",
                "location": "Error Test"
            }
            
            response = requests.post(f"{self.base_url}/donate", json=invalid_donation)
            if response.status_code == 404:
                self.log_test("Error Handling", True, "Properly handled invalid user ID")
                return True
            else:
                self.log_test("Error Handling", False, f"Expected 404, got {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Error Handling", False, f"Error: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all tests and print summary"""
        print("🚀 DONATION PLATFORM COMPREHENSIVE TEST SUITE - PHASE 2")
        print("=" * 70)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all tests in sequence
        tests = [
            self.test_server_health,
            self.test_create_users,
            self.test_leaderboard_empty,
            self.test_first_donation_and_badges,
            self.test_medical_lifesaver_badge,
            self.test_rank_progression_and_badges,
            self.test_leaderboard_populated,
            self.test_generous_giver_badge,
            self.test_point_master_badge,
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
        print("=" * 70)
        print("📊 TEST SUMMARY")
        print("=" * 70)
        
        total_tests = len([r for r in self.test_results])
        passed_total = len([r for r in self.test_results if r["passed"]])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_total} ✅")
        print(f"Failed: {total_tests - passed_total} ❌")
        print(f"Success Rate: {(passed_total/total_tests)*100:.1f}%")
        print()
        
        if passed_total == total_tests:
            print("🎉 ALL TESTS PASSED! Your donation platform with gamification is working perfectly!")
        elif passed_total >= total_tests * 0.9:
            print("🔥 EXCELLENT! Almost all tests passed. Minor issues detected.")
        elif passed_total >= total_tests * 0.7:
            print("👍 GOOD! Most tests passed. Some features need attention.")
        else:
            print("⚠️  NEEDS WORK! Several tests failed. Check the details above.")
        
        print()
        print("🎮 PHASE 2 FEATURES TESTED:")
        print("✅ Leaderboard endpoint with proper sorting")
        print("✅ Badge system with multiple achievements")
        print("✅ Rank progression with rank badges")  
        print("✅ Auto-updating gamification on donations")
        print()
        
        print(f"Created {len(self.users_created)} test users")
        print(f"Made multiple test donations")
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
    success = tester.run_all_tests()
    
    if success:
        print("🎯 Ready for Phase 3 development!")
    else:
        print("🔧 Fix the failing tests before proceeding to Phase 3")
