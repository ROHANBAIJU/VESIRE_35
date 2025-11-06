# 🚀 AgriScan Backend - Architecture & Integration Guide

## Overview

Complete backend API for plant disease detection with:
- **AI Model Inference** (YOLO + confidence scores)
- **RAG Layer** (disease diagnosis & treatment)
- **SQLite Database** (offline support)
- **RESTful API** (Flutter frontend integration)

---

## 📁 Backend Architecture

```
Backend/
├── api/
│   ├── app.py                    # Main Flask/FastAPI server
│   ├── routes/
│   │   ├── detection.py          # Disease detection endpoints
│   │   ├── diagnosis.py          # RAG diagnosis endpoints
│   │   └── history.py            # User history endpoints
│   ├── services/
│   │   ├── model_service.py      # YOLO inference
│   │   ├── rag_service.py        # RAG layer
│   │   └── db_service.py         # Database operations
│   ├── models/
│   │   ├── database.py           # SQLAlchemy models
│   │   └── schemas.py            # Pydantic schemas
│   └── utils/
│       ├── image_utils.py        # Image processing
│       └── config.py             # Configuration
├── data/
│   ├── agriscan.db               # SQLite database
│   └── disease_knowledge.json   # Disease info for RAG
├── models/
│   ├── best.pt                   # Trained YOLO model
│   └── plant_disease_model.tflite
└── requirements.txt              # Python dependencies
```

---

## 🎯 API Endpoints

### 1. **Detection Endpoints**

#### `POST /api/detect`
Detect plant diseases in uploaded image

**Request:**
```json
{
  "image": "base64_encoded_image",
  "confidence_threshold": 0.5
}
```

**Response:**
```json
{
  "success": true,
  "detections": [
    {
      "class_id": 5,
      "class_name": "Tomato leaf late blight",
      "confidence": 0.87,
      "bounding_box": {
        "x": 0.45,
        "y": 0.32,
        "width": 0.25,
        "height": 0.30
      }
    }
  ],
  "processing_time": 0.234,
  "image_id": "uuid-123"
}
```

#### `POST /api/detect/batch`
Batch detection for multiple images

---

### 2. **Diagnosis Endpoints (RAG Layer)**

#### `POST /api/diagnose`
Get disease diagnosis and treatment (requires internet)

**Request:**
```json
{
  "disease_name": "Tomato leaf late blight",
  "language": "en"  // or "kn" for Kannada
}
```

**Response:**
```json
{
  "success": true,
  "disease": {
    "name": "Tomato leaf late blight",
    "scientific_name": "Phytophthora infestans",
    "description": "A fungal disease affecting tomato plants...",
    "symptoms": [
      "Dark spots on leaves",
      "White mold on underside",
      "Yellowing of leaves"
    ],
    "treatment": {
      "organic": [
        "Apply copper-based fungicide",
        "Remove affected leaves"
      ],
      "chemical": [
        "Use chlorothalonil spray",
        "Apply mancozeb"
      ],
      "prevention": [
        "Ensure good air circulation",
        "Avoid overhead watering"
      ]
    },
    "severity": "high",
    "cached": false
  }
}
```

#### `GET /api/diagnose/offline/{disease_id}`
Get cached diagnosis (offline mode)

---

### 3. **History Endpoints**

#### `POST /api/history`
Save detection to history

**Request:**
```json
{
  "user_id": "user-123",
  "image_id": "uuid-123",
  "detections": [...],
  "diagnosis": {...}
}
```

#### `GET /api/history/{user_id}`
Get user's detection history

#### `DELETE /api/history/{detection_id}`
Delete history entry

---

### 4. **Utility Endpoints**

#### `GET /api/health`
Health check endpoint

#### `GET /api/models`
Get available models and versions

#### `GET /api/diseases`
Get list of all supported diseases

---

## 🗄️ Database Schema

### SQLite Tables:

```sql
-- Detection History
CREATE TABLE detections (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    image_path TEXT,
    image_base64 TEXT,  -- For offline access
    detections JSON,    -- Array of detections
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    location TEXT,      -- Optional GPS coordinates
    notes TEXT
);

-- Disease Information (Cached RAG)
CREATE TABLE diseases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    scientific_name TEXT,
    description TEXT,
    symptoms JSON,
    treatment JSON,
    severity TEXT,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- User Preferences
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    name TEXT,
    language TEXT DEFAULT 'en',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔄 Request Flow

### Online Mode (Internet Available):
```
Flutter App
    ↓
POST /api/detect (image)
    ↓
YOLO Model Inference
    ↓
Return detections + confidence
    ↓
POST /api/diagnose (disease_name)
    ↓
RAG Layer (LLM/Knowledge Base)
    ↓
Return diagnosis + treatment
    ↓
Cache to SQLite
    ↓
POST /api/history (save)
    ↓
Return complete response
```

### Offline Mode (No Internet):
```
Flutter App
    ↓
Check local SQLite cache
    ↓
If disease info exists:
    - Return cached diagnosis
    ↓
If not cached:
    - Show basic info
    - Prompt "Connect for full diagnosis"
