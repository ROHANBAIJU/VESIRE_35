# 🎯 Quick Reference: Key Implementation Details

## 🔧 Bounding Box Implementation

### Location
`Frontend/vesire/lib/screens/scan_screen.dart` - `DetectionResultScreen` widget

### Key Code Pattern
```dart
FutureBuilder<Size>(
  future: _getImageSize(imageFile),
  builder: (context, snapshot) {
    // Calculate image render dimensions
    final imageAspectRatio = imageSize.width / imageSize.height;
    final containerAspectRatio = constraints.maxWidth / constraints.maxHeight;
    
    // Determine fit (width or height constrained)
    if (imageAspectRatio > containerAspectRatio) {
      // Image wider - fit to width
      renderWidth = constraints.maxWidth;
      renderHeight = constraints.maxWidth / imageAspectRatio;
      offsetX = 0;
      offsetY = (constraints.maxHeight - renderHeight) / 2;
    } else {
      // Image taller - fit to height
      renderHeight = constraints.maxHeight;
      renderWidth = constraints.maxHeight * imageAspectRatio;
      offsetX = (constraints.maxWidth - renderWidth) / 2;
      offsetY = 0;
    }
    
    // YOLO normalized coords → screen coords
    final centerX = box.x * renderWidth + offsetX;
    final centerY = box.y * renderHeight + offsetY;
    final boxWidth = box.width * renderWidth;
    final boxHeight = box.height * renderHeight;
    
    final left = centerX - boxWidth / 2;
    final top = centerY - boxHeight / 2;
  }
)
```

**Critical Points:**
- YOLO gives normalized coordinates (0-1)
- `box.x` and `box.y` are CENTER coordinates, not top-left
- Must calculate actual image render size (not just container size)
- Apply offsets for letterboxing/pillarboxing

---

## 🌐 RAG Online/Offline Detection

### Backend
`Backend/api/services/rag_service.py` - `get_diagnosis()` method

### Flow
1. Try cache (instant, offline)
2. Try knowledge base (offline, local JSON)
3. Try online Gemini API (requires internet)
4. Return with source indicator

### Frontend Integration
```dart
// API Service
Future<Map<String, dynamic>> getDiagnosisWithSource(
  String diseaseName, {
  String language = 'en',
  bool useCache = true,
}) async {
  final response = await _client.get(url);
  final data = jsonDecode(response.body);
  return {
    'diagnosis': DiagnosisResponse.fromJson(data),
    'source': data['source'], // 'cache', 'knowledge_base', 'online_llm', 'none'
  };
}
```

### UI Indicators
```dart
String _getSourceLabel(String source) {
  switch (source) {
    case 'online_llm': return '🌐 Online AI (Gemini)';
    case 'cache': return '💾 Cached Data';
    case 'knowledge_base': return '📚 Knowledge Base';
    default: return '📱 Offline Data';
  }
}
```

---

## 🔤 Language Support

### Backend Prompt Structure
```python
prompt = f"""
IMPORTANT: You MUST respond in {language.UP PER()} language.

Please respond in JSON format with the following structure:
{{
    "description": "detailed description in {language}",
    "symptoms": ["symptom 1 in {language}", ...],
    "treatment": {{
        "organic": ["method in {language}", ...],
        ...
    }},
    "care_recommendations": ["recommendation in {language}", ...]
}}

CRITICAL: ALL text content MUST be in {language.UPPER()} language
"""
```

### Frontend Language Passing
```dart
// Get current language
final languageProvider = Provider.of<LanguageProvider>(context, listen: false);
final languageCode = languageProvider.locale.languageCode; // 'en', 'hi', 'kn'

// Pass to API
await _apiService.getDiagnosisWithSource(
  diseaseName,
  language: languageCode,  // ← Here
  useCache: true,
);
```

---

## ✍️ Markdown Formatting

### Widget Implementation
`Frontend/vesire/lib/widgets/markdown_text.dart`

```dart
class MarkdownText extends StatelessWidget {
  final String text;
  
  List<TextSpan> _parseMarkdown(String text) {
    final regex = RegExp(r'\*\*(.*?)\*\*');
    // Finds all **text** patterns
    // Converts to bold TextSpan
  }
}
```

