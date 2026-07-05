# 🚀 ZKAS Deployment Guide

Complete guide to deploy your Zero-Knowledge Authentication System to production platforms.

---

## 📊 Platform Comparison

| Platform | Best For | Cost | Difficulty | Setup Time |
|----------|----------|------|------------|-----------|
| **Heroku** | Full-stack apps | $7-50/month | Easy | 5 mins |
| **Render** | Full-stack apps | $7+/month | Easy | 5 mins |
| **AWS** | Production apps | Pay-as-you-go | Medium | 15 mins |
| **DigitalOcean** | Full control | $5+/month | Medium | 10 mins |
| **Netlify** | Frontend only | Free/paid | Very Easy | 2 mins |
| **Vercel** | Frontend only | Free/paid | Very Easy | 2 mins |
| **Docker Hub** | Container registry | Free | Medium | 10 mins |

---

## 🎯 Quick Choice Guide

### If you want everything in one place:
→ **Render.com** or **Railway.app** (recommended for full-stack)

### If you need maximum free tier:
→ **Heroku** (dying) or **Render** (new & better)

### If you want just the website:
→ **Netlify** or **Vercel** (frontend only)

### If you need production-grade infrastructure:
→ **AWS** or **Google Cloud**

### If you want complete control:
→ **DigitalOcean** + Docker

---

## 📋 Prerequisites (All Platforms)

Before deploying, ensure:

```bash
# 1. Git initialized and pushed to GitHub
git status

# 2. All files committed
git add .
git commit -m "Ready for deployment"

# 3. Pushed to GitHub
git push origin main

# 4. Check your GitHub repo is public or accessible
```

---

# 🌐 DEPLOYMENT OPTIONS

---

## 1️⃣ RENDER.COM (Recommended for Full-Stack)

**Why:** Easiest for full-stack, free tier available, great for PostgreSQL

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Click "Get Started"
3. Sign up with GitHub (recommended)

