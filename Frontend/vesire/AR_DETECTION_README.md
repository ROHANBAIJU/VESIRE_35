# AR-Style Disease Detection Feature

## Overview
Real-time plant disease detection with AR-style bounding box overlay on live camera feed. This feature integrates your Flask YOLO backend with the Flutter frontend to provide visual feedback during scanning.

## Features
- ✅ Live camera preview with real-time overlay
- ✅ AR-style bounding boxes with animations
- ✅ Color-coded disease severity (Red/Orange/Yellow/Green)
- ✅ Confidence percentage display
- ✅ Continuous detection mode
- ✅ Animated scanning effects
- ✅ Camera switching (front/back)
- ✅ Optimized image compression (640x640, JPEG 85%)

## Architecture

### Files Created
```
lib/
├── config/
│   └── ar_config.dart          # Backend URL and detection settings
├── models/
│   └── bounding_box.dart       # BoundingBox and DetectionResult models
├── services/
│   ├── camera_service.dart     # Camera management and frame capture
│   └── detection_service.dart  # Flask backend communication
├── widgets/
│   └── ar_overlay_painter.dart # CustomPainter for overlay rendering
└── screens/
    └── ar_detection_screen.dart # Main AR detection UI
```

### Data Flow
1. **Camera Capture**: CameraService captures frame from live preview
2. **Compression**: Image resized to 640x640, JPEG quality 85%
3. **Backend Request**: DetectionService sends multipart HTTP POST
4. **Response Parsing**: BoundingBox.fromJson() parses detection results
5. **Coordinate Scaling**: Model space (640x640) → Screen space (preview size)
6. **Overlay Rendering**: AROverlayPainter draws boxes with animations

## Setup Instructions

### 1. Backend Configuration

Edit `lib/config/ar_config.dart` and update the backend URL:

```dart
static const String backendUrl = 'http://YOUR_IP:5000/api';
```

**Finding Your IP Address:**
- **Windows**: `ipconfig` in Command Prompt
- **Mac/Linux**: `ifconfig` or `ip addr` in Terminal
- **Look for**: IPv4 address (e.g., 192.168.1.100)

**Testing Scenarios:**
- **Android Emulator**: `http://10.0.2.2:5000/api` (default)
- **iOS Simulator**: `http://localhost:5000/api`
- **Physical Device**: `http://YOUR_IP:5000/api` (must be same network)

### 2. Flask Backend Requirements

Your Flask backend should expose these endpoints:

#### POST /api/detect
Accepts multipart form data with `image` file.

**Request:**
```
POST /api/detect
Content-Type: multipart/form-data

Fields:
- image: File (JPEG/PNG)
- confidence_threshold: float (optional, default: 0.5)
- return_image: bool (optional, default: false)
```

**Response:**
```json
{
  "success": true,
  "detections": [
    {
      "bbox": [x, y, width, height],  // or {"x": 0, "y": 0, "width": 100, "height": 100}
      "disease": "Early Blight",
      "confidence": 0.95,
      "severity": "high"  // optional: "low", "medium", "high"
    }
  ],
  "count": 1
}
```

#### GET /api/health
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

#### GET /api/classes
Get available disease classes.

**Response:**
```json
{
  "classes": ["Early Blight", "Late Blight", "Healthy", ...]
}
```

### 3. Add Navigation Route

In your app's navigation (e.g., `main.dart` or home screen):

```dart
import 'package:vesire/screens/ar_detection_screen.dart';

// Navigate to AR detection
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => const ARDetectionScreen(),
  ),
);
```

### 4. Camera Permissions

Ensure camera permissions are declared:

**Android** (`android/app/src/main/AndroidManifest.xml`):
```xml
<uses-permission android:name="android.permission.CAMERA"/>
<uses-feature android:name="android.hardware.camera" android:required="false"/>
```

**iOS** (`ios/Runner/Info.plist`):
```xml
<key>NSCameraUsageDescription</key>
<string>Camera access is required for plant disease detection</string>
```

## Usage

### Single Detection Mode (Default)
1. Open AR Detection screen
2. Point camera at plant leaf
3. Tap **SCAN** button
4. Wait for detection results (~2-3 seconds)
5. Bounding boxes appear with disease labels

### Continuous Detection Mode
1. Tap **Play** icon in app bar
2. App automatically scans every 3 seconds
3. Bounding boxes update in real-time
4. Tap **Pause** to stop continuous mode

### Camera Controls
- **Camera Icon**: Switch between front and back camera
- **Clear Button**: Remove all detection overlays
- **Info Button**: View help and color legend

## Visual Features

### Color Coding
Detection boxes are color-coded by severity:
- 🔴 **Red**: High severity (serious disease)
- 🟠 **Orange**: Medium severity
- 🟡 **Yellow**: Low severity
- 🟢 **Green**: Healthy or high confidence

