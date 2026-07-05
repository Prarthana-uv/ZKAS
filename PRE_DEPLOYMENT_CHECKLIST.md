# ✅ Pre-Deployment Checklist

Complete this checklist before deploying your ZKAS project to any platform.

---

## 📦 Project Structure

- [ ] Backend code in `backend/` directory
- [ ] Frontend code in `frontend/` directory  
- [ ] Crypto service in `crypto/` directory
- [ ] Database schema in `database/` directory
- [ ] Docker files present:
  - [ ] `docker-compose.yml`
  - [ ] `Dockerfile` (or `Dockerfile.backend`, `Dockerfile.crypto`)
- [ ] `package.json` exists in root and `/backend`
- [ ] `requirements.txt` exists in `/crypto`
- [ ] `.gitignore` prevents committing sensitive files

---

## 🔑 Environment & Secrets

- [ ] `.env` file created locally with all required variables
- [ ] `.env` file is in `.gitignore` (NOT committed to Git)
- [ ] `.env.example` created showing all required variables
- [ ] All secrets have strong, unique values (not "password123")
- [ ] No hardcoded API keys in source code
- [ ] No hardcoded database credentials in source code

---

## 📝 Dependencies

### Backend (Node.js)
- [ ] `package.json` in `/backend` includes all dependencies
- [ ] Run: `npm install` works without errors
- [ ] All imports in code exist in `package.json`
- [ ] Production vs development dependencies properly separated

### Crypto Service (Python)
- [ ] `requirements.txt` exists in `/crypto`
- [ ] Run: `pip install -r requirements.txt` works
- [ ] All imports in Python code listed in `requirements.txt`
- [ ] Python version specified (e.g., Python 3.11)

### Frontend (React)
- [ ] `package.json` in `/frontend` includes all dependencies
- [ ] Run: `npm install` works without errors
- [ ] `npm run build` produces output in `build/` or `dist/`

---

## 🗄️ Database

- [ ] Database schema file is ready
- [ ] Schema includes all necessary tables and indexes
- [ ] Migration files prepared (if needed)
- [ ] `.env.example` shows DATABASE_URL format
- [ ] Tested database connections locally

---

## 🔧 Configuration Files

- [ ] `Procfile` created (for Heroku)
- [ ] `render.yaml` created (for Render)
- [ ] `Dockerfile` files created and tested
- [ ] `.dockerignore` excludes unnecessary files
- [ ] `.gitignore` includes:
  - [ ] `node_modules/`
  - [ ] `__pycache__/`
  - [ ] `.env`
  - [ ] `.DS_Store`
  - [ ] `build/`, `dist/`

---

## 🚀 Application Setup

- [ ] Backend starts with: `npm start` or `node app.js`
- [ ] Backend listens on configurable PORT (from env variable)
- [ ] Crypto service starts and listens on PORT
- [ ] Frontend builds with: `npm run build`
- [ ] All services can run independently
- [ ] Health check endpoints exist
  - [ ] Backend: `/api/health` or `/health`
  - [ ] Crypto: `/health` endpoint

---

## 🌐 API Configuration

- [ ] CORS properly configured in backend
- [ ] CORS allows frontend domain (update in production)
- [ ] API routes don't have hardcoded localhost references
- [ ] API endpoints accept configurable base URLs
- [ ] Error responses include helpful messages
- [ ] Rate limiting configured (recommended)

---

## 🔐 Security

- [ ] All database queries use parameterized statements (SQL injection prevention)
- [ ] Passwords hashed with proper algorithm (bcrypt, scrypt, etc.)
- [ ] No sensitive data logged to console in production
- [ ] HTTPS/SSL configuration ready
- [ ] CORS properly restricts origins
- [ ] Authentication tokens have expiration
- [ ] Input validation on all API endpoints
- [ ] File upload validation (if applicable)

---

## 🧪 Testing

- [ ] Backend starts locally: `npm start`
- [ ] Frontend starts locally: `npm start`
- [ ] Crypto service starts locally: `python app.py`
- [ ] Database migration successful: `npm run migrate`
- [ ] Can register a new user (if applicable)
- [ ] Can authenticate successfully
- [ ] All API endpoints respond correctly
- [ ] No console errors in browser (F12)
- [ ] No warnings in backend/frontend startup

---

## 📊 Logging & Monitoring

