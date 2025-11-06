# Quick Integration Guide: AR Detection

## Step 1: Add Navigation to AR Detection Screen

Add this button to your main scan screen or home screen:

```dart
import 'package:vesire/screens/ar_detection_screen.dart';

// In your build method, add this button:
ElevatedButton.icon(
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const ARDetectionScreen(),
      ),
    );
  },
  icon: const Icon(Icons.camera_alt),
  label: const Text('AR Detection'),
  style: ElevatedButton.styleFrom(
    backgroundColor: Colors.green,
    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
  ),
)
```

## Step 2: Configure Backend URL

1. Start your Flask backend server
2. Find your computer's IP address:
   ```bash
   # Mac/Linux
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```

3. Edit `lib/config/ar_config.dart`:
   ```dart
   static const String backendUrl = 'http://YOUR_IP:5000/api';
   // Example: 'http://192.168.1.100:5000/api'
   ```

## Step 3: Test Backend Connection

Add this test to verify connectivity:

```dart
import 'package:vesire/services/detection_service.dart';

// Run this once to test
Future<void> testBackend() async {
  final service = DetectionService();
  final isHealthy = await service.checkBackendHealth();
  
  if (isHealthy) {
    print('✅ Backend connected successfully!');
  } else {
    print('❌ Backend connection failed. Check URL and network.');
  }
}
```

## Step 4: Required Flask Endpoints

Your Flask backend must implement:

### POST /api/detect
```python
@app.route('/api/detect', methods=['POST'])
def detect():
    image = request.files['image']
    confidence_threshold = float(request.form.get('confidence_threshold', 0.5))
    
    # Run YOLO detection
    results = model(image)
    
    detections = []
    for result in results:
        for box in result.boxes:
            detections.append({
                'bbox': box.xywh[0].tolist(),  # [x, y, width, height]
                'disease': model.names[int(box.cls)],
                'confidence': float(box.conf),
                'severity': 'high'  # Optional
            })
    
    return jsonify({
        'success': True,
        'detections': detections,
        'count': len(detections)
    })
```

### GET /api/health
```python
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})
```

## Step 5: Camera Permissions (If Not Already Added)

**Android**: `android/app/src/main/AndroidManifest.xml`
```xml
<uses-permission android:name="android.permission.CAMERA"/>
```

**iOS**: `ios/Runner/Info.plist`
```xml
<key>NSCameraUsageDescription</key>
<string>Camera is required for disease detection</string>
```

## Step 6: Run the App

```bash
cd Frontend/vesire
flutter run
```

## Quick Test Checklist

- [ ] Backend server running (Flask)
- [ ] Backend URL configured in `ar_config.dart`
- [ ] Device/emulator on same network as computer
- [ ] Camera permissions granted
- [ ] Navigation button added to existing screen
- [ ] Test backend health check endpoint
- [ ] Test single detection
- [ ] Test continuous mode
- [ ] Verify bounding boxes align correctly

## Troubleshooting

### Connection Issues
```dart
// Try different URLs based on your setup:
// Android Emulator: 'http://10.0.2.2:5000/api'
// Physical Device: 'http://YOUR_COMPUTER_IP:5000/api'
```

### Coordinate Issues
If bounding boxes don't align properly, check:
1. YOLO output format (normalized 0-1 or pixel coordinates)
2. Backend response format matches `BoundingBox.fromJson()`
3. Image size sent to backend (should be 640x640)

## Example Integration

Here's how to add AR detection to your existing scan screen:

```dart
// In your scan results screen
if (scanResult != null) {
  Column(
    children: [
      Text('Disease: ${scanResult.disease}'),
      SizedBox(height: 16),
      ElevatedButton(
        onPressed: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => const ARDetectionScreen(),
            ),
          );
        },
        child: const Text('Try AR Detection'),
      ),
    ],
  )
}
```

## Next Steps

1. Test with your Flask backend
2. Adjust detection settings in `ar_config.dart`
3. Customize colors/animations in `ar_overlay_painter.dart`
4. Add navigation from your existing screens
5. Deploy backend for production use

For full documentation, see `AR_DETECTION_README.md`
