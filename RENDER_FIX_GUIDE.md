# 🚨 RENDER DEPLOYMENT FIX - Quick Action Steps

## Problem
Render was using Python 3.13.4 which has compatibility issues with numpy 1.24.3

## Solution Applied
1. ✅ Updated `Backend/requirements.txt` - numpy 1.26.2 (wheel-compatible)
2. ✅ Updated `Backend/runtime.txt` - python-3.11.6
3. ✅ Created `render.yaml` - explicit Python version config
4. ✅ Updated build command with pip upgrade

---

## 🎯 EXACT STEPS TO FIX RENDER NOW

### Step 1: Push Changes to GitHub

```powershell
cd Z:\VESIRE_35

# Add all updated files
git add Backend/requirements.txt Backend/runtime.txt render.yaml CLOUD_DEPLOYMENT_GUIDE.md

# Commit with clear message
git commit -m "fix: update Python 3.11 and numpy 1.26 for Render compatibility"

# Push to trigger Render rebuild
git push origin main
```

### Step 2: Update Render Service Settings

Go to: https://dashboard.render.com → Your Service → Settings

**CRITICAL CHANGES:**

1. **Python Version** (Environment section):
   - Click the dropdown next to "Python Version"
   - Select **3.11.6** (NOT 3.13.x)
   - Save changes

2. **Build Command** (Build & Deploy section):
   ```
   python -m pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
   ```

3. **Environment Variables** (add if not present):
   ```
   USE_ONLINE_RAG = true
   GEMINI_API_KEY = AIzaSyDKCnXD1fuM22M0sYpc05DOAAaJmv3mXFo
   DEBUG = false
   CORS_ORIGINS = *
   ```

4. **Click "Save Changes"** - This will trigger auto-redeploy

### Step 3: Monitor Build Logs

- Go to "Logs" tab in Render dashboard
- Watch for:
  ```
  ==> Using Python version 3.11.6
  Successfully installed numpy-1.26.2 ...
  ==> Build successful 🎉
  ```

### Step 4: Test Deployment

Once deployed (URL: https://agriscan-backend-XXXX.onrender.com):

```powershell
# Test health endpoint
curl https://your-render-url.onrender.com/api/health

# Test multilingual RAG
curl "https://your-render-url.onrender.com/api/diagnose/Tomato%20leaf%20late%20blight?language=hi&use_cache=false"
```

---

## 🔍 If Build Still Fails

### Option A: Use Blueprint (render.yaml)
1. Delete existing service in Render dashboard
2. Click "New" → "Blueprint"
3. Connect repo → Select `render.yaml`
4. Add GEMINI_API_KEY environment variable
5. Deploy

### Option B: Manual Python Version Override
In Render service settings:
- Go to "Environment" tab
- Add: `PYTHON_VERSION = 3.11.6`
- Redeploy

### Option C: Use requirements without version pins
Replace `Backend/requirements.txt` with:
```
Flask>=3.0.0
flask-cors>=4.0.0
gunicorn>=21.2.0
SQLAlchemy>=2.0.0
python-dotenv>=1.0.0
ultralytics>=8.1.0
opencv-python-headless>=4.8.0
numpy>=1.26.0
Pillow>=10.0.0
onnxruntime>=1.16.0
google-generativeai>=0.3.0
openai>=1.3.0
requests>=2.31.0
```

---

## ✅ Expected Success Output

```
==> Installing Python version 3.11.6...
==> Using Python version 3.11.6
==> Running build command...
Collecting Flask==3.0.0
Collecting numpy==1.26.2
  Downloading numpy-1.26.2-cp311-cp311-manylinux_2_17_x86_64.whl (18.2 MB)
Successfully installed Flask-3.0.0 numpy-1.26.2 ...
==> Build successful 🎉
==> Starting service...
✅ Model loaded from Backend/models/agriscan_combined/weights/best.pt
🌐 Server: http://0.0.0.0:10000
```

---

## 📞 Quick Commands

```powershell
# Commit and push
git add -A && git commit -m "fix: Render deployment compatibility" && git push

# Test local backend
cd Z:\VESIRE_35\Backend\api && python app.py

# Test deployed backend
curl https://agriscan-backend.onrender.com/api/health
```

---

**Next after successful deploy:**
- Update `Frontend/vesire/lib/config/app_config.dart` with Render URL
- Build Flutter web: `flutter build web --release`
- Deploy to Netlify
