# ✅ AgriScan Cloud Deployment Checklist

## 📋 Pre-Deployment

- [ ] Code is working locally (backend + frontend)
- [ ] Multilingual RAG tested (Hindi & Kannada working)
- [ ] Model file included in repo (`Backend/models/agriscan_combined/weights/best.pt`)
- [ ] Git repository is up to date
- [ ] Gemini API key obtained from https://makersuite.google.com/app/apikey

---

## 🔧 Backend Deployment (Render)

### Setup
- [ ] Created Render account at https://render.com
- [ ] Connected GitHub repository to Render
- [ ] Created new Web Service

### Configuration
- [ ] Set **Root Directory**: `Backend`
- [ ] Set **Build Command**: `pip install -r requirements.txt`
- [ ] Set **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 api.app:app`
- [ ] Set **Environment**: Python 3
- [ ] Set **Region**: Oregon (or closest to you)
- [ ] Set **Plan**: Free

### Environment Variables
- [ ] `USE_ONLINE_RAG` = `true`
- [ ] `GEMINI_API_KEY` = `your_actual_key_here`
- [ ] `DEBUG` = `false`
- [ ] `CORS_ORIGINS` = `*` (or specific domains)

### Deployment
- [ ] Clicked "Create Web Service"
- [ ] Watched build logs (no errors)
- [ ] Deployment successful
- [ ] Noted down backend URL: `https://_____________.onrender.com`

### Testing
- [ ] Health endpoint works: `curl https://your-app.onrender.com/api/health`
- [ ] Returns: `{"status":"healthy","model_loaded":true,...}`
- [ ] Hindi RAG works: Test `/api/diagnose/Tomato%20leaf%20late%20blight?language=hi`
- [ ] Kannada RAG works: Test `/api/diagnose/Tomato%20leaf%20late%20blight?language=kn`

---

## 🌐 Frontend Deployment (Netlify)

### Update Configuration
- [ ] Updated `Frontend/vesire/lib/config/app_config.dart`:
  ```dart
  static const String _productionApiUrl = 'https://your-app.onrender.com/api';
  ```
- [ ] Committed changes to Git

### Build
- [ ] Ran `flutter pub get`
- [ ] Ran `flutter build web --release --web-renderer canvaskit`
- [ ] Verified `build/web` folder created
- [ ] Checked folder size (~15-20 MB)

### Setup
- [ ] Created Netlify account at https://netlify.com
- [ ] Noted down deployment method (drag-drop or Git)

### Deploy (Drag & Drop)
- [ ] Went to https://app.netlify.com/
- [ ] Clicked "Add new site" → "Deploy manually"
- [ ] Dragged `Frontend/vesire/build/web` folder
- [ ] Deployment successful
- [ ] Noted down frontend URL: `https://_____________.netlify.app`

### Deploy (Git - Optional)
- [ ] Connected Netlify to GitHub
- [ ] Selected repository
- [ ] Set base directory: `Frontend/vesire`
- [ ] Set build command: `flutter build web --release`
- [ ] Set publish directory: `Frontend/vesire/build/web`
- [ ] Triggered deployment

### Testing
- [ ] Frontend loads at Netlify URL
- [ ] No console errors in browser
- [ ] Language switcher works (English/Hindi/Kannada)
- [ ] UI translations display correctly

---

## 🔗 Integration Testing

### CORS Configuration
- [ ] Updated `CORS_ORIGINS` on Render to include Netlify URL:
  ```
  CORS_ORIGINS=https://your-app.netlify.app,http://localhost:*
  ```
- [ ] Redeployed backend on Render

### End-to-End Testing
- [ ] Opened frontend at Netlify URL
- [ ] Changed language to Hindi
- [ ] Started plant detection
- [ ] Captured/uploaded image
- [ ] Verified detection works
- [ ] Checked RAG response is in Hindi
- [ ] Changed to Kannada and repeated test
- [ ] Verified Kannada responses work

### Mobile Testing
- [ ] Updated mobile app config to use production backend:
  ```dart
  static const bool _forceProduction = true;
  ```
