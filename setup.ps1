# ============================================================================
# Vidensbank Flask - Quick Setup Script for Windows
# ============================================================================

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "   Vidensbank Flask Application - Quick Setup                    " -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/7] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python not found! Please install Python 3.12+" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "[2/7] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   ℹ Virtual environment already exists, skipping..." -ForegroundColor Blue
} else {
    python -m venv venv
    Write-Host "   ✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/7] Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "   ✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[4/7] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "   ✓ Dependencies installed" -ForegroundColor Green

# Setup environment file
Write-Host ""
Write-Host "[5/7] Setting up environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "   ℹ .env file already exists, skipping..." -ForegroundColor Blue
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "   ✓ .env file created from template" -ForegroundColor Green
    Write-Host "   ⚠ Please edit .env and set your SECRET_KEY!" -ForegroundColor Yellow
}

# Initialize database
Write-Host ""
Write-Host "[6/7] Initializing database..." -ForegroundColor Yellow
$env:FLASK_APP = "app.py"
if (Test-Path "vidensbank.db") {
    Write-Host "   ℹ Database already exists, skipping..." -ForegroundColor Blue
} else {
    flask init-db
    Write-Host "   ✓ Database initialized" -ForegroundColor Green
    
    # Create admin user
    Write-Host "   Creating admin user..." -ForegroundColor Yellow
    flask create-admin
    Write-Host "   ✓ Admin user created (username: admin, password: admin123)" -ForegroundColor Green
}

# Success message
Write-Host ""
Write-Host "[7/7] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "   Next Steps:                                                   " -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Edit .env file and set a secure SECRET_KEY" -ForegroundColor White
Write-Host "   Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the development server:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Open your browser and go to:" -ForegroundColor White
Write-Host "   http://127.0.0.1:5000" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Login with admin credentials:" -ForegroundColor White
Write-Host "   Username: admin" -ForegroundColor Gray
Write-Host "   Password: admin123" -ForegroundColor Gray
Write-Host "   ⚠ Change this password in production!" -ForegroundColor Yellow
Write-Host ""
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "   For deployment to Heroku, see DEPLOYMENT.md                  " -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host ""
