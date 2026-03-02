# PowerShell script to check status of all services
# Run this in PowerShell: .\check_system_status.ps1

Write-Host "🔍 Bharat Content AI - System Status Check" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Function to test HTTP endpoint
function Test-Endpoint($url, $name) {
    try {
        $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $name is running" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "❌ $name is not responding" -ForegroundColor Red
        return $false
    }
}

# Check Redis
Write-Host "📦 Checking Redis..." -ForegroundColor Yellow
$redisCheck = redis-cli ping 2>$null
if ($redisCheck -eq "PONG") {
    Write-Host "✅ Redis: Running" -ForegroundColor Green
} else {
    Write-Host "❌ Redis: Not running" -ForegroundColor Red
}
Write-Host ""

# Check PostgreSQL
Write-Host "🗄️  Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $pgCheck = psql -U postgres -c "SELECT version();" 2>$null
    if ($pgCheck) {
        Write-Host "✅ PostgreSQL: Running" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ PostgreSQL: Not running or not accessible" -ForegroundColor Red
}
Write-Host ""

# Check Backend API
Write-Host "🌐 Checking Backend API..." -ForegroundColor Yellow
$backendRunning = Test-Endpoint "http://localhost:8000/api/monitoring/health" "Backend API (port 8000)"
Write-Host ""

# Check Frontend
Write-Host "🎨 Checking Frontend..." -ForegroundColor Yellow
$frontendRunning = Test-Endpoint "http://localhost:3000" "Frontend (port 3000)"
Write-Host ""

# Check Flower
Write-Host "🌸 Checking Flower..." -ForegroundColor Yellow
$flowerRunning = Test-Endpoint "http://localhost:5555" "Flower (port 5555)"
Write-Host ""

# If backend is running, get detailed status
if ($backendRunning) {
    Write-Host "📊 Detailed Backend Status:" -ForegroundColor Cyan
    Write-Host ""
    
    try {
        # Get health status
        Write-Host "  Health Check:" -ForegroundColor Yellow
        $health = Invoke-RestMethod -Uri "http://localhost:8000/api/monitoring/health" -Method GET
        Write-Host "    Status: $($health.status)" -ForegroundColor $(if ($health.status -eq "healthy") { "Green" } else { "Red" })
        Write-Host ""
        
        # Get circuit breaker status
        Write-Host "  Circuit Breakers:" -ForegroundColor Yellow
        $circuits = Invoke-RestMethod -Uri "http://localhost:8000/api/monitoring/circuit-breakers" -Method GET
        Write-Host "    Total: $($circuits.summary.total)" -ForegroundColor White
        Write-Host "    Closed: $($circuits.summary.closed)" -ForegroundColor Green
        Write-Host "    Open: $($circuits.summary.open)" -ForegroundColor $(if ($circuits.summary.open -gt 0) { "Red" } else { "Green" })
        Write-Host ""
        
        # Get AI services status
        Write-Host "  AI Services:" -ForegroundColor Yellow
        $aiServices = Invoke-RestMethod -Uri "http://localhost:8000/api/monitoring/ai-services/health" -Method GET
        Write-Host "    Available: $($aiServices.summary.total_available)" -ForegroundColor White
        Write-Host "    Healthy: $($aiServices.summary.total_healthy)" -ForegroundColor Green
        Write-Host ""
        
        # Get statistics
        Write-Host "  Statistics:" -ForegroundColor Yellow
        $stats = Invoke-RestMethod -Uri "http://localhost:8000/api/monitoring/ai-services/statistics" -Method GET
        Write-Host "    Total Requests: $($stats.total_requests)" -ForegroundColor White
        Write-Host "    Success Rate: $($stats.success_rate)%" -ForegroundColor Green
        Write-Host "    Fallback Rate: $($stats.fallback_rate)%" -ForegroundColor Yellow
        Write-Host ""
    }
    catch {
        Write-Host "  ⚠️  Could not fetch detailed status" -ForegroundColor Yellow
        Write-Host ""
    }
}

# Summary
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host ""

$totalServices = 5
$runningServices = 0

if ($redisCheck -eq "PONG") { $runningServices++ }
if ($pgCheck) { $runningServices++ }
if ($backendRunning) { $runningServices++ }
if ($frontendRunning) { $runningServices++ }
if ($flowerRunning) { $runningServices++ }

Write-Host "  Running Services: $runningServices / $totalServices" -ForegroundColor $(if ($runningServices -eq $totalServices) { "Green" } else { "Yellow" })
Write-Host ""

if ($runningServices -eq $totalServices) {
    Write-Host "✅ All services are running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 System is fully operational!" -ForegroundColor Green
} elseif ($runningServices -gt 0) {
    Write-Host "⚠️  Some services are not running" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 To start missing services, run:" -ForegroundColor Cyan
    Write-Host "   .\start_all_services.ps1" -ForegroundColor White
} else {
    Write-Host "❌ No services are running" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 To start all services, run:" -ForegroundColor Cyan
    Write-Host "   .\start_all_services.ps1" -ForegroundColor White
}

Write-Host ""
Write-Host "📚 For more information, see:" -ForegroundColor Cyan
Write-Host "   PROJECT_RESTART_GUIDE.md" -ForegroundColor White
Write-Host ""
