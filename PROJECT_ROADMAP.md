# 🚀 AgriScan AR - Project Completion Roadmap

## Current Status: Learning Phase → Production Phase

**Goal:** Transform AR test app into real-time plant disease detection with AR overlays

---

## 📋 PHASE 1: AI Model Preparation (WEEK 1) ⭐ START HERE

### Step 1.1: Train & Select Best Model
**Location:** `Backend/DATASET/`

**Actions:**
1. Run all 4 training notebooks in Google Colab:
   - `YOLOv8_large_object_detection.ipynb`
   - `YOLOv8_seg_large_segmentation.ipynb`
   - `faster_rcnn_object_detection.ipynb`
   - `mask_r_cnn_segmentation.ipynb`

2. Compare model performance:
   - Check mAP (mean Average Precision)
   - Check inference speed (FPS)
   - **Recommendation:** YOLOv8m or YOLOv8l (best balance of speed + accuracy)

3. Select final model based on:
   - ✅ High accuracy (mAP > 0.75)
   - ✅ Fast inference (> 15 FPS on mobile)
   - ✅ Small size (< 50 MB for mobile)

**Expected Output:**
- Trained model weights (`.pt` file for YOLO, `.pth` for others)
- Performance metrics documented

---

### Step 1.2: Convert Model to TensorFlow Lite
**Critical for mobile deployment!**

**For YOLOv8 (Recommended Path):**

```python
# In your notebook or new script
from ultralytics import YOLO

# Load your trained model
model = YOLO('path/to/best.pt')

# Export to TFLite (with INT8 quantization for speed)
model.export(
    format='tflite',
    imgsz=640,  # or 416 for faster inference
    int8=True,  # Enable INT8 quantization
    data='your_dataset.yaml'  # For representative dataset
)

# This creates: best_saved_model/best_int8.tflite
```

**For Faster R-CNN/Mask R-CNN:**
- Use TensorFlow's converter (more complex)
- Or stick with YOLOv8 for simplicity

**Expected Output:**
- `plant_disease_model.tflite` (your final model file)
- Model size: 10-30 MB (quantized)
- Labels file: `labels.txt` (14 disease classes)

---

### Step 1.3: Test Model Locally
**Verify it works before mobile integration**

```python
import tensorflow as tf
import numpy as np
from PIL import Image

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path='plant_disease_model.tflite')
interpreter.allocate_tensors()

# Get input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test with sample image
image = Image.open('test_plant.jpg').resize((640, 640))
input_data = np.expand_dims(np.array(image), axis=0).astype(np.float32) / 255.0

# Run inference
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

# Get results
detections = interpreter.get_tensor(output_details[0]['index'])
print("Detections:", detections)
```

**Expected Output:**
- Successfully detect diseases in test images
- Inference time < 100ms on your PC

---

## 📋 PHASE 2: Flutter Integration (WEEK 2)

### Step 2.1: Add TFLite Dependencies

**Update `ar_test_app/pubspec.yaml`:**

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # Camera for live feed
  camera: ^0.10.5+5
  
  # TFLite for on-device AI
  tflite_flutter: ^0.10.4
  tflite_flutter_helper: ^0.3.1
  
  # Image processing
  image: ^4.1.3
  
  # Local database
  sqflite: ^2.3.0
  path_provider: ^2.1.1
  
  # UI
  cupertino_icons: ^1.0.8
```

**Run:**
```bash
cd ar_test_app
flutter pub get
```

---

### Step 2.2: Add Model Assets

**Create assets folder:**
```
ar_test_app/
  assets/
    models/
      plant_disease_model.tflite
      labels.txt
```

**Update `pubspec.yaml`:**
```yaml
flutter:
  assets:
    - assets/models/plant_disease_model.tflite
    - assets/models/labels.txt
