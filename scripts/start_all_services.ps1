# PowerShell script to start all Bharat Content AI services
# Run this in PowerShell: .\start_all_services.ps1

Write-Host "🚀 Starting Bharat Content AI - Complete System" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Function to check if a command exists
function Test-Command($command) {
    try {
        if (Get-Command $command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Python
if (Test-Command python) {
    $pythonVersion = python --version
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
if (Test-Command node) {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check Redis
Write-Host ""
Write-Host "📦 Checking Redis..." -ForegroundColor Yellow
$redisCheck = redis-cli ping 2>$null
if ($redisCheck -eq "PONG") {
    Write-Host "✅ Redis is running" -ForegroundColor Green
} else {
    Write-Host "❌ Redis is not running!" -ForegroundColor Red
    Write-Host "Please start Redis first:" -ForegroundColor Yellow
    Write-Host "  - Windows (WSL): wsl -> redis-server" -ForegroundColor Cyan
    Write-Host "  - Or download from: https://github.com/microsoftarchive/redis/releases" -ForegroundColor Cyan
    exit 1
}

# Check PostgreSQL
Write-Host ""
Write-Host "📦 Checking PostgreSQL..." -ForegroundColor Yellow
try {
    $pgCheck = psql -U postgres -c "SELECT 1" 2>$null
    Write-Host "✅ PostgreSQL is running" -ForegroundColor Green
} catch {
    Write-Host "⚠️  PostgreSQL check failed (may still be running)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "🚀 Starting all services..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

# Start Backend - FastAPI
Write-Host "🌐 Starting FastAPI server (port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; Write-Host '🌐 FastAPI Server' -ForegroundColor Cyan; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
Start-Sleep -Seconds 3

# Start Backend - Celery Worker
Write-Host "⚙️  Starting Celery worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; Write-Host '⚙️  Celery Worker' -ForegroundColor Cyan; celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo"
Start-Sleep -Seconds 3

# Start Backend - Flower Monitoring
Write-Host "🌸 Starting Flower monitoring (port 5555)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; Write-Host '🌸 Flower Monitoring' -ForegroundColor Cyan; celery -A app.config.celery_config.celery_app flower --port=5555"
Start-Sleep -Seconds 3

# Start Frontend - Next.js
Write-Host "🎨 Starting Next.js frontend (port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend-new'; Write-Host '🎨 Next.js Frontend' -ForegroundColor Cyan; npm run dev"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""

Write-Host "📍 Service URLs:" -ForegroundColor Cyan
Write-Host "  🌐 Frontend:        http://localhost:3000" -ForegroundColor White
Write-Host "  🔧 Backend API:     http://localhost:8000" -ForegroundColor White
Write-Host "  📚 API Docs:        http://localhost:8000/api/docs" -ForegroundColor White
Write-Host "  🌸 Flower:          http://localhost:5555" -ForegroundColor White
Write-Host "  🗄️  PostgreSQL:      localhost:5432" -ForegroundColor White
Write-Host "  📦 Redis:           localhost:6379" -ForegroundColor White
Write-Host ""

Write-Host "🔍 Health Checks:" -ForegroundColor Cyan
Write-Host "  curl http://localhost:8000/api/monitoring/health" -ForegroundColor White
Write-Host "  curl http://localhost:8000/api/monitoring/circuit-breakers" -ForegroundColor White
Write-Host "  curl http://localhost:8000/api/monitoring/system/status" -ForegroundColor White
Write-Host ""

Write-Host "📝 To stop services:" -ForegroundColor Yellow
Write-Host "  - Close each PowerShell window" -ForegroundColor White
Write-Host "  - Or press Ctrl+C in each window" -ForegroundColor White
Write-Host ""

Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "  - PROJECT_RESTART_GUIDE.md" -ForegroundColor White
Write-Host "  - backend/QUICK_START.md" -ForegroundColor White
Write-Host "  - backend/API_DOCUMENTATION.md" -ForegroundColor White
Write-Host ""

Write-Host "🎉 System is ready! Happy coding!" -ForegroundColor Green
Write-Host ""

# Wait for user input before closing
Write-Host "Press any key to open API documentation in browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open API docs in browser
Start-Process "http://localhost:8000/api/docs"
