# 🎯 AgriScan Deployment Quickstart

> **TL;DR**: Deploy your multilingual plant disease detection app in 15 minutes!

---

## 📦 What You'll Deploy

| Component | Service | URL Format | Cost |
|-----------|---------|------------|------|
| **Backend** (Flask + YOLO + RAG) | Render | `https://your-app.onrender.com` | Free |
| **Frontend** (Flutter Web) | Netlify | `https://your-app.netlify.app` | Free |
| **Database** | SQLite on Render | Persistent storage | Free |
| **AI Model** | YOLOv8n (11.72 MB) | Included | Free |
| **Multilingual RAG** | Gemini API | Free tier | Free (60 req/min) |

---

## ⚡ Quick Deploy Steps

### 1️⃣ Backend to Render (10 minutes)

```bash
# Push code to GitHub
git add .
git commit -m "Deploy to cloud"
git push origin main
```

**Then on Render.com**:
1. New Web Service → Connect GitHub repo
2. Settings:
   - **Root Directory**: `Backend`
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 api.app:app`
3. Environment Variables:
   ```
   USE_ONLINE_RAG = true
   GEMINI_API_KEY = your_gemini_key_here
   DEBUG = false
   ```
4. Deploy! ✅

**Test it**:
```bash
curl https://your-app.onrender.com/api/health
```

---

### 2️⃣ Frontend to Netlify (5 minutes)

**Update backend URL in code**:
```dart
// Frontend/vesire/lib/config/app_config.dart
static const String _productionApiUrl = 'https://your-app.onrender.com/api';
```

**Build Flutter web**:
```powershell
cd Frontend\vesire
flutter build web --release --web-renderer canvaskit
```

**Deploy**:
- Go to Netlify.com
- Drag `build/web` folder into deployment area
- Done! ✅

---

## 🧪 Testing

### Local Testing (Development Mode)
```powershell
# Start everything locally
.\start_local.ps1
```

### Cloud Testing (Production Mode)
```powershell
# Test cloud deployment
.\test_cloud_deployment.ps1
```

---

## 🔄 Switching Between Local and Cloud

### In Your Flutter App

**Use Local Backend** (for development):
```dart
// lib/config/app_config.dart
static const bool _forceProduction = false;
```

**Use Cloud Backend** (for testing production):
```dart
// lib/config/app_config.dart
static const bool _forceProduction = true;
```

Then:
```bash
flutter run
```

---

## 📱 Mobile App Configuration

### For Local Testing (Same WiFi/Hotspot)
```dart
static const String _localApiUrl = 'http://YOUR_LAPTOP_IP:5000/api';
static const bool _forceProduction = false;
```

### For Cloud Testing (Anywhere)
```dart
static const bool _forceProduction = true;  // Uses Render backend
```

---

## ✅ Success Checklist

After deployment, verify:

- [ ] Backend health check: `https://your-app.onrender.com/api/health`
- [ ] Hindi RAG working: Test with Hindi language selection
- [ ] Kannada RAG working: Test with Kannada language selection  
- [ ] Frontend loads: Open your Netlify URL
- [ ] Detection working: Upload plant image
- [ ] Mobile app connects: Test on physical device
- [ ] CORS configured: No console errors

---

## 🚨 Common Issues & Fixes

### Backend Issues

**"Model not loading"**
```bash
# Ensure model file is in Git
git add Backend/models/agriscan_combined/weights/best.pt
git commit -m "Add model"
git push
```

**"Cold start timeout"**
- Normal on free tier (first request takes 60s)
- Subsequent requests are fast
- Keep-alive ping: Call `/api/health` every 10 minutes

**"CORS error in browser"**
```python
# Add your Netlify URL to Backend/api/config.py
CORS_ORIGINS = ['https://your-app.netlify.app']
```

### Frontend Issues

**"API connection failed"**
```dart
// Check Backend URL in app_config.dart matches your Render URL
print('Using API: ${AppConfig.apiBaseUrl}');
```

**"Language not changing"**
- Verify Gemini API key on Render
- Check `USE_ONLINE_RAG=true` in environment variables
- Clear browser cache and retry

---

## 📊 Monitoring

### Backend (Render)
- **Logs**: Render Dashboard → Your Service → Logs
- **Metrics**: CPU, Memory, Request count
- **Health**: `/api/health` returns JSON with model status

### Frontend (Netlify)
- **Analytics**: Netlify Dashboard → Analytics
- **Logs**: Build logs and deploy logs
- **Performance**: Use Chrome DevTools Lighthouse

---

## 💰 Cost Breakdown

### Free Tier Limits

**Render**:
- 750 hours/month (one service 24/7)
- 512MB RAM, 0.1 CPU
- Spins down after 15 min inactivity

**Netlify**:
- 100GB bandwidth/month
- 300 build minutes/month
- Unlimited sites

**Gemini API**:
- 60 requests/minute
- 1500 requests/day
- Perfect for testing/small apps

### When to Upgrade

**Render** ($7/month):
- Always-on (no cold starts)
- More RAM/CPU
- Better for production

**Netlify** ($19/month):
- More bandwidth
- More build minutes
- Team collaboration

---

## 🎓 Next Steps

1. **Custom Domain**: 
   - Render: Add custom domain in settings
   - Netlify: Add custom domain in settings

2. **CI/CD**: 
   - Already set up! Push to `main` = auto-deploy

3. **Monitoring**:
   - Add Sentry for error tracking
   - Add Google Analytics for usage

4. **Scaling**:
   - Upgrade Render tier when needed
   - Consider Cloudflare CDN for frontend

---

## 📚 Full Documentation

See `CLOUD_DEPLOYMENT_GUIDE.md` for complete step-by-step instructions with troubleshooting.

---

## 🆘 Need Help?

1. Check logs on Render/Netlify
2. Test endpoints with curl
3. Verify environment variables
4. Check browser console for errors

**Quick Test Commands**:
```bash
# Test backend
curl https://your-app.onrender.com/api/health

# Test Hindi RAG
curl "https://your-app.onrender.com/api/diagnose/Tomato%20leaf%20late%20blight?language=hi"

# Open frontend
start https://your-app.netlify.app
```

---

**Ready to deploy? Let's go! 🚀**

Made with ❤️ by AgriScan Team | Multilingual Plant Disease Detection
