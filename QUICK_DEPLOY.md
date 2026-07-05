# 🚀 QUICK DEPLOYMENT GUIDES

## 🎯 Choose Your Platform

Pick one and follow the step-by-step guide below.

---

# 1️⃣ RENDER (RECOMMENDED - Easiest)

## ⏱️ Time: 5-10 minutes

### Step 1: Create Account
```
1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub (connect your account)
```

### Step 2: Create Database
```
1. From Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Fill in:
   - Name: zkas-database
   - Database: zkas
   - User: postgres
   - Region: (choose closest to you)
4. Click "Create Database"
5. Wait for creation (1-2 minutes)
6. Copy the connection string (you'll need this!)
```

### Step 3: Deploy Backend API
```
1. Click "New +" → "Web Service"
2. Select your GitHub repo
3. Configure:
   - Name: zkas-api
   - Environment: Node
   - Branch: main
   - Build Command: cd backend && npm install
   - Start Command: node backend/app.js
4. Under "Advanced", add Environment Variables:
   - DATABASE_URL: (paste your PostgreSQL connection)
   - NODE_ENV: production
5. Click "Create Web Service"
6. Wait for deployment (2-5 minutes)
```

### Step 4: Deploy Crypto Service
```
1. Click "New +" → "Web Service"
2. Select your GitHub repo again
3. Configure:
   - Name: zkas-crypto
   - Environment: Python 3
   - Branch: main
   - Build Command: pip install -r crypto/requirements.txt
   - Start Command: python crypto/flask_api.py
4. Under "Advanced", add Environment Variables:
   - FLASK_ENV: production
5. Click "Create Web Service"
6. Wait for deployment
```

### Step 5: Deploy Frontend
```
1. Click "New +" → "Static Site"
2. Select your GitHub repo
3. Configure:
   - Name: zkas-frontend
   - Build Command: cd frontend && npm install && npm run build
   - Publish Directory: frontend/build
4. Click "Create Static Site"
5. Wait for deployment
```

### Step 6: Update API URLs
Edit `frontend/.env.production` (or create it):
```
REACT_APP_API_URL=https://zkas-api.onrender.com
REACT_APP_CRYPTO_URL=https://zkas-crypto.onrender.com
```

Push to GitHub:
```bash
git add frontend/.env.production
git commit -m "Update API URLs for production"
git push origin main
```

Frontend will auto-redeploy with new URLs.

### ✅ Done!
Your app is live at the Render-provided URLs! 🎉

### Cost: 
- Free tier available
- Paid starts at $7/month

---

# 2️⃣ HEROKU (Legacy, Free Tier Ending)

## ⏱️ Time: 10-15 minutes

### Step 1: Install Heroku CLI
**Windows:**
```bash
# Install using Chocolatey
choco install heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login
```bash
heroku login
# Opens browser for authentication
```

### Step 3: Create Apps
```bash
heroku create zkas-api
heroku create zkas-crypto
heroku create zkas-frontend
```

### Step 4: Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:hobby-dev -a zkas-api
```

### Step 5: Set Environment Variables
```bash
heroku config:set NODE_ENV=production -a zkas-api
heroku config:set DATABASE_URL=$(heroku config:get DATABASE_URL -a zkas-api) -a zkas-api
```

### Step 6: Deploy Backend
```bash
git push heroku main -a zkas-api
```

### Step 7: Deploy Crypto Service
```bash
git push heroku main:master -a zkas-crypto
```

### Step 8: Deploy Frontend
```bash
# Install buildpack
heroku buildpacks:add heroku/nodejs -a zkas-frontend

# Deploy
git push heroku main -a zkas-frontend
```

### Step 9: Update URLs
```bash
# Get your Heroku app URLs
heroku apps -A

# Update frontend to point to Heroku backend
# Edit frontend/.env.production with your Heroku URLs
```

### ✅ Done!

### Cost: 
- Free tier ending
- Now requires paid dynos ($7+/month)

---

# 3️⃣ AWS (Production-Grade)

## ⏱️ Time: 20-30 minutes

### Prerequisites
```bash
# Install AWS CLI
choco install awscli

# Configure credentials
aws configure
# Enter: Access Key, Secret Access Key, Region (us-east-1), Output format (json)
```

### Step 1: Push Docker Images
```bash
# Authenticate with AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
cd backend
docker build -t zkas-api:latest .
docker tag zkas-api:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/zkas-api:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/zkas-api:latest

# Build and push crypto service
cd ../crypto
docker build -t zkas-crypto:latest .
docker tag zkas-crypto:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/zkas-crypto:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/zkas-crypto:latest

cd ..
```

### Step 2: Create RDS Database
```bash
aws rds create-db-instance \
  --db-instance-identifier zkas-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password MyPassword123! \
  --allocated-storage 20 \
  --publicly-accessible false \
  --storage-type gp2
```

