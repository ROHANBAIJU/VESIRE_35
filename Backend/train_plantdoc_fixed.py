"""
AgriScan AR - PlantDoc to YOLOv8 Training Pipeline
Converts PlantDoc dataset to YOLO format and trains YOLOv8 model for plant disease detection
Exports to TFLite format for Flutter mobile deployment
"""

import json
import shutil
from pathlib import Path
from PIL import Image

# ============================================================================
# Configuration
# ============================================================================
PLANTDOC_DIR = Path("Z:/VESIRE_35/plantdoc-DatasetNinja")
YOLO_DATASET_DIR = Path("Z:/VESIRE_35/Backend/yolo_dataset")
OUTPUT_DIR = Path("Z:/VESIRE_35/Backend/models")
FLUTTER_ASSETS = Path("Z:/VESIRE_35/ar_test_app/assets/models")

# Training parameters
MODEL_SIZE = 'yolov8n'  # Changed to nano for faster training with limited data
EPOCHS = 30  # Reduced epochs for small dataset
BATCH_SIZE = 8  # Smaller batch for limited data
IMG_SIZE = 640

# ============================================================================
# STEP 1: Load PlantDoc Metadata
# ============================================================================
print("\n" + "=" * 70)
print("🚀 AgriScan AR - PlantDoc Training Pipeline")
print("=" * 70)
print("\n📋 STEP 1: Loading PlantDoc Metadata")

meta_path = PLANTDOC_DIR / "meta.json"
with open(meta_path, 'r') as f:
    meta = json.load(f)

# Extract class names from meta.json
class_names = []
class_id_map = {}

for idx, cls in enumerate(meta['classes']):
    class_title = cls['title']
    class_names.append(class_title)
    class_id_map[class_title] = idx

print(f"✅ Loaded {len(class_names)} classes from {meta_path}")

# Create YOLO dataset structure
train_imgs_dir = YOLO_DATASET_DIR / "images" / "train"
train_labels_dir = YOLO_DATASET_DIR / "labels" / "train"
test_imgs_dir = YOLO_DATASET_DIR / "images" / "val"
test_labels_dir = YOLO_DATASET_DIR / "labels" / "val"

for dir_path in [train_imgs_dir, train_labels_dir, test_imgs_dir, test_labels_dir]:
    dir_path.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Helper Functions
# ============================================================================

def convert_annotation_to_yolo(ann_file, img_width, img_height, class_id_map):
    """Convert PlantDoc JSON annotation to YOLO format"""
    with open(ann_file, 'r') as f:
        annotation = json.load(f)
    
    yolo_lines = []
    for obj in annotation.get('objects', []):
        class_title = obj['classTitle']
        
        if class_title not in class_id_map:
            continue
        
        class_id = class_id_map[class_title]
        
        # Get bounding box points
        points = obj['points']['exterior']
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        
        # Convert to YOLO format (normalized x_center, y_center, width, height)
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        x_center = ((x_min + x_max) / 2) / img_width
        y_center = ((y_min + y_max) / 2) / img_height
        width = (x_max - x_min) / img_width
        height = (y_max - y_min) / img_height
        
        # Validate coordinates
        if not (0 <= x_center <= 1 and 0 <= y_center <= 1 and 0 <= width <= 1 and 0 <= height <= 1):
            continue  # Skip invalid boxes
        
        yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    
    return yolo_lines


def convert_split(src_img_dir, dst_img_dir, dst_label_dir, class_id_map):
    """Convert a dataset split to YOLO format"""
    img_dir = PLANTDOC_DIR / src_img_dir / "img"
    ann_dir = PLANTDOC_DIR / src_img_dir / "ann"
    
    if not img_dir.exists():
        print(f"   ⚠️  Directory not found: {img_dir}")
        return 0, 0
    
    converted_count = 0
    skipped_count = 0
    
    img_files = list(img_dir.glob("*"))
    
    for i, img_file in enumerate(img_files):
        if i > 0 and i % 100 == 0:
            print(f"   Processing: {i}/{len(img_files)} images...")
        
        # Find corresponding annotation file
        ann_file = ann_dir / f"{img_file.name}.json"
        
        if not ann_file.exists():
            print(f"   ⚠️  Skipping {img_file.name} - no annotation file")
            skipped_count += 1
            continue
        
        try:
            # Get image dimensions
            with Image.open(img_file) as img:
                img_width, img_height = img.size
            
            # Convert annotation
            yolo_lines = convert_annotation_to_yolo(ann_file, img_width, img_height, class_id_map)
            
            if not yolo_lines:
                print(f"   ⚠️  Skipping {img_file.name} - no valid annotations")
                skipped_count += 1
                continue
            
            # Copy image
            dst_img_path = dst_img_dir / img_file.name
            shutil.copy2(img_file, dst_img_path)
            
            # Write YOLO label file
            label_file = dst_label_dir / f"{img_file.stem}.txt"
            with open(label_file, 'w') as f:
                f.write('\n'.join(yolo_lines))
            
            converted_count += 1
            
        except Exception as e:
            print(f"   ⚠️  Error processing {img_file.name}: {e}")
            skipped_count += 1
    
    return converted_count, skipped_count


# ============================================================================
# Main Training Function
# ============================================================================

