#!/usr/bin/env python3
"""Quick test to verify Gemini API is working"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 60)
print("QUICK API TEST")
print("=" * 60)
print()

# Test 1: Health Check
print("[1/4] Health Check...")
try:
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print("✓ PASS - Server is running")
    else:
        print(f"✗ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"✗ FAIL - {e}")

print()

# Test 2: AI Services Status
print("[2/4] AI Services Status...")
try:
    response = requests.get(f"{BASE_URL}/api/content/ai-services/status")
    data = response.json()
    if data.get('service_status', {}).get('gemini'):
        print(f"✓ PASS - Gemini detected (Primary: {data.get('primary_service')})")
    else:
        print("✗ FAIL - Gemini not detected")
except Exception as e:
    print(f"✗ FAIL - {e}")

print()

# Test 3: Content Generation
print("[3/4] Content Generation (Gemini API)...")
print("   Generating content (may take 5-10 seconds)...")
try:
    response = requests.post(
        f"{BASE_URL}/api/content/generate",
        json={
            "prompt": "Write a short motivational quote about technology",
            "language": "english",
            "tone": "inspirational",
            "content_type": "social_post",
            "user_id": 3
        },
        timeout=30
    )
    
    if response.status_code == 201:
        data = response.json()
        print("✓ PASS - Content generated successfully!")
        print()
        print("   Generated Content:")
        print("   " + "-" * 56)
        print(f"   {data['generated_content'][:200]}...")
        print("   " + "-" * 56)
        print(f"   Model: {data.get('model_used')}")
        print(f"   Time: {data.get('generation_time_ms')}ms")
        print(f"   Words: {data.get('word_count')}")
    else:
        print(f"✗ FAIL - Status: {response.status_code}")
        print(f"   Error: {response.json().get('detail')}")
except Exception as e:
    print(f"✗ FAIL - {e}")

print()

# Test 4: Translation
print("[4/4] Translation...")
try:
    response = requests.get(f"{BASE_URL}/api/translation/languages/supported")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ PASS - {data.get('total')} languages supported")
    else:
        print(f"✗ FAIL - Status: {response.status_code}")
except Exception as e:
    print(f"✗ FAIL - {e}")

print()
print("=" * 60)
print("TEST COMPLETE")
print("=" * 60)
