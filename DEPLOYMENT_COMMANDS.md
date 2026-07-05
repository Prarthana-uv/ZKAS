# ⚡ Deployment Quick Commands

Fast reference for deployment commands. Keep this handy!

---

## 🌐 RENDER.COM

### Create Services
```bash
# Create PostgreSQL database
# Go to: render.com → New + → PostgreSQL

# Create Backend Service
# Go to: render.com → New + → Web Service
# Select your GitHub repo
# Name: zkas-api
# Start Command: node backend/app.js

# Create Crypto Service  
# Go to: render.com → New + → Web Service
# Name: zkas-crypto
# Start Command: python crypto/flask_api.py

# Create Frontend
# Go to: render.com → New + → Static Site
# Name: zkas-frontend
# Build: cd frontend && npm install && npm run build
# Publish: frontend/build
```

### View Logs
```
Dashboard → Service → Logs tab
```

### Redeploy
```
Push to GitHub → Auto-deploys!
```

---

## 🔴 HEROKU

### Install CLI
```bash
choco install heroku
# or download from heroku.com/cli
```

### Login
```bash
heroku login
```

### Create App
```bash
heroku create zkas-api
heroku create zkas-crypto
heroku create zkas-frontend
```

### Add Database
```bash
heroku addons:create heroku-postgresql:hobby-dev -a zkas-api
```

### Set Environment Variables
```bash
heroku config:set NODE_ENV=production -a zkas-api
heroku config:set DATABASE_URL=your_url -a zkas-api
heroku config:set FLASK_ENV=production -a zkas-crypto
```

### View Variables
```bash
heroku config -a zkas-api
```

### Deploy
```bash
git push heroku main
```

### View Logs
```bash
heroku logs -a zkas-api --tail
heroku logs -a zkas-api -n 100  # Last 100 lines
```

### Open App
```bash
heroku open -a zkas-api
```

---

## 🐳 DOCKER

### Build Images
```bash
# Backend
docker build -t zkas-api:latest -f Dockerfile.backend .

# Crypto
docker build -t zkas-crypto:latest -f Dockerfile.crypto .

# Frontend
docker build -t zkas-frontend:latest frontend/
```

### Run Container
```bash
docker run -p 3000:3000 zkas-api:latest
```

### Docker Compose (All Services)
```bash
docker-compose up -d          # Start all
docker-compose down           # Stop all
docker-compose logs -f        # View logs
docker-compose ps             # Status
```

### Push to Docker Hub
```bash
docker login
docker tag zkas-api:latest yourusername/zkas-api:latest
docker push yourusername/zkas-api:latest
```

---

## ☁️ AWS

### Configure AWS CLI
```bash
aws configure
# Enter: Access Key, Secret Key, Region, Format
```

### Push to ECR
```bash
# Login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t zkas-api .
docker tag zkas-api:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/zkas-api:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/zkas-api:latest
```

### Create RDS Database
```bash
aws rds create-db-instance \
  --db-instance-identifier zkas-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password Password123!
```

### Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name zkas-prod
```

### Deploy Service
```bash
aws ecs register-task-definition --cli-input-json file://task-def.json
aws ecs create-service --cluster zkas-prod --service-name zkas-api --task-definition zkas-api
```

---

## 🚀 NETLIFY/VERCEL

### Deploy Frontend
```bash
# Build locally
npm run build

# Deploy to Netlify
netlify deploy --prod --dir=build

# Or use web interface:
# netlify.com → New Site → Connect GitHub
```

---

## 💻 DIGITALOCEAN DROPLET

### SSH Into Droplet
```bash
ssh root@your_droplet_ip
```

### Setup Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Install Docker Compose
```bash
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### Clone and Deploy
```bash
git clone https://github.com/yourusername/zkas.git
cd zkas
cp .env.example .env
nano .env  # Edit variables
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f
docker logs container_name
```

---

## 🔍 DEBUGGING COMMANDS

### Test Connection
```bash
# Test backend API
curl https://your-api.example.com/api/health

# Test database
psql $DATABASE_URL

# Test local server
curl http://localhost:3000/api/health
```

### Find Port Usage
```bash
# Windows
netstat -ano | findstr :3000

# Mac/Linux
lsof -i :3000
```

### Kill Process
```bash
# Windows
taskkill /PID <PID> /F

# Mac/Linux
kill -9 <PID>
```

