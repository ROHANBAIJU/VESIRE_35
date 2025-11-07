# 📱 AgriScan APK Distribution Guide

## ✅ Current Setup

- **Cloud Backend**: `https://vesire-35.onrender.com/api` (Deployed on Render)
- **APK Build**: Configured to connect to cloud backend
- **Offline Mode**: Automatic fallback to on-device detection
- **Languages**: English, Hindi (हिंदी), Kannada (ಕನ್ನಡ)

---

## 🔨 Build APK

### Option 1: Use PowerShell Script (Easiest)

```powershell
cd Z:\VESIRE_35
.\build-apk-cloud.ps1
```

This will:
1. Clean previous builds
2. Get dependencies
3. Build release APK
4. Show APK location and size

### Option 2: Manual Build

```powershell
cd Z:\VESIRE_35\Frontend\vesire
flutter clean
flutter pub get
flutter build apk --release
```

**APK Location**: `Z:\VESIRE_35\Frontend\vesire\build\app\outputs\flutter-apk\app-release.apk`

---

## 📤 Distribution Methods

### Method 1: Google Drive / Dropbox (Recommended)

1. Upload `app-release.apk` to Google Drive
2. Set sharing to "Anyone with the link"
3. Share link via WhatsApp/Email/Social Media

**Example**:
```
📱 AgriScan App Download
🌾 Plant Disease Detection with AI
🔗 https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing

✅ Features:
- Real-time disease detection
- Multilingual (English/Hindi/Kannada)
- Works offline
- Free to use
```

### Method 2: Your Website

1. Upload APK to your website's hosting
2. Add download page with instructions

**HTML Example**:
```html
<a href="/downloads/agriscan-v1.0.apk" download>
  <button>Download AgriScan APK</button>
</a>
```

### Method 3: Direct Share

1. Copy APK to phone storage
2. Share via:
   - WhatsApp
   - Telegram
   - Bluetooth
   - Email attachment

### Method 4: APK Hosting Sites

- **APKPure**: https://apkpure.com/developer-upload
- **APKMirror**: https://www.apkmirror.com/developer-upload/
- **F-Droid**: https://f-droid.org/ (open source)

---

## 📲 User Installation Instructions

### For Users Installing APK:

1. **Download APK** from your shared link
2. **Enable Unknown Sources**:
   - Go to Settings → Security
   - Enable "Install from Unknown Sources"
   - Or enable for specific app (Chrome, Files, etc.)
3. **Install APK**:
   - Tap on downloaded APK file
   - Click "Install"
   - Click "Open" after installation
4. **Grant Permissions**:
   - Camera: Required for live detection
   - Storage: Required for saving scan history
   - Internet: Required for cloud diagnosis (optional)

---

## 🌐 How It Works

### With Internet Connection ✅
- Uses Render cloud backend: `https://vesire-35.onrender.com/api`
- Full AI detection + RAG diagnosis
- Multilingual responses (Hindi/Kannada)
- Saves scan history to cloud database
- **First call may take 30-60s** (Render cold start on free tier)

### Without Internet Connection 📵
- Automatic fallback to on-device detection
- YOLO model runs locally on phone
- Shows detections with bounding boxes
- No diagnosis available offline
- Still fast and smooth

---

## ⚙️ Backend Configuration (Already Done ✅)

Your APK is already configured to connect to Render backend:

```dart
// lib/config/app_config.dart
static const String _productionApiUrl = 'https://vesire-35.onrender.com/api';
static const bool _forceProduction = true; // APK uses cloud backend
```

**Offline Fallback** is automatic via `HybridDetectionService`:
- Checks connectivity before API calls
- Falls back to on-device if offline
- Shows user-friendly "Offline mode" message

---

## 🧪 Testing Before Distribution

### Test Checklist:

