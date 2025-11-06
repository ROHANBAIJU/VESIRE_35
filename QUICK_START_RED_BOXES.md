# 🚀 Quick Start - Real-Time Red Bounding Boxes

## Start Testing in 3 Steps

### Step 1: Start Flask Backend
```powershell
cd Z:\VESIRE_35\Backend\api
python app.py
```

**Expected Output:**
```
 * Running on http://192.168.43.46:5000
```

### Step 2: Run Flutter App
```powershell
cd Z:\VESIRE_35\Frontend\vesire
flutter run
```

### Step 3: Test Detection

1. **Open app** → Login → Tap "Scan"
2. **Point camera at a plant image** (can use the laptop screen as shown in your screenshot)
3. **Wait 2 seconds** - Red boxes will appear automatically!

---

## 🔍 What to Look For

### ✅ Success Indicators:

#### In Flutter Terminal:
```
🚀 [FLUTTER] Starting real-time detection...
📸 [FLUTTER] Frame captured, sending to backend...
🔵 [FLUTTER API] Starting detection request to http://192.168.43.46:5000/api/detect
🔵 [FLUTTER API] Image converted to base64
🔵 [FLUTTER API] Response received: Status 200
✅ [FLUTTER API] Detection successful: 2 detections
🎯 [FLUTTER] Detections found: Tomato Blight(87.3%)
```

#### In Flask Terminal:
```
🟢 [FLASK] ========== NEW DETECTION REQUEST ==========
🟢 [FLASK] Request from: 192.168.43.x
🟢 [FLASK] Running TFLite model detection...
🟢 [FLASK] ✅ Detection complete: 2 detections found
🟢 [FLASK]    [1] Tomato Early Blight: 87.34%
🟢 [FLASK] ================================================
```

#### On Phone Screen:
- 🔴 **RED bounding boxes** around detected plants
- **Confidence percentages** (e.g., "Tomato Blight 87%")
- **Red floating bar** with "Plant Detected!" message
- **"Analytics" button** to navigate

---

## ❌ If You See No Red Boxes

### Check 1: Backend Running?
Look for Flask logs. If nothing, backend isn't receiving requests.

**Fix:**
```powershell
# Check if backend is accessible
curl http://192.168.43.46:5000/api/health
```

### Check 2: Network Connected?
Phone and computer must be on same Wi-Fi.

**Fix:**
```powershell
# Get your IP address
ipconfig
# Look for "IPv4 Address" under your Wi-Fi adapter
# Update lib/config/app_config.dart if different
```

### Check 3: Confidence Too High?
Lower the threshold to see more detections.

**Fix:** In `scan_screen.dart` line ~106:
```dart
final response = await _apiService.detectDisease(
  imageFile,
  confidenceThreshold: 0.3, // Changed from 0.4 to 0.3
  ...
);
```

---

## 🎯 Key Features Implemented

✅ **Real-time detection** every 2 seconds
✅ **RED bounding boxes** (as requested)
✅ **Confidence scores** on each box
✅ **Floating navigation bar** after detection
✅ **Debug logs** in both Flutter and Flask
✅ **Proper network configuration** for physical device

---

## 📱 Expected Behavior

1. **Camera opens** → Real-time detection starts automatically
2. **Every 2 seconds** → Frame captured and sent to backend
3. **When plant detected** → RED boxes appear with labels
4. **Floating bar appears** → "Plant Detected!" with Analytics button
5. **Tap Analytics** → Navigate to analytics screen

---

## 🐛 Common Issues

### "No logs in terminal"
- Backend not running → Start Flask server
- Network issue → Check IP address and Wi-Fi

### "Green box still showing"
- Old code running → Hot reload: Press `r` in Flutter terminal
- Or restart: Press `R` in Flutter terminal

### "Detection too slow"
- Normal for first detection (model loading)
- Should be fast after first detection (~500ms)

---

## 💡 Tips

- **Use laptop screen** as shown in your screenshot - works great for testing!
- **Good lighting** improves detection accuracy
- **Keep camera steady** for best results
- **Watch both terminals** to see full request/response cycle

---

Ready to test? Run the two commands above and point your camera at a plant! 🌱
