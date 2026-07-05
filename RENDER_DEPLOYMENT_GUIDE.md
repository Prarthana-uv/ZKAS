# 🎯 Render.com Complete Deployment Guide

**Recommended platform for ZKAS - Free tier available, easy to use, great for learning.**

---

## 📊 Why Render?

✅ Free PostgreSQL database  
✅ Auto-deploys on GitHub push  
✅ Web services + static sites  
✅ Fast and reliable  
✅ Great documentation  
✅ 500 free build minutes/month  
✅ Easy to scale when needed  

---

## ⏱️ Total Time: 15-20 minutes

---

## STEP 1: Create Render Account

### 1.1 Go to Render
Open: https://render.com

### 1.2 Sign Up
- Click "Get Started"
- Choose "Continue with GitHub"
- Authorize Render to access your GitHub

### 1.3 Verify Email (Check inbox)

✅ **Account created!**

---

## STEP 2: Create PostgreSQL Database

### 2.1 Create Database
From Render dashboard:
1. Click "New +" button (top right)
2. Select "PostgreSQL"

### 2.2 Configure Database
Fill in the form:
```
Name: zkas-database
Database: zkas
User: postgres
Password: (auto-generated - copy this somewhere)
Region: (choose closest to you)
Version: (keep default)
```

### 2.3 Create
- Click "Create Database"
- Wait 1-2 minutes for creation
- You'll see a blue checkmark when ready

### 2.4 Copy Connection String
Once created:
1. Click on your database name
2. Scroll to "Connections" section
3. Copy the "Internal Database URL"
4. Also available: "External Database URL" (for local testing)

**Save this URL - you'll need it!**

Example format:
```
postgres://postgres:password@host:5432/zkas
```

✅ **Database created!**

---

## STEP 3: Deploy Backend API (Node.js)

### 3.1 Create Web Service
From dashboard:
1. Click "New +"
2. Select "Web Service"

### 3.2 Connect Repository
1. Choose "Existing repository" or search for your GitHub repo
2. Search for your "ZKAS" or repository name
3. Click to select it
4. Authorize Render to access

### 3.3 Configure Service
Fill in the fields:

**Name:**
```
zkas-api
```

**Environment:**
```
Node
```

**Region:**
```
(choose same as database)
```

**Branch:**
```
main
```

**Build Command:**
```
cd backend && npm install
```

**Start Command:**
```
node app.js
```

### 3.4 Add Environment Variables
Scroll down to "Environment"

Click "Add Environment Variable" and add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (paste your PostgreSQL connection string) |
| `NODE_ENV` | `production` |
| `PORT` | `3000` |

### 3.5 Configure Advanced Settings (Optional)
- **Auto-Deploy:** Keep enabled (auto-redeploy on push)
- **Max Parallel Builds:** 1
- **Autoscaling:** Optional for free tier

### 3.6 Create Service
- Scroll to bottom
- Click "Create Web Service"
- Wait for deployment (2-5 minutes)
- You'll see a green checkmark when deployed
- Copy the service URL (e.g., `https://zkas-api.onrender.com`)

**Note:** First deploy might take longer

✅ **Backend API deployed!**

---

## STEP 4: Deploy Crypto Service (Python)

### 4.1 Create Another Web Service
From dashboard:
1. Click "New +"
2. Select "Web Service"

### 4.2 Connect Same Repository
Select your ZKAS GitHub repo again

### 4.3 Configure Service
Fill in the fields:

**Name:**
```
zkas-crypto
```

**Environment:**
```
Python 3
```

**Region:**
```
(same as database)
```

**Branch:**
```
main
```

**Build Command:**
```
pip install -r crypto/requirements.txt
```

**Start Command:**
```
python crypto/flask_api.py
```

### 4.4 Add Environment Variables
Add these:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `PORT` | `5000` |

### 4.5 Create Service
- Click "Create Web Service"
- Wait for deployment
- Copy the service URL (e.g., `https://zkas-crypto.onrender.com`)

✅ **Crypto Service deployed!**

---

## STEP 5: Deploy Frontend (React)

### 5.1 Create Static Site
From dashboard:
1. Click "New +"
2. Select "Static Site"

### 5.2 Connect Repository
Select your ZKAS GitHub repo

### 5.3 Configure Site
Fill in the fields:

**Name:**
```
zkas-frontend
```

**Region:**
```
(any)
```

**Branch:**
```
main
```

**Build Command:**
```
cd frontend && npm install && npm run build
```

**Publish Directory:**
```
frontend/build
```

### 5.4 Add Environment Variables
Click "Add Environment Variable":

| Key | Value |
|-----|-------|
| `REACT_APP_API_URL` | `https://zkas-api.onrender.com` |
| `REACT_APP_CRYPTO_URL` | `https://zkas-crypto.onrender.com` |

*(Use the exact URLs you copied from your services)*

### 5.5 Create Site
- Click "Create Static Site"
- Wait for deployment (1-3 minutes)
- Copy the site URL (e.g., `https://zkas-frontend.onrender.com`)

✅ **Frontend deployed!**

---

## STEP 6: Test Your Live App

### 6.1 Visit Your Website
Open in browser:
```
https://zkas-frontend.onrender.com
```

You should see your ZKAS landing page! 🎉

### 6.2 Test Registration
1. Click "Register"
2. Enter an email
3. Click "Register"
4. If successful, you'll see confirmation

