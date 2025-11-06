"""
AgriScan AR - PlantDoc Dataset Training Pipeline
=================================================

This script will:
1. Convert PlantDoc dataset to YOLO format
2. Train YOLOv8 model
3. Export to TFLite for Flutter integration
4. Test the model

Author: Team VESIRE - SJBIT Hackathon 2025
"""

import os
import json
import shutil
from pathlib import Path
import cv2

print("=" * 70)
print("🚀 AgriScan AR - PlantDoc Training Pipeline")
print("=" * 70)

# ============================================================================
# Configuration
# ============================================================================

BASE_DIR = Path(__file__).parent.parent
PLANTDOC_DIR = BASE_DIR / "plantdoc-DatasetNinja"
YOLO_DATASET_DIR = BASE_DIR / "Backend" / "yolo_dataset"
OUTPUT_DIR = BASE_DIR / "Backend" / "models"
FLUTTER_ASSETS_DIR = BASE_DIR / "ar_test_app" / "assets" / "models"

# Create directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
FLUTTER_ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# Model settings
MODEL_SIZE = "yolov8m"  # Options: yolov8n, yolov8s, yolov8m, yolov8l
EPOCHS = 50  # Adjust based on time available (minimum 30, recommended 100)
BATCH_SIZE = 16  # Adjust based on GPU memory
IMG_SIZE = 640

print(f"\n⚙️  Configuration:")
print(f"   Model: {MODEL_SIZE}")
print(f"   Epochs: {EPOCHS}")
print(f"   Batch Size: {BATCH_SIZE}")
print(f"   Image Size: {IMG_SIZE}x{IMG_SIZE}")
print(f"   Dataset: {PLANTDOC_DIR}")

# ============================================================================
# STEP 1: Load PlantDoc Metadata
# ============================================================================
print("\n" + "=" * 70)
print("📋 STEP 1: Loading PlantDoc Metadata")
print("=" * 70)

meta_file = PLANTDOC_DIR / "meta.json"
with open(meta_file, 'r') as f:
    meta_data = json.load(f)

classes = meta_data['classes']
class_names = [cls['title'] for cls in classes]
class_id_map = {cls['id']: idx for idx, cls in enumerate(classes)}
class_name_to_id = {cls['title']: idx for idx, cls in enumerate(classes)}

print(f"✅ Loaded {len(class_names)} classes:")
for idx, name in enumerate(class_names[:10]):
    print(f"   {idx}: {name}")
if len(class_names) > 10:
    print(f"   ... and {len(class_names) - 10} more")

# ============================================================================
# STEP 2: Convert Dataset to YOLO Format
# ============================================================================
print("\n" + "=" * 70)
print("📦 STEP 2: Converting PlantDoc to YOLO Format")
print("=" * 70)

def convert_annotation_to_yolo(ann_file, img_width, img_height, class_id_map):
    """Convert PlantDoc annotation to YOLO format"""
    with open(ann_file, 'r') as f:
        ann_data = json.load(f)
    
    yolo_lines = []
    
    if 'objects' in ann_data:
        for obj in ann_data['objects']:
            class_id = obj['classId']
            if class_id not in class_id_map:
                continue
            
            yolo_class_id = class_id_map[class_id]
            
            # Get bounding box coordinates
            points = obj['points']['exterior']
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            
            x_min = min(x_coords)
            y_min = min(y_coords)
            x_max = max(x_coords)
            y_max = max(y_coords)
            
            # Convert to YOLO format (normalized center x, center y, width, height)
            x_center = ((x_min + x_max) / 2) / img_width
            y_center = ((y_min + y_max) / 2) / img_height
            width = (x_max - x_min) / img_width
            height = (y_max - y_min) / img_height
            
            yolo_lines.append(f"{yolo_class_id} {x_center} {y_center} {width} {height}")
    
    return yolo_lines

