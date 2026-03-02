#!/bin/bash

# Verification Script for Integration Fixes
# Run this to verify all fixes have been applied correctly

echo "🔍 Verifying Integration Fixes..."
echo "=================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counter for issues
ISSUES=0

# Check 1: No hardcoded URLs
echo "1️⃣  Checking for hardcoded URLs..."
HARDCODED=$(grep -r "http://127.0.0.1:8000" frontend-new/src/components/dashboard/ 2>/dev/null | wc -l)
if [ "$HARDCODED" -eq 0 ]; then
    echo -e "${GREEN}✅ PASS: No hardcoded URLs found${NC}"
else
    echo -e "${RED}❌ FAIL: Found $HARDCODED hardcoded URLs${NC}"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# Check 2: No localStorage userId
echo "2️⃣  Checking for localStorage userId usage..."
LOCALSTORAGE=$(grep -r "localStorage.getItem('userId')" frontend-new/src/components/dashboard/ 2>/dev/null | wc -l)
if [ "$LOCALSTORAGE" -eq 0 ]; then
    echo -e "${GREEN}✅ PASS: No localStorage userId usage found${NC}"
else
    echo -e "${RED}❌ FAIL: Found $LOCALSTORAGE localStorage userId usages${NC}"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# Check 3: All components use fetchAPI
echo "3️⃣  Checking for direct fetch() calls..."
DIRECT_FETCH=$(grep -r "fetch(" frontend-new/src/components/dashboard/ 2>/dev/null | grep -v "fetchAPI" | grep -v "node_modules" | wc -l)
if [ "$DIRECT_FETCH" -eq 0 ]; then
    echo -e "${GREEN}✅ PASS: All components use fetchAPI${NC}"
else
    echo -e "${YELLOW}⚠️  WARNING: Found $DIRECT_FETCH direct fetch() calls (may be acceptable)${NC}"
fi
echo ""

# Check 4: API_ENDPOINTS imported
echo "4️⃣  Checking for API_ENDPOINTS imports..."
IMPORTS=$(grep -r "import.*API_ENDPOINTS.*from.*@/lib/api" frontend-new/src/components/dashboard/ 2>/dev/null | wc -l)
if [ "$IMPORTS" -ge 8 ]; then
    echo -e "${GREEN}✅ PASS: Found $IMPORTS API_ENDPOINTS imports${NC}"
else
    echo -e "${YELLOW}⚠️  WARNING: Only found $IMPORTS API_ENDPOINTS imports (expected 8+)${NC}"
fi
echo ""

# Check 5: fetchAPI imported
echo "5️⃣  Checking for fetchAPI imports..."
FETCH_IMPORTS=$(grep -r "import.*fetchAPI.*from.*@/lib/api" frontend-new/src/components/dashboard/ 2>/dev/null | wc -l)
if [ "$FETCH_IMPORTS" -ge 8 ]; then
    echo -e "${GREEN}✅ PASS: Found $FETCH_IMPORTS fetchAPI imports${NC}"
else
    echo -e "${YELLOW}⚠️  WARNING: Only found $FETCH_IMPORTS fetchAPI imports (expected 8+)${NC}"
fi
echo ""

# Check 6: Error handling added
echo "6️⃣  Checking for error state management..."
ERROR_STATES=$(grep -r "setError\|const \[error" frontend-new/src/components/dashboard/ 2>/dev/null | wc -l)
if [ "$ERROR_STATES" -ge 10 ]; then
    echo -e "${GREEN}✅ PASS: Found $ERROR_STATES error handling implementations${NC}"
else
    echo -e "${YELLOW}⚠️  INFO: Found $ERROR_STATES error handling implementations${NC}"
fi
echo ""