### Check Environment Variables
```bash
# Windows
echo %DATABASE_URL%

# Mac/Linux
echo $DATABASE_URL
```

### Install Dependencies
```bash
# Node
npm install
npm ci  # Cleaner

# Python
pip install -r requirements.txt
```

### Build & Test
```bash
# Backend test
npm start

# Frontend build
npm run build

# Crypto service
python app.py
```

---

## 📊 GIT COMMANDS

### Prepare for Deployment
```bash
# Check status
git status

# Add files
git add .

# Commit
git commit -m "Deploy to production"

# Push
git push origin main
```

### View Git Log
```bash
git log --oneline -10
```

### Undo Last Commit
```bash
git reset --soft HEAD~1
```

### Force Push (Careful!)
```bash
git push origin main --force
```

---

## 🔑 ENVIRONMENT VARIABLES

### Set Variable (All Platforms)

**Backend (Node):**
```javascript
const url = process.env.DATABASE_URL;
```

**Crypto Service (Python):**
```python
import os
url = os.getenv('DATABASE_URL')
```

**Frontend (React):**
```javascript
const url = process.env.REACT_APP_API_URL;
```

### Common Variables
```
DATABASE_URL=postgresql://user:pass@host:5432/db
NODE_ENV=production
PORT=3000
JWT_SECRET=your-secret-key
REACT_APP_API_URL=https://api.example.com
```

---

## 🆘 TROUBLESHOOTING COMMANDS

### View All Containers
```bash
docker ps -a
```

### Remove Container
```bash
docker rm container_id
```

### Check Server Health
```bash
# Backend
curl https://your-api.com/api/health -i

# Status should be: 200 OK
```

### Watch Logs in Real-Time
```bash
# Render/Heroku
heroku logs -a app-name --tail

# Docker
docker-compose logs -f service-name

# DigitalOcean
docker logs -f container_name
```

### Rebuild Without Cache
```bash
docker build --no-cache -t zkas-api .
```

### Restart All Services
```bash
docker-compose restart
```

---

## 📋 TYPICAL DEPLOYMENT WORKFLOW

### 1. Prepare
```bash
npm install
npm run build
git add .
git commit -m "Ready for deployment"
```

### 2. Push
```bash
git push origin main
```

### 3. Deploy
```bash
# Render: Auto-deploys!
# Heroku: git push heroku main
# AWS: docker push & update service
```

### 4. Test
```bash
curl https://your-app.example.com/api/health
```

### 5. Monitor
```bash
heroku logs -a your-app --tail
# or check platform dashboard
```

---

## ⚡ ONE-LINERS

```bash
# Start everything locally
docker-compose up -d && npm start

# Stop everything
docker-compose down

# Check all service status
docker-compose ps

# Rebuild a single service
docker-compose build backend

# Deploy to Heroku
git push heroku main && heroku open

# Test API endpoint
curl -X POST https://api.example.com/api/auth/login -H "Content-Type: application/json" -d "{}"

# SSH and check logs
ssh user@host && tail -f /var/log/app.log

# Copy file to remote server
scp -r ./backend user@host:/app/

# Monitor real-time
watch -n 1 'curl -s https://api.example.com/api/health | jq'
```

---

## 🎯 Quick Platform Commands

| Task | Render | Heroku | AWS |
|------|--------|--------|-----|
| View Logs | Dashboard → Logs | `heroku logs -a app --tail` | CloudWatch |
| Set Variable | Dashboard → Env | `heroku config:set KEY=VAL` | `aws` CLI |
| Redeploy | Push to GitHub | `git push heroku main` | Update service |
| View Status | Dashboard → Logs | `heroku ps -a app` | ECS dashboard |
| Restart | Auto on push | Restart dyno | Scale task |

---

## 📱 Mobile Testing

### Get Local IP
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

### Access from Phone
```
http://192.168.x.x:3000
# (Use your local IP, not localhost)
```

### Test on Same WiFi
```
Phone on same WiFi as computer
Open: http://192.168.x.x:3000
```

---

## 🎓 Learning Resources

```bash
# View command help
docker --help
heroku --help
aws help

# Check version
docker --version
node --version
python --version
```

---

**Bookmark this page for quick reference!** 🔖

Most of your deployment will be:
1. `git push origin main`
2. Check platform dashboard
3. Done! ✅
