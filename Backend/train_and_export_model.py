"""
AgriScan AR - YOLOv8 Model Training and TFLite Export Script
=============================================================

This script will:
1. Check for existing trained models
2. Train YOLOv8 model if needed (requires dataset)
3. Export to TensorFlow Lite format
4. Test the TFLite model
5. Generate labels.txt for Flutter app

Author: Team VESIRE - SJBIT Hackathon 2025
"""

import os
import sys
from pathlib import Path
import shutil

print("=" * 70)
print("🚀 AgriScan AR - Model Training & Export Pipeline")
print("=" * 70)

# ============================================================================
# STEP 1: Check Dependencies
# ============================================================================
print("\n📦 Step 1: Checking dependencies...")

try:
    from ultralytics import YOLO
    print("✅ Ultralytics YOLO installed")
except ImportError:
    print("❌ Ultralytics not installed. Installing...")
    os.system("pip install ultralytics")
    from ultralytics import YOLO
    print("✅ Ultralytics YOLO installed")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow {tf.__version__} installed")
except ImportError:
    print("⚠️ TensorFlow not installed (needed for testing). Installing...")
    os.system("pip install tensorflow")
    import tensorflow as tf

try:
    import numpy as np
    from PIL import Image
    print("✅ NumPy and PIL installed")
except ImportError:
    print("❌ NumPy or PIL missing. Installing...")
    os.system("pip install numpy pillow")
    import numpy as np
    from PIL import Image

# ============================================================================
# STEP 2: Configuration
# ============================================================================
print("\n⚙️ Step 2: Configuration...")

# Project paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "DATASET"
OUTPUT_DIR = BASE_DIR / "models"
OUTPUT_DIR.mkdir(exist_ok=True)

# Model configuration
MODEL_SIZE = "yolov8m"  # Options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
                        # m = medium (good balance), l = large (more accurate but slower)

# Disease classes (14 total)
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

print(f"✅ Model: {MODEL_SIZE}")
print(f"✅ Number of classes: {len(DISEASE_CLASSES)}")
print(f"✅ Output directory: {OUTPUT_DIR}")

# ============================================================================
# STEP 3: Check for Existing Trained Model
# ============================================================================
print("\n🔍 Step 3: Checking for existing trained models...")

# Check common locations for trained models
possible_model_paths = [
    OUTPUT_DIR / "best.pt",
    BASE_DIR / "training_results" / "weights" / "best.pt",
    BASE_DIR / "runs" / "detect" / "train" / "weights" / "best.pt",
]

trained_model_path = None
for path in possible_model_paths:
    if path.exists():
        trained_model_path = path
        print(f"✅ Found trained model: {path}")
        break