### Animations
- **Pulsing Glow**: Animated glow effect around boxes
- **Scanning Line**: Vertical line sweeps down during detection
- **Corner Markers**: AR-style corner brackets
- **Fade-in**: Smooth appearance of detection results

## Performance Optimization

### Image Compression
- **Max Size**: 640x640 pixels (matches YOLO input)
- **Quality**: 85% JPEG compression
- **Format**: Optimized for fast upload

### Request Throttling
- **Processing Flag**: Prevents concurrent requests
- **Continuous Mode**: 3-second intervals between scans
- **Timeout**: 10-second backend response timeout

### Coordinate Transformation
Detections are scaled from model space to screen space:
```dart
final scaleX = screenWidth / 640;
final scaleY = screenHeight / 640;
final scaledBox = box.scale(scaleX: scaleX, scaleY: scaleY);
```

## Customization

### Detection Settings

Edit `lib/config/ar_config.dart`:

```dart
class ARConfig {
  static const double confidenceThreshold = 0.5;     // Min confidence (0.0-1.0)
  static const int detectionTimeout = 10;            // Backend timeout (seconds)
  static const int continuousModeInterval = 3;       // Scan interval (seconds)
  static const int maxImageSize = 640;               // Image compression size
  static const int imageQuality = 85;                // JPEG quality (0-100)
  static const bool showConfidenceLabels = true;     // Show % confidence
  static const bool showCornerMarkers = true;        // Show AR corners
}
```

### Visual Customization

Edit `lib/widgets/ar_overlay_painter.dart`:

```dart
// Change corner length
final cornerLength = 20.0;

// Change stroke widths
final cornerWidth = 4.0;
final boxStrokeWidth = 3.0;

// Customize label style
TextStyle(
  color: Colors.white,
  fontSize: 14,
  fontWeight: FontWeight.bold,
)
```

## Troubleshooting

### No Detections Appearing
- ✅ Check backend URL in `ar_config.dart`
- ✅ Test backend health: `curl http://YOUR_IP:5000/api/health`
- ✅ Ensure device and computer on same network
- ✅ Check Flutter console for error messages

### Camera Issues
- ✅ Verify camera permissions granted
- ✅ Check device has available cameras
- ✅ Try switching cameras (front/back)
- ✅ Restart app if camera initialization fails

### Backend Connection Errors
- ✅ Verify Flask server is running
- ✅ Check firewall allows port 5000
- ✅ Use computer IP, not `localhost` for physical devices
- ✅ Test with Postman/curl before testing in app

### Coordinate Misalignment
- ✅ Ensure YOLO model outputs normalized coordinates (0-1) or pixel coordinates
- ✅ Check `BoundingBox.fromJson()` parses your backend format correctly
- ✅ Verify coordinate transformation in `_performDetection()`

### Performance Issues
- ✅ Reduce image quality in `ar_config.dart`
- ✅ Increase `continuousModeInterval` to 5+ seconds
- ✅ Use lower ResolutionPreset in CameraService
- ✅ Optimize backend model (TensorRT, ONNX, quantization)

## Testing

### 1. Test Backend Connection
```dart
final service = DetectionService();
final isHealthy = await service.checkBackendHealth();
print('Backend healthy: $isHealthy');
```

### 2. Test Detection
```dart
final service = DetectionService();
final imageFile = File('path/to/test/image.jpg');
final result = await service.detectDisease(imageFile);
print('Detections: ${result?.detections.length}');
```

### 3. Test Coordinate Scaling
```dart
final box = BoundingBox(x: 100, y: 100, width: 200, height: 200, ...);
final scaled = box.scale(scaleX: 2.0, scaleY: 1.5);
// Verify: scaled.x == 200, scaled.width == 400, etc.
```

## Integration with Existing Features

### Navigate from Scan Screen
Add a button in your existing scan screen:

```dart
ElevatedButton(
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const ARDetectionScreen(),
      ),
    );
  },
  child: const Text('AR Detection Mode'),
)
```

### Use Detection Results Elsewhere
Export detection results for TTS or history:

```dart
void _onDetectionComplete(DetectionResult result) {
  for (final detection in result.detections) {
    print('Found: ${detection.disease} (${detection.confidence})');
    
    // Trigger TTS
    if (ttsEnabled) {
      ttsService.speak('Detected ${detection.disease}');
    }
    
    // Save to history
    historyService.addDetection(detection);
  }
}
```

## Next Steps

1. **Deploy Flask Backend**: Use Render, Railway, or AWS for production URL
2. **Update Config**: Change `backendUrl` to production endpoint
3. **Add Caching**: Cache recent detections for offline mode
4. **Improve UX**: Add haptic feedback, sound effects, tutorials
5. **Analytics**: Track detection accuracy and usage metrics

## Support

For issues related to:
- **Backend**: Check Flask logs and API responses
- **Camera**: Verify permissions and device capabilities
- **Coordinates**: Add debug prints in `_performDetection()`
- **Performance**: Profile with Flutter DevTools

## License
Part of VESIRE - Plant Disease Detection App
