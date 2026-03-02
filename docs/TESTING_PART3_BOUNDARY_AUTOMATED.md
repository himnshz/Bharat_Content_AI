# 📏 PART 3: Boundary Value Testing

## Boundary Test 1: Input Length Limits

### BV1.1: Prompt Length
| Test Case | Input Length | Expected Result |
|-----------|-------------|-----------------|
| Minimum valid | 10 chars | ✅ Accepted |
| Just below minimum | 9 chars | ❌ 422 Error: "min_length=10" |
| Normal | 500 chars | ✅ Accepted |
| Maximum valid | 2000 chars | ✅ Accepted |
| Just above maximum | 2001 chars | ❌ 422 Error: "max_length=2000" |
| Extreme | 10000 chars | ❌ 422 Error |

**Test Data:**
```python
# Minimum boundary
prompt_9 = "a" * 9  # Should fail
prompt_10 = "a" * 10  # Should pass

# Maximum boundary
prompt_2000 = "a" * 2000  # Should pass
prompt_2001 = "a" * 2001  # Should fail
```

### BV1.2: Campaign Name Length
| Test Case | Input Length | Expected Result |
|-----------|-------------|-----------------|
| Empty string | 0 chars | ❌ 422 Error: "min_length=1" |
| Minimum valid | 1 char | ✅ Accepted |
| Normal | 50 chars | ✅ Accepted |
| Maximum valid | 255 chars | ✅ Accepted |
| Just above maximum | 256 chars | ❌ 422 Error: "max_length=255" |

### BV1.3: Twitter Post Length
| Test Case | Input Length | Expected Result |
|-----------|-------------|-----------------|
| Normal | 100 chars | ✅ Accepted |
| At limit | 280 chars | ✅ Accepted |
| Just over limit | 281 chars | ❌ 400 Error or auto-truncate |
| Double limit | 560 chars | ❌ 400 Error or auto-truncate |

---

## Boundary Test 2: Numeric Limits

### BV2.1: Campaign Budget
| Test Case | Value | Expected Result |
|-----------|-------|-----------------|
| Negative | -1.00 | ❌ 422 Error: "must be >= 0" |
| Zero | 0.00 | ✅ Accepted (free campaign) |
| Small | 0.01 | ✅ Accepted |
| Normal | 10000.00 | ✅ Accepted |
| Large | 999999999.99 | ✅ Accepted |
| Overflow | 1e15 | ❌ Database overflow or validation error |

### BV2.2: Engagement Rate
| Test Case | Value | Expected Result |
|-----------|-------|-----------------|
| Negative | -1.0 | ❌ Invalid (rate cannot be negative) |
| Zero | 0.0 | ✅ Accepted |
| Low | 0.5 | ✅ Accepted |
| Normal | 4.5 | ✅ Accepted |
| High | 15.0 | ✅ Accepted |
| Unrealistic | 100.0 | ⚠️ Warning but accepted |
| Over 100% | 150.0 | ⚠️ Warning but accepted |

### BV2.3: User Quota Limits
| Tier | Quota | Test at Boundary | Expected Result |
|------|-------|-----------------|-----------------|
| Free | 100 | Generate 99th | ✅ Success |
| Free | 100 | Generate 100th | ✅ Success |
| Free | 100 | Generate 101st | ❌ 429 Quota exceeded |
| Basic | 1000 | Generate 1000th | ✅ Success |
| Basic | 1000 | Generate 1001st | ❌ 429 Quota exceeded |

---

## Boundary Test 3: Date & Time Boundaries

### BV3.1: Post Scheduling Time
| Test Case | Scheduled Time | Expected Result |
|-----------|---------------|-----------------|
| 1 second in past | now() - 1s | ❌ 400 Error: "must be in future" |
| Exactly now | now() | ❌ 400 Error: "must be in future" |
| 1 second in future | now() + 1s | ✅ Accepted |
| 1 hour in future | now() + 1h | ✅ Accepted |
| 1 year in future | now() + 365d | ✅ Accepted |
| 10 years in future | now() + 3650d | ⚠️ Warning but accepted |

