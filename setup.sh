#!/bin/bash
# ============================================================================
# Vidensbank Flask - Quick Setup Script for Unix/Linux/macOS
# ============================================================================

echo "=================================================================="
echo "   Vidensbank Flask Application - Quick Setup                    "
echo "=================================================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check Python installation
echo -e "${YELLOW}[1/7] Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "   ${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "   ${RED}✗ Python not found! Please install Python 3.12+${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo -e "${YELLOW}[2/7] Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "   ${BLUE}ℹ Virtual environment already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "   ${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo ""
echo -e "${YELLOW}[3/7] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "   ${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo ""
echo -e "${YELLOW}[4/7] Installing dependencies...${NC}"
pip install -r requirements.txt --quiet
echo -e "   ${GREEN}✓ Dependencies installed${NC}"

# Setup environment file
echo ""
echo -e "${YELLOW}[5/7] Setting up environment configuration...${NC}"
if [ -f ".env" ]; then
    echo -e "   ${BLUE}ℹ .env file already exists, skipping...${NC}"
else
    cp .env.example .env
    echo -e "   ${GREEN}✓ .env file created from template${NC}"
    echo -e "   ${YELLOW}⚠ Please edit .env and set your SECRET_KEY!${NC}"
fi

# Initialize database
echo ""
echo -e "${YELLOW}[6/7] Initializing database...${NC}"
export FLASK_APP=app.py
if [ -f "vidensbank.db" ]; then
    echo -e "   ${BLUE}ℹ Database already exists, skipping...${NC}"
else
    flask init-db
    echo -e "   ${GREEN}✓ Database initialized${NC}"
    
    # Create admin user
    echo -e "   ${YELLOW}Creating admin user...${NC}"
    flask create-admin
    echo -e "   ${GREEN}✓ Admin user created (username: admin, password: admin123)${NC}"
fi

# Success message
echo ""
echo -e "${GREEN}[7/7] Setup complete!${NC}"
echo ""
echo -e "${CYAN}==================================================================${NC}"
echo -e "${CYAN}   Next Steps:                                                   ${NC}"
echo -e "${CYAN}==================================================================${NC}"
echo ""
echo -e "1. Edit .env file and set a secure SECRET_KEY"
echo -e "   Generate one with: python3 -c 'import secrets; print(secrets.token_hex(32))'"
echo ""
echo -e "2. Start the development server:"
echo -e "   python3 app.py"
echo ""
echo -e "3. Open your browser and go to:"
echo -e "   http://127.0.0.1:5000"
echo ""
echo -e "4. Login with admin credentials:"
echo -e "   Username: admin"
echo -e "   Password: admin123"
echo -e "   ${YELLOW}⚠ Change this password in production!${NC}"
echo ""
echo -e "${CYAN}==================================================================${NC}"
echo -e "${CYAN}   For deployment to Heroku, see DEPLOYMENT.md                  ${NC}"
echo -e "${CYAN}==================================================================${NC}"
echo ""
