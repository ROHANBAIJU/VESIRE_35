# ar_test_app

A new Flutter project.

## Getting Started

# AR Test App - 3D Cube Placement in Flutter

A simple Flutter AR application for learning the basics of Augmented Reality. Place 3D cubes on detected surfaces and view them from different angles as if they're really there!

## 🎯 Purpose

This is a **test/learning project** designed to help you understand:
- How to integrate AR into Flutter apps
- How ARKit (iOS) and ARCore (Android) work
- How to detect real-world surfaces
- How to place and anchor 3D objects in space
- How hit testing and world tracking function

## ✨ Features

- ✅ Real-time surface detection (floors, tables, walls)
- ✅ Tap-to-place 3D cubes
- ✅ Multiple object placement
- ✅ 6DOF tracking (move around objects naturally)
- ✅ Visual feedback and status indicators
- ✅ Clear all objects functionality
- ✅ Cross-platform (iOS & Android)

## 📋 Prerequisites

### Development Environment:
- Flutter SDK (3.0 or higher)
- Dart SDK
- Android Studio / Xcode
- Physical device for testing (AR requires real camera and sensors)

### Device Requirements:

**Android:**
- Android 7.0 (API 24) or higher
- ARCore-compatible device ([Check compatibility](https://developers.google.com/ar/devices))

**iOS:**
- iPhone 6S or newer
- iOS 11.0 or higher
- A9 chip or later

## 🚀 Quick Start

### 1. Clone/Navigate to Project
```bash
cd ar_test_app
```

### 2. Install Dependencies
```bash
flutter pub get
```

### 3. Connect Physical Device
- Enable Developer Mode (Android) or Trust Computer (iOS)
- Connect via USB

### 4. Run the App
```bash
flutter run
```

### 5. Grant Camera Permission
- When prompted, allow camera access

## 📖 How to Use

1. **Launch the app** - Camera view opens
2. **Scan environment** - Move your phone slowly to detect surfaces
3. **Wait for detection** - Yellow/white planes appear on flat surfaces
4. **Tap to place** - Tap on a detected surface to place a cube
5. **Walk around** - Move your phone to view the cube from different angles
6. **Place multiple cubes** - Tap multiple locations
7. **Clear all** - Tap the red button to remove all cubes

## 📁 Project Structure

```
ar_test_app/
├── android/                 # Android-specific files
│   └── app/
│       ├── build.gradle.kts  # ARCore configuration
│       └── src/main/
│           └── AndroidManifest.xml  # Permissions & AR metadata
├── ios/                     # iOS-specific files
│   └── Runner/
│       └── Info.plist       # Camera permission & ARKit declaration
├── lib/
│   └── main.dart           # Main application code
├── pubspec.yaml            # Dependencies (ar_flutter_plugin)
├── AR_LEARNING_GUIDE.md    # Detailed conceptual guide
└── README.md              # This file
```

## 🔧 Key Technologies

- **Flutter** - Cross-platform framework
- **ar_flutter_plugin** - AR bridge to native platforms
- **ARKit** - Apple's AR framework (iOS)
- **ARCore** - Google's AR platform (Android)
- **glTF/GLB** - 3D model format

## 📚 Learning Resources

For a **detailed step-by-step conceptual guide** (no code, just concepts), see:
👉 **[AR_LEARNING_GUIDE.md](./AR_LEARNING_GUIDE.md)**

This guide explains:
- How AR surface detection works
- The complete setup process
- Platform-specific configurations
- Anchoring and world tracking concepts
- Troubleshooting tips
- Next steps for advanced features

## 🛠️ Troubleshooting

### Planes not detecting?
- Move to a well-lit area
- Point at textured surfaces (avoid blank walls)
- Move phone slowly in different directions

### App crashes?
- Verify device supports ARCore/ARKit
- Check camera permissions are granted
- Ensure configurations in AndroidManifest.xml and Info.plist are correct

### Cube not appearing?
- Wait for surface detection (status indicator changes)
- Ensure internet connection (model loads from web)
- Tap on detected plane (yellow/white overlay)

### Build errors?
- Run `flutter clean`
- Run `flutter pub get`
- Verify minSdk is 24 in build.gradle.kts

## 🎓 What You'll Learn

By exploring this project, you'll understand:

1. **AR Basics:**
   - Surface/plane detection
   - World tracking
   - Hit testing
   - Object anchoring

2. **Flutter Integration:**
   - Using native AR plugins
   - Platform-specific configuration
   - Camera permission handling
   - State management in AR context

3. **3D Graphics:**
   - Coordinate systems
   - 3D transformations
   - Model loading (glTF)
   - Rendering in AR

## 🔜 Next Steps

Once comfortable with basics, try:
- Loading custom 3D models (create .glb files in Blender)
- Adding gesture controls (pinch to scale, rotate)
- Implementing object occlusion
- Using image tracking
- Adding physics interactions
- Experimenting with lighting estimation

## 📝 Notes

- This is a **learning/test project**, not production-ready
- AR requires a **physical device** - emulator won't work
- 3D model loads from internet (requires connection)
- Performance varies by device capabilities

## 🤝 Contributing

This is a personal learning project, but feel free to:
- Fork and experiment
- Report issues
- Suggest improvements
- Share your AR learning journey!

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed for learning AR development.

---

**Happy AR Learning! 🚀**

For detailed conceptual explanations, check [AR_LEARNING_GUIDE.md](./AR_LEARNING_GUIDE.md)
