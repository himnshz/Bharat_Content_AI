# PowerShell script to start all bulk operations services
# Run this in PowerShell: .\start_bulk_services.ps1

Write-Host "🚀 Starting Bulk Operations Services..." -ForegroundColor Green
Write-Host ""

# Check if Redis is installed
Write-Host "📦 Checking Redis..." -ForegroundColor Yellow
$redisCheck = redis-cli ping 2>$null
if ($redisCheck -ne "PONG") {
    Write-Host "❌ Redis is not running!" -ForegroundColor Red
    Write-Host "Please start Redis first:" -ForegroundColor Yellow
    Write-Host "  - Windows: wsl -> redis-server" -ForegroundColor Cyan
    Write-Host "  - Or download from: https://github.com/microsoftarchive/redis/releases" -ForegroundColor Cyan
    exit 1
}
Write-Host "✅ Redis is running" -ForegroundColor Green
Write-Host ""

# Start FastAPI in new window
Write-Host "🌐 Starting FastAPI server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; uvicorn app.main:app --reload"
Start-Sleep -Seconds 2

# Start Celery worker in new window
Write-Host "⚙️  Starting Celery worker..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; celery -A app.config.celery_config.celery_app worker --loglevel=info --pool=solo"
Start-Sleep -Seconds 2

# Start Flower monitoring in new window
Write-Host "🌸 Starting Flower monitoring..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot'; celery -A app.config.celery_config.celery_app flower"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Service URLs:" -ForegroundColor Cyan
Write-Host "  - FastAPI:  http://localhost:8000" -ForegroundColor White
Write-Host "  - API Docs: http://localhost:8000/api/docs" -ForegroundColor White
Write-Host "  - Flower:   http://localhost:5555" -ForegroundColor White
Write-Host ""
Write-Host "📝 To stop services, close the PowerShell windows" -ForegroundColor Yellow
