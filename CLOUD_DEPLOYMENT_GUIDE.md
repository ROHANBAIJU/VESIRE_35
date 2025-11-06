# 🚀 AgriScan Cloud Deployment Guide

Complete guide to deploy AgriScan Backend and Frontend to the cloud.

## 📋 Overview

- **Backend**: Flask API on Render (Free tier)
- **Frontend**: Flutter Web on Netlify (Free tier)
- **Database**: SQLite (persistent on Render)
- **AI Model**: YOLOv8n ONNX (included in deployment)
- **RAG**: Gemini API for multilingual responses

---

## 🔧 Part 1: Deploy Backend to Render

### Prerequisites
- GitHub account
- Render account (sign up at https://render.com)
- Gemini API key (from https://makersuite.google.com/app/apikey)

### Step 1: Push Code to GitHub

```bash
cd Z:\VESIRE_35
git add .
git commit -m "Prepare for cloud deployment"
git push origin main
```

### Step 2: Create Render Web Service

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Click "New +" → "Web Service"**
3. **Connect Your Repository**:
   - Click "Connect GitHub" or "Connect GitLab"
   - Authorize Render to access your repository
   - Select your `VESIRE_35` repository

4. **Configure Service**:
   ```
   Name: agriscan-backend
   Region: Oregon (US West)
   Branch: main
   Root Directory: Backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 api.app:app
   Instance Type: Free
   ```

5. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable":
   
   ```
   USE_ONLINE_RAG = true
   GEMINI_API_KEY = your_actual_gemini_api_key_here
   DEBUG = false
   CORS_ORIGINS = https://your-netlify-app.netlify.app,http://localhost:*
   ```

6. **Click "Create Web Service"**

7. **Wait for Deployment** (5-10 minutes first time):
   - Watch the build logs
   - Once deployed, you'll get a URL like: `https://agriscan-backend.onrender.com`

### Step 3: Test Backend

Open your browser or use curl:

```bash
# Health check
curl https://agriscan-backend.onrender.com/api/health

# Should return:
# {"status":"healthy","timestamp":"...","version":"1.0.0","model_loaded":true}
```

### 🚨 Important Notes for Render:

1. **Cold Starts**: Free tier spins down after 15 minutes of inactivity. First request after may take 30-60 seconds.

2. **Model Loading**: The YOLOv8n model (~12MB) loads on startup. Check logs if issues occur.

3. **Persistent Storage**: SQLite database persists on Render's free tier (25GB limit).

4. **Gemini API**: Free tier limited to 60 requests/minute. Sufficient for testing.

5. **Logs**: View logs in Render dashboard under "Logs" tab.

---

## 🌐 Part 2: Deploy Frontend to Netlify

### Prerequisites
- Netlify account (sign up at https://netlify.com)
- Flutter SDK installed locally
- Your backend URL from Render

### Step 1: Update Backend URL

Edit `Frontend/vesire/lib/config/app_config.dart`:

```dart
static const String _productionApiUrl = 'https://agriscan-backend.onrender.com/api';
```

Replace `agriscan-backend.onrender.com` with your actual Render URL.

### Step 2: Build Flutter Web App Locally

```powershell
cd Z:\VESIRE_35\Frontend\vesire

# Enable web support (if not already)
flutter config --enable-web

# Get dependencies
flutter pub get

# Build for production
flutter build web --release --web-renderer canvaskit
```

This creates `build/web/` folder with your compiled Flutter web app.

### Step 3: Deploy to Netlify

#### Option A: Drag & Drop (Easiest)

1. Go to https://app.netlify.com/
2. Click "Add new site" → "Deploy manually"
3. Drag the `Frontend/vesire/build/web` folder into the upload area
4. Wait for deployment (1-2 minutes)
5. You'll get a URL like: `https://random-name-123.netlify.app`

#### Option B: Git Integration (Recommended)

1. **Update netlify.toml** with correct paths
2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Netlify config"
   git push origin main
   ```

3. **In Netlify Dashboard**:
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub
   - Select `VESIRE_35` repository
   - Configure:
     ```
     Base directory: Frontend/vesire
     Build command: flutter build web --release
     Publish directory: Frontend/vesire/build/web
     ```
   - Click "Deploy site"

4. **Custom Domain** (Optional):
   - Go to "Domain settings"
   - Add custom domain: `agriscan.yourdomain.com`

### Step 4: Test Frontend

1. Open your Netlify URL
2. Change language to Hindi/Kannada
3. Start detection
4. Verify RAG responses are in the selected language

---

## 🔄 Part 3: Link Backend and Frontend

### Update CORS on Render

1. Go to Render dashboard → Your service → Environment
2. Update `CORS_ORIGINS` variable:
   ```
   CORS_ORIGINS = https://your-netlify-app.netlify.app,https://agriscan-backend.onrender.com,http://localhost:*
   ```
3. Save and redeploy

### Update Frontend Config

If you change your backend URL later:

```dart
// lib/config/app_config.dart
static const String _productionApiUrl = 'https://new-backend-url.onrender.com/api';
```

Then rebuild and redeploy:

```powershell
flutter build web --release
# Re-upload to Netlify
```

---

## 🧪 Testing Both Environments

### Local Testing (Development)

```dart
// lib/config/app_config.dart
static const bool _forceProduction = false; // Use local backend
```

```powershell
# Start local backend
cd Z:\VESIRE_35\Backend\api
python app.py

# Run Flutter app
cd Z:\VESIRE_35\Frontend\vesire
flutter run -d chrome
```

### Cloud Testing (Production)

```dart
// lib/config/app_config.dart
static const bool _forceProduction = true; // Use cloud backend
```

```powershell
# Run Flutter app (connects to Render backend)
cd Z:\VESIRE_35\Frontend\vesire
flutter run -d chrome
```

### Mobile Testing

**Local Backend** (same WiFi/hotspot):
```dart
static const String _localApiUrl = 'http://10.190.144.95:5000/api'; // Your laptop IP
static const bool _forceProduction = false;
```

**Cloud Backend** (anywhere with internet):
```dart
static const bool _forceProduction = true; // Uses Render backend
```

---

## 📊 Monitoring and Maintenance

### Backend (Render)

- **Logs**: https://dashboard.render.com → Your service → Logs
- **Metrics**: Check CPU, Memory, Requests
- **Health Check**: `/api/health` endpoint

### Frontend (Netlify)

- **Analytics**: Netlify dashboard shows traffic
- **Logs**: Build logs and function logs
- **Performance**: Use Lighthouse in Chrome DevTools

### Costs

- **Render Free Tier**:
  - 750 hours/month
  - Spins down after 15 min inactivity
  - 512MB RAM, 0.1 CPU

- **Netlify Free Tier**:
  - 100GB bandwidth/month
  - 300 build minutes/month
  - Unlimited sites

---

## 🚨 Troubleshooting

### Backend Issues

**Model not loading**:
```bash
# Check Render logs for:
ERROR: Model file not found

# Solution: Ensure model file is committed to Git
git lfs track "*.pt"
git add Backend/models/agriscan_combined/weights/best.pt
git commit -m "Add model file"
git push
```

**Cold start timeout**:
- First request may take 60s on free tier
- Subsequent requests are fast
- Consider paid tier ($7/month) for always-on

**CORS errors**:
```python
# Check config.py CORS_ORIGINS includes your Netlify domain
CORS_ORIGINS = ['https://your-app.netlify.app']
```

### Frontend Issues

**Blank page after deployment**:
- Check browser console for errors
- Verify backend URL in app_config.dart
- Test backend health endpoint directly

**API connection failed**:
```dart
// Check if using correct URL
print('API URL: ${AppConfig.apiBaseUrl}');
```

**Language not switching**:
- Clear browser cache
- Check Gemini API key on Render
- Verify USE_ONLINE_RAG=true

---

## 🎯 Quick Reference

### URLs After Deployment

```yaml
Local Backend: http://localhost:5000
Cloud Backend: https://agriscan-backend.onrender.com
Local Frontend: http://localhost:*
Cloud Frontend: https://your-app.netlify.app
```

### Key Environment Variables

**Render (Backend)**:
```env
USE_ONLINE_RAG=true
GEMINI_API_KEY=your_key
DEBUG=false
PORT=10000
```

**Netlify (Frontend)**:
```
No environment variables needed (URLs are in app_config.dart)
```

---

## 🎉 Success Checklist

- [ ] Backend deployed to Render
- [ ] Backend health check returns 200 OK
- [ ] Frontend built successfully
- [ ] Frontend deployed to Netlify
- [ ] CORS configured correctly
- [ ] Hindi/Kannada responses working
- [ ] Mobile app connects to cloud backend
- [ ] Local development still works

---

## 📞 Support

If you encounter issues:

1. Check Render logs for backend errors
2. Check browser console for frontend errors
3. Verify all environment variables are set
4. Test backend endpoints with curl/Postman
5. Ensure Git LFS is tracking model files

**Common Commands**:

```bash
# Rebuild and redeploy backend
git push origin main

# Rebuild and redeploy frontend
flutter build web --release
# Then re-upload to Netlify

# Test backend locally
curl http://localhost:5000/api/health

# Test backend on cloud
curl https://agriscan-backend.onrender.com/api/health
```

---

Made with ❤️ by AgriScan Team
