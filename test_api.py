#!/usr/bin/env python3
"""Comprehensive test script for Bharat Content AI API"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

# Store IDs for cross-endpoint testing
test_data = {
    "user_id": None,
    "content_id": None,
    "translation_id": None,
    "post_id": None
}


def print_response(title, response):
    """Helper to print formatted responses"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")
    print()


def test_health_check():
    """Test API health endpoint"""
    print("\n[1] Testing Health Check...")
    response = requests.get(f"{BASE_URL}/api/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_user_registration():
    """Test user registration"""
    print("\n[2] Testing User Registration...")
    response = requests.post(
        f"{BASE_URL}/api/users/register",
        json={
            "email": f"test_{datetime.now().timestamp()}@example.com",
            "username": f"testuser_{int(datetime.now().timestamp())}",
            "password": "SecurePass123!",
            "full_name": "Test User",
            "role": "student",
            "preferred_language": "hindi"
        }
    )
    print_response("User Registration", response)
    
    if response.status_code == 201:
        test_data["user_id"] = response.json()["id"]
        return True
    return False


def test_content_generation():
    """Test content generation"""
    print("\n[3] Testing Content Generation...")
    if not test_data["user_id"]:
        print("Skipping - No user_id available")
        return False
    
    response = requests.post(
        f"{BASE_URL}/api/content/generate",
        json={
            "prompt": "Write a social media post about learning Python programming",
            "language": "hindi",
            "tone": "casual",
            "content_type": "social_post",
            "user_id": test_data["user_id"]
        }
    )
    print_response("Content Generation", response)
    
    if response.status_code == 201:
        test_data["content_id"] = response.json()["id"]
        return True
    return False


def test_content_list():
    """Test listing content"""
    print("\n[4] Testing Content List...")
    if not test_data["user_id"]:
        print("Skipping - No user_id available")
        return False
    
    response = requests.get(
        f"{BASE_URL}/api/content/list",
        params={"user_id": test_data["user_id"], "limit": 10}
    )
    print_response("Content List", response)
    return response.status_code == 200


def test_translation():
    """Test content translation"""
    print("\n[5] Testing Translation...")
    if not test_data["content_id"]:
        print("Skipping - No content_id available")
        return False
    
    response = requests.post(
        f"{BASE_URL}/api/translation/translate",
        json={
            "content_id": test_data["content_id"],
            "target_language": "tamil",
            "maintain_tone": True,
            "cultural_adaptation": False
        }
    )
    print_response("Translation", response)
    
    if response.status_code == 201:
        test_data["translation_id"] = response.json()["id"]
        return True
    return False


def test_direct_translation():
    """Test direct text translation"""
    print("\n[6] Testing Direct Translation...")
    if not test_data["user_id"]:
        print("Skipping - No user_id available")
        return False
    
    response = requests.post(
        f"{BASE_URL}/api/translation/translate/direct",
        json={
            "text": "Hello, how are you today?",
            "source_language": "english",
            "target_language": "hindi",
            "tone": "neutral",
            "user_id": test_data["user_id"]
        }
    )
    print_response("Direct Translation", response)
    return response.status_code == 201


def test_supported_languages():
    """Test getting supported languages"""
    print("\n[7] Testing Supported Languages...")
    response = requests.get(f"{BASE_URL}/api/translation/languages/supported")
    print_response("Supported Languages", response)
    return response.status_code == 200


def test_schedule_post():
    """Test scheduling a social media post"""
    print("\n[8] Testing Post Scheduling...")
    if not test_data["user_id"] or not test_data["content_id"]:
        print("Skipping - Missing user_id or content_id")
        return False
    
    scheduled_time = (datetime.utcnow() + timedelta(hours=2)).isoformat() + "Z"
    
    response = requests.post(
        f"{BASE_URL}/api/social/schedule",
        json={
            "user_id": test_data["user_id"],
            "content_id": test_data["content_id"],
            "text_content": "Check out our latest content!",
            "platform": "instagram",
            "scheduled_time": scheduled_time,
            "title": "Test Post"
        }
    )
    print_response("Schedule Post", response)
    
    if response.status_code == 201:
        test_data["post_id"] = response.json()["id"]
        return True
    return False


def test_bulk_schedule():
    """Test bulk scheduling to multiple platforms"""
    print("\n[9] Testing Bulk Schedule...")
    if not test_data["user_id"] or not test_data["content_id"]:
        print("Skipping - Missing user_id or content_id")
        return False
    
    scheduled_time = (datetime.utcnow() + timedelta(hours=3)).isoformat() + "Z"
    
    response = requests.post(
        f"{BASE_URL}/api/social/schedule/bulk",
        json={
            "user_id": test_data["user_id"],
            "content_id": test_data["content_id"],
            "platforms": ["facebook", "twitter", "linkedin"],
            "scheduled_time": scheduled_time,
            "customize_per_platform": True
        }
    )
    print_response("Bulk Schedule", response)
    return response.status_code == 201


def test_post_list():
    """Test listing posts"""
    print("\n[10] Testing Post List...")
    if not test_data["user_id"]:
        print("Skipping - No user_id available")
        return False
    
    response = requests.get(
        f"{BASE_URL}/api/social/list",
        params={"user_id": test_data["user_id"]}
    )
    print_response("Post List", response)
    return response.status_code == 200


def test_analytics_overview():
    """Test analytics overview"""
    print("\n[11] Testing Analytics Overview...")
    if not test_data["user_id"]:
        print("Skipping - No user_id available")
        return False
    
    response = requests.get(
        f"{BASE_URL}/api/analytics/overview/{test_data['user_id']}",
        params={"days": 30}
    )
    print_response("Analytics Overview", response)
    return response.status_code == 200


def test_platform_performance():
    """Test platform performance analytics"""
    print("\n[12] Testing Platform Performance...")
    if not test_data["user_id"]:
        print("Skipping - No user_id available")
        return False
    
    response = requests.get(
        f"{BASE_URL}/api/analytics/platform-performance/{test_data['user_id']}",
        params={"days": 30}
    )
    print_response("Platform Performance", response)
    return response.status_code == 200


def test_user_stats():
    """Test user statistics"""
    print("\n[13] Testing User Stats...")
    if not test_data["user_id"]:
        print("Skipping - No user_id available")
        return False
    
    response = requests.get(f"{BASE_URL}/api/users/{test_data['user_id']}/stats")
    print_response("User Stats", response)
    return response.status_code == 200


def test_content_summarize():
    """Test content summarization"""
    print("\n[14] Testing Content Summarization...")
    if not test_data["content_id"]:
        print("Skipping - No content_id available")
        return False
    
    response = requests.post(
        f"{BASE_URL}/api/content/summarize",
        json={
            "content_id": test_data["content_id"],
            "target_length": 50
        }
    )
    print_response("Content Summarization", response)
    return response.status_code == 200


def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("BHARAT CONTENT AI - COMPREHENSIVE API TESTS")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("User Registration", test_user_registration),
        ("Content Generation", test_content_generation),
        ("Content List", test_content_list),
        ("Translation", test_translation),
        ("Direct Translation", test_direct_translation),
        ("Supported Languages", test_supported_languages),
        ("Schedule Post", test_schedule_post),
        ("Bulk Schedule", test_bulk_schedule),
        ("Post List", test_post_list),
        ("Analytics Overview", test_analytics_overview),
        ("Platform Performance", test_platform_performance),
        ("User Stats", test_user_stats),
        ("Content Summarization", test_content_summarize),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error in {name}: {e}")
            results.append((name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\n{passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    if test_data["user_id"]:
        print(f"\nTest User ID: {test_data['user_id']}")
    if test_data["content_id"]:
        print(f"Test Content ID: {test_data['content_id']}")
    if test_data["post_id"]:
        print(f"Test Post ID: {test_data['post_id']}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n✗ Fatal Error: {e}")
        print("\nMake sure:")
        print("1. Backend server is running: uvicorn app.main:app --reload")
        print("2. Database is initialized: python -c 'from app.config.database import init_db; init_db()'")
        print("3. Environment variables are set in backend/.env")