**Test Code:**
```python
from datetime import datetime, timedelta

# Boundary tests
past = datetime.utcnow() - timedelta(seconds=1)
now = datetime.utcnow()
future_1s = datetime.utcnow() + timedelta(seconds=1)

# Test each
response_past = schedule_post(scheduled_time=past)  # Should fail
response_now = schedule_post(scheduled_time=now)    # Should fail
response_future = schedule_post(scheduled_time=future_1s)  # Should pass
```

### BV3.2: Campaign Duration
| Test Case | Start Date | End Date | Expected Result |
|-----------|-----------|----------|-----------------|
| Same day | 2026-06-01 | 2026-06-01 | ✅ Accepted (1 day campaign) |
| End before start | 2026-06-01 | 2026-05-31 | ❌ 400 Error: "end must be after start" |
| Normal duration | 2026-06-01 | 2026-08-31 | ✅ Accepted (3 months) |
| Very long | 2026-01-01 | 2030-12-31 | ⚠️ Warning but accepted (5 years) |

### BV3.3: Team Invite Expiration
| Test Case | Expires At | Expected Result |
|-----------|-----------|-----------------|
| Already expired | now() - 1 day | ❌ 400 Error: "Invite expired" |
| Expires today | now() | ❌ 400 Error: "Invite expired" |
| Expires tomorrow | now() + 1 day | ✅ Accepted |
| Standard (7 days) | now() + 7 days | ✅ Accepted |

---

## Boundary Test 4: Collection Sizes

### BV4.1: Bulk Post Scheduling
| Test Case | Number of Platforms | Expected Result |
|-----------|-------------------|-----------------|
| Zero platforms | 0 | ❌ 422 Error: "min_items=1" |
| One platform | 1 | ✅ Accepted |
| All platforms | 7 | ✅ Accepted |
| Duplicate platforms | [instagram, instagram] | ⚠️ Deduplicated or error |

### BV4.2: Campaign Hashtags
| Test Case | Number of Hashtags | Expected Result |
|-----------|-------------------|-----------------|
| No hashtags | [] | ✅ Accepted |
| One hashtag | ["#ai"] | ✅ Accepted |
| Many hashtags | 30 hashtags | ✅ Accepted |
| Too many | 100 hashtags | ⚠️ Performance warning |

### BV4.3: Team Members
| Test Case | Number of Members | Expected Result |
|-----------|------------------|-----------------|
| Owner only | 1 | ✅ Accepted |
| Small team | 5 | ✅ Accepted |
| Medium team | 50 | ✅ Accepted |
| Large team | 500 | ⚠️ Performance impact |
| Extreme | 10000 | ❌ Pagination required |

---

## Boundary Test 5: File Upload Limits

### BV5.1: Media File Size
| Test Case | File Size | Expected Result |
|-----------|-----------|-----------------|
| Empty file | 0 KB | ❌ Error: "File is empty" |
| Tiny file | 1 KB | ✅ Accepted |
| Normal image | 500 KB | ✅ Accepted |
| Large image | 5 MB | ✅ Accepted |
| At limit | 10 MB | ✅ Accepted |
| Over limit | 11 MB | ❌ 413 Error: "File too large" |
| Extreme | 100 MB | ❌ 413 Error: "File too large" |

### BV5.2: CSV Upload for Bulk Operations
| Test Case | Number of Rows | Expected Result |
|-----------|---------------|-----------------|
| Empty CSV | 0 rows | ❌ Error: "No data" |
| One row | 1 row | ✅ Accepted |
| Normal | 100 rows | ✅ Accepted |
| Large | 1000 rows | ✅ Accepted (background task) |
| Very large | 10000 rows | ⚠️ Performance warning |
| Extreme | 100000 rows | ❌ Error: "Too many rows" |

---

# 🤖 PART 4: Automated Test Recommendations

## Backend Testing (Pytest) - 80% Coverage Target

### Critical Files to Test

#### 1. `backend/app/routes/content.py` (Priority: CRITICAL)

**Target Coverage:** 85%