def main():
    """Main training function with multiprocessing guard for Windows"""
    
    train_dir = "train"
    test_dir = "test"
    
    print(f"\n{'='*70}")
    print(f"📦 STEP 2: Converting PlantDoc to YOLO Format")
    print(f"{'='*70}")
    
    # Convert train split
    print(f"\n🔄 Converting train split...")
    train_converted, train_skipped = convert_split(
        train_dir, 
        train_imgs_dir, 
        train_labels_dir, 
        class_id_map
    )
    print(f"   ✅ Converted {train_converted} images in train split")
    print(f"   ⚠️  Skipped {train_skipped} images")
    
    # Convert test split
    print(f"\n🔄 Converting test split...")
    test_converted, test_skipped = convert_split(
        test_dir, 
        test_imgs_dir, 
        test_labels_dir, 
        class_id_map
    )
    print(f"   ✅ Converted {test_converted} images in test split")
    print(f"   ⚠️  Skipped {test_skipped} images")
    
    # Check if we have enough data
    if train_converted < 3:
        print(f"\n❌ ERROR: Only {train_converted} images have valid annotations!")
        print(f"   This is insufficient for proper training.")
        print(f"\n💡 Solutions:")
        print(f"   1. Use a pre-annotated dataset from Roboflow")
        print(f"   2. Manually annotate more images using LabelImg or Roboflow")
        print(f"   3. Use Google Colab with the original notebooks")
        return
    
    print(f"\n{'='*70}")
    print(f"📝 STEP 3: Creating data.yaml")
    print(f"{'='*70}")
    
    # Create data.yaml
    data_yaml_content = f"""# PlantDoc Dataset Configuration
path: {str(YOLO_DATASET_DIR.resolve())}
train: images/train
val: images/val

nc: {len(class_names)}
names: {class_names}
"""
    
    data_yaml_path = YOLO_DATASET_DIR / "data.yaml"
    with open(data_yaml_path, 'w') as f:
        f.write(data_yaml_content)
    
    print(f"✅ Created: {data_yaml_path}")
    
    # Also create labels.txt for Flutter
    labels_path = YOLO_DATASET_DIR / "labels.txt"
    with open(labels_path, 'w') as f:
        for name in class_names:
            f.write(f"{name}\n")
    
    print(f"✅ Created: {labels_path}")
    
    print(f"\n{'='*70}")
    print(f"🏋️  STEP 4: Training YOLOv8 Model")
    print(f"{'='*70}")
    print(f"⚠️  WARNING: Training with only {train_converted} images")
    print(f"   Model will have LIMITED accuracy - suitable for testing only!")
    print(f"{'='*70}\n")
    
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
            print(f"   ⚠️  Using CPU (slower)")
        
        # Load pretrained model
        model = YOLO(f'{MODEL_SIZE}.pt')
        print(f"\n✅ Loaded {MODEL_SIZE} pretrained model")
        
        # Train the model
        print(f"\n🚀 Starting training...")
        print(f"   Model: {MODEL_SIZE}")
        print(f"   Epochs: {EPOCHS}")
        print(f"   Batch: {BATCH_SIZE}")
        print(f"   Image Size: {IMG_SIZE}")
        print(f"   Device: {'GPU' if use_gpu else 'CPU'}")
        
        results = model.train(
            data=str(data_yaml_path),
            epochs=EPOCHS,
            imgsz=IMG_SIZE,
            batch=BATCH_SIZE,
            device=device,
            name='agriscan_plantdoc',
            project=str(OUTPUT_DIR),
            workers=0,  # CRITICAL: Set to 0 to avoid multiprocessing issues on Windows
            cache=False,  # Disabled cache due to insufficient RAM warning
            patience=10,
            save=True,
            verbose=True,
        )
        
        trained_model_path = OUTPUT_DIR / 'agriscan_plantdoc' / 'weights' / 'best.pt'
        print(f"\n✅ Training complete!")
        print(f"   Model saved: {trained_model_path}")
        
        # ============================================================================
        # STEP 5: Export to TFLite
        # ============================================================================
        print("\n" + "=" * 70)
        print("📤 STEP 5: Exporting to TensorFlow Lite")
        print("=" * 70)
        
        # Export to TFLite
        export_path = model.export(format='tflite', imgsz=IMG_SIZE)
        print(f"\n✅ TFLite model exported: {export_path}")
        
        # Copy to Flutter assets
        FLUTTER_ASSETS.mkdir(parents=True, exist_ok=True)
        
        tflite_dest = FLUTTER_ASSETS / "plant_disease_model.tflite"
        shutil.copy2(export_path, tflite_dest)
        print(f"✅ Copied to Flutter assets: {tflite_dest}")
        
        # Copy labels.txt
        labels_dest = FLUTTER_ASSETS / "labels.txt"
        shutil.copy2(labels_path, labels_dest)
        print(f"✅ Copied labels to Flutter assets: {labels_dest}")
        
        # ============================================================================
        # Summary
        # ============================================================================
        print("\n" + "=" * 70)
        print("🎉 SUCCESS - Pipeline Complete!")
        print("=" * 70)
        print(f"\n📊 Summary:")
        print(f"   Training Images: {train_converted}")
        print(f"   Validation Images: {test_converted}")
        print(f"   Classes: {len(class_names)}")
        print(f"   Model: {trained_model_path}")
        print(f"   TFLite: {tflite_dest}")
        
        print(f"\n⚠️  IMPORTANT:")
        print(f"   This model was trained on only {train_converted} images")
        print(f"   Accuracy will be LIMITED - suitable for testing Flutter integration only")
        print(f"\n💡 For production:")
        print(f"   1. Get a better annotated dataset (Roboflow, etc.)")
        print(f"   2. Train with at least 100+ images per class")
        print(f"   3. Use data augmentation")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Build Flutter detection screen")
        print(f"   2. Integrate TFLite model")
        print(f"   3. Test with camera feed")
        print(f"   4. Create AR bounding box overlay")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


# ============================================================================
# Entry Point with Windows Multiprocessing Guard
# ============================================================================
if __name__ == '__main__':
    # Required for Windows multiprocessing
    from multiprocessing import freeze_support
    freeze_support()
    main()