# Create YOLO dataset structure
for split in ['train', 'test']:
    print(f"\n🔄 Converting {split} split...")
    
    src_img_dir = PLANTDOC_DIR / split / 'img'
    src_ann_dir = PLANTDOC_DIR / split / 'ann'
    
    dst_img_dir = YOLO_DATASET_DIR / 'images' / ('val' if split == 'test' else split)
    dst_lbl_dir = YOLO_DATASET_DIR / 'labels' / ('val' if split == 'test' else split)
    
    dst_img_dir.mkdir(parents=True, exist_ok=True)
    dst_lbl_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all images
    images = list(src_img_dir.glob('*.jpg')) + list(src_img_dir.glob('*.png'))
    
    converted_count = 0
    skipped_count = 0
    for img_file in images:
        try:
            # Read image first to get dimensions
            img = cv2.imread(str(img_file))
            if img is None:
                print(f"   ⚠️  Skipping {img_file.name} - cannot read image")
                skipped_count += 1
                continue
            
            img_height, img_width = img.shape[:2]
            
            # Convert annotation
            ann_file = src_ann_dir / f"{img_file.stem}.json"
            
            if not ann_file.exists():
                print(f"   ⚠️  Skipping {img_file.name} - no annotation file")
                skipped_count += 1
                continue
            
            # Convert to YOLO format
            yolo_lines = convert_annotation_to_yolo(
                ann_file, img_width, img_height, class_id_map
            )
            
            if not yolo_lines:
                print(f"   ⚠️  Skipping {img_file.name} - no valid annotations")
                skipped_count += 1
                continue
            
            # Copy image
            shutil.copy(img_file, dst_img_dir / img_file.name)
            
            # Save YOLO label file
            label_file = dst_lbl_dir / f"{img_file.stem}.txt"
            with open(label_file, 'w') as f:
                f.write('\n'.join(yolo_lines))
            
            converted_count += 1
            
            if converted_count % 100 == 0:
                print(f"   ... processed {converted_count} images")
        
        except Exception as e:
            print(f"   ⚠️  Error processing {img_file.name}: {e}")
            skipped_count += 1
    
    print(f"   ✅ Converted {converted_count} images in {split} split")
    if skipped_count > 0:
        print(f"   ⚠️  Skipped {skipped_count} images")

# ============================================================================
# STEP 3: Create data.yaml
# ============================================================================
print("\n" + "=" * 70)
print("📝 STEP 3: Creating data.yaml")
print("=" * 70)

data_yaml_path = YOLO_DATASET_DIR / 'data.yaml'
data_yaml_content = f"""# PlantDoc Dataset for AgriScan AR
path: {str(YOLO_DATASET_DIR).replace(chr(92), '/')}
train: images/train
val: images/val

nc: {len(class_names)}
names: {class_names}
"""

with open(data_yaml_path, 'w') as f:
    f.write(data_yaml_content)

print(f"✅ Created: {data_yaml_path}")

# ============================================================================
# STEP 4: Train YOLOv8 Model
# ============================================================================
print("\n" + "=" * 70)
print("🏋️  STEP 4: Training YOLOv8 Model")
print("=" * 70)
print(f"⏰ This will take approximately {EPOCHS * 2} minutes")
print("=" * 70)

try:
    from ultralytics import YOLO
    import torch
    
    # Check GPU availability
    use_gpu = torch.cuda.is_available()
    device = 0 if use_gpu else 'cpu'
    
    print(f"\n🖥️  Hardware Detection:")
    print(f"   CUDA Available: {torch.cuda.is_available()}")
    print(f"   GPU Count: {torch.cuda.device_count()}")
    if use_gpu:
        print(f"   GPU Name: {torch.cuda.get_device_name(0)}")
        print(f"   ✅ Using GPU for training")
    else:
        print(f"   ⚠️  No GPU detected - using CPU (slower)")
        print(f"   💡 Install CUDA PyTorch for GPU: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121")
    
    # Load pretrained model
    model = YOLO(f'{MODEL_SIZE}.pt')
    print(f"\n✅ Loaded {MODEL_SIZE} pretrained model")
    
    # Adjust batch size for CPU if needed
    if not use_gpu and BATCH_SIZE > 8:
        print(f"   ⚠️  Reducing batch size from {BATCH_SIZE} to 8 for CPU")
        BATCH_SIZE = 8
    
    # Train the model
    print(f"\n🚀 Starting training...")
    print(f"   Epochs: {EPOCHS}")
    print(f"   Batch: {BATCH_SIZE}")
    print(f"   Image Size: {IMG_SIZE}")
    print(f"   Device: {'GPU' if use_gpu else 'CPU'}")
    
    results = model.train(
        data=str(data_yaml_path),
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch=BATCH_SIZE,
        name='agriscan_plantdoc',
        project=str(OUTPUT_DIR),
        patience=15,  # Early stopping
        save=True,
        device=device,  # Auto-detect GPU or use CPU
        cache=use_gpu,  # Only cache if using GPU
        workers=4 if use_gpu else 2,  # More workers for GPU
        verbose=True,
    )
    
    trained_model_path = OUTPUT_DIR / 'agriscan_plantdoc' / 'weights' / 'best.pt'
    print(f"\n✅ Training complete!")
    print(f"   Model: {trained_model_path}")
    