**Unit Tests:**
```python
# tests/test_routes_content.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Content

client = TestClient(app)

class TestContentGeneration:
    """Test content generation endpoints"""
    
    def test_generate_content_success(self, auth_token, mock_ai_service):
        """Test successful content generation"""
        response = client.post(
            "/api/content/generate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "prompt": "Create a post about AI",
                "language": "hindi",
                "tone": "casual",
                "content_type": "social_post"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["generated_content"] is not None
        assert data["language"] == "hindi"
        assert data["model_used"] in ["gemini", "bedrock", "openai"]
    
    def test_generate_content_quota_exceeded(self, auth_token_quota_exceeded):
        """Test quota enforcement"""
        response = client.post(
            "/api/content/generate",
            headers={"Authorization": f"Bearer {auth_token_quota_exceeded}"},
            json={"prompt": "test"}
        )
        assert response.status_code == 429
        assert "quota exceeded" in response.json()["detail"].lower()
    
    def test_generate_content_invalid_prompt(self, auth_token):
        """Test prompt validation"""
        response = client.post(
            "/api/content/generate",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"prompt": "'; DROP TABLE users; --"}
        )
        assert response.status_code == 400
        assert "Invalid prompt" in response.json()["detail"]
    
    def test_generate_content_async(self, auth_token):
        """Test async generation"""
        response = client.post(
            "/api/content/generate/async",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"prompt": "test"}
        )
        assert response.status_code == 202
        assert "task_id" in response.json()
    
    def test_get_generation_status(self, auth_token, task_id):
        """Test task status endpoint"""
        response = client.get(
            f"/api/content/generate/status/{task_id}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 200
        assert response.json()["status"] in ["processing", "completed", "failed"]

# Fixtures
@pytest.fixture
def auth_token(db_session):
    """Create test user and return JWT token"""
    user = User(email="test@example.com", username="testuser")
    db_session.add(user)
    db_session.commit()
    return create_access_token({"sub": user.id})

@pytest.fixture
def mock_ai_service(monkeypatch):
    """Mock AI service to return test content"""
    def mock_generate(*args, **kwargs):
        return {
            "content": "Test generated content",
            "model_used": "gemini-pro",
            "generation_time_ms": 1000
        }
    monkeypatch.setattr("app.services.content_generation.ai_service_manager.generate_content", mock_generate)
```

**Integration Tests:**
```python
# tests/integration/test_content_flow.py

class TestContentGenerationFlow:
    """End-to-end content generation flow"""
    
    def test_full_content_lifecycle(self, client, auth_token):
        """Test: Generate → Edit → Translate → Schedule"""
        # 1. Generate content
        gen_response = client.post("/api/content/generate", ...)
        content_id = gen_response.json()["id"]
        
        # 2. Edit content
        edit_response = client.put(f"/api/content/{content_id}", ...)
        assert edit_response.status_code == 200
        
        # 3. Translate content
        trans_response = client.post("/api/translation/translate", ...)
        assert trans_response.status_code == 201
        
        # 4. Schedule post
        post_response = client.post("/api/social/schedule", ...)
        assert post_response.status_code == 201
```

---

#### 2. `backend/app/services/content_generation/ai_service_manager_v2.py` (Priority: CRITICAL)

**Target Coverage:** 90%