```
✅ Online Mode:
   [ ] Open app with internet
   [ ] Scan a plant image
   [ ] Verify detection works
   [ ] Check diagnosis shows (English)
   [ ] Switch to Hindi - verify RAG response
   [ ] Switch to Kannada - verify RAG response

✅ Offline Mode:
   [ ] Turn off WiFi and mobile data
   [ ] Scan a plant image
   [ ] Verify detection still works
   [ ] Verify "Offline mode" message shows
   [ ] Check no diagnosis available

✅ Real-time Camera:
   [ ] Open camera mode
   [ ] Point at plant
   [ ] Verify bounding boxes appear
   [ ] Verify boxes are smooth (30+ FPS)
   [ ] Check detection labels show

✅ Multilingual:
   [ ] Switch between English/Hindi/Kannada
   [ ] Verify UI updates
   [ ] Verify TTS works (if enabled)
   [ ] Check diagnosis in selected language
```

---

## 📊 Backend Status Monitoring

### Check Backend Health:

```bash
# Test backend is running
curl https://vesire-35.onrender.com/api/health

# Should return:
{
  "status": "healthy",
  "timestamp": "2025-11-07T...",
  "version": "1.0.0",
  "model_loaded": true
}
```

### Render Dashboard:
- **URL**: https://dashboard.render.com
- **View Logs**: Check real-time API requests
- **Monitor**: CPU, Memory, Response times
- **Cold Starts**: First request after 15min idle = 30-60s

---

## 🚨 Troubleshooting

### APK Won't Install
- Enable "Install from Unknown Sources"
- Check Android version (min SDK 21 = Android 5.0)
- Clear space on phone (APK ~50-80 MB)

### API Connection Failed
- Check internet connection
- Verify backend is running: `curl https://vesire-35.onrender.com/api/health`
- Check Render logs for errors
- Wait 60s if cold start (backend was sleeping)

### Camera Not Working
- Grant camera permission in Settings
- Check other apps can use camera
- Restart app after granting permission

### Detections Not Showing
- Check image is clear and well-lit
- Ensure plant leaf is visible
- Try different angle or closer shot
- Check console logs for errors

---

## 📈 Scaling (When You Get Users)

### Free Tier Limits:
- **Render**: 750 hours/month (enough for ~1000 requests/day)
- **Gemini API**: 60 requests/minute (free tier)
- **SQLite**: 25GB storage on Render

### When to Upgrade:
- **Render Pro ($7/month)**: 
  - No cold starts
  - Always-on backend
  - Faster response times
  
- **Gemini API Paid**:
  - Higher rate limits
  - More requests/minute

---

## 🎯 Distribution Checklist

```
Before sharing APK:

✅ Backend deployed and running
   https://vesire-35.onrender.com/api/health returns 200 OK

✅ APK built with correct backend URL
   _forceProduction = true in app_config.dart

✅ Tested on physical Android device
   Online and offline modes work

✅ Created download page/link
   Google Drive / Website / APK hosting

✅ Wrote installation instructions
   How to enable unknown sources and install

✅ Prepared support contact
   Email/WhatsApp for user issues
```

---

## 📞 User Support Template

When users ask for help:

```
Hi! Here's the AgriScan app setup:

1. Download APK: [YOUR_LINK]
2. Install: Enable "Unknown Sources" in Settings
3. Open app and grant camera permission
4. Point camera at plant leaf to scan

Features:
✅ Real-time AI detection
✅ Works offline (limited features)
✅ Supports Hindi and Kannada
✅ Free to use

Need help? Contact: [YOUR_EMAIL/WHATSAPP]
```

---

## 🎉 You're Ready!

Your APK is configured and ready to distribute. The backend is running on Render with automatic cold start recovery. Users can download and install the APK, and it will automatically connect to your cloud backend when online, or fall back to on-device detection when offline.

**Next Steps**:
1. Run `.\build-apk-cloud.ps1` to build APK
2. Test on your Android phone
3. Upload to Google Drive/Dropbox
4. Share the download link! 🚀

---

Made with ❤️ by AgriScan Team
