# Campaign API Documentation

## Overview
The Campaign API provides complete CRUD (Create, Read, Update, Delete) operations for managing marketing campaigns. This API is designed for Creator Management and Social Media Collaboration platforms.

## Base URL
```
http://127.0.0.1:8000/api/campaigns
```

## Campaign Model

### Campaign Status
- `draft` - Campaign is being planned
- `active` - Campaign is currently running
- `paused` - Campaign is temporarily paused
- `completed` - Campaign has finished
- `cancelled` - Campaign was cancelled

### Campaign Types
- `influencer` - Influencer marketing campaign
- `brand` - Brand awareness campaign
- `product_launch` - Product launch campaign
- `awareness` - General awareness campaign
- `engagement` - Engagement-focused campaign
- `conversion` - Conversion-focused campaign

## API Endpoints

### 1. Create Campaign
**POST** `/api/campaigns/`

Create a new marketing campaign.

**Request Body:**
```json
{
  "user_id": 1,
  "name": "Summer Product Launch 2024",
  "description": "Launch campaign for our new summer collection",
  "campaign_type": "product_launch",
  "status": "draft",
  "objectives": ["Increase brand awareness", "Drive sales"],
  "target_audience": {
    "age_range": "18-35",
    "interests": ["fashion", "lifestyle"],
    "location": ["India", "USA"]
  },
  "budget": 50000.00,
  "currency": "USD",
  "start_date": "2024-06-01T00:00:00",
  "end_date": "2024-08-31T23:59:59",
  "platforms": ["instagram", "facebook", "twitter"],
  "content_guidelines": "Use bright colors, summer vibes, include product shots",
  "hashtags": ["#SummerVibes", "#NewCollection", "#Fashion2024"],
  "mentions": ["@brandname"],
  "creator_ids": [101, 102, 103],
  "min_followers": 10000,
  "max_creators": 10,
  "target_reach": 1000000,
  "target_impressions": 5000000,
  "target_engagement_rate": 3.5,
  "target_conversions": 5000,
  "requires_approval": true,
  "brand_assets": ["https://example.com/logo.png", "https://example.com/banner.jpg"],
  "landing_page_url": "https://example.com/summer-collection",
  "tracking_links": ["https://example.com/track?utm_campaign=summer2024"],
  "team_members": [1, 2, 3],
  "notes": "Focus on Instagram Stories and Reels"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Summer Product Launch 2024",
  "description": "Launch campaign for our new summer collection",
  "campaign_type": "product_launch",
  "status": "draft",
  "objectives": ["Increase brand awareness", "Drive sales"],
  "target_audience": {...},
  "budget": 50000.00,
  "currency": "USD",
  "start_date": "2024-06-01T00:00:00",
  "end_date": "2024-08-31T23:59:59",
  "platforms": ["instagram", "facebook", "twitter"],
  "actual_reach": 0,
  "actual_impressions": 0,
  "actual_engagement_rate": 0.0,
  "actual_conversions": 0,
  "total_spent": 0.0,
  "revenue_generated": 0.0,
  "roi": 0.0,
  "approved_by": null,
  "approved_at": null,
  "created_at": "2024-03-01T10:00:00",
  "updated_at": "2024-03-01T10:00:00",
  "is_active": false,
  "days_remaining": 92,
  "budget_spent_percentage": 0.0
}
```

---

### 2. Get All Campaigns
**GET** `/api/campaigns/`

Retrieve all campaigns with optional filters.

**Query Parameters:**
- `user_id` (optional) - Filter by user ID
- `status` (optional) - Filter by status (draft, active, paused, completed, cancelled)
- `campaign_type` (optional) - Filter by campaign type
- `skip` (optional, default: 0) - Number of records to skip (pagination)
- `limit` (optional, default: 100, max: 1000) - Maximum records to return

**Example Request:**
```
GET /api/campaigns/?user_id=1&status=active&limit=10
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Summer Product Launch 2024",
    "status": "active",
    ...
  },
  {
    "id": 2,
    "name": "Holiday Campaign",
    "status": "active",
    ...
  }
]
```

---

### 3. Get Campaign by ID
**GET** `/api/campaigns/{campaign_id}`

Retrieve a specific campaign by its ID.

**Path Parameters:**
- `campaign_id` (required) - The ID of the campaign

**Example Request:**
```
GET /api/campaigns/1
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Summer Product Launch 2024",
  "status": "active",
  "budget": 50000.00,
  "total_spent": 15000.00,
  "roi": 45.5,
  ...
}
```

**Error Response:** `404 Not Found`
```json
{
  "detail": "Campaign with ID 999 not found"
}
```

---

### 4. Update Campaign
**PUT** `/api/campaigns/{campaign_id}`

Update an existing campaign. All fields are optional - only provided fields will be updated.

**Path Parameters:**
- `campaign_id` (required) - The ID of the campaign to update

**Request Body:**
```json
{
  "name": "Updated Campaign Name",
  "budget": 75000.00,
  "end_date": "2024-09-30T23:59:59",
  "status": "active"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Updated Campaign Name",
  "budget": 75000.00,
  "updated_at": "2024-03-01T15:30:00",
  ...
}
```

---

### 5. Update Campaign Metrics
**PATCH** `/api/campaigns/{campaign_id}/metrics`

Update campaign performance metrics. This endpoint is typically called by analytics services to update real-time campaign performance.

**Path Parameters:**
- `campaign_id` (required) - The ID of the campaign

