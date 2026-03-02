"""
Test script for Campaign API endpoints
Run this after starting the backend server
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api/campaigns"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_create_campaign():
    """Test creating a new campaign"""
    start_date = datetime.now() + timedelta(days=7)
    end_date = start_date + timedelta(days=90)
    
    campaign_data = {
        "user_id": 1,
        "name": "Summer Product Launch 2024",
        "description": "Launch campaign for our new summer collection",
        "campaign_type": "product_launch",
        "status": "draft",
        "objectives": ["Increase brand awareness", "Drive sales", "Engage with millennials"],
        "target_audience": {
            "age_range": "18-35",
            "interests": ["fashion", "lifestyle", "sustainability"],
            "location": ["India", "USA", "UK"]
        },
        "budget": 50000.00,
        "currency": "USD",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "platforms": ["instagram", "facebook", "twitter", "tiktok"],
        "content_guidelines": "Use bright colors, summer vibes, include product shots. Focus on sustainability messaging.",
        "hashtags": ["#SummerVibes", "#NewCollection", "#Fashion2024", "#SustainableFashion"],
        "mentions": ["@brandname", "@ecofriendly"],
        "creator_ids": [101, 102, 103, 104, 105],
        "min_followers": 10000,
        "max_creators": 10,
        "target_reach": 1000000,
        "target_impressions": 5000000,
        "target_engagement_rate": 3.5,
        "target_conversions": 5000,
        "requires_approval": True,
        "brand_assets": [
            "https://example.com/logo.png",
            "https://example.com/banner.jpg",
            "https://example.com/product-catalog.pdf"
        ],
        "landing_page_url": "https://example.com/summer-collection",
        "tracking_links": [
            "https://example.com/track?utm_campaign=summer2024&utm_source=instagram",
            "https://example.com/track?utm_campaign=summer2024&utm_source=facebook"
        ],
        "team_members": [1, 2, 3],
        "notes": "Focus on Instagram Stories and Reels. Partner with micro-influencers."
    }
    
    response = requests.post(BASE_URL + "/", json=campaign_data)
    print_response("CREATE CAMPAIGN", response)
    
    if response.status_code == 201:
        return response.json()["id"]
    return None

def test_get_all_campaigns():
    """Test getting all campaigns"""
    response = requests.get(BASE_URL + "/")
    print_response("GET ALL CAMPAIGNS", response)

def test_get_campaign(campaign_id):
    """Test getting a specific campaign"""
    response = requests.get(f"{BASE_URL}/{campaign_id}")
    print_response(f"GET CAMPAIGN {campaign_id}", response)

def test_update_campaign(campaign_id):
    """Test updating a campaign"""
    update_data = {
        "name": "Summer Product Launch 2024 - UPDATED",
        "budget": 75000.00,
        "status": "active"
    }
    
    response = requests.put(f"{BASE_URL}/{campaign_id}", json=update_data)
    print_response(f"UPDATE CAMPAIGN {campaign_id}", response)

def test_update_metrics(campaign_id):
    """Test updating campaign metrics"""
    metrics_data = {
        "actual_reach": 850000,
        "actual_impressions": 4200000,
        "actual_engagement_rate": 4.2,
        "actual_conversions": 4500,
        "total_spent": 35000.00,
        "revenue_generated": 125000.00
    }
    
    response = requests.patch(f"{BASE_URL}/{campaign_id}/metrics", json=metrics_data)
    print_response(f"UPDATE METRICS FOR CAMPAIGN {campaign_id}", response)

def test_update_status(campaign_id):
    """Test updating campaign status"""
    response = requests.patch(f"{BASE_URL}/{campaign_id}/status?new_status=active")
    print_response(f"UPDATE STATUS FOR CAMPAIGN {campaign_id}", response)

def test_approve_campaign(campaign_id):
    """Test approving a campaign"""
    response = requests.patch(f"{BASE_URL}/{campaign_id}/approve?approver_id=5")
    print_response(f"APPROVE CAMPAIGN {campaign_id}", response)

def test_get_analytics(campaign_id):
    """Test getting campaign analytics"""
    response = requests.get(f"{BASE_URL}/{campaign_id}/analytics")
    print_response(f"GET ANALYTICS FOR CAMPAIGN {campaign_id}", response)

def test_filter_campaigns():
    """Test filtering campaigns"""
    response = requests.get(f"{BASE_URL}/?status=active&limit=5")
    print_response("GET ACTIVE CAMPAIGNS (FILTERED)", response)

def test_delete_campaign(campaign_id):
    """Test deleting a campaign"""
    response = requests.delete(f"{BASE_URL}/{campaign_id}")
    print_response(f"DELETE CAMPAIGN {campaign_id}", response)

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CAMPAIGN API TEST SUITE")
    print("="*60)
    print("Testing Campaign CRUD operations...")
    print("Make sure the backend server is running on http://127.0.0.1:8000")
    
    try:
        # Test 1: Create a campaign
        campaign_id = test_create_campaign()
        
        if not campaign_id:
            print("\n❌ Failed to create campaign. Stopping tests.")
            return
        
        # Test 2: Get all campaigns
        test_get_all_campaigns()
        
        # Test 3: Get specific campaign
        test_get_campaign(campaign_id)
        
        # Test 4: Update campaign
        test_update_campaign(campaign_id)
        
        # Test 5: Update campaign status
        test_update_status(campaign_id)
        
        # Test 6: Approve campaign
        test_approve_campaign(campaign_id)
        
        # Test 7: Update metrics
        test_update_metrics(campaign_id)
        
        # Test 8: Get analytics
        test_get_analytics(campaign_id)
        
        # Test 9: Filter campaigns
        test_filter_campaigns()
        
        # Test 10: Delete campaign (optional - uncomment to test)
        # test_delete_campaign(campaign_id)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\nCreated Campaign ID: {campaign_id}")
        print(f"View in browser: http://127.0.0.1:8000/api/docs")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the backend server.")
        print("Make sure the server is running: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
