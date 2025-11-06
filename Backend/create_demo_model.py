"""
AgriScan AR - Quick TFLite Converter
=====================================

This script creates a DEMO TFLite model using pretrained YOLOv8
for immediate Flutter integration testing.

IMPORTANT: Replace this with your actual trained model later!

Usage:
1. Run this script to create demo model
2. Test Flutter integration
3. Train your real model in Colab
4. Replace the model file
"""

import os
from pathlib import Path
import shutil

print("=" * 70)
print("🚀 AgriScan AR - DEMO Model Creator")
print("=" * 70)

# Install dependencies if needed
try:
    from ultralytics import YOLO
    print("✅ Ultralytics YOLO installed")
except ImportError:
    print("Installing ultralytics...")
    os.system("pip install ultralytics")
    from ultralytics import YOLO

# Configuration
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "models"
OUTPUT_DIR.mkdir(exist_ok=True)

FLUTTER_ASSETS_DIR = BASE_DIR.parent / "ar_test_app" / "assets" / "models"
FLUTTER_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Disease classes (your 14 classes)
DISEASE_CLASSES = [
    "Tomato_Septoria",
    "Corn_Leaf_Blight",
    "Squash_Powdery_Leaf",
    "Apple_Healthy",
    "Tomato_Bacterial_Spot",
    "Tomato_Healthy",
    "Apple_Rust_Leaf",
    "Apple_Scab_Leaf",
    "Grape_Healthy",
    "Corn_Rust_Leaf",
    "Grape_Black_Rot",
    "Corn_Gray_Leaf_Spot",
    "BellPepper_Healthy",
    "BellPepper_Leaf_Spot"
]

print("\n📥 Step 1: Creating DEMO model from pretrained YOLOv8...")
print("   (This is just for testing - replace with your trained model later!)")

try:
    # Load pretrained YOLOv8n (nano - smallest/fastest)
    print("\n   Downloading YOLOv8 nano model...")
    model = YOLO('yolov8n.pt')  # This will auto-download
    print("   ✅ Model loaded")
    
    # Export to TFLite
    print("\n📤 Step 2: Exporting to TFLite...")
    print("   This may take a few minutes...")
    
    export_result = model.export(format='tflite', imgsz=640)
    print(f"   ✅ Export complete: {export_result}")
    
    # Find the TFLite file
    if isinstance(export_result, str) and os.path.exists(export_result):
        tflite_path = export_result
    else:
        # Search for it
        possible_locations = [
            Path(export_result),
            Path('yolov8n_saved_model') / 'yolov8n_float32.tflite',
            Path('yolov8n_saved_model') / 'yolov8n_float16.tflite',
        ]
        
        tflite_path = None
        for loc in possible_locations:
            if loc.exists():
                tflite_path = str(loc)
                break
            # Check parent directory
            parent = loc.parent
            if parent.exists():
                tflite_files = list(parent.glob('*.tflite'))
                if tflite_files:
                    tflite_path = str(tflite_files[0])
                    break
    
    if tflite_path and os.path.exists(tflite_path):
        # Copy to output directory
        final_model_path = OUTPUT_DIR / "plant_disease_model_DEMO.tflite"
        shutil.copy(tflite_path, final_model_path)
        
        model_size = os.path.getsize(final_model_path) / (1024 * 1024)
        print(f"\n✅ DEMO Model created!")
        print(f"   Size: {model_size:.2f} MB")
        print(f"   Location: {final_model_path}")
        
        # Copy to Flutter assets
        flutter_model_path = FLUTTER_ASSETS_DIR / "plant_disease_model.tflite"
        shutil.copy(final_model_path, flutter_model_path)
        print(f"   ✅ Copied to Flutter: {flutter_model_path}")
    else:
        print(f"\n⚠️ Could not find TFLite file at: {export_result}")
        print("   Checking directory...")
        if isinstance(export_result, str):
            parent_dir = Path(export_result).parent
            print(f"   Contents of {parent_dir}:")
            for item in parent_dir.iterdir():
                print(f"      - {item.name}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Create labels file
print("\n📝 Step 3: Creating labels.txt...")
labels_path = OUTPUT_DIR / "labels.txt"
with open(labels_path, 'w', encoding='utf-8') as f:
    for disease in DISEASE_CLASSES:
        f.write(f"{disease}\n")

flutter_labels_path = FLUTTER_ASSETS_DIR / "labels.txt"
shutil.copy(labels_path, flutter_labels_path)

print(f"✅ Labels created:")
print(f"   {labels_path}")
print(f"   {flutter_labels_path}")

print("\n" + "=" * 70)
print("✅ DEMO MODEL READY FOR FLUTTER TESTING!")
print("=" * 70)

print("\n⚠️  IMPORTANT - This is a DEMO model:")
print("   - Uses pretrained COCO weights (80 classes)")
print("   - NOT trained on your plant disease dataset")
print("   - Will detect general objects, not specific diseases")
print("   - ONLY for testing Flutter integration")

print("\n📋 TO GET YOUR REAL MODEL:")
print("   1. Open Google Colab")
print("   2. Run: Backend/DATASET/YOLOv8_large_object_detection.ipynb")
print("   3. After training, download 'best.pt' file")
print("   4. Place it in: Z:\\VESIRE_35\\Backend\\models\\best.pt")
print("   5. Run: convert_trained_model.py")

print("\n🚀 NEXT: Start building Flutter detection screen!")
print("=" * 70)