**Unit Tests:**
```python
# tests/test_ai_service_manager.py

import pytest
from app.services.content_generation.ai_service_manager_v2 import (
    EnhancedAIServiceManager, AIServiceError, AIServiceUnavailableError
)

class TestAIServiceManager:
    """Test AI service manager with fallback"""
    
    def test_fallback_chain_built_correctly(self):
        """Test fallback chain prioritization"""
        manager = EnhancedAIServiceManager()
        assert manager.fallback_chain[0].value == "gemini"  # Primary
        assert len(manager.fallback_chain) >= 1
    
    def test_primary_service_success(self, mock_gemini_success):
        """Test successful generation with primary service"""
        manager = EnhancedAIServiceManager()
        result = manager.generate_content_with_fallback(prompt="test")
        assert result["service_used"] == "gemini"
        assert result["fallback_used"] == False
    
    def test_fallback_on_primary_failure(self, mock_gemini_fail, mock_bedrock_success):
        """Test fallback when primary fails"""
        manager = EnhancedAIServiceManager()
        result = manager.generate_content_with_fallback(prompt="test")
        assert result["service_used"] == "bedrock"
        assert result["fallback_used"] == True
        assert result["attempts"] == 2
    
    def test_all_services_fail(self, mock_all_services_fail):
        """Test error when all services fail"""
        manager = EnhancedAIServiceManager()
        with pytest.raises(AIServiceError) as exc_info:
            manager.generate_content_with_fallback(prompt="test")
        assert "All AI services failed" in str(exc_info.value)
    
    def test_circuit_breaker_opens(self, mock_gemini_fail):
        """Test circuit breaker opens after failures"""
        manager = EnhancedAIServiceManager()
        # Trigger 5 failures
        for _ in range(5):
            try:
                manager._call_service_with_circuit_breaker("gemini", "test")
            except:
                pass
        # Check circuit is open
        health = manager.get_service_health()
        assert health["gemini"]["circuit_state"] == "open"
    
    def test_statistics_tracking(self, mock_gemini_success):
        """Test usage statistics"""
        manager = EnhancedAIServiceManager()
        manager.generate_content_with_fallback(prompt="test")
        stats = manager.get_statistics()
        assert stats["total_requests"] == 1
        assert stats["successful_requests"] == 1
        assert stats["service_usage"]["gemini"] == 1
```

---

#### 3. `backend/app/routes/teams.py` (Priority: HIGH)

**Target Coverage:** 80%

**Unit Tests:**
```python
# tests/test_routes_teams.py

class TestTeamManagement:
    """Test team CRUD and role-based access"""
    
    def test_create_team(self, auth_token):
        """Test team creation"""
        response = client.post(
            "/api/teams/",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"name": "Test Team", "description": "Test"}
        )
        assert response.status_code == 201
        assert response.json()["owner_id"] == 1
    
    def test_invite_member_as_owner(self, auth_token, team_id):
        """Test owner can invite members"""
        response = client.post(
            f"/api/teams/{team_id}/invites",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"email": "new@example.com", "role": "editor"}
        )
        assert response.status_code == 201
    
    def test_invite_member_as_viewer_fails(self, viewer_token, team_id):
        """Test viewer cannot invite members"""
        response = client.post(
            f"/api/teams/{team_id}/invites",
            headers={"Authorization": f"Bearer {viewer_token}"},
            json={"email": "new@example.com", "role": "editor"}
        )
        assert response.status_code == 403
    
    def test_get_team_members_with_eager_loading(self, auth_token, team_id):
        """Test N+1 query fix"""
        with assert_num_queries(1):  # Should be 1 query, not N+1
            response = client.get(
                f"/api/teams/{team_id}/members",
                headers={"Authorization": f"Bearer {auth_token}"}
            )
        assert response.status_code == 200
```

---

#### 4. `backend/app/auth/dependencies.py` (Priority: CRITICAL)

**Target Coverage:** 95%

**Unit Tests:**
```python
# tests/test_auth.py

class TestAuthentication:
    """Test JWT authentication"""
    
    def test_create_access_token(self):
        """Test token creation"""
        token = create_access_token({"sub": 1})
        assert token is not None
        payload = verify_token(token)
        assert payload["sub"] == 1
    
    def test_expired_token_rejected(self):
        """Test expired token"""
        token = create_access_token({"sub": 1}, expires_delta=timedelta(seconds=-1))
        with pytest.raises(HTTPException) as exc_info:
            verify_token(token)
        assert exc_info.value.status_code == 401
    
    def test_tampered_token_rejected(self):
        """Test tampered token"""
        token = create_access_token({"sub": 1})
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(HTTPException):
            verify_token(tampered)
    
    def test_quota_enforcement(self, db_session):
        """Test quota limits"""
        user = User(subscription_tier="free", content_generated_count=100)
        assert not check_user_quota(user, "content_generation")
        
        user.content_generated_count = 99
        assert check_user_quota(user, "content_generation")
```

---

## Frontend Testing (Jest + Cypress) - 80% Coverage Target

### Critical Components to Test

#### 1. `frontend-new/src/components/dashboard/GenerateContent.tsx`

