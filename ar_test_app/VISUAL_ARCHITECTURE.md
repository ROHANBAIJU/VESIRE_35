# Camera Overlay Architecture - Visual Reference

## Widget Tree Structure

```
MaterialApp
│
└─ CameraOverlayTest (StatefulWidget)
    │
    └─ Scaffold
        │
        ├─ AppBar
        │   └─ "Camera Overlay Test"
        │
        └─ Body: Stack (StackFit.expand)
            │
            ├─ Layer 1: CameraPreview
            │   └─ [Full-screen live camera feed]
            │
            └─ Layer 2: Overlay UI Stack
                │
                ├─ Positioned (dynamic position)
                │   ├─ left: (_xPosition * screenWidth) - 75
                │   ├─ top: (_yPosition * screenHeight) - 75
                │   │
                │   └─ Container (Mock Detection Box)
                │       ├─ width: 150
                │       ├─ height: 150
                │       ├─ border: red, 3px
                │       ├─ color: red.withOpacity(0.2)
                │       │
                │       └─ Text: "TEST BOX"
                │
                └─ Positioned (bottom controls)
                    ├─ left: 0
                    ├─ right: 0
                    ├─ bottom: 0
                    │
                    └─ Container (Control Panel)
                        ├─ backgroundColor: black87
                        │
                        └─ Column
                            ├─ Text: "Move the box with sliders:"
                            ├─ X Slider (horizontal control)
                            │   ├─ value: _xPosition (0.0 to 1.0)
                            │   ├─ color: red
                            │   └─ onChanged: updates _xPosition
                            │
                            ├─ Y Slider (vertical control)
                            │   ├─ value: _yPosition (0.0 to 1.0)
                            │   ├─ color: blue
                            │   └─ onChanged: updates _yPosition
                            │
                            └─ Text: "Position: X%, Y%"
```

---

## State Flow Diagram

```
User Action: Move X Slider
       │
       ↓
Slider.onChanged(newValue)
       │
       ↓
setState(() { _xPosition = newValue; })
       │
       ↓
Widget rebuild triggered
       │
       ↓
_buildOverlayUI() called
       │
       ↓
Calculate new position:
  screenWidth = MediaQuery.of(context).size.width
  leftPosition = (_xPosition × screenWidth) - 75
       │
       ↓
Positioned widget updated
       │
       ↓
Mock box moves to new position
       │
       ↓
UI rendered at 60 FPS
```

---

## Position Calculation Visual

### Screen Coordinates System
```
        0px (left edge)
        │
        ↓
    ┌───────────────────────┐ ← 0px (top edge)
    │                       │
    │   Screen Area         │
    │   (e.g., 400×800)     │
    │                       │
    │         ●             │ ← Slider position (center of box)
    │      ┌─────┐          │
    │      │TEST │          │
    │      │ BOX │          │
    │      └─────┘          │
    │                       │
    └───────────────────────┘ ← 800px (bottom edge)
                            │
                            ↓
                        400px (right edge)
```

### Positioning Formula Breakdown
```
Given:
- screenWidth = 400px
- screenHeight = 800px
- boxWidth = 150px
- boxHeight = 150px
- _xPosition = 0.75 (slider value)
- _yPosition = 0.25 (slider value)

Step 1: Calculate center point (where sliders point to)
  centerX = _xPosition × screenWidth = 0.75 × 400 = 300px
  centerY = _yPosition × screenHeight = 0.25 × 800 = 200px

Step 2: Calculate top-left corner (where Positioned places widget)
  leftPosition = centerX - (boxWidth / 2) = 300 - 75 = 225px
  topPosition = centerY - (boxHeight / 2) = 200 - 75 = 125px

Result:
    ┌───────────────────────┐
    │                       │
    │            ● (300,200)│ ← Center point from slider
 125│      ┌─────┐          │
    │      │TEST │          │
    │  225 │ BOX │          │
    │  →   └─────┘          │
    │                       │
    └───────────────────────┘
```

---

## Slider Value Mapping

### X-Axis (Horizontal)
```
Slider: 0.0    0.25    0.5    0.75    1.0
        │       │       │       │       │
Screen: ├───────┼───────┼───────┼───────┤
        0px   100px   200px   300px   400px
        
        LEFT            CENTER         RIGHT
```

### Y-Axis (Vertical)
```
Slider: 0.0
        │
Screen: ├─────  0px   (TOP)
        │
      0.25
        │
        ├───── 200px
        │
      0.5
        │
        ├───── 400px  (CENTER)
        │
      0.75
        │
        ├───── 600px
        │
      1.0
        │
        └───── 800px  (BOTTOM)
```

---

## Camera Initialization Flow