### Usage
```dart
MarkdownText(
  text: "This is **bold** text with **multiple** bold words",
  baseStyle: TextStyle(fontSize: 14),
)
// Result: This is bold text with multiple bold words
```

### Backend Generation
```python
# In Gemini prompt:
"use **bold** for key terms like disease names, plant parts, key actions"

# Output example:
"The **tomato plant** shows signs of **late blight** affecting the **leaves**"
```

---

## 🎯 4-Point Care Recommendations

### Backend Enforcement
```python
# In rag_service.py:
"care_recommendations": [
    "EXACTLY 4 care recommendations in {language}",
    "recommendation 2",
    "recommendation 3", 
    "recommendation 4"
],

# In prompt:
"care_recommendations MUST contain EXACTLY 4 points"
```

### Model Structure
```dart
class Disease {
  final List<String> careRecommendations; // MUST have 4 items
}
```

### UI Display
```dart
_buildMarkdownListSection(
  '🤖 AI Care Recommendations',
  Icons.auto_awesome,
  disease.careRecommendations,  // Always 4 items
  isAI: true, // Purple background
),
```

---

## 📊 Analytics Data Flow

### Provider Architecture
```dart
class AnalyticsProvider extends ChangeNotifier {
  AnalyticsData? _currentAnalytics;
  
  Future<void> loadAnalytics() async {
    // 1. Get history from API
    final history = await _apiService.getUserHistory(userId);
    
    // 2. Calculate metrics
    final healthMetrics = _calculateHealthMetrics(history);
    
    // 3. Build analytics data
    _currentAnalytics = AnalyticsData(
      plantName: latestDetection.className,
      healthPercentage: healthMetrics['healthy'],
      diseaseRisk: healthMetrics['diseaseRisk'],
      careRecommendations: diagnosis.careRecommendations,
      ...
    );
    
    notifyListeners(); // ← Updates UI
  }
}
```

### Health Calculation
```dart
Map<String, int> _calculateHealthMetrics(List<DetectionHistory> history) {
  double avgConfidence = 0.0;
  
  // Average confidence across all detections
  for (var record in history) {
    for (var detection in record.detections) {
      avgConfidence += detection['confidence'];
    }
  }
  
  avgConfidence /= totalDetections;
  
  // Simple health calculation
  final diseaseRisk = (avgConfidence * 100).round();
  final unhealthy = diseaseRisk;
  final healthy = 100 - unhealthy;
  
  return {
    'healthy': healthy,
    'unhealthy': unhealthy,
    'diseaseRisk': diseaseRisk,
  };
}
```

### Screen Integration
```dart
@override
void initState() {
  super.initState();
  WidgetsBinding.instance.addPostFrameCallback((_) {
    Provider.of<AnalyticsProvider>(context, listen: false).loadAnalytics();
  });
}

@override
Widget build(BuildContext context) {
  final analyticsProvider = Provider.of<AnalyticsProvider>(context);
  
  return analyticsProvider.isLoading
    ? Center(child: CircularProgressIndicator())
    : RefreshIndicator(
        onRefresh: () => analyticsProvider.refresh(),
        child: _buildContent(analyticsProvider.currentAnalytics!),
      );
}
```

---

## 🔗 API Endpoint Quick Reference

### Detection
```
POST /api/detect
Body: {
  "image": "data:image/jpeg;base64,<base64>",
  "confidence_threshold": 0.5,
  "save_history": false,
  "user_id": "user-123"
}
Response: {
  "detections": [{
    "class_name": "Tomato leaf late blight",
    "confidence": 0.95,
    "bounding_box": { "x": 0.5, "y": 0.5, "width": 0.3, "height": 0.4 }
  }]
}
```

### Diagnosis
```
GET /api/diagnose/<disease_name>?language=en&use_cache=true
Response: {
  "success": true,
  "disease": {
    "name": "...",
    "description": "...",
    "symptoms": [...],
    "treatment": {...},
    "care_recommendations": [...]
  },
  "source": "online_llm" | "cache" | "knowledge_base"
}
```