except Exception as e:
    print(f"\n❌ Training failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# STEP 5: Validate Model
# ============================================================================
print("\n" + "=" * 70)
print("📊 STEP 5: Validating Model")
print("=" * 70)

try:
    # Validate the model
    metrics = model.val()
    
    print(f"\n✅ Validation Results:")
    print(f"   mAP50: {metrics.box.map50:.3f}")
    print(f"   mAP50-95: {metrics.box.map:.3f}")
    print(f"   Precision: {metrics.box.p.mean():.3f}")
    print(f"   Recall: {metrics.box.r.mean():.3f}")
    
except Exception as e:
    print(f"⚠️  Validation error: {e}")

# ============================================================================
# STEP 6: Export to TFLite
# ============================================================================
print("\n" + "=" * 70)
print("📤 STEP 6: Exporting to TensorFlow Lite")
print("=" * 70)

try:
    # Load the best model
    model = YOLO(trained_model_path)
    
    # Export to TFLite
    print("🔄 Converting to TFLite (this may take 5-10 minutes)...")
    
    export_path = model.export(
        format='tflite',
        imgsz=IMG_SIZE,
    )
    
    print(f"✅ TFLite export complete: {export_path}")
    
    # Find and copy TFLite file
    if isinstance(export_path, str) and os.path.exists(export_path):
        tflite_path = export_path
    else:
        # Search for .tflite file
        search_dir = Path(export_path).parent if isinstance(export_path, str) else trained_model_path.parent
        tflite_files = list(search_dir.glob('**/*.tflite'))
        
        if tflite_files:
            tflite_path = str(tflite_files[0])
        else:
            raise FileNotFoundError("TFLite file not found after export")
    
    # Copy to output and Flutter assets
    final_model_path = OUTPUT_DIR / "plant_disease_model.tflite"
    shutil.copy(tflite_path, final_model_path)
    
    flutter_model_path = FLUTTER_ASSETS_DIR / "plant_disease_model.tflite"
    shutil.copy(final_model_path, flutter_model_path)
    
    model_size = os.path.getsize(final_model_path) / (1024 * 1024)
    
    print(f"\n✅ Model files created:")
    print(f"   Size: {model_size:.2f} MB")
    print(f"   Backend: {final_model_path}")
    print(f"   Flutter: {flutter_model_path}")
    
except Exception as e:
    print(f"\n❌ Export failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# STEP 7: Create Labels File
# ============================================================================
print("\n" + "=" * 70)
print("📝 STEP 7: Creating Labels File")
print("=" * 70)

labels_path = OUTPUT_DIR / "labels.txt"
with open(labels_path, 'w', encoding='utf-8') as f:
    for name in class_names:
        f.write(f"{name}\n")

flutter_labels_path = FLUTTER_ASSETS_DIR / "labels.txt"
shutil.copy(labels_path, flutter_labels_path)

print(f"✅ Labels file created:")
print(f"   Backend: {labels_path}")
print(f"   Flutter: {flutter_labels_path}")
print(f"   Classes: {len(class_names)}")

# ============================================================================
# STEP 8: Summary
# ============================================================================
print("\n" + "=" * 70)
print("🎉 SUCCESS! Training Pipeline Complete")
print("=" * 70)

print(f"\n📊 Summary:")
print(f"   ✅ Dataset: PlantDoc ({len(class_names)} classes)")
print(f"   ✅ Model: {MODEL_SIZE} trained for {EPOCHS} epochs")
print(f"   ✅ TFLite Model: {model_size:.2f} MB")
print(f"   ✅ Flutter Assets: Ready")

print(f"\n📁 Output Files:")
print(f"   1. Trained Model: {trained_model_path}")
print(f"   2. TFLite Model: {final_model_path}")
print(f"   3. Flutter Model: {flutter_model_path}")
print(f"   4. Labels: {labels_path}")
print(f"   5. Training Results: {OUTPUT_DIR / 'agriscan_plantdoc'}")

print(f"\n🚀 Next Steps:")
print(f"   1. ✅ Model is ready!")
print(f"   2. Build Flutter detection screen")
print(f"   3. Integrate TFLite inference")
print(f"   4. Test on physical device")
print(f"   5. Build treatment database")

print("\n" + "=" * 70)
print("Ready for Flutter Integration! 🎯")
print("=" * 70)
