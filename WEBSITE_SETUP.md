# 🌐 How to View ZKAS Website

The website file (`index.html`) cannot be opened directly in a browser due to security restrictions. You need to run it through a local web server.

## 🚀 Quick Start (Easiest Method - Windows)

### Option 1: Run Batch Script (Windows Only)
```bash
# Double-click this file in File Explorer:
run-server.bat

# Or open PowerShell and run:
cd "c:\Users\PRARTHANA\OneDrive - Noida Institute of Engineering and Technology\Desktop\ZKAS"
.\run-server.bat
```

Your browser should automatically open to the website.

---

## 🐍 Option 2: Python Server (All Platforms)

### Prerequisites
- Python 3.x installed (usually comes with most systems)

### Run Server
```bash
# Navigate to ZKAS directory
cd "c:\Users\PRARTHANA\OneDrive - Noida Institute of Engineering and Technology\Desktop\ZKAS"

# Run the server
python server.py

# On some systems:
python3 server.py
```

### Expected Output
```
============================================================

   ZKAS - Zero-Knowledge Authentication System
   Starting Web Server...

============================================================

Starting server on http://localhost:8000

Press Ctrl+C to stop the server

Opening browser...
```

Then visit: **http://localhost:8000**

---

## 🟢 Option 3: Node.js Server (If Node is Installed)

### Prerequisites
- Node.js 14+ installed

### Run Server
```bash
# Navigate to ZKAS directory
cd "c:\Users\PRARTHANA\OneDrive - Noida Institute of Engineering and Technology\Desktop\ZKAS"

# Run the server
node server.js
```

### Expected Output
```
============================================================
🌐 ZKAS Website Server
============================================================

✓ Server running at: http://localhost:8000
✓ Open your browser and visit: http://localhost:8000
✓ Press Ctrl+C to stop
```

Then visit: **http://localhost:8000**

---

## 🔧 Option 4: VS Code Live Server (If Using VS Code)

1. Open ZKAS folder in VS Code
2. Install "Live Server" extension (by Ritwick Dey)
3. Right-click on `index.html`
4. Select "Open with Live Server"
5. Website opens automatically at `http://127.0.0.1:5500`

---

## 📋 Troubleshooting

### Error: "Python not found"
- Install Python from python.org
- Or use Python server option

### Error: "Port 8000 already in use"
- Another app is using port 8000
- Solutions:
  - Close other applications
  - Use different port: `python server.py --port 8001`
  - Or modify the `server.py` file to use a different port

### Error: "Module not found"
- Make sure you're in the correct directory (ZKAS folder)
- Check file permissions

### Browser shows "Cannot GET /"
- Server is running but file path issue
- Make sure `index.html` exists in ZKAS folder
- Check console for detailed error

---

## ✅ What You Should See

Once the server is running and you open `http://localhost:8000`:

1. **Hero Section** - Large gradient title with buttons
2. **Demo Flow** - 5-step authentication process visualization
3. **Features** - 6 feature cards with icons
4. **Security** - 6 threat protection cards
5. **Tech Stack** - Technology choices displayed
6. **Statistics** - Project metrics (3,500+ LOC, 95%+ coverage, etc.)
7. **Code Example** - Docker quick start
8. **Call-to-Action** - Engagement section
9. **Footer** - Links and copyright

---

## 🔌 Access Points

Once server is running:

| Service | URL | What It Shows |
|---------|-----|---------------|
| **Website** | http://localhost:8000 | ZKAS landing page |
| **Backend API** | http://localhost:3000 | (if running separately) |
| **Crypto Service** | http://localhost:5000 | (if running separately) |

---

## 🛑 Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## 🌍 Deploy Website

Once you verify the website works locally, you can deploy it to:

- **GitHub Pages** - Free hosting, automatic deployment
- **Netlify** - Drag & drop deployment
- **Vercel** - Optimized for web apps
- **AWS S3 + CloudFront** - Production-grade
- **Google Cloud Storage** - Enterprise option
- **Any web server** - Apache, Nginx, IIS

Just upload the `index.html` file to your hosting provider.

---

## 💡 Tips

1. **Keep server running** - Don't close the terminal while using the website
2. **Refresh browser** - If changes don't appear, press `Ctrl+F5` or `Cmd+Shift+R`
3. **Check console** - Open browser DevTools (F12) to see any errors
4. **Mobile testing** - Get your local IP and access from phone on same WiFi

---

**Still having issues?** 

The most common solution is to ensure:
1. ✓ You're in the ZKAS directory
2. ✓ Python or Node.js is installed
3. ✓ Port 8000 is not in use
4. ✓ Open browser to http://localhost:8000 (not file://)

Enjoy exploring ZKAS! 🚀
