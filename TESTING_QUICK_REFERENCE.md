# 🚀 Testing Quick Reference Guide

Quick commands and examples for running tests in Bharat Content AI.

---

## 📋 Table of Contents

1. [Backend Testing Commands](#backend-testing-commands)
2. [Frontend Testing Commands](#frontend-testing-commands)
3. [Common Test Scenarios](#common-test-scenarios)
4. [Debugging Tests](#debugging-tests)
5. [CI/CD Integration](#cicd-integration)

---

## Backend Testing Commands

### Setup
```bash
cd backend
pip install pytest pytest-cov pytest-asyncio httpx
export DATABASE_URL="postgresql://user:pass@localhost/test_db"
```

### Run Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=term

# Specific file
pytest tests/test_routes_content.py

# Specific test class
pytest tests/test_routes_content.py::TestContentGeneration

# Specific test method
pytest tests/test_routes_content.py::TestContentGeneration::test_generate_content_success

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run tests matching pattern
pytest -k "content"
```

### Coverage Reports
```bash
# HTML report
pytest --cov=app --cov-report=html
open htmlcov/index.html

# Terminal report with missing lines
pytest --cov=app --cov-report=term-missing

# XML report (for CI/CD)
pytest --cov=app --cov-report=xml
```

### Test Markers
```bash
# Run only critical tests
pytest -m critical

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Run unit tests only
pytest -m unit
```

---

## Frontend Testing Commands

### Setup
```bash
cd frontend-new
npm install --save-dev @testing-library/react @testing-library/jest-dom cypress
```

### Jest Unit Tests
```bash
# Run all tests
npm run test

# With coverage
npm run test -- --coverage

# Watch mode
npm run test -- --watch

# Specific file
npm run test -- GenerateContent.test.tsx

# Update snapshots
npm run test -- -u

# Verbose output
npm run test -- --verbose
```

### Cypress E2E Tests
```bash
# Open Cypress Test Runner (interactive)
npm run cypress:open

# Run all E2E tests (headless)
npm run cypress:run

# Run specific test file
npm run cypress:run -- --spec "cypress/e2e/content-generation.cy.ts"

# Run with specific browser
npm run cypress:run -- --browser chrome

# Record test run
npm run cypress:run -- --record --key <record-key>
```

---

## Common Test Scenarios

### Test AI Content Generation
```bash
# Backend
pytest tests/test_routes_content.py::TestContentGeneration::test_generate_content_success -v

# Frontend
npm run test -- GenerateContent.test.tsx
```

### Test Authentication
```bash
# Backend
pytest tests/test_auth.py -v

# Frontend
npm run cypress:run -- --spec "cypress/e2e/auth.cy.ts"
```

### Test Campaign Management
```bash
# Backend
pytest tests/test_routes_campaigns.py -v

# Frontend
npm run test -- CampaignsContent.test.tsx
```

### Test Team Collaboration
```bash
# Backend
pytest tests/test_routes_teams.py -v

# Frontend
npm run test -- TeamContent.test.tsx
```

### Test Post Scheduling
```bash
# Backend
pytest tests/test_routes_social.py -v

# Frontend
npm run test -- ScheduleContent.test.tsx
```

---

## Debugging Tests

### Backend Debugging

**Print Debug Output:**
```bash
# Show print statements
pytest -s

# Show captured output on failure
pytest --capture=no
```

**Use Python Debugger:**
```python
# Add to test
import pdb; pdb.set_trace()

# Run with debugger
pytest --pdb
```

**Verbose Logging:**
```bash
# Show all logs
pytest --log-cli-level=DEBUG
```

### Frontend Debugging

**Jest Debugging:**
```bash
# Run single test with debugging
node --inspect-brk node_modules/.bin/jest --runInBand GenerateContent.test.tsx

# Then open chrome://inspect in Chrome
```

**Cypress Debugging:**
```javascript
// Add to test
cy.pause()  // Pause test execution
cy.debug()  // Debug current subject
```

**Console Logs:**
```bash
# Show console output
npm run test -- --verbose
```

---

## CI/CD Integration

### GitHub Actions

**Backend Tests:**
```yaml
- name: Run Backend Tests
  run: |
    cd backend
    pytest tests/ --cov=app --cov-report=xml
    
- name: Upload Coverage
  uses: codecov/codecov-action@v2
  with:
    file: ./backend/coverage.xml
```

**Frontend Tests:**
```yaml
- name: Run Frontend Tests
  run: |
    cd frontend-new
    npm run test -- --coverage
    npm run cypress:run
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash

echo "Running tests before commit..."

# Backend tests
cd backend
pytest tests/ --cov=app --cov-fail-under=80
if [ $? -ne 0 ]; then
    echo "Backend tests failed. Commit aborted."
    exit 1
fi

# Frontend tests
cd ../frontend-new
npm run test -- --coverage --watchAll=false
if [ $? -ne 0 ]; then
    echo "Frontend tests failed. Commit aborted."
    exit 1
fi

echo "All tests passed!"
exit 0
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Test Data & Fixtures

### Backend Test Fixtures

**Create Test User:**
```python
@pytest.fixture
def test_user(db_session):
    user = User(email="test@example.com", username="testuser")
    db_session.add(user)
    db_session.commit()
    return user
```

**Create Auth Token:**
```python
@pytest.fixture
def auth_token(test_user):
    return create_access_token({"sub": test_user.id})
```

**Mock AI Service:**
```python
@pytest.fixture
def mock_ai_service(monkeypatch):
    def mock_generate(*args, **kwargs):
        return {"content": "Test content", "model_used": "gemini"}
    monkeypatch.setattr("app.services.ai_service_manager.generate", mock_generate)
```

### Frontend Test Utilities

**Mock API Calls:**
```typescript
jest.mock('@/lib/api')

beforeEach(() => {
  (fetchAPI as jest.Mock).mockResolvedValue({
    ok: true,
    json: async () => ({ data: 'test' })
  })
})
```

**Custom Render:**
```typescript
const customRender = (ui: React.ReactElement) => {
  return render(ui, {
    wrapper: ({ children }) => (
      <AuthProvider>
        <ThemeProvider>{children}</ThemeProvider>
      </AuthProvider>
    )
  })
}
```

---

## Performance Testing

### Load Testing with Locust

**Run Load Test:**
```bash
cd backend/tests/load
locust -f locustfile.py --host=http://localhost:8000

# Headless mode
locust -f locustfile.py --host=http://localhost:8000 \
  --users 100 --spawn-rate 10 --run-time 5m --headless
```

**View Results:**
- Open browser: http://localhost:8089
- Set number of users and spawn rate
- Click "Start swarming"

---

## Troubleshooting

### Common Issues

**Issue: Tests fail with database errors**
```bash
# Solution: Reset test database
dropdb bharat_content_test
createdb bharat_content_test
cd backend && alembic upgrade head
```

**Issue: Import errors in tests**
```bash
# Solution: Install package in editable mode
cd backend
pip install -e .
```

**Issue: Cypress tests timeout**
```javascript
// Solution: Increase timeout
cy.get('[data-testid="element"]', { timeout: 10000 })
```

**Issue: Jest tests fail with module not found**
```bash
# Solution: Clear Jest cache
npm run test -- --clearCache
```

---

## Best Practices

### Writing Tests
- ✅ Use descriptive test names
- ✅ Follow AAA pattern (Arrange, Act, Assert)
- ✅ Test one thing per test
- ✅ Use fixtures for test data
- ✅ Mock external dependencies
- ✅ Clean up after tests

### Test Organization
- ✅ Group related tests in classes
- ✅ Use consistent naming conventions
- ✅ Keep tests close to source code
- ✅ Separate unit, integration, and E2E tests

### Maintenance
- ✅ Keep tests fast (< 2 min for unit tests)
- ✅ Fix flaky tests immediately
- ✅ Update tests when code changes
- ✅ Review test coverage regularly

---

## Quick Links

- **Full Testing Matrix:** `COMPREHENSIVE_TESTING_MATRIX.md`
- **Implementation Summary:** `TESTING_IMPLEMENTATION_SUMMARY.md`
- **Performance Optimization:** `COMPLETE_PERFORMANCE_OPTIMIZATION.md`
- **Security Implementation:** `COMPLETE_SECURITY_IMPLEMENTATION.md`

---

**Last Updated:** March 2, 2026  
**Version:** 1.0