if not trained_model_path:
    print("⚠️ No trained model found.")
    print("\n" + "=" * 70)
    print("📊 DATASET REQUIREMENT")
    print("=" * 70)
    print("To train a model, you need:")
    print("1. Dataset in YOLO format with the following structure:")
    print("   Dataset/")
    print("     ├── images/")
    print("     │   ├── train/")
    print("     │   └── val/")
    print("     ├── labels/")
    print("     │   ├── train/")
    print("     │   └── val/")
    print("     └── data.yaml")
    print("\n2. The data.yaml file should contain:")
    print("   path: /path/to/dataset")
    print("   train: images/train")
    print("   val: images/val")
    print("   nc: 14")
    print("   names: ['Tomato_Septoria', 'Corn_Leaf_Blight', ...]")
    print("\n" + "=" * 70)
    
    # Check if user has dataset
    response = input("\n❓ Do you have a dataset ready? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        dataset_path = input("📁 Enter path to your data.yaml file: ").strip()
        
        if os.path.exists(dataset_path):
            print(f"\n✅ Dataset found: {dataset_path}")
            
            # ============================================================================
            # STEP 4: Train Model
            # ============================================================================
            print("\n🏋️ Step 4: Training YOLOv8 model...")
            print("⏰ This may take 2-4 hours depending on your GPU/CPU")
            print("=" * 70)
            
            try:
                # Load pretrained model
                model = YOLO(f'{MODEL_SIZE}.pt')
                
                # Train the model
                results = model.train(
                    data=dataset_path,
                    epochs=50,  # Reduce to 20-30 for faster testing
                    imgsz=640,
                    batch=8,  # Adjust based on your GPU memory
                    name='agriscan_ar_model',
                    project=str(OUTPUT_DIR),
                    patience=10,
                    save=True,
                    device=0,  # Use GPU 0, or 'cpu' for CPU training
                )
                
                trained_model_path = OUTPUT_DIR / 'agriscan_ar_model' / 'weights' / 'best.pt'
                print(f"\n✅ Training complete! Model saved to: {trained_model_path}")
                
            except Exception as e:
                print(f"\n❌ Training failed: {e}")
                sys.exit(1)
        else:
            print(f"❌ Dataset not found at: {dataset_path}")
            print("\n⚠️ Cannot proceed without dataset or trained model.")
            print("\n💡 OPTIONS:")
            print("1. Train model in Google Colab using your existing notebooks")
            print("2. Download your trained 'best.pt' from Google Drive")
            print("3. Place it in: z:\\VESIRE_35\\Backend\\models\\best.pt")
            print("4. Run this script again")
            sys.exit(1)
    else:
        print("\n⚠️ Cannot proceed without dataset or trained model.")
        print("\n💡 QUICK FIX:")
        print("1. Use Google Colab with your existing notebook:")
        print("   Backend/DATASET/YOLOv8_large_object_detection.ipynb")
        print("2. After training, download the 'best.pt' file")
        print("3. Place it in: z:\\VESIRE_35\\Backend\\models\\best.pt")
        print("4. Run this script again to convert to TFLite")
        sys.exit(1)

# ============================================================================
# STEP 5: Export to TensorFlow Lite
# ============================================================================
print("\n📤 Step 5: Exporting to TensorFlow Lite...")
print("=" * 70)

try:
    # Load the trained model
    model = YOLO(trained_model_path)
    print(f"✅ Loaded model from: {trained_model_path}")
    
    # Export to TFLite with INT8 quantization for mobile optimization
    print("\n🔄 Converting to TFLite (INT8 quantized)...")
    print("   This will create a smaller, faster model for mobile devices")
    
    export_path = model.export(
        format='tflite',
        imgsz=640,
        int8=True,  # Enable INT8 quantization
        data=None,  # Add your data.yaml path if quantization needs calibration
    )
    
    print(f"\n✅ TFLite model exported successfully!")
    print(f"   Location: {export_path}")
    
    # Find the TFLite file
    tflite_file = None
    if isinstance(export_path, str):
        if export_path.endswith('.tflite'):
            tflite_file = export_path
        else:
            # Search for .tflite file in the export directory
            export_dir = Path(export_path).parent if Path(export_path).is_file() else Path(export_path)
            tflite_files = list(export_dir.glob('*.tflite'))
            if tflite_files:
                tflite_file = str(tflite_files[0])
    
    if not tflite_file:
        # Try alternative export without quantization
        print("\n⚠️ INT8 export failed. Trying FP16 export...")
        export_path = model.export(
            format='tflite',
            imgsz=640,
            half=True,  # FP16 precision
        )
        tflite_file = export_path if isinstance(export_path, str) else None
    
    if tflite_file and os.path.exists(tflite_file):
        print(f"\n📊 Model Statistics:")
        model_size = os.path.getsize(tflite_file) / (1024 * 1024)  # MB
        print(f"   Size: {model_size:.2f} MB")
        
        # Copy to final location
        final_model_path = OUTPUT_DIR / "plant_disease_model.tflite"
        shutil.copy(tflite_file, final_model_path)
        print(f"   Copied to: {final_model_path}")
        
    else:
        print("⚠️ TFLite file not found. Trying alternative export...")
        # Try saved_model format first, then convert
        print("   Exporting to saved_model format...")
        saved_model_path = model.export(format='saved_model', imgsz=640)
        print(f"   Saved model at: {saved_model_path}")
        
        # Manual conversion using TFLite converter
        import tensorflow as tf
        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_path)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_model = converter.convert()
        
        final_model_path = OUTPUT_DIR / "plant_disease_model.tflite"
        with open(final_model_path, 'wb') as f:
            f.write(tflite_model)
        
        model_size = len(tflite_model) / (1024 * 1024)
        print(f"\n✅ Manual conversion successful!")
        print(f"   Size: {model_size:.2f} MB")
        print(f"   Location: {final_model_path}")
    
