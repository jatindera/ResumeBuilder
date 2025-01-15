DOCKER AND CI/CD SETUP GUIDE
===========================

TABLE OF CONTENTS
----------------
1. Docker Setup
2. CI/CD Configuration
3. Deployment Instructions
4. Monitoring

1. DOCKER SETUP
--------------

ONE-LINE DOCKER SETUP:
# Build and run
docker-compose up --build -d

# View logs
docker-compose logs -f

ESSENTIAL DOCKER FILES:

A. Dockerfile
------------
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

B. docker-compose.yml
--------------------
version: '3.8'

services:
  web:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      - db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:14-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:

COMMON DOCKER COMMANDS:
---------------------
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes
docker-compose down -v

2. CI/CD CONFIGURATION
---------------------

GITHUB ACTIONS SETUP:

A. .github/workflows/main.yml
----------------------------
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r backend/requirements.txt
        
    - name: Run tests
      env:
        POSTGRES_USER: test_user
        POSTGRES_PASSWORD: test_password
        POSTGRES_DB: test_db
        POSTGRES_HOST: localhost
      run: |
        cd backend
        pytest

B. Deployment Script (scripts/deploy.sh)
--------------------------------------
#!/bin/bash

# Pull latest changes
git pull origin main

# Build and restart containers
docker-compose up -d --build

# Run migrations
docker-compose exec web alembic upgrade head

# Clear cache
docker-compose exec web python -c "import cache; cache.clear_all()"

# Health check
curl -f http://localhost:8000/api/v1/health

3. DEPLOYMENT INSTRUCTIONS
-------------------------

REQUIRED GITHUB SECRETS:
- HOST: Your server IP
- USERNAME: SSH username
- SSH_KEY: SSH private key
- DOCKER_USERNAME: Docker Hub username
- DOCKER_PASSWORD: Docker Hub password

SERVER SETUP COMMANDS:
--------------------
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

DEPLOYMENT COMMANDS:
------------------
# Manual deploy
./scripts/deploy.sh

# View deployment logs
docker-compose logs -f

# Rollback to previous version
git reset --hard HEAD^
./scripts/deploy.sh

4. MONITORING
------------

START MONITORING STACK:
# Launch monitoring services
docker-compose -f docker-compose.monitoring.yml up -d

ACCESS URLS:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

ADDITIONAL RESOURCES
-------------------
1. DOCKER_SETUP.md - Container customization
2. CI_CD_SETUP.md - Deployment configuration
3. MONITORING.md - Observability setup

NOTES
-----
- Always backup data before deployment
- Test in staging environment first
- Monitor logs after deployment
- Keep secrets secure
- Regular security updates

END OF SETUP GUIDE 