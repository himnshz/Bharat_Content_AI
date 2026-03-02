# 🔄 Testing Workflow Guide

Visual guide to the testing workflow for Bharat Content AI.

---

## 📋 Development Workflow with Testing

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT WORKFLOW                      │
└─────────────────────────────────────────────────────────────┘

1. WRITE CODE
   │
   ├─→ Create new feature/fix bug
   │
   └─→ Write code in backend/ or frontend-new/

2. WRITE TESTS
   │
   ├─→ Backend: Create test file in backend/tests/
   │   └─→ test_routes_*.py, test_services_*.py
   │
   └─→ Frontend: Create test file in __tests__/
       └─→ ComponentName.test.tsx

3. RUN TESTS LOCALLY
   │
   ├─→ Backend: pytest tests/ --cov=app
   │   └─→ Check coverage: Should be ≥ 80%
   │
   └─→ Frontend: npm run test -- --coverage
       └─→ Check coverage: Should be ≥ 75%

4. COMMIT CODE
   │
   ├─→ Pre-commit hook runs tests
   │   └─→ If tests fail: Fix issues, go back to step 3
   │
   └─→ If tests pass: Commit proceeds

5. PUSH TO GITHUB
   │
   └─→ GitHub Actions CI/CD triggered

6. CI/CD PIPELINE
   │
   ├─→ Run backend tests
   ├─→ Run frontend tests
   ├─→ Run E2E tests
   ├─→ Generate coverage reports
   ├─→ Upload to Codecov
   │
   └─→ If all pass: Ready for merge

7. CODE REVIEW
   │
   ├─→ Reviewer checks code quality
   ├─→ Reviewer checks test coverage
   └─→ Reviewer approves or requests changes

8. MERGE TO MAIN
   │
   └─→ Deploy to staging/production
```

---

## 🧪 Test Types & When to Use

```
┌─────────────────────────────────────────────────────────────┐
│                      TEST PYRAMID                            │
└─────────────────────────────────────────────────────────────┘

                    ▲
                   ╱ ╲
                  ╱   ╲
                 ╱ E2E ╲          10% - Slow, Expensive
                ╱───────╲         Test complete user flows
               ╱         ╲        Example: Login → Generate → Schedule
              ╱───────────╲
             ╱             ╲
            ╱ Integration  ╲     20% - Medium Speed
           ╱───────────────╲     Test component interactions
          ╱                 ╲    Example: API → Service → Database
         ╱───────────────────╲
        ╱                     ╲
       ╱      Unit Tests      ╲  70% - Fast, Cheap
      ╱───────────────────────╲  Test individual functions
     ╱                         ╲ Example: validate_prompt(), create_token()
    ╱___________________________╲
```

### When to Write Each Type

**Unit Tests (70% of tests)**
- ✅ Testing individual functions
- ✅ Testing class methods
- ✅ Testing utility functions
- ✅ Testing validation logic
- ✅ Fast execution (< 1 second each)

**Integration Tests (20% of tests)**
- ✅ Testing API endpoints
- ✅ Testing database operations
- ✅ Testing service interactions
- ✅ Testing authentication flow
- ✅ Medium execution (1-5 seconds each)

**E2E Tests (10% of tests)**
- ✅ Testing complete user flows
- ✅ Testing critical business processes
- ✅ Testing UI interactions
- ✅ Testing cross-browser compatibility
- ✅ Slow execution (10-30 seconds each)

---

## 🔄 Test-Driven Development (TDD) Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    TDD CYCLE (RED-GREEN-REFACTOR)            │
└─────────────────────────────────────────────────────────────┘

1. RED - Write Failing Test
   │
   ├─→ Write test for new feature
   ├─→ Test should fail (feature doesn't exist yet)
   └─→ Example: test_generate_content_success()

2. GREEN - Make Test Pass
   │
   ├─→ Write minimal code to make test pass
   ├─→ Don't worry about perfection
   └─→ Example: Implement generate_content() function

3. REFACTOR - Improve Code
   │
   ├─→ Clean up code
   ├─→ Remove duplication
   ├─→ Improve readability
   └─→ Tests still pass

4. REPEAT
   │
   └─→ Go back to step 1 for next feature

Benefits:
✅ Better code design
✅ Higher test coverage
✅ Fewer bugs
✅ Easier refactoring
```

