# 🆘 Deployment Troubleshooting & FAQ

Complete guide to fixing deployment issues and answering common questions.

---

## ❓ Frequently Asked Questions

### Q1: "How do I know my app deployed successfully?"
**A:** Look for:
- ✅ Green checkmark next to service on platform
- ✅ "Deploy successful" in build logs
- ✅ Service URL is accessible in browser
- ✅ No errors in console (F12)

### Q2: "My code works locally but fails on platform"
**A:** Common causes:
1. **Environment variables missing** → Add them to platform
2. **Different OS path format** → Use `/` not `\`
3. **Different Node/Python versions** → Specify in runtime.txt
4. **Port number conflict** → Use PORT env variable
5. **Database credentials wrong** → Verify DATABASE_URL

### Q3: "How do I update my app?"
**A:** For auto-deploy platforms:
```bash
git add .
git commit -m "Your message"
git push origin main
# Platform automatically redeploys!
```

### Q4: "My app is slow"
**A:** Check:
1. Is it a cold start? (Normal on free tier)
2. Check database query performance
3. Add caching where needed
4. Optimize frontend bundle size
5. Upgrade to paid plan for faster servers

### Q5: "How do I see what's wrong?"
**A:** Check logs:
- Render: Dashboard → Logs tab
- Heroku: `heroku logs -a app-name --tail`
- AWS: CloudWatch
- Docker: `docker logs container-name`

### Q6: "Where do I store files/uploads?"
**A:** Options:
1. **AWS S3** - Cloud file storage
2. **Firebase Storage** - Easy integration
3. **DigitalOcean Spaces** - S3-compatible
4. **Database BLOB** - Simple but limited
5. **Cloudinary** - Image-specific

### Q7: "Can I use my own domain?"
**A:** Yes! Add CNAME record:
```
Name: @ or www
Type: CNAME
Value: your-platform-url
```
See your platform docs for details.

### Q8: "How do I backup my database?"
**A:** 
- Render: Automatic backups included
- Heroku: Heroku Postgres automatic backups
- AWS RDS: Automated snapshots
- Self-hosted: Use `pg_dump` command

### Q9: "How much does it cost?"
**A:** See platform comparison in DEPLOYMENT_GUIDE.md
- Free tier exists for all major platforms
- Paid usually starts $7-15/month

### Q10: "Can I deploy from GitHub?"
**A:** Yes! All modern platforms support:
- Auto-deploy on push
- Deploy from specific branch
- Require status checks before deploy

---

## 🐛 Common Issues & Solutions

### Issue 1: "Port Already In Use"

**Error Message:**
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solution:**

**Windows:**
```bash
# Find what's using port
netstat -ano | findstr :3000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

**Mac/Linux:**
```bash
# Find process
lsof -i :3000

# Kill process
kill -9 <PID>
```

**Or change port in code:**
```javascript
const PORT = process.env.PORT || 3000;
```

---

### Issue 2: "Module Not Found"

**Error Message:**
```
Error: Cannot find module 'express'
```

**Solution:**

1. Check module is in package.json:
```bash
cat package.json | grep express
```

2. Reinstall dependencies:
```bash
npm install
npm ci  # Cleaner install
```

3. Check node_modules exists:
```bash
ls node_modules/express
```

4. On platform, ensure build command includes `npm install`:
```
Build: npm install
```

---

### Issue 3: "Database Connection Refused"

**Error Message:**
```
Error: connect ECONNREFUSED 127.0.0.1:5432
PostgreSQL connection failed
```

**Solution:**

1. Check DATABASE_URL format:
```
postgres://user:password@host:port/database
```

2. Verify in environment:
```bash
echo $DATABASE_URL
```

3. Test connection:
```bash
psql $DATABASE_URL
```

4. Check firewall allows connection:
   - Platform → Security settings
   - Whitelist your IP

5. Verify database is running:
   - Render: Check PostgreSQL service status
   - Local: `sudo systemctl status postgres`

---

### Issue 4: "CORS Error"

**Error Message:**
```
Access to XMLHttpRequest at 'https://api.example.com' from origin 
'https://frontend.example.com' has been blocked by CORS policy
```

**Solution:**

Add CORS to your backend:

```javascript
// backend/app.js
const cors = require('cors');

app.use(cors({
  origin: [
    'https://frontend.onrender.com',
    'http://localhost:3000'
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
```

Or allow all (dev only):
```javascript
app.use(cors());  // Be careful in production!
```

---

### Issue 5: "Build Failed"

**Error Message:**
```
Build failed with exit code 1
npm ERR! code ENOENT
```

**Solution:**

1. Check files exist:
```bash
# Verify package.json exists
ls backend/package.json

# Verify build directory exists
ls frontend/src
```

2. Verify build command:
```bash
# Test locally
npm run build
```

3. Check dependencies:
```bash
npm install --verbose
```

4. Review full error logs
5. Common fixes:
   - Add `npm install` before build
   - Specify correct directory
   - Check for typos

---

### Issue 6: "Static Files Not Loading"

**Error Message:**
```
GET /style.css 404 Not Found
```

**Solution:**

1. For frontend, ensure:
```javascript
// Serve static files
app.use(express.static('public'));
```

2. Verify public directory exists:
```bash
ls frontend/public/
```

