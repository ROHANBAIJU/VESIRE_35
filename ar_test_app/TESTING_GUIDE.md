# Quick Testing Guide - Run on Your Phone

## 🚀 Steps to Test on Your Phone

### Option 1: Android Device (Recommended for Testing)

#### 1. Enable Developer Mode on Your Phone
1. Go to **Settings** → **About Phone**
2. Find **Build Number** (might be under "Software Information")
3. Tap **Build Number** 7 times
4. You'll see a message "You are now a developer!"

#### 2. Enable USB Debugging
1. Go to **Settings** → **Developer Options** (now visible)
2. Enable **USB Debugging**
3. Enable **Install via USB** (if available)

#### 3. Connect Phone to Computer
1. Connect your Android phone via USB cable
2. On your phone, you'll see a popup: **"Allow USB debugging?"**
3. Check **"Always allow from this computer"**
4. Tap **Allow**

#### 4. Verify Device is Connected
Open PowerShell in the project directory and run:
```powershell
cd z:\VESIRE_35\ar_test_app
flutter devices
```

You should see your device listed (like "Samsung SM-G991B" or similar)

#### 5. Check if Your Phone Supports ARCore
Before testing, verify your device supports ARCore:
- Visit: https://developers.google.com/ar/devices
- Search for your phone model
- If listed, you're good to go!

**Popular ARCore Devices:**
- Samsung Galaxy S8 and newer
- Google Pixel phones
- OnePlus 5 and newer
- Xiaomi Mi 8 and newer
- Most phones from 2018 onwards

#### 6. Run the App
```powershell
cd z:\VESIRE_35\ar_test_app
flutter run
```

**Expected output:**
```
Multiple devices found:
Windows (desktop) • windows • windows-x64 • Microsoft Windows...
SM G991B (mobile)  • RZ8N1... • android-arm64 • Android 13 (API 33)

[1]: Windows (windows)
[2]: SM G991B (RZ8N1...)
Please choose one (or "q" to quit): 
```

Type **2** (or the number for your phone) and press Enter.

#### 7. First Run - Grant Permissions
When the app starts on your phone:
1. You'll see: **"ar_test_app needs camera permission"**
2. Tap **Allow** or **While using the app**
3. You might also see **"Install ARCore?"** - Tap **Yes/Install**

#### 8. Testing AR Features
1. **Point camera at floor/table** - Move phone slowly
2. **Watch for yellow/white plane overlays** - These indicate detected surfaces
3. **Wait for "Surface detected!"** message at the top
4. **Tap on the plane** - A cube should appear
5. **Walk around** - The cube stays in place as you move
6. **Tap multiple times** - Place more cubes
7. **Red button** - Clears all cubes

---

### Option 2: iOS Device (iPhone)

#### 1. Prerequisites
- Mac with Xcode installed
- Apple Developer account (free tier works)
- iPhone 6S or newer

#### 2. Setup on Mac
1. Open project in Xcode:
   ```bash
   cd z:\VESIRE_35\ar_test_app
   open ios/Runner.xcworkspace
   ```

2. In Xcode:
   - Select your iPhone from device dropdown
   - Go to **Signing & Capabilities**
   - Select your Team (Apple ID)
   - Change Bundle Identifier if needed

3. Connect iPhone via USB
4. Trust computer on iPhone when prompted

5. Run from terminal:
   ```bash
   flutter run
   ```

---

## 📱 What to Expect - Visual Guide

### 1. App Launch
```
┌─────────────────────────┐
│   AR Cube Placement     │ ← App Bar
├─────────────────────────┤
│                         │
│    📷 Camera View       │
│                         │
│  ┌─────────────────┐   │
│  │ 🔍 Move phone   │   │ ← Status Message
│  │ to detect...    │   │
│  └─────────────────┘   │
│                         │
└─────────────────────────┘
```

### 2. Surface Detected
```
┌─────────────────────────┐
│   AR Cube Placement     │
├─────────────────────────┤
│  ┌─────────────────┐   │
│  │ ✅ Surface      │   │
│  │ detected! Tap   │   │
│  │ Cubes: 0        │   │
│  └─────────────────┘   │
│                         │
│  ═══════════════════    │ ← Yellow plane on floor
│  ═══════════════════    │
│                         │
└─────────────────────────┘
```

### 3. Cube Placed
```
┌─────────────────────────┐
│   AR Cube Placement     │
├─────────────────────────┤
│  ┌─────────────────┐   │
│  │ ✅ Surface      │   │
│  │ detected! Tap   │   │
│  │ Cubes: 1        │   │ ← Counter updated
│  └─────────────────┘   │
│                         │
│       [CUBE]            │ ← 3D Cube on surface
│  ═══════════════════    │
│  ═══════════════════    │
│                    🗑️   │ ← Clear button appears
└─────────────────────────┘
```