---

## 🚦 CI/CD Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    GITHUB ACTIONS PIPELINE                   │
└─────────────────────────────────────────────────────────────┘

TRIGGER: Push to branch or Pull Request
   │
   ├─→ Checkout code
   │
   ├─→ Setup Python 3.11
   │
   ├─→ Setup Node.js 18
   │
   ├─→ Install dependencies
   │   ├─→ Backend: pip install -r requirements.txt
   │   └─→ Frontend: npm ci
   │
   ├─→ Run Backend Tests
   │   ├─→ pytest tests/ --cov=app --cov-report=xml
   │   ├─→ Check coverage ≥ 80%
   │   └─→ If fail: ❌ Pipeline fails
   │
   ├─→ Run Frontend Tests
   │   ├─→ npm run test -- --coverage
   │   ├─→ Check coverage ≥ 75%
   │   └─→ If fail: ❌ Pipeline fails
   │
   ├─→ Run E2E Tests
   │   ├─→ npm run cypress:run
   │   └─→ If fail: ❌ Pipeline fails
   │
   ├─→ Upload Coverage Reports
   │   └─→ Codecov
   │
   ├─→ Run Security Scan
   │   └─→ Check for vulnerabilities
   │
   └─→ If all pass: ✅ Ready to merge

MERGE TO MAIN
   │
   ├─→ Deploy to Staging
   │   ├─→ Run smoke tests
   │   └─→ If pass: Deploy to Production
   │
   └─→ Monitor production metrics
```

---

## 🎯 Feature Development Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              FEATURE: AI Content Generation                  │
└─────────────────────────────────────────────────────────────┘

STEP 1: Plan
   │
   ├─→ Review requirements
   ├─→ Identify test scenarios
   └─→ Check COMPREHENSIVE_TESTING_MATRIX.md

STEP 2: Write Tests (TDD)
   │
   ├─→ Unit Tests
   │   ├─→ test_generate_content_success()
   │   ├─→ test_generate_content_quota_exceeded()
   │   ├─→ test_generate_content_invalid_prompt()
   │   └─→ test_generate_content_ai_service_failure()
   │
   ├─→ Integration Tests
   │   └─→ test_full_content_generation_flow()
   │
   └─→ E2E Tests
       └─→ test_user_generates_and_schedules_content()

STEP 3: Implement Feature
   │
   ├─→ Backend: routes/content.py
   ├─→ Service: ai_service_manager_v2.py
   └─→ Frontend: GenerateContent.tsx

STEP 4: Run Tests
   │
   ├─→ pytest tests/test_routes_content.py -v
   ├─→ npm run test -- GenerateContent.test.tsx
   └─→ Fix any failures

STEP 5: Check Coverage
   │
   ├─→ pytest --cov=app.routes.content --cov-report=term
   ├─→ Ensure ≥ 85% coverage
   └─→ Add more tests if needed

STEP 6: Manual Testing
   │
   ├─→ Follow test cases in COMPREHENSIVE_TESTING_MATRIX.md
   ├─→ Test happy path (Flow 1)
   ├─→ Test edge cases (EC1)
   └─→ Test boundary values (BV1.1)

STEP 7: Code Review
   │
   ├─→ Create Pull Request
   ├─→ CI/CD runs automatically
   ├─→ Reviewer checks code and tests
   └─→ Address feedback

STEP 8: Merge & Deploy
   │
   ├─→ Merge to main
   ├─→ Deploy to staging
   ├─→ Run smoke tests
   └─→ Deploy to production
```

---

## 🐛 Bug Fix Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    BUG FIX WORKFLOW                          │
└─────────────────────────────────────────────────────────────┘

STEP 1: Reproduce Bug
   │
   ├─→ Understand the issue
   ├─→ Identify affected component
   └─→ Create minimal reproduction case

STEP 2: Write Failing Test
   │
   ├─→ Write test that reproduces the bug
   ├─→ Test should fail (bug exists)
   └─→ Example: test_quota_not_decremented_on_error()

STEP 3: Fix Bug
   │
   ├─→ Implement fix
   └─→ Run test - should now pass

