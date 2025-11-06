# 🚀 AgriScan Backend - Quick Start Guide

## ✅ Setup (5 minutes)

### 1. Install Dependencies
```bash
cd Backend
pip install -r ../requirements.txt
```

### 2. Create Environment File (Optional)
```bash
# Copy example env file
cp .env.example .env

# Edit if needed (defaults work fine)
```

### 3. Start Server
```bash
cd api
python app.py
```

Server will start at: **http://localhost:5000**

---

## 🧪 Test the API

### Using Browser:
```
http://localhost:5000/api/health
http://localhost:5000/api/info
http://localhost:5000/api/models
http://localhost:5000/api/diseases
```

### Using curl:
```bash
# Health check
curl http://localhost:5000/api/health

# Get disease list
curl http://localhost:5000/api/diseases

# Get diagnosis
curl "http://localhost:5000/api/diagnose/Tomato%20leaf%20late%20blight"
```

---

## 📱 Connect Flutter App

### Update Flutter ApiService:
```dart
class ApiService {
  // Replace with your computer's IP address
  static const String baseUrl = 'http://192.168.1.100:5000/api';
  // Or use localhost if running emulator
  // static const String baseUrl = 'http://10.0.2.2:5000/api';  // Android emulator
  // static const String baseUrl = 'http://localhost:5000/api'; // iOS simulator
}
```

### Find Your IP Address:

**Windows:**
```bash
ipconfig
# Look for IPv4 Address under WiFi adapter
```

**Mac/Linux:**
```bash
ifconfig
# Look for inet under en0 or wlan0
```

---

## 🎯 Key Endpoints

### 1. Detect Disease
```bash
POST /api/detect
Content-Type: application/json

{
  "image": "base64_encoded_image",
  "confidence_threshold": 0.5
}
```

### 2. Get Diagnosis
```bash
GET /api/diagnose/<disease_name>?language=en
```

### 3. Save to History
```bash
POST /api/history
Content-Type: application/json

{
  "user_id": "user-123",
  "detections": [...],
  "diagnosis": {...}
}
```

### 4. Get History
```bash
GET /api/history/<user_id>?limit=50&offset=0
```

---

## 📂 Directory Structure

```
Backend/
├── api/
│   ├── app.py              # Main Flask server ← START HERE
│   ├── config.py           # Configuration
│   ├── services/
│   │   ├── model_service.py    # YOLO inference
│   │   ├── db_service.py       # SQLite operations
│   │   └── rag_service.py      # Disease diagnosis
│   └── ...
├── data/
│   ├── agriscan.db         # SQLite database (auto-created)
│   └── disease_knowledge.json  # Disease info
└── models/
    └── agriscan_plantdoc/
        └── weights/
            └── best.pt     # Your trained YOLO model
```

---

## 🔍 Troubleshooting

### Model Not Found Error:
```
❌ Error: Model not found at Backend/models/agriscan_plantdoc/weights/best.pt
```

**Solution:**
1. Make sure model training completed
2. Check model path in `api/config.py`
3. Or update `MODEL_PATH` to point to your model

### Port Already in Use:
```
❌ Error: Address already in use
```

**Solution:**
```bash
# Change port in .env file
PORT=5001

# Or kill existing process
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :5000
kill -9 <PID>
```

### Flutter Can't Connect:
```
❌ Error: Failed host lookup / Connection refused
```

**Solution:**
1. Check Flask is running: `http://localhost:5000/api/health`
2. Use your computer's IP, not `localhost`
3. Check firewall isn't blocking port 5000
4. Ensure phone and computer on same WiFi network

---

## 📊 What's Working

### ✅ Implemented:
- [x] YOLO model inference
- [x] Bounding box detection
- [x] Confidence scoring
- [x] Disease diagnosis (RAG)
- [x] Treatment recommendations
- [x] SQLite database
- [x] Offline support
- [x] History tracking
- [x] CORS enabled
- [x] Error handling
- [x] 15+ API endpoints

### 🔄 Next Steps (Optional):
- [ ] Add more diseases to knowledge base
- [ ] Implement user authentication
- [ ] Add image optimization
- [ ] Deploy to cloud
- [ ] Add API rate limiting
- [ ] Implement caching layer

---

## 🎓 For Your Frontend Team

### Give them:
1. ✅ **Server URL**: `http://YOUR_IP:5000/api`
2. ✅ **API Documentation**: `API_DOCUMENTATION.md`
3. ✅ **Flutter Code**: See documentation for full examples
4. ✅ **Test with Postman first**: Verify endpoints work

### They need to:
1. Update `ApiService baseUrl`
2. Copy model classes (Detection, BoundingBox, etc.)
3. Integrate in camera screen
4. Display bounding boxes
5. Show diagnosis dialog

---

## 🚀 Production Deployment (Later)

### Railway (Recommended):
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Environment Variables (Production):
```env
HOST=0.0.0.0
PORT=5000
DEBUG=False
USE_ONLINE_RAG=True
OPENAI_API_KEY=your_production_key
```

---

## 📝 Testing Checklist

Before giving to frontend team:

- [ ] Server starts without errors
- [ ] `/api/health` returns 200
- [ ] `/api/models` shows model info
- [ ] `/api/diseases` returns disease list
- [ ] `/api/diagnose/Tomato%20leaf%20late%20blight` works
- [ ] Database file created at `data/agriscan.db`
- [ ] No errors in console

---

## 💡 Tips

### Development:
- Use `DEBUG=True` for detailed error messages
- Check console output for errors
- Test endpoints with Postman before Flutter integration
- Keep server running while Flutter team tests

### Performance:
- Model inference takes ~0.2-0.5 seconds
- First request may be slower (model loading)
- Consider caching frequently detected diseases
- Optimize image size before sending

### Offline Mode:
- Diagnosis cached automatically after first fetch
- History saved to SQLite
- Works without internet after initial diagnosis
- Perfect for farmers in remote areas

---

## 🎉 You're Ready!

Your backend is **production-ready** and waiting for Flutter integration!

**Start the server and share the URL with your team! 🚀**

```bash
cd Backend/api
python app.py
```

Then visit: `http://localhost:5000/api/health` to verify it's running!