```

**Create `labels.txt`:**
```
Tomato_Septoria
Corn_Leaf_Blight
Squash_Powdery_Leaf
Apple_Healthy
Tomato_Bacterial_Spot
Tomato_Healthy
Apple_Rust_Leaf
Apple_Scab_Leaf
Grape_Healthy
Corn_Rust_Leaf
Grape_Black_Rot
Corn_Gray_Leaf_Spot
BellPepper_Healthy
BellPepper_Leaf_Spot
```

---

### Step 2.3: Create TFLite Service Class

**Create `lib/services/disease_detector.dart`:**

This will handle:
- ✅ Loading TFLite model
- ✅ Processing camera frames
- ✅ Running inference
- ✅ Parsing detections (bounding boxes + class labels)

---

### Step 2.4: Build Camera + AR Overlay Screen

**Create `lib/screens/ar_detection_screen.dart`:**

**Features:**
- Live camera feed
- Real-time frame processing (every 100ms)
- Draw bounding boxes over detected diseases
- Show disease name labels
- Tap box for treatment info

**UI Layout:**
```
┌─────────────────────────┐
│   Camera Feed (Full)    │
│                         │
│   ┌──────────────┐     │  ← Bounding box overlay
│   │ Tomato Blight│     │  ← Disease label
│   └──────────────┘     │
│                         │
│   [Status: Scanning]    │  ← Top overlay
│   [Tap box for info]    │
└─────────────────────────┘
```

---

### Step 2.5: Implement Custom Painter for Bounding Boxes

**Create `lib/widgets/detection_painter.dart`:**

```dart
// Will use CustomPaint to draw:
// - Rectangles around detected diseases
// - Labels with disease names
// - Confidence scores
```

---

## 📋 PHASE 3: Offline Database (WEEK 2-3)

### Step 3.1: Create Treatment Database

**Create `lib/services/treatment_database.dart`:**

**SQLite Schema:**
```sql
CREATE TABLE treatments (
  id INTEGER PRIMARY KEY,
  disease_name TEXT NOT NULL,
  description TEXT,
  symptoms TEXT,
  treatment TEXT,
  prevention TEXT,
  severity TEXT,
  affected_crops TEXT
);
```

---

### Step 3.2: Populate Database with Treatment Data

**For each of 14 diseases, add:**
- Symptoms description
- Immediate treatment steps
- Organic solutions
- Chemical solutions (if needed)
- Prevention tips
- Severity level (Low/Medium/High)

**Example Entry:**
```json
{
  "disease_name": "Tomato_Bacterial_Spot",
  "description": "Bacterial infection causing dark spots on leaves and fruits",
  "symptoms": "Small dark spots with yellow halos, leaf curling",
  "treatment": "1. Remove infected leaves\n2. Apply copper-based fungicide\n3. Improve air circulation",
  "prevention": "Use disease-resistant varieties, avoid overhead watering",
  "severity": "High"
}
```

---

### Step 3.3: Build Treatment Detail Screen

**Create `lib/screens/treatment_detail_screen.dart`:**

**When user taps detected disease:**
- Show full disease information
- Treatment steps with images
- Shopping list for treatments
- "Call Expert" button (optional online feature)

---

## 📋 PHASE 4: Localization (WEEK 3)

### Step 4.1: Add Localization Dependencies

```yaml
dependencies:
  flutter_localizations:
    sdk: flutter
  intl: ^0.19.0
```

---

### Step 4.2: Create Translation Files

**Create `lib/l10n/`:**
- `app_en.arb` (English)
- `app_kn.arb` (Kannada)

**Example:**
```json
// app_en.arb
{
  "appTitle": "AgriScan AR",
  "scanPlant": "Scan Plant",
  "diseaseDetected": "Disease Detected",
  "treatment": "Treatment"
}