STEP 4: Add Regression Tests
   │
   ├─→ Add edge case tests
   ├─→ Add boundary value tests
   └─→ Prevent bug from happening again

STEP 5: Run Full Test Suite
   │
   ├─→ Ensure no other tests broke
   └─→ Check coverage didn't decrease

STEP 6: Deploy Fix
   │
   ├─→ Create PR with bug fix + tests
   ├─→ Fast-track review for critical bugs
   └─→ Deploy to production
```

---

## 📊 Test Coverage Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                 COVERAGE IMPROVEMENT WORKFLOW                │
└─────────────────────────────────────────────────────────────┘

STEP 1: Check Current Coverage
   │
   ├─→ Backend: pytest --cov=app --cov-report=html
   ├─→ Frontend: npm run test -- --coverage
   └─→ Open coverage report in browser

STEP 2: Identify Gaps
   │
   ├─→ Find files with < 80% coverage
   ├─→ Find uncovered lines (red in report)
   └─→ Prioritize critical files

STEP 3: Write Missing Tests
   │
   ├─→ Focus on uncovered branches
   ├─→ Test error handling
   ├─→ Test edge cases
   └─→ Test boundary values

STEP 4: Verify Improvement
   │
   ├─→ Run tests with coverage
   ├─→ Check coverage increased
   └─→ Repeat until target reached

STEP 5: Maintain Coverage
   │
   ├─→ Set coverage threshold in CI/CD
   ├─→ Block PRs that decrease coverage
   └─→ Monitor coverage trends
```

---

## 🔍 Debugging Failed Tests Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                 DEBUGGING FAILED TESTS                       │
└─────────────────────────────────────────────────────────────┘

STEP 1: Identify Failure
   │
   ├─→ Read error message carefully
   ├─→ Check which test failed
   └─→ Check assertion that failed

STEP 2: Run Single Test
   │
   ├─→ Backend: pytest tests/test_file.py::test_name -v
   ├─→ Frontend: npm run test -- test_file.test.tsx
   └─→ Isolate the problem

STEP 3: Add Debug Output
   │
   ├─→ Backend: pytest -s (show print statements)
   ├─→ Frontend: console.log() in test
   └─→ Understand what's happening

STEP 4: Use Debugger
   │
   ├─→ Backend: pytest --pdb (drop into debugger)
   ├─→ Frontend: node --inspect-brk jest
   └─→ Step through code

STEP 5: Check Test Data
   │
   ├─→ Verify fixtures are correct
   ├─→ Check mocks are working
   └─→ Ensure database state is clean

STEP 6: Fix Issue
   │
   ├─→ Fix code or fix test
   ├─→ Run test again
   └─→ Verify it passes

STEP 7: Run Full Suite
   │
   ├─→ Ensure fix didn't break other tests
   └─→ Commit fix
```

---

## 📚 Quick Reference

### Daily Development
```bash
# Before starting work
git pull origin main

# Write code + tests
# ...

# Run tests locally
cd backend && pytest tests/ --cov=app
cd frontend-new && npm run test

# Commit and push
git add .
git commit -m "feat: add new feature with tests"
git push origin feature-branch
```

### Before Code Review
```bash
# Run full test suite
pytest tests/ --cov=app --cov-report=html
npm run test -- --coverage

# Check coverage reports
open backend/htmlcov/index.html
open frontend-new/coverage/lcov-report/index.html

# Ensure coverage ≥ targets
# Backend: 80%, Frontend: 75%
```

### Before Merge
```bash
# Ensure CI/CD passes
# Check GitHub Actions status

# Run E2E tests locally
cd frontend-new
npm run cypress:run

# Verify no regressions
```

---

## 🎯 Success Checklist

### For Each Feature
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] E2E tests written and passing (if applicable)
- [ ] Coverage ≥ target (80% backend, 75% frontend)
- [ ] Manual testing completed
- [ ] CI/CD pipeline passes
- [ ] Code review approved
- [ ] Documentation updated

### For Each Bug Fix
- [ ] Reproduction test written
- [ ] Bug fixed
- [ ] Regression tests added
- [ ] All tests passing
- [ ] Coverage maintained or improved
- [ ] CI/CD pipeline passes

---

**Last Updated:** March 2, 2026  
**Version:** 1.0