# Check 7: lib/api.ts has required functions
echo "7️⃣  Checking lib/api.ts for required functions..."
if [ -f "frontend-new/src/lib/api.ts" ]; then
    HAS_TOKEN_CHECK=$(grep -c "isTokenExpired" frontend-new/src/lib/api.ts)
    HAS_CLEAR_AUTH=$(grep -c "clearAuthAndRedirect" frontend-new/src/lib/api.ts)
    HAS_FETCH_API=$(grep -c "export async function fetchAPI" frontend-new/src/lib/api.ts)
    
    if [ "$HAS_TOKEN_CHECK" -ge 1 ] && [ "$HAS_CLEAR_AUTH" -ge 1 ] && [ "$HAS_FETCH_API" -ge 1 ]; then
        echo -e "${GREEN}✅ PASS: lib/api.ts has all required functions${NC}"
    else
        echo -e "${RED}❌ FAIL: lib/api.ts missing required functions${NC}"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo -e "${RED}❌ FAIL: lib/api.ts not found${NC}"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# Check 8: Enum mappings fixed
echo "8️⃣  Checking enum mappings..."
if [ -f "frontend-new/src/lib/api.ts" ]; then
    PLATFORM_LOWERCASE=$(grep -c "'facebook': 'facebook'" frontend-new/src/lib/api.ts)
    CONTENT_LOWERCASE=$(grep -c "'social_media': 'social_post'" frontend-new/src/lib/api.ts)
    
    if [ "$PLATFORM_LOWERCASE" -ge 1 ] && [ "$CONTENT_LOWERCASE" -ge 1 ]; then
        echo -e "${GREEN}✅ PASS: Enum mappings use lowercase values${NC}"
    else
        echo -e "${RED}❌ FAIL: Enum mappings not fixed${NC}"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo -e "${RED}❌ FAIL: lib/api.ts not found${NC}"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# Check 9: ScheduleContent field name fixed
echo "9️⃣  Checking ScheduleContent field name fix..."
if [ -f "frontend-new/src/components/dashboard/ScheduleContent.tsx" ]; then
    HAS_TEXT_CONTENT=$(grep -c "text_content:" frontend-new/src/components/dashboard/ScheduleContent.tsx)
    
    if [ "$HAS_TEXT_CONTENT" -ge 1 ]; then
        echo -e "${GREEN}✅ PASS: ScheduleContent uses text_content field${NC}"
    else
        echo -e "${RED}❌ FAIL: ScheduleContent still uses wrong field name${NC}"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo -e "${RED}❌ FAIL: ScheduleContent.tsx not found${NC}"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# Check 10: CalendarContent reschedule endpoint fixed
echo "🔟 Checking CalendarContent reschedule endpoint..."
if [ -f "frontend-new/src/components/dashboard/CalendarContent.tsx" ]; then
    HAS_RESCHEDULE=$(grep -c "/reschedule/" frontend-new/src/components/dashboard/CalendarContent.tsx)
    
    if [ "$HAS_RESCHEDULE" -ge 1 ]; then
        echo -e "${GREEN}✅ PASS: CalendarContent uses correct reschedule endpoint${NC}"
    else
        echo -e "${RED}❌ FAIL: CalendarContent reschedule endpoint not fixed${NC}"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo -e "${RED}❌ FAIL: CalendarContent.tsx not found${NC}"
    ISSUES=$((ISSUES + 1))
fi
echo ""

# Summary
echo "=================================="
echo "📊 VERIFICATION SUMMARY"
echo "=================================="
echo ""

if [ "$ISSUES" -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL CHECKS PASSED!${NC}"
    echo -e "${GREEN}✅ Project is ready for production deployment${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Set NEXT_PUBLIC_API_URL environment variable"
    echo "2. Run: cd frontend-new && npm run build"
    echo "3. Test authentication flow"
    echo "4. Deploy to production"
    exit 0
else
    echo -e "${RED}❌ FOUND $ISSUES CRITICAL ISSUES${NC}"
    echo -e "${RED}⚠️  Please review and fix the issues above${NC}"
    echo ""
    echo "For help, check:"
    echo "- QA_INTEGRATION_REPORT.md"
    echo "- QA_FIX_CHECKLIST.md"
    echo "- PROJECT_UPGRADE_COMPLETE.md"
    exit 1
fi