```

---

## 🧠 RAG Layer Options

### Option 1: Local Knowledge Base
```python
# Use pre-populated JSON with disease information
disease_knowledge = {
    "Tomato leaf late blight": {
        "description": "...",
        "treatment": "...",
        "symptoms": [...]
    }
}
```

### Option 2: OpenAI API
```python
# Use GPT-4 for dynamic diagnosis
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "system",
        "content": "You are a plant pathology expert..."
    }, {
        "role": "user",
        "content": f"Diagnose {disease_name}"
    }]
)
```

### Option 3: LangChain RAG
```python
# Use LangChain with vector database
from langchain import RetrievalQA

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever()
)
```

---

## 📦 Tech Stack

### Backend Framework:
**Option A: Flask** (Simpler, faster to setup)
```python
from flask import Flask, request, jsonify
app = Flask(__name__)
```

**Option B: FastAPI** (Modern, automatic docs, async)
```python
from fastapi import FastAPI
app = FastAPI()
```

### Dependencies:
```txt
# Core
flask==3.0.0  # or fastapi==0.104.1
flask-cors==4.0.0
python-dotenv==1.0.0

# AI/ML
ultralytics==8.0.200
torch==2.1.0
torchvision==0.16.0
opencv-python==4.8.1.78
Pillow==10.1.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1

# RAG (choose one)
openai==1.3.5  # For OpenAI
langchain==0.0.340  # For LangChain
sentence-transformers==2.2.2  # For embeddings

# Utilities
pydantic==2.5.0
numpy==1.24.3
```

---

## 🚀 Implementation Steps

### Step 1: Create Flask API Server
```python
# api/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.model_service import YOLOService
from services.db_service import DatabaseService

app = Flask(__name__)
CORS(app)

model_service = YOLOService()
db_service = DatabaseService()

@app.route('/api/detect', methods=['POST'])
def detect():
    # Your detection logic
    pass
```

### Step 2: Implement Model Service
```python
# api/services/model_service.py
from ultralytics import YOLO

class YOLOService:
    def __init__(self):
        self.model = YOLO('path/to/best.pt')
    
    def detect(self, image, confidence=0.5):
        results = self.model(image, conf=confidence)
        return self.format_results(results)
```

### Step 3: Setup Database
```python
# api/services/db_service.py
import sqlite3

class DatabaseService:
    def __init__(self):
        self.db = sqlite3.connect('data/agriscan.db')
    
    def save_detection(self, data):
        # Save to database
        pass
```

### Step 4: Implement RAG Layer
```python
# api/services/rag_service.py
class RAGService:
    def get_diagnosis(self, disease_name):
        # Fetch from knowledge base or LLM
        pass
```

---

## 🔌 Flutter Integration

### 1. Create API Service in Flutter:
```dart
class ApiService {
  static const baseUrl = 'http://your-server:5000/api';
  
  Future<DetectionResponse> detectDisease(File image) async {
    // Convert image to base64
    final bytes = await image.readAsBytes();
    final base64Image = base64Encode(bytes);
    
    // Call API
    final response = await http.post(
      Uri.parse('$baseUrl/detect'),
      body: jsonEncode({'image': base64Image}),
    );
    
    return DetectionResponse.fromJson(jsonDecode(response.body));
  }
}
```

### 2. Use with Camera:
```dart
// In your camera overlay screen
final detections = await apiService.detectDisease(imageFile);

// Display bounding boxes
for (var detection in detections.detections) {
  Positioned(
    left: detection.boundingBox.x * screenWidth,
    top: detection.boundingBox.y * screenHeight,
    child: BoundingBox(
      label: detection.className,
      confidence: detection.confidence,
    ),
  )
}
```

---

## 🎯 Recommended Approach

### **For Your Hackathon/Project:**

1. **Use Flask** (simpler, faster to setup)
2. **Local Knowledge Base** (no API costs, works offline)
3. **SQLite** (easy, portable, offline-first)
4. **Deploy on:** 
   - **Local**: Run on your laptop during demo
   - **Cloud**: Deploy to Heroku/Railway/Render (free tier)
   - **Mobile**: Bundle with app (if model is small enough)

---

## ⏱️ Timeline

### Today (2-3 hours):
- ✅ Create Flask API structure
- ✅ Implement detection endpoint
- ✅ Setup SQLite database
- ✅ Create disease knowledge base

### Tomorrow (2-3 hours):
- ✅ Implement RAG layer
- ✅ Add history endpoints
- ✅ Test with Postman
- ✅ Document API

### Integration (1-2 hours):
- ✅ Flutter team integrates endpoints
- ✅ Test end-to-end flow
- ✅ Fix bugs

---

## 🎁 What I'll Create for You

I can immediately create:
1. ✅ **Complete Flask API** (`app.py`, all routes)
2. ✅ **Model Service** (YOLO inference)
3. ✅ **Database Service** (SQLite operations)
4. ✅ **RAG Service** (disease diagnosis)
5. ✅ **Disease Knowledge Base** (JSON with treatments)
6. ✅ **API Documentation** (endpoints, request/response)
7. ✅ **Flutter Integration Example** (Dart code)

---

## 🚀 Ready to Build?

**Say the word and I'll create:**
- Complete Flask backend with all endpoints
- Database schema and services
- Disease knowledge base
- API documentation
- Flutter integration code

**Your frontend team can start integrating immediately!** 🔥

Let's build this! 🌱