**Request Body:**
```json
{
  "actual_reach": 850000,
  "actual_impressions": 4200000,
  "actual_engagement_rate": 4.2,
  "actual_conversions": 4500,
  "total_spent": 35000.00,
  "revenue_generated": 125000.00
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "actual_reach": 850000,
  "actual_impressions": 4200000,
  "actual_engagement_rate": 4.2,
  "actual_conversions": 4500,
  "total_spent": 35000.00,
  "revenue_generated": 125000.00,
  "roi": 257.14,
  "updated_at": "2024-03-01T16:00:00",
  ...
}
```

---

### 6. Update Campaign Status
**PATCH** `/api/campaigns/{campaign_id}/status`

Update the status of a campaign.

**Path Parameters:**
- `campaign_id` (required) - The ID of the campaign

**Query Parameters:**
- `new_status` (required) - New status value

**Example Request:**
```
PATCH /api/campaigns/1/status?new_status=active
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "status": "active",
  "updated_at": "2024-03-01T17:00:00",
  ...
}
```

---

### 7. Approve Campaign
**PATCH** `/api/campaigns/{campaign_id}/approve`

Approve a campaign for execution.

**Path Parameters:**
- `campaign_id` (required) - The ID of the campaign to approve

**Query Parameters:**
- `approver_id` (required) - The ID of the user approving the campaign

**Example Request:**
```
PATCH /api/campaigns/1/approve?approver_id=5
```

**Response:** `200 OK`
```json
{
  "message": "Campaign approved successfully",
  "campaign_id": 1,
  "approved_by": 5,
  "approved_at": "2024-03-01T18:00:00"
}
```

---

### 8. Delete Campaign
**DELETE** `/api/campaigns/{campaign_id}`

Delete a campaign permanently.

**Path Parameters:**
- `campaign_id` (required) - The ID of the campaign to delete

**Example Request:**
```
DELETE /api/campaigns/1
```

**Response:** `204 No Content`

---

### 9. Get Campaign Analytics
**GET** `/api/campaigns/{campaign_id}/analytics`

Get detailed analytics and performance metrics for a campaign.

**Path Parameters:**
- `campaign_id` (required) - The ID of the campaign

**Example Request:**
```
GET /api/campaigns/1/analytics
```

**Response:** `200 OK`
```json
{
  "campaign_id": 1,
  "campaign_name": "Summer Product Launch 2024",
  "status": "active",
  "is_active": true,
  "days_remaining": 45,
  "budget": {
    "total": 50000.00,
    "spent": 35000.00,
    "remaining": 15000.00,
    "spent_percentage": 70.0
  },
  "performance": {
    "reach": {
      "target": 1000000,
      "actual": 850000,
      "percentage": 85.0
    },
    "impressions": {
      "target": 5000000,
      "actual": 4200000,
      "percentage": 84.0
    },
    "engagement_rate": {
      "target": 3.5,
      "actual": 4.2,
      "percentage": 120.0
    },
    "conversions": {
      "target": 5000,
      "actual": 4500,
      "percentage": 90.0
    }
  },
  "roi": {
    "total_spent": 35000.00,
    "revenue_generated": 125000.00,
    "roi_percentage": 257.14,
    "profit": 90000.00
  },
  "timeline": {
    "start_date": "2024-06-01T00:00:00",
    "end_date": "2024-08-31T23:59:59",
    "created_at": "2024-03-01T10:00:00",
    "updated_at": "2024-03-01T16:00:00"
  }
}
```

---

## Testing the API

### Using cURL (Windows PowerShell)

**Create a Campaign:**
```powershell
$body = @{
    user_id = 1
    name = "Test Campaign"
    campaign_type = "awareness"
    budget = 10000
    start_date = "2024-06-01T00:00:00"
    end_date = "2024-08-31T23:59:59"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/campaigns/" -Method POST -Body $body -ContentType "application/json"
```

**Get All Campaigns:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/campaigns/" -Method GET
```

**Get Campaign by ID:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/campaigns/1" -Method GET
```

**Update Campaign:**
```powershell
$body = @{
    name = "Updated Campaign Name"
    budget = 15000
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/campaigns/1" -Method PUT -Body $body -ContentType "application/json"
```

**Delete Campaign:**
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/campaigns/1" -Method DELETE
```

---

## Interactive API Documentation

Visit the interactive API documentation at:
- **Swagger UI:** http://127.0.0.1:8000/api/docs
- **ReDoc:** http://127.0.0.1:8000/api/redoc

You can test all endpoints directly from the browser using the Swagger UI.

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 404 Not Found
```json
{
  "detail": "Campaign with ID {id} not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Failed to create campaign: error details"
}
```

---

## Campaign Properties

### Computed Properties

The Campaign model includes several computed properties:

- **is_active**: Boolean indicating if the campaign is currently active
- **days_remaining**: Number of days remaining until campaign end
- **budget_spent_percentage**: Percentage of budget spent

These properties are automatically calculated and included in API responses.

---

## Best Practices

1. **Always set start_date and end_date** for campaigns to enable proper tracking
2. **Update metrics regularly** using the `/metrics` endpoint for accurate ROI calculation
3. **Use the analytics endpoint** to get comprehensive performance insights
4. **Set requires_approval to true** for campaigns that need management approval
5. **Track team_members** to manage collaboration and access control
6. **Use tracking_links** with UTM parameters for accurate attribution

---

## Database Schema

The Campaign table includes:
- Basic info (name, description, type, status)
- Budget and timeline
- Target metrics (reach, impressions, engagement, conversions)
- Actual metrics (updated during campaign)
- ROI tracking (spent, revenue, ROI percentage)
- Approval workflow
- Team collaboration
- Timestamps and audit trail

All campaigns are linked to a user (creator/brand) and support multi-user collaboration through team_members.
