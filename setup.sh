#!/bin/bash
# ZKAS Initialization Script
# Sets up the entire system for development or production

set -e

echo "🔐 ZKAS - Zero-Knowledge Authentication System Setup"
echo "======================================================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi

echo -e "${GREEN}✓ Docker and Docker Compose found${NC}"

# Create environment files
echo -e "${BLUE}Setting up environment files...${NC}"

if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo -e "${GREEN}✓ Created backend/.env${NC}"
else
    echo -e "${YELLOW}⚠ backend/.env already exists${NC}"
fi

# Build and start services
echo -e "${BLUE}Building Docker images...${NC}"
docker-compose build

echo -e "${BLUE}Starting services...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${BLUE}Waiting for services to be ready...${NC}"
sleep 10

# Initialize database
echo -e "${BLUE}Initializing database...${NC}"
docker-compose exec -T postgres psql -U postgres -d zkas_db < database/schema.sql 2>/dev/null || true

# Check health
echo -e "${BLUE}Checking service health...${NC}"

if docker-compose exec -T backend curl -f http://localhost:3000/api/health &> /dev/null; then
    echo -e "${GREEN}✓ Backend healthy${NC}"
else
    echo -e "${YELLOW}⚠ Backend not responding yet${NC}"
fi

if docker-compose exec -T crypto-service curl -f http://localhost:5000/health &> /dev/null; then
    echo -e "${GREEN}✓ Crypto service healthy${NC}"
else
    echo -e "${YELLOW}⚠ Crypto service not responding yet${NC}"
fi

echo ""
echo -e "${GREEN}✓ ZKAS Setup Complete!${NC}"
echo ""
echo "Access your application:"
echo -e "  ${BLUE}Frontend:${NC}      http://localhost:3001"
echo -e "  ${BLUE}Backend API:${NC}   http://localhost:3000"
echo -e "  ${BLUE}Crypto Service:${NC} http://localhost:5000"
echo ""
echo "Next steps:"
echo "  1. Visit http://localhost:3001 in your browser"
echo "  2. Register a new account"
echo "  3. Login with your email"
echo ""
echo "To stop services: docker-compose down"
echo "To view logs:     docker-compose logs -f"
echo ""
