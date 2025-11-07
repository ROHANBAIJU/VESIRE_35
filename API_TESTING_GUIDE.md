# 🔧 API Connection Testing Guide

## Problem Diagnosed
Your Gemini RAG diagnosis is not communicating with the frontend. Let's test and fix this!

---

## ✅ What I've Added

### 1. **API Test Screen** (Built-in Flutter Tool)
A comprehensive testing interface directly in your app!

**Location:** Top-right corner of Home Screen (API icon 🔧)

**Features:**
- ✅ Tests all 5 critical endpoints
- ✅ Shows response times
- ✅ Displays detailed error messages
- ✅ Tests RAG diagnosis specifically
- ✅ Beautiful UI with color-coded results

**How to Use:**
1. Run your Flutter app: `flutter run`
2. On Home Screen, tap the **API icon** (top-right, next to language selector)
3. Tap **"Run All Tests"**
4. See results instantly!

---

### 2. **PowerShell Backend Tester**
Quick command-line testing without running Flutter.

**File:** `test_render_backend.ps1`

**Run it:**
```powershell
cd Z:\VESIRE_35
.\test_render_backend.ps1
```

**What it tests:**
1. ✅ Base URL reachability
2. ✅ Health check endpoint
3. ✅ API info endpoint
4. ✅ Models info endpoint
5. ✅ **RAG Diagnosis endpoint (CRITICAL)**

---

## 🔍 Current Configuration

### App Configuration
**File:** `Frontend/vesire/lib/config/app_config.dart`

```dart
// Production URL (Render)
https://vesire-35.onrender.com/api

// Force Production: TRUE ✅
```

Your app is currently configured to use **Render backend** (production).

---

## 🐛 Common Issues & Solutions

### Issue 1: RAG Diagnosis Returns NULL
**Symptoms:**
- Detection works ✅
- Diagnosis shows "No diagnosis available" ❌

**Causes:**
1. **GEMINI_API_KEY not set in Render**
2. Backend timeout (RAG takes 10-30 seconds)
3. Knowledge base file missing

**Fix:**
```bash
# Check Render Dashboard
1. Go to https://dashboard.render.com
2. Select "agriscan-backend" service
3. Go to Environment tab
4. Verify GEMINI_API_KEY exists
5. If missing, add it:
   Key: GEMINI_API_KEY
   Value: [Your Gemini API Key]
6. Save → Redeploy
```

---

### Issue 2: Connection Timeout
**Symptoms:**
- App says "offline mode"
- Tests fail with timeout errors

**Causes:**
1. Render free tier cold start (can take 50 seconds)
2. Network issues
3. Wrong URL

**Fix:**
```dart
// Increase timeout in api_service.dart
.timeout(const Duration(seconds: 60)) // Increased from 30
```

---

### Issue 3: CORS Errors
**Symptoms:**
- Browser console shows CORS error
- App can't connect

**Fix:**
Already configured in backend:
```python
# Backend/api/app.py
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

## 📊 Testing Checklist

### Before Testing:
- [ ] Backend deployed on Render
- [ ] GEMINI_API_KEY set in Render environment
- [ ] App configured with `_forceProduction = true`
- [ ] Internet connection active

### Test Steps:
1. **Run PowerShell Test**
   ```powershell
   .\test_render_backend.ps1
   ```
   - All tests should pass ✅
   - RAG diagnosis should return data ✅

2. **Run Flutter App Test**
   ```bash
   flutter run
   ```
   - Tap API icon (top-right)
   - Run all tests
   - Check Test 4: RAG Diagnosis

3. **Test Real Scan**
   - Scan a plant
   - Wait for detection
   - Check if diagnosis appears

---

## 🎯 Expected Results

### ✅ Working RAG Diagnosis:
```json
{
  "success": true,
  "disease": {
    "name": "Tomato leaf late blight",
    "scientific_name": "Phytophthora infestans",
    "description": "AI-generated description...",
    "care_recommendations": ["..."]
  },
  "source": "online_llm"  // ← This means Gemini is working!
}
```

### ❌ Failed RAG Diagnosis:
```json
{
  "success": false,
  "error": "No diagnosis found",
  "source": "synthetic"  // ← Fallback to offline data
}
```

---

## 🔧 Debug Commands

### Check Current URL:
```bash
# Look for this log when app starts:
🌐 [APP_CONFIG] Using PRODUCTION URL: https://vesire-35.onrender.com/api
```

### Check API Logs:
```bash
# In Flutter console, look for:
🔵 [FLUTTER API] Starting detection request to https://vesire-35.onrender.com/api/detect
🔵 [FLUTTER API] Response received: Status 200
🌐 [API SERVICE] ONLINE MODE - Requesting RAG diagnosis for: Tomato leaf late blight
✅ [API SERVICE] RAG Diagnosis successful! Source: online_llm
```

### Check Backend Logs:
1. Go to Render Dashboard
2. Select your service
3. Click "Logs" tab
4. Look for RAG requests:
```
🟢 [FLASK] ========== NEW DETECTION REQUEST ==========
🟢 [FLASK] 🔍 Auto-diagnosing primary detection: Tomato leaf late blight...
✅ [FLASK] RAG diagnosis received! Source: online_llm
```

---

## 🚀 Quick Test Now!

### Option 1: PowerShell (Fastest)
```powershell
cd Z:\VESIRE_35
.\test_render_backend.ps1
```

### Option 2: Flutter App (Visual)
```bash
cd Z:\VESIRE_35\Frontend\vesire
flutter run
# Tap API icon → Run All Tests
```

---

## 📞 If Still Not Working

### 1. Check Render Service Status
- Go to https://dashboard.render.com
- Check if service is "Live" (green)
- Click "Manual Deploy" to redeploy

### 2. Verify Environment Variables
Required in Render:
```
GEMINI_API_KEY = [your-key]
USE_ONLINE_RAG = true
DEBUG = false
```

### 3. Check Backend Health
Visit in browser:
```
https://vesire-35.onrender.com/api/health
```

Should return:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### 4. Test RAG Directly
Visit in browser:
```
https://vesire-35.onrender.com/api/diagnose/Tomato%20leaf%20late%20blight?language=en
```

Should return diagnosis data within 30 seconds.

---

## 📝 Next Steps

1. **Run the PowerShell test script** → Quick backend check
2. **Run Flutter app** → Test with built-in API tester
3. **Check results** → See which endpoint is failing
4. **Fix the issue** → Follow the specific solution
5. **Test again** → Verify it's working

---

## 💡 Pro Tips

1. **First Time?** Render free tier has cold start - first request takes 50 seconds!
2. **RAG Slow?** Normal! Gemini API takes 10-20 seconds
3. **Timeout Errors?** Increase timeout in `api_service.dart`
4. **Offline Mode?** Check connectivity snackbar at top
5. **No Diagnosis?** Check GEMINI_API_KEY in Render

---

## ✨ Features Added

- ✅ Global connectivity monitoring with snackbars
- ✅ In-app API testing tool (5 comprehensive tests)
- ✅ PowerShell backend testing script
- ✅ Debug logging in app_config.dart
- ✅ Better timeout handling
- ✅ Detailed error messages

---

**Good luck! 🚀 Run those tests and let me know what you find!**