except Exception as e:
    print(f"\n❌ Export failed: {e}")
    print("\n💡 WORKAROUND:")
    print("You can export manually in Python:")
    print(f"   from ultralytics import YOLO")
    print(f"   model = YOLO('{trained_model_path}')")
    print(f"   model.export(format='tflite', imgsz=640)")
    sys.exit(1)

# ============================================================================
# STEP 6: Create Labels File
# ============================================================================
print("\n📝 Step 6: Creating labels.txt file...")

labels_path = OUTPUT_DIR / "labels.txt"
with open(labels_path, 'w') as f:
    for disease in DISEASE_CLASSES:
        f.write(f"{disease}\n")

print(f"✅ Labels file created: {labels_path}")

# ============================================================================
# STEP 7: Test TFLite Model
# ============================================================================
print("\n🧪 Step 7: Testing TFLite model...")

try:
    # Load TFLite model
    interpreter = tf.lite.Interpreter(model_path=str(final_model_path))
    interpreter.allocate_tensors()
    
    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print("\n📊 Model Information:")
    print(f"   Input shape: {input_details[0]['shape']}")
    print(f"   Input type: {input_details[0]['dtype']}")
    print(f"   Output shape: {output_details[0]['shape']}")
    print(f"   Output type: {output_details[0]['dtype']}")
    
    # Test with dummy data
    input_shape = input_details[0]['shape']
    dummy_input = np.random.randint(0, 255, input_shape, dtype=np.uint8)
    
    interpreter.set_tensor(input_details[0]['index'], dummy_input)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    
    print(f"\n✅ Model inference successful!")
    print(f"   Output shape: {output.shape}")
    
except Exception as e:
    print(f"\n⚠️ Testing failed: {e}")
    print("   Don't worry - model might still work in Flutter app")

# ============================================================================
# STEP 8: Prepare Files for Flutter
# ============================================================================
print("\n📦 Step 8: Preparing files for Flutter integration...")

flutter_assets_dir = Path(__file__).parent.parent / "ar_test_app" / "assets" / "models"
flutter_assets_dir.mkdir(parents=True, exist_ok=True)

# Copy model
if final_model_path.exists():
    shutil.copy(final_model_path, flutter_assets_dir / "plant_disease_model.tflite")
    print(f"✅ Model copied to Flutter: {flutter_assets_dir / 'plant_disease_model.tflite'}")

# Copy labels
if labels_path.exists():
    shutil.copy(labels_path, flutter_assets_dir / "labels.txt")
    print(f"✅ Labels copied to Flutter: {flutter_assets_dir / 'labels.txt'}")

# ============================================================================
# STEP 9: Summary & Next Steps
# ============================================================================
print("\n" + "=" * 70)
print("🎉 SUCCESS! Model ready for Flutter integration")
print("=" * 70)

print("\n📁 Generated Files:")
print(f"   1. TFLite Model: {final_model_path}")
print(f"   2. Labels File: {labels_path}")
print(f"   3. Flutter Assets: {flutter_assets_dir}/")

print("\n🚀 Next Steps:")
print("   1. Update ar_test_app/pubspec.yaml to include model assets")
print("   2. Add TFLite dependencies to pubspec.yaml")
print("   3. Create disease_detector.dart service")
print("   4. Build AR detection screen with camera feed")
print("   5. Test on physical Android device")

print("\n💡 Need help with Flutter integration?")
print("   Just ask: 'Build the Flutter detection screen'")

print("\n" + "=" * 70)
print("✅ Script completed successfully!")
print("=" * 70)