3. Check file path is correct:
   - Use `/` not `\`
   - Relative to public directory

4. Clear browser cache:
```
Ctrl+Shift+Delete → Clear cached images/files
```

5. Check build output directory:
```bash
ls frontend/build/
```

---

### Issue 7: "Environment Variables Not Working"

**Error Message:**
```
process.env.DATABASE_URL is undefined
```

**Solution:**

1. Verify variable is set:
   - Platform → Environment variables
   - Check spelling exactly matches

2. Restart service after adding variables:
   - Most platforms auto-restart
   - If not, click "Deploy" again

3. Access correctly in code:
```javascript
// Node.js
const url = process.env.DATABASE_URL;

// Python
import os
url = os.getenv('DATABASE_URL')

// React (must start with REACT_APP_)
const url = process.env.REACT_APP_API_URL;
```

4. Check `.env` is ignored:
```bash
cat .gitignore | grep .env
# Should include: .env
```

---

### Issue 8: "Frontend Can't Connect to API"

**Error Message:**
```
TypeError: fetch failed
GET https://api.example.com/health 404
```

**Solution:**

1. Check API URL is correct:
```javascript
// frontend/.env.production
REACT_APP_API_URL=https://zkas-api.onrender.com
```

2. Verify backend is running:
```bash
# Visit backend health endpoint
https://zkas-api.onrender.com/api/health
```

3. Check CORS is enabled (see Issue 4)

4. Verify request format:
```javascript
const response = await fetch(
  `${process.env.REACT_APP_API_URL}/api/auth/login`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }
);
```

5. Check Content-Type header

---

### Issue 9: "Health Check Failing"

**Error Message:**
```
Health check failed: connection timeout
Service is unhealthy
```

**Solution:**

1. Create health endpoint:
```javascript
// backend/app.js
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date() });
});
```

2. Endpoint should return 200:
```bash
curl https://your-api.com/api/health
# Should return: {"status":"ok"}
```

3. Endpoint must be fast (<30s)

4. Verify in platform settings:
   - Health check enabled
   - Correct endpoint path
   - Correct port

---

### Issue 10: "SSL Certificate Error"

**Error Message:**
```
SSL_ERROR_RX_RECORD_TOO_LONG
or
Certificate validation failed
```

**Solution:**

1. Use HTTPS not HTTP:
```
https://yourdomain.com  ✅
http://yourdomain.com   ❌
```

2. For custom domain:
   - Add CNAME record
   - Wait 24-48 hours for DNS
   - Platform auto-generates SSL

3. Force HTTPS in code:
```javascript
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https') {
    res.redirect(`https://${req.header('host')}${req.url}`);
  }
  next();
});
```

---

## 🔧 Advanced Troubleshooting

### Check Platform Limits
Each platform has limits:
- Render: 5GB storage, 512MB RAM (free)
- Heroku: Limited free dynos
- AWS: Free tier has limits
- Check your platform's specs

### Enable Debug Mode
```javascript
// Node.js
const debug = require('debug')('app');
debug('detailed logs here');

// Python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use Monitoring Tools
- **Sentry** - Error tracking
- **LogRocket** - Frontend monitoring
- **New Relic** - Performance monitoring
- **Datadog** - Comprehensive monitoring

### Test Locally First
Always test changes locally before pushing:
```bash
npm install
npm start  # or your start command
npm test   # if you have tests
```

---

## 📝 When to Ask for Help

If you're still stuck:

1. **Gather Information:**
   - Full error message (copy-paste)
   - Platform being used
   - Steps to reproduce
   - Screenshot of error
   - Log output

2. **Search Known Issues:**
   - Platform documentation
   - GitHub Issues
   - Stack Overflow
   - Community forums

3. **Ask on Platform:**
   - Render Support: render.com/support
   - Heroku Help: devcenter.heroku.com
   - AWS Support: aws.amazon.com/support
   - Community Discord/Slack

4. **Check Repo Issues:**
   - GitHub repo → Issues tab
   - Search for similar problems
   - Create new issue with details

---

## ✅ Deployment Verification

After deploying, verify everything works:

### 1. Website Loads
```bash
# Open in browser
https://your-frontend.onrender.com
```

### 2. No Console Errors
```
Press F12 → Console tab → No red errors
```

### 3. API Responds
```bash
curl https://your-api.onrender.com/api/health
```

### 4. Database Connected
Try registration or login - should work!

### 5. Performance Acceptable
Website should load in <3 seconds

### 6. Logs Show No Warnings
Check platform logs for warnings/errors

---

## 🚀 Quick Fixes Cheat Sheet

| Issue | Quick Fix |
|-------|-----------|
| Port in use | `kill -9 $(lsof -t -i:3000)` |
| Module missing | `npm install` |
| DB connection fails | Check DATABASE_URL |
| CORS error | Add cors() middleware |
| Build fails | Run build locally first |
| Env var undefined | Check variable name/spelling |
| API unreachable | Verify URL in frontend |
| Health check fails | Create /health endpoint |
| SSL error | Use https:// not http:// |
| Slow performance | Check server resources |

---

## 📚 Additional Resources

- Platform Docs: See DEPLOYMENT_GUIDE.md
- Local Setup: See README.md
- API Documentation: See DOCUMENTATION.md
- Security: See SECURITY_ANALYSIS.md

---

**Still stuck? The logs are your best friend! Always check them first. 🔍**