---

## 🐛 Troubleshooting

### Problem: Device not showing in `flutter devices`

**Solution:**
1. Unplug and replug USB cable
2. Try a different USB port
3. On phone: Disable and re-enable USB debugging
4. Try different USB cable (some are charge-only)
5. Install device drivers (Windows): Check manufacturer website

**Check connection:**
```powershell
adb devices
```
Should show your device. If it shows "unauthorized", check phone for permission popup.

---

### Problem: "App Installation Failed"

**Solution:**
1. Check storage space on phone
2. Try: `flutter clean` then `flutter run` again
3. Uninstall old version of app from phone
4. Check Android version (needs 7.0+)

---

### Problem: "ARCore not installed"

**Solution:**
1. Phone will prompt to install ARCore
2. Tap Install and wait
3. Restart app after installation
4. If fails, install manually from Play Store: "Google Play Services for AR"

---

### Problem: Camera permission denied

**Solution:**
1. Go to phone Settings → Apps → ar_test_app → Permissions
2. Enable Camera permission
3. Restart app

---

### Problem: Planes not detecting

**Possible causes:**
- ❌ Too dark → Move to well-lit area
- ❌ Plain white surface → Point at textured surface (patterned floor, table with objects)
- ❌ Moving too fast → Move phone slowly and steadily
- ❌ Pointing at wall → Try pointing at floor first

**Best surfaces for detection:**
- ✅ Wood floors with visible grain
- ✅ Carpet with patterns
- ✅ Tables with items on them
- ✅ Tiled floors

---

### Problem: Build errors

**If you see compilation errors:**

```powershell
cd z:\VESIRE_35\ar_test_app
flutter clean
flutter pub get
flutter run
```

**If still failing:**
1. Check `minSdk` in `android/app/build.gradle.kts` is 24
2. Verify AndroidManifest.xml has all AR permissions
3. Make sure you ran `flutter pub get` after editing pubspec.yaml

---

## 📊 Performance Notes

### Expected Behavior:
- **Plane detection**: 2-10 seconds (depends on environment)
- **Cube placement**: Instant
- **Frame rate**: 30-60 FPS (depends on device)
- **Multiple cubes**: 5-10 cubes should work smoothly

### If App is Laggy:
- Phone might be older (pre-2018)
- Too many cubes placed (clear and start fresh)
- Other apps running in background (close them)

---

## 🎯 Testing Checklist

Use this to verify everything works:

- [ ] App installs without errors
- [ ] Camera permission granted
- [ ] Camera view appears (not black screen)
- [ ] Status message shows "Move phone to detect..."
- [ ] After moving phone, planes appear (yellow/white overlays)
- [ ] Status changes to "Surface detected!"
- [ ] Tapping plane places a cube
- [ ] Cube counter increases
- [ ] Snackbar shows "Cube #1 placed!"
- [ ] Can place multiple cubes
- [ ] Walking around: cubes stay in position
- [ ] Clear button appears when cubes exist
- [ ] Tapping clear button removes all cubes
- [ ] Can place cubes again after clearing

---

## 📱 Quick Commands Reference

```powershell
# Navigate to project
cd z:\VESIRE_35\ar_test_app

# Check connected devices
flutter devices

# Install dependencies
flutter pub get

# Clean build
flutter clean

# Run app (select device when prompted)
flutter run

# Run on specific device
flutter run -d <device-id>

# Check for issues
flutter doctor

# Hot reload (while app running)
# Just press 'r' in terminal or save file in IDE

# Hot restart (full restart)
# Press 'R' in terminal

# Quit app
# Press 'q' in terminal
```

---

## 🎉 Success!

If you see the cube and can walk around it, **congratulations!** You've successfully:
- ✅ Set up Flutter AR development
- ✅ Configured ARCore/ARKit
- ✅ Implemented surface detection
- ✅ Placed 3D objects in real world
- ✅ Tested AR tracking

Now you can experiment with:
- Different 3D models (change the URI in main.dart)
- Different scales (modify the scale parameter)
- Different positions (tap in various locations)
- Walking around to see 3D perspective

---

## 📞 Need Help?

If you encounter issues not covered here:

1. **Check logs:**
   ```powershell
   flutter run --verbose
   ```
   Look for error messages in red

2. **Common error patterns:**
   - "Camera not available" → Permission issue
   - "ARCore not supported" → Device compatibility
   - "Network error" → Internet needed for 3D model

3. **Device info:**
   - Check what's needed: https://developers.google.com/ar/devices

---

**Good luck with your AR testing! 🚀📱**