### 6.3 Test Login
1. Click "Login"
2. Enter the email you registered
3. Complete the ZKP authentication flow
4. If successful, you'll see your dashboard

### 6.4 Check Browser Console
Press F12 to open developer tools:
- **Console tab:** Should show no red errors
- **Network tab:** All requests should be 2xx/3xx status
- **Application tab:** Check localStorage for auth token

✅ **Live app tested!**

---

## STEP 7: View Deployment Logs

### 7.1 View Logs
For each service:
1. Open the service on Render
2. Click "Logs" tab on the right
3. You should see deployment progress and any errors

### 7.2 Common Logs
```
✓ Build started
✓ Installing dependencies
✓ Build successful
✓ Starting server on port 3000
```

### 7.3 If There Are Errors
1. Read the error message carefully
2. Common issues:
   - Missing environment variables
   - Build command incorrect
   - Start command incorrect
   - Dependency not in package.json
3. Fix the issue locally
4. Push to GitHub
5. Render auto-redeploys! ✅

---

## STEP 8: Set Custom Domain (Optional)

### 8.1 Add Domain
1. Open your service on Render
2. Click "Settings"
3. Scroll to "Custom Domain"
4. Enter your domain (e.g., zkas.yourdomain.com)
5. Update your domain's DNS:
   ```
   CNAME: your-service.onrender.com
   ```

### 8.2 Enable SSL (Automatic)
Render automatically enables HTTPS! 🔒

---

## 🔄 Auto-Deploy on Every Push

Render is configured to auto-deploy when you push to GitHub!

### To Push Updates:
```bash
# Make changes locally
# Test thoroughly!

# Commit changes
git add .
git commit -m "Description of changes"

# Push to GitHub
git push origin main

# Render automatically redeploys! ✅
```

### To View Build Progress:
1. Open the service on Render
2. Click "Logs" tab
3. Watch the build in real-time

---

## 🔐 Environment Variables Reference

### Used Environment Variables:
| Service | Variable | Value |
|---------|----------|-------|
| Backend | DATABASE_URL | PostgreSQL connection |
| Backend | NODE_ENV | production |
| Backend | PORT | 3000 |
| Crypto | FLASK_ENV | production |
| Crypto | PORT | 5000 |
| Frontend | REACT_APP_API_URL | Backend URL |
| Frontend | REACT_APP_CRYPTO_URL | Crypto URL |

### To Change Variables:
1. Open service on Render
2. Click "Environment"
3. Click variable to edit
4. Change value
5. Service auto-redeploys ✅

---

## 🆘 Troubleshooting

### Issue: "Failed to connect to database"
**Solution:**
1. Check DATABASE_URL is correct
2. Verify PostgreSQL service is running
3. Check service can reach database from same region

### Issue: "Build failed"
**Solution:**
1. Check build command is correct
2. Verify all dependencies in package.json
3. Test build locally: `npm run build`

### Issue: "Service won't start"
**Solution:**
1. Check start command is correct
2. Verify process listens on PORT env variable
3. Check logs for error messages

### Issue: "Frontend can't connect to API"
**Solution:**
1. Check API URLs in environment variables
2. Verify backend service is running
3. Check CORS is enabled in backend
4. Check API URL format (must be https://)

### Issue: "Health check failing"
**Solution:**
1. Add health check endpoint: `/health`
2. Return status 200 on success
3. Endpoint should be fast (<30s)

---

## 📊 Monitor Your Services

### View Metrics
1. Open any service
2. Click "Metrics" tab
3. See:
   - CPU usage
   - Memory usage
   - Network traffic
   - Build logs

### Set Up Alerts (Optional)
1. Click "Settings"
2. Find "Notifications"
3. Add email notifications
4. Render alerts you on failures

---

## 💰 Costs

### Free Tier:
- ✅ PostgreSQL database (free)
- ✅ 500 free build minutes/month
- ✅ Web services (if not actively used, spin down after 15 mins)
- ✅ Static sites (free)

### Pricing When You Need It:
| Service | Free | Paid Starts |
|---------|------|------------|
| PostgreSQL | ✅ | $15/month |
| Web Service | ✅* | $7/month |
| Static Site | ✅ | $7/month |

*Web services on free tier spin down after 15 mins of inactivity

---

## 🚀 Next Steps

1. ✅ Visit your live app at the URL
2. ✅ Share the URL with others
3. ✅ Make changes and push to GitHub
4. ✅ Watch auto-deploy happen
5. ✅ Monitor logs if needed
6. ✅ Scale or customize later

---

## 📞 Get Help

- **Render Docs:** https://render.com/docs
- **Render Support:** https://render.com/support
- **Discord Community:** https://render.com/community

---

## ✅ Deployment Checklist

- [ ] GitHub account and repo ready
- [ ] Render account created
- [ ] PostgreSQL database created and URL copied
- [ ] Backend API deployed
- [ ] Crypto service deployed
- [ ] Frontend deployed
- [ ] All environment variables set correctly
- [ ] Live app tested and working
- [ ] Custom domain added (optional)
- [ ] Monitoring set up (optional)

---

**Congratulations! Your ZKAS system is live on the internet! 🎉**

### Your URLs:
```
Frontend: https://zkas-frontend.onrender.com
Backend API: https://zkas-api.onrender.com
Crypto Service: https://zkas-crypto.onrender.com
```

---

**Enjoy your deployed application!** 🚀