### Step 2: Create Database
1. Dashboard → "New +"
2. Select "PostgreSQL"
3. Name: `zkas-db`
4. Region: Choose closest to you
5. Click "Create Database"
6. **Copy connection string** (you'll need this)

### Step 3: Deploy Backend API
1. Dashboard → "New +"
2. Select "Web Service"
3. Connect your GitHub repo (ZKAS)
4. Configure:
   - **Name:** `zkas-api`
   - **Environment:** `Node`
   - **Build Command:** `npm install`
   - **Start Command:** `npm start` or `node backend/app.js`
5. Add Environment Variables:
   ```
   DATABASE_URL=<paste your PostgreSQL connection string>
   NODE_ENV=production
   PORT=3000
   ```
6. Click "Create Web Service"

### Step 4: Deploy Frontend
1. Dashboard → "New +"
2. Select "Static Site"
3. Connect your GitHub repo
4. Configure:
   - **Name:** `zkas-frontend`
   - **Build Command:** `npm run build`
   - **Publish Directory:** `frontend/build`
5. Click "Create Static Site"

### Step 5: Deploy Crypto Service (Python)
1. Dashboard → "New +"
2. Select "Web Service"
3. Configure:
   - **Name:** `zkas-crypto`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python crypto/flask_api.py`
4. Add Environment Variables:
   ```
   FLASK_ENV=production
   PORT=5000
   ```
5. Click "Create Web Service"

### Step 6: Update API Endpoints
In your frontend, update:
```javascript
// frontend/src/App.jsx
const BACKEND_URL = "https://zkas-api.onrender.com";
const CRYPTO_URL = "https://zkas-crypto.onrender.com";
```

### Cost: ~$7-15/month

---

## 2️⃣ HEROKU (Classic, Free Tier Ending)

**Why:** Still popular, but free tier being discontinued

### Step 1: Install Heroku CLI
```bash
# Windows (using chocolatey)
choco install heroku-cli

# Or download from heroku.com/cli
```

### Step 2: Login
```bash
heroku login
# Opens browser for authentication
```

### Step 3: Create Apps
```bash
# Backend
heroku create zkas-api
heroku create zkas-crypto
heroku create zkas-frontend

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev -a zkas-api
```

### Step 4: Set Environment Variables
```bash
heroku config:set DATABASE_URL=your_url -a zkas-api
heroku config:set NODE_ENV=production -a zkas-api
```

### Step 5: Deploy
```bash
git push heroku main
heroku open -a zkas-api
```

### Cost: Now requires paid dynos ($7+/month)

---

## 3️⃣ RAILWAY.APP (Modern Alternative)

**Why:** Modern, fast, integrates all services easily

### Step 1: Create Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### Step 2: Create New Project
1. Click "New Project"
2. Select "GitHub Repo"
3. Choose your ZKAS repo

### Step 3: Add Services
Railway auto-detects your services:
- Detects Node.js backend
- Detects Python crypto service
- Can add PostgreSQL from marketplace

### Step 4: Configure
Each service auto-configures, but set:
- **Start Commands** for each service
- **Environment Variables**
- **Port Mappings**

### Step 5: Deploy
Push to GitHub → Railway auto-deploys!

### Cost: $5/month minimum credit, then pay-as-you-go

---

## 4️⃣ AWS (PRODUCTION-GRADE)

**Why:** Production-ready, scalable, enterprise-grade

### Option A: ECS + RDS (Recommended)

#### Step 1: Push Docker Image
```bash
# Authenticate with AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t zkas-api .
docker tag zkas-api:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/zkas-api:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/zkas-api:latest
```

#### Step 2: Create RDS Database
```bash
aws rds create-db-instance \
  --db-instance-identifier zkas-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password YourPassword123! \
  --allocated-storage 20 \
  --publicly-accessible false
```

#### Step 3: Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name zkas-cluster
```

#### Step 4: Register Task Definition
Create `task-definition.json`:
```json
{
  "family": "zkas-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "zkas-api",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/zkas-api:latest",
      "portMappings": [
        {
          "containerPort": 3000
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://admin:password@zkas-db.abc123.us-east-1.rds.amazonaws.com:5432/zkas"
        }
      ]
    }
  ]
}
```

Register it:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

#### Step 5: Create Service
```bash
aws ecs create-service \
  --cluster zkas-cluster \
  --service-name zkas-api-service \
  --task-definition zkas-api \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-123],securityGroups=[sg-123]}"
```

### Option B: EC2 (Simpler)

```bash
# 1. Launch EC2 instance
aws ec2 run-instances --image-id ami-0c55b159cbfafe1f0 --count 1 --instance-type t2.micro

# 2. SSH into instance
ssh -i your-key.pem ec2-user@your-instance-ip

# 3. Install dependencies
sudo yum update -y
sudo yum install -y docker nodejs npm postgresql

# 4. Start services
docker run -d -p 5432:5432 postgres:15
npm install && npm start

# 5. Attach Elastic IP
aws ec2 associate-address --instance-id i-123456 --public-ip 203.0.113.0
```

### Cost: $5-50+/month depending on usage

---

## 5️⃣ NETLIFY (Frontend Only)

**Why:** Easiest, instant deploy, free CDN

### Step 1: Create Account
1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub

### Step 2: Deploy Frontend
1. Click "New Site from Git"
2. Select GitHub repository
3. Configure:
   - **Build Command:** `npm run build`
   - **Publish Directory:** `frontend/build`
4. Click "Deploy"

### Step 3: Update API URLs
Create `frontend/.env.production`:
```
REACT_APP_API_URL=https://your-backend.herokuapp.com
REACT_APP_CRYPTO_URL=https://your-crypto.herokuapp.com
```

### Step 4: Redeploy
Push to GitHub and Netlify auto-deploys!

### Cost: Free to $19+/month

---

## 6️⃣ VERCEL (Frontend Only)

**Why:** Optimized for React, super fast, free tier

### Step 1: Create Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

### Step 2: Import Project
1. Click "New Project"
2. Import GitHub repo
3. Vercel auto-detects React

### Step 3: Environment Variables
1. Settings → Environment Variables
2. Add:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.com
   NEXT_PUBLIC_CRYPTO_URL=https://your-crypto.com
   ```

### Step 4: Deploy
1. Click "Deploy"
2. Auto-deploys on every GitHub push

### Cost: Free to $20+/month

---

## 7️⃣ DIGITALOCEAN (Full Control)

**Why:** Affordable, great documentation, full control

### Step 1: Create Account
1. Go to [digitalocean.com](https://digitalocean.com)
2. Sign up

### Step 2: Create Droplet
1. Droplet → Create Droplet
2. Choose OS: Ubuntu 22.04
3. Basic plan: $4-6/month
4. Create

### Step 3: Connect via SSH
```bash
ssh root@your_droplet_ip
```

### Step 4: Setup Environment
```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone repo
git clone https://github.com/yourusername/zkas.git
cd zkas
```

### Step 5: Create Environment File
```bash
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost:5432/zkas
NODE_ENV=production
PORT=3000
EOF
```

### Step 6: Start Services
```bash
docker-compose up -d
```

### Step 7: Setup Firewall
```bash
ufw allow 80
ufw allow 443
ufw allow 3000
ufw enable
```

### Step 8: Setup SSL (Let's Encrypt)
```bash
apt install -y certbot python3-certbot-nginx
certbot certonly --standalone -d yourdomain.com
```

### Cost: $4-12+/month

---

## 8️⃣ DOCKER HUB (Container Registry)

**Why:** Push your Docker images for easy deployment

### Step 1: Create Docker Hub Account
1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up for free account

### Step 2: Build and Push Images
```bash
# Login
docker login

# Build backend
cd backend
docker build -t yourusername/zkas-api:latest .
docker push yourusername/zkas-api:latest

# Build crypto service
cd ../crypto
docker build -t yourusername/zkas-crypto:latest .
docker push yourusername/zkas-crypto:latest

# Build frontend
cd ../frontend
docker build -t yourusername/zkas-frontend:latest .
docker push yourusername/zkas-frontend:latest
```

### Step 3: Deploy From Any Platform
Any platform can now pull your images:
```bash
docker pull yourusername/zkas-api:latest
docker run -d -p 3000:3000 yourusername/zkas-api:latest
```

### Cost: Free

---

# 🔑 Step-by-Step Deployment Summary

## For Beginners (Netlify + Heroku)

```
1. Deploy Frontend → Netlify (Easy)
2. Deploy Backend → Heroku (Free tier ending)
3. Database → Heroku PostgreSQL add-on
4. Done! 🎉
```

## For Students (Render)

```
1. Sign up at render.com
2. Create PostgreSQL database
3. Deploy backend service
4. Deploy frontend service
5. Deploy crypto service
6. Connect them with environment variables
7. Done! 🎉
```

## For Production (AWS)

```
1. Push Docker images to ECR
2. Create RDS database
3. Create ECS cluster & tasks
4. Create load balancer
5. Setup CloudFront CDN
6. Configure Route 53 DNS
7. Setup CloudWatch monitoring
8. Done! 🎉
```

---

# 📝 Deployment Checklist

Before deploying to ANY platform:

- [ ] Code committed to GitHub
- [ ] `.env` file created locally (not in GitHub)
- [ ] All dependencies in `package.json` / `requirements.txt`
- [ ] Database schema migrations ready
- [ ] Environment variables documented
- [ ] CORS settings configured
- [ ] Error handling tested
- [ ] Logs setup for debugging
- [ ] HTTPS/SSL enabled
- [ ] Database backups enabled
- [ ] Monitoring alerts configured
- [ ] Rate limiting implemented
- [ ] API documentation ready

---

# 🚨 Common Deployment Issues

### "Port already in use"
```bash
# Find what's using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>
```

### "Database connection refused"
```bash
# Check connection string
echo $DATABASE_URL

# Verify credentials
psql $DATABASE_URL
```

### "Module not found"
```bash
# Reinstall dependencies
npm install

# or for Python
pip install -r requirements.txt
```

### "Build fails"
```bash
# Check build logs
npm run build --verbose

# Test locally first
npm start
```

### "CORS errors"
Add to your backend:
```javascript
const cors = require('cors');
app.use(cors({
  origin: 'https://your-frontend-domain.com',
  credentials: true
}));
```

---

# 🎯 My Recommendation for You

**Best Option: RENDER.COM**

Why?
1. ✅ Free PostgreSQL database
2. ✅ Easy full-stack deployment
3. ✅ Auto-redeploy on GitHub push
4. ✅ Web services + static sites
5. ✅ Great documentation
6. ✅ Good free tier for learning
7. ✅ Paid plans starting at $7/month

**Quick Render Deployment:**
1. Sign up at render.com
2. Click "New +" → PostgreSQL
3. Click "New +" → Web Service (connect GitHub)
4. Set environment variables
5. Deploy! ✅

---

# 📞 Next Steps

1. **Choose your platform** (I recommend Render)
2. **Create account** on that platform
3. **Push code to GitHub** (must be public or grant access)
4. **Follow platform's deployment steps** (usually 5-10 minutes)
5. **Test your live app** at the provided URL
6. **Monitor logs** for any errors

---

## 📚 Platform Documentation

- [Render Docs](https://render.com/docs)
- [Heroku Docs](https://devcenter.heroku.com)
- [AWS Docs](https://docs.aws.amazon.com)
- [Netlify Docs](https://docs.netlify.com)
- [DigitalOcean Docs](https://docs.digitalocean.com)

---

**Happy Deploying! 🚀**

If you need help with specific platform, let me know!