### Step 3: Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name zkas-prod
```

### Step 4: Deploy Services
```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-def.json

# Create service
aws ecs create-service \
  --cluster zkas-prod \
  --service-name zkas-api \
  --task-definition zkas-api:1 \
  --desired-count 1 \
  --launch-type FARGATE
```

### ✅ Done!

### Cost: 
- Pay-as-you-go
- Estimate: $20-50+/month

---

# 4️⃣ NETLIFY (Frontend Only)

## ⏱️ Time: 2-5 minutes

### Step 1: Create Account
```
1. Go to https://netlify.com
2. Click "Sign Up"
3. Choose "GitHub" (connect your account)
```

### Step 2: Deploy Frontend
```
1. Click "Add new site"
2. Select "Import an existing project"
3. Choose your ZKAS GitHub repo
4. Configure:
   - Branch to deploy: main
   - Build command: cd frontend && npm install && npm run build
   - Publish directory: frontend/build
5. Add Environment Variables (optional):
   - REACT_APP_API_URL: https://your-api.com
   - REACT_APP_CRYPTO_URL: https://your-crypto.com
6. Click "Deploy site"
```

### Step 3: Auto-Deploy
Every time you push to GitHub, Netlify auto-deploys! 🚀

### ✅ Done!

### Cost: 
- Free tier available
- Pro: $19/month

---

# 5️⃣ VERCEL (Frontend Only - React Optimized)

## ⏱️ Time: 2-5 minutes

### Step 1: Create Account
```
1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "GitHub" (connect your account)
```

### Step 2: Import Project
```
1. Click "New Project"
2. Select your ZKAS GitHub repo
3. Vercel auto-detects it's a React app
4. Configure:
   - Framework: Create React App
   - Build Command: (auto-detected)
   - Output Directory: frontend/build
5. Add Environment Variables:
   - REACT_APP_API_URL: your-api-url
   - REACT_APP_CRYPTO_URL: your-crypto-url
6. Click "Deploy"
```

### ✅ Done!

### Cost: 
- Free tier
- Pro: $20/month

---

# 6️⃣ DIGITALOCEAN (Full Control)

## ⏱️ Time: 15-20 minutes

### Step 1: Create Account
```
1. Go to https://digitalocean.com
2. Sign up
```

### Step 2: Create Droplet
```
1. Click "Create" → "Droplet"
2. Choose:
   - OS: Ubuntu 22.04
   - Size: Basic ($4/month)
   - Region: Closest to you
3. Create
```

### Step 3: Connect via SSH
```bash
ssh root@your_droplet_ip
```

### Step 4: Install Docker & Setup
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Install Git
apt install -y git

# Clone your repo
git clone https://github.com/yourusername/zkas.git
cd zkas
```

### Step 5: Setup Environment
```bash
# Create .env file
cp .env.example .env

# Edit with your values
nano .env

# Save: Ctrl+X, then Y, then Enter
```

### Step 6: Start Services
```bash
docker-compose up -d
```

### Step 7: Setup Domain (Optional)
```bash
# Point your domain's DNS to DigitalOcean nameservers
# Then update your docker-compose.yml with domain names
```

### ✅ Done!

### Cost: 
- $4-12+/month

---

# 🔗 After Deployment

## Test Your Live App
```
1. Visit your deployed frontend URL
2. Try registering a new user
3. Try logging in with ZKP proof
4. Check browser console (F12) for errors
```

## Monitor Logs
```bash
# Render: Dashboard → Logs tab
# Heroku: heroku logs -a zkas-api --tail
# AWS: CloudWatch
# DigitalOcean: docker logs container_id
```

## Update Code
```bash
# Make changes locally
git add .
git commit -m "Your message"
git push origin main

# Most platforms auto-redeploy!
# (Render, Netlify, Vercel, Heroku)
```

---

# 🆘 Common Issues & Fixes

### "Build failed"
```
1. Check your build command is correct
2. Test locally: npm run build
3. Make sure package.json exists
4. Check logs for specific errors
```

### "Database connection failed"
```
1. Verify DATABASE_URL is correct
2. Check database is running
3. Check firewall allows connections
4. Test connection locally first
```

### "Static files not loading"
```
1. Check public folder exists
2. Verify build output path
3. Check CORS headers in backend
4. Clear browser cache (Ctrl+Shift+Delete)
```

### "API returns 404"
```
1. Verify backend URL is correct
2. Check endpoint exists in code
3. Check request method (GET vs POST)
4. Verify request body format
```

---

# 📞 Get Help

- **Render Support:** render.com/support
- **Heroku Help:** devcenter.heroku.com
- **AWS Documentation:** aws.amazon.com/documentation
- **Netlify Docs:** docs.netlify.com
- **DigitalOcean Tutorials:** digitalocean.com/tutorials

---

**Ready to deploy? Pick a platform and let's go! 🚀**