- [ ] Built and ran mobile app
- [ ] Tested detection on mobile
- [ ] Verified cloud backend connection works
- [ ] Tested offline (should show error gracefully)

---

## 📱 Mobile App Updates

### For Cloud Backend
- [ ] Set `_forceProduction = true` in `app_config.dart`
- [ ] Rebuilt app: `flutter build apk` (Android) or `flutter build ios` (iOS)
- [ ] Tested on physical device
- [ ] Verified works on mobile data (not just WiFi)

### For Local Backend (Development)
- [ ] Set `_forceProduction = false`
- [ ] Ensured `_localApiUrl` has correct laptop IP
- [ ] Connected to same WiFi/hotspot
- [ ] Tested local development

---

## 🚨 Troubleshooting

### Backend Issues
- [ ] Checked Render logs for errors
- [ ] Verified model file uploaded (should see "Model loaded: True")
- [ ] Tested health endpoint returns 200 OK
- [ ] Confirmed Gemini API key is valid
- [ ] Verified `USE_ONLINE_RAG=true` in environment

### Frontend Issues
- [ ] Checked browser console for errors
- [ ] Verified backend URL is correct in code
- [ ] Cleared browser cache and retried
- [ ] Tested in incognito mode
- [ ] Verified CORS is configured correctly

### Connection Issues
- [ ] Checked CORS includes Netlify domain
- [ ] Verified backend is not sleeping (call health endpoint first)
- [ ] Tested backend URL directly in browser
- [ ] Checked network tab in DevTools for failed requests

---

## 📊 Monitoring Setup

### Backend Monitoring
- [ ] Set up uptime monitor (e.g., UptimeRobot) for `/api/health`
- [ ] Configured alerts for downtime
- [ ] Bookmarked Render logs page

### Frontend Monitoring
- [ ] Enabled Netlify Analytics (optional, $9/month)
- [ ] Added Google Analytics (optional)
- [ ] Configured error tracking with Sentry (optional)

---

## 🎉 Final Verification

### Core Features
- [ ] Detection works on cloud
- [ ] Hindi translation works
- [ ] Kannada translation works
- [ ] Image upload works
- [ ] Results display correctly
- [ ] Analytics page shows data
- [ ] Mobile app connects to cloud

### Performance
- [ ] First load time < 5 seconds (after cold start)
- [ ] Detection completes < 3 seconds
- [ ] RAG response < 20 seconds
- [ ] No console errors
- [ ] No CORS errors

### Documentation
- [ ] Updated README with cloud URLs
- [ ] Documented backend URL
- [ ] Documented frontend URL
- [ ] Shared links with team

---

## 🔄 Continuous Deployment

### Auto-Deploy Setup
- [ ] Render auto-deploys on push to `main` branch
- [ ] Netlify auto-deploys on push to `main` branch (if Git connected)
- [ ] Tested by making a small change and pushing

### Version Control
- [ ] Tagged release: `git tag v1.0.0`
- [ ] Pushed tags: `git push --tags`
- [ ] Created release notes

---

## 📝 Post-Deployment Tasks

### Share with Team
- [ ] Backend URL: `https://_____________.onrender.com`
- [ ] Frontend URL: `https://_____________.netlify.app`
- [ ] Gemini API usage limits documented
- [ ] Known limitations documented

### Next Steps
- [ ] Custom domain setup (optional)
- [ ] SSL certificate (auto on Render/Netlify)
- [ ] Upgrade to paid tier if needed
- [ ] Monitor usage and costs
- [ ] Collect user feedback

---

## 🎯 Success Criteria

**✅ Deployment is successful when**:
1. Backend health endpoint returns 200 OK
2. Frontend loads without errors
3. Can detect plant diseases
4. RAG returns multilingual responses (Hindi/Kannada)
5. Mobile app connects to cloud backend
6. No CORS errors
7. Detection + RAG completes end-to-end

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Netlify Docs**: https://docs.netlify.com
- **Flutter Web**: https://docs.flutter.dev/platform-integration/web
- **Gemini API**: https://ai.google.dev/docs

---

**Congratulations! Your multilingual plant disease detection app is now live! 🎉**

---

Last Updated: November 2025
Version: 1.0.0