```
App Start
   │
   ↓
initState() called
   │
   ↓
_initializeCamera()
   │
   ├─→ availableCameras()
   │   └─→ Get device camera list
   │
   ├─→ Create CameraController
   │   ├─ camera: cameras[0] (back camera)
   │   ├─ preset: ResolutionPreset.medium
   │   └─ audio: false
   │
   ├─→ controller.initialize()
   │   └─→ Wait for async completion
   │
   └─→ setState(() { _isCameraInitialized = true; })
       │
       ↓
   Widget rebuilds
       │
       ├─→ Show CircularProgressIndicator (if not ready)
       └─→ Show CameraPreview + Overlay (if ready)
```

---

## Real-time Update Cycle

```
┌─────────────────────────────────────────┐
│  60 FPS Flutter Rendering Loop          │
├─────────────────────────────────────────┤
│                                         │
│  Camera Frame → CameraPreview Widget    │
│       ↓                                 │
│  Stack layers composited                │
│       ↓                                 │
│  Positioned box at current position     │
│       ↓                                 │
│  Rendered to screen                     │
│       ↓                                 │
│  [User moves slider]                    │
│       ↓                                 │
│  setState() triggers rebuild            │
│       ↓                                 │
│  New position calculated                │
│       ↓                                 │
│  Box moves smoothly                     │
│       ↓                                 │
│  Back to top of loop                    │
│                                         │
└─────────────────────────────────────────┘
```

---

## AI Model Integration (Future)

### Current Architecture:
```
User Input (Sliders)
       │
       ↓
State Variables (_xPosition, _yPosition)
       │
       ↓
Position Calculation
       │
       ↓
Single Positioned Widget
       │
       ↓
Mock Box
```

### Future Architecture:
```
Camera Frame
       │
       ↓
AI Model Inference (YOLO)
       │
       ↓
Detection List [
  { x: 0.3, y: 0.4, label: "disease1", conf: 0.95 },
  { x: 0.7, y: 0.2, label: "disease2", conf: 0.87 },
  ...
]
       │
       ↓
Loop: detections.map((detection) => ...)
       │
       ↓
Multiple Positioned Widgets
       │
       ↓
Detection Boxes with Labels
```

### Same Formula, Different Source:
```
BEFORE (Test):
  x = _xPosition (from slider)
  
AFTER (AI):
  x = detection.x (from model)

Both use: leftPosition = x × screenWidth - (boxWidth / 2)
```

---

## Performance Considerations

### Why This Architecture is Efficient:

1. **Camera runs independently**
   - Native camera preview (hardware accelerated)
   - No frame-by-frame processing in test mode
   
2. **UI updates are lightweight**
   - Only Positioned widget rebuilds
   - Camera preview doesn't rebuild
   - Stack composition is fast

3. **Slider interaction is smooth**
   - setState only updates position values
   - Flutter's rendering engine optimizes redraws
   - 60 FPS maintained

### When Adding AI:

```
Good Practice:
- Run inference on background isolate
- Debounce detection updates (e.g., 10 FPS)
- Only rebuild when new detections arrive
- Limit number of simultaneous boxes

Avoid:
- Processing every camera frame (30-60 FPS)
- Rebuilding entire widget tree
- Synchronous heavy computations
- Blocking the UI thread
```

---

## Coordinate System Comparison

### Flutter Screen Coordinates:
```
(0,0) ──────────→ X
  │
  │
  │
  ↓
  Y

Origin: Top-left corner
X increases: Left to right
Y increases: Top to bottom
```

### AI Model Coordinates (Typical):
```
Same as Flutter!

Normalized: 0.0 to 1.0
- (0.0, 0.0) = top-left
- (0.5, 0.5) = center
- (1.0, 1.0) = bottom-right

Perfect match! Just multiply by screen size.
```

---

## Summary: The Magic of This Approach

### Why It Works:
✅ **Simple**: No 3D math, no complex transformations  
✅ **Fast**: Direct pixel positioning  
✅ **Flexible**: Easy to add/remove boxes  
✅ **Responsive**: Adapts to any screen size  
✅ **Testable**: UI works without AI model  
✅ **Future-proof**: Same code for AI integration  

### Key Insight:
> Slider values (0.0-1.0) simulate AI model output format  
> Position calculation is identical for both  
> **UI logic is proven before AI training begins!** 🎯

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│  CAMERA OVERLAY FORMULA CARD            │
├─────────────────────────────────────────┤
│                                         │
│  Given:                                 │
│  • relativeX, relativeY (0.0 to 1.0)    │
│  • boxWidth, boxHeight (pixels)         │
│                                         │
│  Calculate:                             │
│  1. screenWidth = MediaQuery.size.width │
│  2. screenHeight = MediaQuery.size.height│
│                                         │
│  3. left = relativeX × screenWidth      │
│           - (boxWidth / 2)              │
│                                         │
│  4. top = relativeY × screenHeight      │
│          - (boxHeight / 2)              │
│                                         │
│  Use:                                   │
│  Positioned(                            │
│    left: left,                          │
│    top: top,                            │
│    child: YourWidget()                  │
│  )                                      │
│                                         │
└─────────────────────────────────────────┘
```
