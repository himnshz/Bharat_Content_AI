#!/usr/bin/env python3
"""Check if Gemini API key is valid"""

import os
from dotenv import load_dotenv

load_dotenv('backend/.env')

print("=" * 60)
print("GEMINI API KEY DIAGNOSTIC")
print("=" * 60)
print()

# Check if key exists
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ NO API KEY FOUND")
    print("   The GEMINI_API_KEY environment variable is not set.")
    print()
    print("   Action: Add GEMINI_API_KEY to backend/.env file")
    exit(1)

# Check key format
print(f"✓ API Key Found")
print(f"  Length: {len(api_key)} characters")
print(f"  Starts with: {api_key[:10]}...")
print(f"  Ends with: ...{api_key[-5:]}")
print()

# Check for common issues
issues = []

if api_key == "your_gemini_api_key_here":
    issues.append("Key is still the placeholder value")

if len(api_key) < 30:
    issues.append("Key seems too short (should be ~39 characters)")

if ' ' in api_key:
    issues.append("Key contains spaces")

if '\t' in api_key:
    issues.append("Key contains tabs")

if '`' in api_key:
    issues.append("Key contains backticks")

if not api_key.startswith('AIza'):
    issues.append("Key doesn't start with 'AIza' (typical for Gemini keys)")

if issues:
    print("⚠️  POTENTIAL ISSUES DETECTED:")
    for issue in issues:
        print(f"   • {issue}")
    print()
    print("   Action: Get a new API key from:")
    print("   https://makersuite.google.com/app/apikey")
else:
    print("✓ Key format looks correct")
    print()
    print("   If content generation still fails, the key might be:")
    print("   • Expired or revoked")
    print("   • Has API restrictions enabled")
    print("   • From a project without billing enabled")
    print()
    print("   Try generating a new key at:")
    print("   https://makersuite.google.com/app/apikey")

print()
print("=" * 60)