**Jest Unit Tests:**
```typescript
// __tests__/GenerateContent.test.tsx

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import GenerateContent from '@/components/dashboard/GenerateContent'
import { fetchAPI } from '@/lib/api'

jest.mock('@/lib/api')

describe('GenerateContent Component', () => {
  it('renders form fields', () => {
    render(<GenerateContent />)
    expect(screen.getByLabelText(/prompt/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/language/i)).toBeInTheDocument()
  })
  
  it('submits form and displays generated content', async () => {
    (fetchAPI as jest.Mock).mockResolvedValue({
      ok: true,
      json: async () => ({ generated_content: 'Test content', id: 123 })
    })
    
    render(<GenerateContent />)
    fireEvent.change(screen.getByLabelText(/prompt/i), {
      target: { value: 'Test prompt' }
    })
    fireEvent.click(screen.getByText(/generate/i))
    
    await waitFor(() => {
      expect(screen.getByText('Test content')).toBeInTheDocument()
    })
  })
  
  it('displays error on API failure', async () => {
    (fetchAPI as jest.Mock).mockResolvedValue({
      ok: false,
      status: 429,
      json: async () => ({ detail: 'Quota exceeded' })
    })
    
    render(<GenerateContent />)
    fireEvent.click(screen.getByText(/generate/i))
    
    await waitFor(() => {
      expect(screen.getByText(/quota exceeded/i)).toBeInTheDocument()
    })
  })
})
```

**Cypress E2E Tests:**
```typescript
// cypress/e2e/content-generation.cy.ts

describe('Content Generation Flow', () => {
  beforeEach(() => {
    cy.login('test@example.com', 'password')
    cy.visit('/dashboard')
  })
  
  it('generates content successfully', () => {
    cy.contains('Generate Content').click()
    cy.get('[data-testid="prompt-input"]').type('Create a post about AI')
    cy.get('[data-testid="language-select"]').select('Hindi')
    cy.get('[data-testid="generate-button"]').click()
    
    cy.get('[data-testid="generated-content"]', { timeout: 20000 })
      .should('be.visible')
      .and('not.be.empty')
  })
  
  it('shows quota exceeded error', () => {
    cy.intercept('POST', '/api/content/generate', {
      statusCode: 429,
      body: { detail: 'Monthly quota exceeded' }
    })
    
    cy.contains('Generate Content').click()
    cy.get('[data-testid="generate-button"]').click()
    cy.contains(/quota exceeded/i).should('be.visible')
  })
})
```

---

#### 2. `frontend-new/src/components/dashboard/CampaignsContent.tsx`

**Jest Tests:**
```typescript
// __tests__/CampaignsContent.test.tsx

describe('CampaignsContent Component', () => {
  it('renders campaign list', async () => {
    render(<CampaignsContent />)
    await waitFor(() => {
      expect(screen.getByText(/campaign pipeline/i)).toBeInTheDocument()
    })
  })
  
  it('handles drag and drop', () => {
    render(<CampaignsContent />)
    const creator = screen.getByText('Sarah Johnson')
    const column = screen.getByText('Negotiating')
    
    fireEvent.dragStart(creator)
    fireEvent.drop(column)
    
    // Verify creator moved to new column
    expect(creator.closest('[data-status="negotiating"]')).toBeInTheDocument()
  })
})
```

---

### Test Coverage Goals

| File | Current Coverage | Target Coverage | Priority |
|------|-----------------|----------------|----------|
| `routes/content.py` | 45% | 85% | CRITICAL |
| `ai_service_manager_v2.py` | 30% | 90% | CRITICAL |
| `routes/teams.py` | 60% | 80% | HIGH |
| `routes/campaigns.py` | 50% | 75% | HIGH |
| `auth/dependencies.py` | 70% | 95% | CRITICAL |
| `routes/social.py` | 55% | 75% | MEDIUM |
| `GenerateContent.tsx` | 40% | 80% | HIGH |
| `CampaignsContent.tsx` | 35% | 75% | MEDIUM |

---

## Test Execution Commands

```bash
# Backend tests
cd backend
pytest tests/ --cov=app --cov-report=html --cov-report=term

# Frontend tests
cd frontend-new
npm run test -- --coverage
npm run test:e2e  # Cypress

# Generate coverage report
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