- [ ] Application logs important events
- [ ] Error logging configured
- [ ] Logs don't expose sensitive information
- [ ] Logging level can be configured via environment
- [ ] Health check endpoint ready
- [ ] Error monitoring service (optional): Sentry, etc.

---

## 🐳 Docker Testing (If Using Docker)

- [ ] `docker build` succeeds for each service
- [ ] `docker run` starts without errors
- [ ] Services can communicate with each other
- [ ] `docker-compose up` successfully runs all services
- [ ] Services connect to shared network
- [ ] Volume mounts work correctly

---

## 📦 Build & Production Settings

### Backend
- [ ] Environment set to: `NODE_ENV=production`
- [ ] `npm run build` or similar compiles successfully (if applicable)
- [ ] Minification/uglification configured (if applicable)
- [ ] Unnecessary packages removed

### Frontend
- [ ] Build command works: `npm run build`
- [ ] Build output in correct directory
- [ ] `.env.production` configured with production URLs
- [ ] All environment variables in `REACT_APP_*` format
- [ ] Service worker configured (if using PWA)

### Crypto Service
- [ ] Python optimized for production
- [ ] No debug mode enabled in production
- [ ] Static files served correctly

---

## 📋 GitHub Preparation

- [ ] Repository is public or access granted to platform
- [ ] All code committed: `git status` shows nothing
- [ ] Main branch is default branch
- [ ] `.gitignore` prevents large files (node_modules, etc.)
- [ ] No sensitive files in git history
  - [ ] No `.env` files
  - [ ] No API keys or secrets
- [ ] README.md up to date
- [ ] Instructions for local setup included
- [ ] Deployment branch is up to date

---

## 🎯 Platform-Specific Preparation

### For Heroku
- [ ] `Procfile` created and tested
- [ ] `runtime.txt` specifies Node/Python version (optional but recommended)
- [ ] `postdeploy.sh` for database migrations (if needed)
- [ ] Heroku account created

### For Render
- [ ] `render.yaml` created with all services
- [ ] Environment variables listed in YAML
- [ ] Build commands tested locally
- [ ] Render account created

### For AWS
- [ ] AWS account with credentials configured
- [ ] Docker images tested and push-ready
- [ ] AWS CLI installed
- [ ] IAM role configured for ECS

### For Netlify/Vercel
- [ ] Frontend builds successfully: `npm run build`
- [ ] Output directory is correct (usually `build/`)
- [ ] Environment variables in `.env.production`
- [ ] Account created

### For DigitalOcean
- [ ] Droplet size chosen
- [ ] SSH key generated
- [ ] Docker Compose tested locally

---

## 📞 Final Checks

- [ ] Documentation updated with deployment instructions
- [ ] Team members know deployment process
- [ ] Backup strategy for database
- [ ] Monitoring alerts configured
- [ ] Support contact information available
- [ ] Incident response plan ready

---

## 🚀 Deployment Day

1. **Final Commit**
   ```bash
   git status  # Should be clean
   git add .
   git commit -m "Final pre-deployment checks"
   git push origin main
   ```

2. **Choose Platform** (see QUICK_DEPLOY.md)

3. **Deploy** following platform-specific steps

4. **Test Live Application**
   - [ ] Website loads
   - [ ] All pages work
   - [ ] Forms submit successfully
   - [ ] API calls return correct data

5. **Monitor** first 24 hours
   - [ ] Check logs for errors
   - [ ] Monitor performance
   - [ ] Watch for user reports

---

## ✅ Success Indicators

Your deployment is successful when:
- ✅ Website loads without errors
- ✅ All pages are accessible
- ✅ API responses are correct
- ✅ Database connections work
- ✅ Authentication flows properly
- ✅ Error messages are helpful
- ✅ Performance is acceptable (<2s load time)
- ✅ No sensitive data in logs

---

## 🆘 If Something Goes Wrong

1. **Check logs immediately** (platform-specific)
2. **Verify environment variables** are set correctly
3. **Test locally** to isolate the issue
4. **Revert last change** if recent deployment broke something
5. **Check platform documentation** for specific errors
6. **Reach out to platform support** if stuck

---

## 📚 Next: Deployment Guides

- See `QUICK_DEPLOY.md` for step-by-step platform guides
- See `DEPLOYMENT_GUIDE.md` for detailed platform information

---

**Everything checked? You're ready to deploy! 🚀**