// app_kn.arb
{
  "appTitle": "ಅಗ್ರಿಸ್ಕ್ಯಾನ್ AR",
  "scanPlant": "ಸಸ್ಯವನ್ನು ಸ್ಕ್ಯಾನ್ ಮಾಡಿ",
  "diseaseDetected": "ರೋಗ ಪತ್ತೆಯಾಗಿದೆ",
  "treatment": "ಚಿಕಿತ್ಸೆ"
}
```

---

### Step 4.3: Translate Treatment Database

- Translate all disease names
- Translate treatment instructions
- Translate UI text

---

## 📋 PHASE 5: Polish & Testing (WEEK 4)

### Step 5.1: UI/UX Improvements
- Add loading indicators
- Add success/error messages
- Add onboarding tutorial
- Add settings (language, camera quality)

---

### Step 5.2: Performance Optimization
- Reduce inference frequency (every 200ms instead of every frame)
- Implement frame skipping
- Add confidence threshold (only show detections > 70%)
- Cache model in memory

---

### Step 5.3: Real-World Testing
- Test with real plants
- Test in different lighting conditions
- Test with farmers (if possible)
- Gather feedback

---

### Step 5.4: Add Optional Cloud Features (If Time)
- Firebase setup
- Cloud Functions for Gemini API
- "Get Advanced Tips" button
- Upload image for second opinion

---

## 📋 PHASE 6: Deployment (WEEK 4)

### Step 6.1: Build Release APK

```bash
cd ar_test_app
flutter build apk --release
```

---

### Step 6.2: Test on Multiple Devices
- Low-end Android (to check performance)
- Different screen sizes
- Different Android versions

---

### Step 6.3: Prepare Hackathon Presentation
- Demo video
- Slide deck
- Live demo on phone
- Impact statistics

---

## 🎯 MINIMUM VIABLE PRODUCT (MVP) Checklist

**Must Have for Hackathon:**
- [x] Dataset prepared (DONE ✅)
- [ ] TFLite model trained and converted
- [ ] Live camera feed working
- [ ] Real-time disease detection
- [ ] AR bounding box overlay
- [ ] At least 3-5 disease classes working
- [ ] Basic treatment database
- [ ] Offline functionality proven
- [ ] Clean UI

**Nice to Have:**
- [ ] All 14 disease classes
- [ ] Kannada localization
- [ ] Cloud features
- [ ] Advanced UI/UX

---

## 📊 Timeline Summary

| Week | Focus | Deliverable |
|------|-------|-------------|
| **Week 1** | AI Model | Working TFLite model |
| **Week 2** | Flutter Integration | Live detection working |
| **Week 3** | Database + i18n | Offline treatments + Kannada |
| **Week 4** | Polish + Test | Hackathon-ready app |

---

## 🚨 CRITICAL PATH (Fastest Route to Demo)

### Day 1-2: Model
1. Train YOLOv8m on your dataset
2. Export to TFLite
3. Test inference locally

### Day 3-5: Basic Flutter App
1. Add camera feed
2. Integrate TFLite
3. Draw bounding boxes
4. Show disease labels

### Day 6-7: Make it Useful
1. Add basic treatment database (even just 5 diseases)
2. Create detail screen
3. Polish UI

### Day 8-10: Test & Refine
1. Test on phone
2. Fix bugs
3. Optimize performance
4. Record demo video

---

## 📝 CODE ARCHITECTURE (Target)

```
ar_test_app/
├── lib/
│   ├── main.dart                      # App entry
│   ├── screens/
│   │   ├── ar_detection_screen.dart   # Main AR camera screen
│   │   ├── treatment_detail_screen.dart
│   │   └── settings_screen.dart
│   ├── services/
│   │   ├── disease_detector.dart      # TFLite inference
│   │   ├── treatment_database.dart    # SQLite database
│   │   └── camera_service.dart        # Camera handling
│   ├── models/
│   │   ├── detection_result.dart      # Data class for detections
│   │   └── treatment.dart             # Data class for treatments
│   ├── widgets/
│   │   ├── detection_painter.dart     # Custom painter for boxes
│   │   ├── detection_box.dart         # Bounding box widget
│   │   └── status_overlay.dart        # Top status bar
│   └── l10n/                          # Localization files
├── assets/
│   └── models/
│       ├── plant_disease_model.tflite
│       └── labels.txt
└── pubspec.yaml
```

---

## 🎉 Success Metrics

### Technical Success:
- ✅ Model runs on device < 100ms per frame
- ✅ Detection accuracy > 75%
- ✅ App works 100% offline
- ✅ No crashes in 30-minute testing session

### Hackathon Success:
- ✅ Live demo works smoothly
- ✅ Judges can test on real plants
- ✅ Clear value proposition demonstrated
- ✅ Social impact clearly communicated

---

## 🔥 YOUR IMMEDIATE NEXT ACTION

**RIGHT NOW, DO THIS:**

1. **Open your best training notebook** (probably YOLOv8)
2. **Train the model** (or check if already trained)
3. **Export to TFLite** using code above
4. **Test the .tflite file** with sample images
5. **Copy the .tflite file** to `ar_test_app/assets/models/`

**Then come back and I'll help you build the Flutter detection screen!**

---

**Let's build this! 🚀🌾📱**