### History
```
GET /api/history/<user_id>?limit=10&offset=0
Response: {
  "history": [{
    "id": "uuid",
    "detections": [...],
    "diagnosis": {...},
    "timestamp": "2024-11-06T14:30:00Z"
  }]
}
```

---

## 🎨 Color Scheme Reference

### Primary Colors
- Main Green: `#4CAF50`
- Purple (AI): `#9C27B0`
- Blue (Cache): `#2196F3`
- Orange (Knowledge): `#FF9800`
- Red (Risk): `#F44336`

### Bounding Box
- Box Border: `#00FF00` (Bright green)
- Label Background: `#00FF00`
- Label Text: `Colors.black`

### Source Badges
```dart
'online_llm': Colors.purple.shade600
'cache': Colors.blue.shade600
'knowledge_base': Colors.orange.shade600
'offline': Colors.grey.shade600
```

---

## 📝 Model Structures

### Detection
```dart
class Detection {
  final String className;
  final double confidence;
  final BoundingBox boundingBox;
}

class BoundingBox {
  final double x;      // Center X (0-1)
  final double y;      // Center Y (0-1)
  final double width;  // Width (0-1)
  final double height; // Height (0-1)
}
```

### Diagnosis
```dart
class DiagnosisResponse {
  final bool success;
  final Disease disease;
  final String source; // ← Important for UI
  final String language;
}

class Disease {
  final String name;
  final String scientificName;
  final String description;
  final List<String> symptoms;
  final Treatment treatment;
  final List<String> prevention;
  final List<String> careRecommendations; // ← NEW
  final String severity;
}
```

### Analytics
```dart
class AnalyticsData {
  final String plantName;
  final DateTime scanDate;
  final int healthPercentage;
  final int unhealthyPercentage;
  final int diseaseRisk;
  final double aiConfidence;
  final String aiSummary;
  final List<String> careRecommendations;
  final Map<String, int> environmentalData;
}
```

---

## 🚨 Common Pitfalls & Solutions

### 1. Bounding boxes off-screen
**Problem:** Not accounting for image aspect ratio
**Solution:** Use LayoutBuilder + calculate render dimensions + apply offsets

### 2. Language not changing
**Problem:** Not passing language to backend
**Solution:** Get from LanguageProvider, pass to API methods

### 3. Markdown showing literally
**Problem:** Using `Text` widget instead of `MarkdownText`
**Solution:** Replace with `MarkdownText` widget

### 4. Analytics showing mock data
**Problem:** Provider not initialized or not called
**Solution:** Add to main.dart MultiProvider + call loadAnalytics() in initState

### 5. "No data" in analytics
**Problem:** No detection history saved
**Solution:** Set `save_history: true` in detect API call

---

## 🔍 Debugging Commands

### Check backend status
```bash
curl http://192.168.43.46:5000/api/health
```

### Test detection
```bash
curl -X POST http://192.168.43.46:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"image":"data:image/jpeg;base64,...","confidence_threshold":0.5}'
```

### Check language support
```bash
curl "http://192.168.43.46:5000/api/diagnose/Tomato%20leaf%20late%20blight?language=hi"
```

### View history
```bash
curl "http://192.168.43.46:5000/api/history/user-123?limit=5"
```

---

## 📚 File Reference

### Frontend Key Files
```
lib/
├── screens/
│   ├── scan_screen.dart         ← Camera + Bounding boxes + Diagnosis
│   └── analytics_screen.dart    ← Real data dashboard
├── providers/
│   ├── language_provider.dart   ← Language switching
│   └── analytics_provider.dart  ← Analytics state management
├── widgets/
│   └── markdown_text.dart       ← Bold text rendering
├── services/
│   └── api_service.dart         ← Backend communication
└── models/
    ├── detection_response.dart
    ├── diagnosis_response.dart
    └── detection_history.dart
```

### Backend Key Files
```
Backend/api/
├── app.py                       ← Main Flask routes
├── services/
│   ├── rag_service.py          ← Gemini/OpenAI integration
│   ├── model_service.py        ← YOLOv8 inference
│   └── db_service.py           ← SQLite operations
└── config.py                    ← Environment variables
```

---

🎉 **You now have everything you need to maintain and extend this application!**
