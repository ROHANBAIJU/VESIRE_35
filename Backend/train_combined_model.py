"""
AgriScan - Combined Dataset Training Script
Combines PlantDoc, Rice, and Wheat datasets and trains a lightweight YOLOv8n model
Exports to TFLite for fast inference
"""

import os
import json
import shutil
from pathlib import Path
import yaml
from ultralytics import YOLO
import cv2
import numpy as np
from tqdm import tqdm

# Paths
BASE_DIR = Path(__file__).parent
DATASET_DIR = BASE_DIR / "DATASET"
OUTPUT_DIR = BASE_DIR / "unified_dataset"
MODEL_OUTPUT_DIR = BASE_DIR / "models" / "agriscan_combined"

# Dataset paths
PLANTDOC_DIR = DATASET_DIR / "plantdoc-DatasetNinja"
RICE_DIR = DATASET_DIR / "RICE DATASET"
WHEAT_DIR = DATASET_DIR / "Wheat Disease Detection.v4i.yolov8-obb"


def convert_supervisely_to_yolo(img_dir, ann_dir, output_img_dir, output_label_dir, class_mapping):
    """
    Convert Supervisely format annotations to YOLO format
    
    Args:
        img_dir: Directory containing images
        ann_dir: Directory containing annotations
        output_img_dir: Output directory for images
        output_label_dir: Output directory for labels
        class_mapping: Dictionary mapping class names to class IDs
    """
    img_dir = Path(img_dir)
    ann_dir = Path(ann_dir)
    output_img_dir = Path(output_img_dir)
    output_label_dir = Path(output_label_dir)
    
    output_img_dir.mkdir(parents=True, exist_ok=True)
    output_label_dir.mkdir(parents=True, exist_ok=True)
    
    converted_count = 0
    skipped_count = 0
    
    # Get all annotation files
    ann_files = list(ann_dir.glob("*.json"))
    
    print(f"  Processing {len(ann_files)} annotations...")
    
    for ann_file in tqdm(ann_files, desc="  Converting"):
        try:
            # Read annotation
            with open(ann_file, 'r') as f:
                ann_data = json.load(f)
            
            # The annotation filename format is: original_image_name.extension.json
            # We need to extract the original image name
            # e.g., "0.jpg.json" -> "0.jpg"
            json_stem = ann_file.stem  # This gives us "0.jpg" from "0.jpg.json"
            
            # Try to find the image file
            img_path = None
            
            # First, try the exact name from json stem
            test_path = img_dir / json_stem
            if test_path.exists():
                img_path = test_path
            else:
                # Try different extensions on the base name (without the extension in json stem)
                base_name = json_stem.rsplit('.', 1)[0] if '.' in json_stem else json_stem
                for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                    test_path = img_dir / (base_name + ext)
                    if test_path.exists():
                        img_path = test_path
                        break
            
            if img_path is None:
                skipped_count += 1
                continue
            
            # Read image to get dimensions
            img = cv2.imread(str(img_path))
            if img is None:
                skipped_count += 1
                continue
                
            img_height, img_width = img.shape[:2]
            
            # Process objects
            yolo_annotations = []
            
            if 'objects' in ann_data and len(ann_data['objects']) > 0:
                for obj in ann_data['objects']:
                    class_name = obj.get('classTitle', '')
                    
                    # Get class ID
                    if class_name not in class_mapping:
                        continue
                    
                    class_id = class_mapping[class_name]
                    
                    # Get bounding box
                    if 'points' in obj and 'exterior' in obj['points']:
                        points = obj['points']['exterior']
                        if len(points) >= 2:
                            # Get bounding box coordinates
                            x_coords = [p[0] for p in points]
                            y_coords = [p[1] for p in points]
                            
                            x_min = min(x_coords)
                            x_max = max(x_coords)
                            y_min = min(y_coords)
                            y_max = max(y_coords)
                            
                            # Skip invalid boxes
                            if x_max <= x_min or y_max <= y_min:
                                continue
                            
                            # Convert to YOLO format (normalized)
                            x_center = ((x_min + x_max) / 2) / img_width
                            y_center = ((y_min + y_max) / 2) / img_height
                            width = (x_max - x_min) / img_width
                            height = (y_max - y_min) / img_height
                            
                            # Ensure values are within bounds
                            x_center = max(0, min(1, x_center))
                            y_center = max(0, min(1, y_center))
                            width = max(0, min(1, width))
                            height = max(0, min(1, height))
                            
                            # Skip if box is too small
                            if width < 0.01 or height < 0.01:
                                continue
                            
                            yolo_annotations.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
            
            # Skip if no valid annotations
            if not yolo_annotations:
                skipped_count += 1
                continue
            
            # Copy image with unique name to avoid conflicts
            output_img_path = output_img_dir / img_path.name
            if output_img_path.exists():
                # Add unique suffix if file already exists
                base = img_path.stem
                ext = img_path.suffix
                counter = 1
                while output_img_path.exists():
                    output_img_path = output_img_dir / f"{base}_{counter}{ext}"
                    counter += 1
            
            shutil.copy2(img_path, output_img_path)
            
            # Write YOLO annotation with same name as image
            output_label_path = output_label_dir / (output_img_path.stem + '.txt')
            with open(output_label_path, 'w') as f:
                f.write('\n'.join(yolo_annotations))
            
            converted_count += 1
            
        except Exception as e:
            print(f"    Error processing {ann_file.name}: {e}")
            skipped_count += 1
            continue
    
    print(f"  ✅ Converted: {converted_count}, Skipped: {skipped_count}")
    return converted_count


def prepare_unified_dataset():
    """
    Prepare unified dataset from all three sources
    """
    print("\n" + "="*60)
    print("PREPARING UNIFIED DATASET")
    print("="*60)
    
    # Create output directories
    for split in ['train', 'val']:
        (OUTPUT_DIR / split / 'images').mkdir(parents=True, exist_ok=True)
        (OUTPUT_DIR / split / 'labels').mkdir(parents=True, exist_ok=True)
    
    # Define unified class mapping
    class_names = []
    class_mapping = {}
    
    # Load PlantDoc classes
    print("\n📦 Loading PlantDoc dataset...")
    plantdoc_meta = json.load(open(PLANTDOC_DIR / "meta.json"))
    for cls in plantdoc_meta['classes']:
        if cls['title'] not in class_mapping:
            class_mapping[cls['title']] = len(class_names)
            class_names.append(cls['title'])
    
    # Load Rice classes
    print("📦 Loading Rice dataset...")
    rice_meta = json.load(open(RICE_DIR / "meta.json"))
    for cls in rice_meta['classes']:
        if cls['title'] not in class_mapping:
            class_mapping[cls['title']] = len(class_names)
            class_names.append(cls['title'])
    
    # Load Wheat classes
    print("📦 Loading Wheat dataset...")
    wheat_yaml = yaml.safe_load(open(WHEAT_DIR / "data.yaml"))
    for cls_id, cls_name in wheat_yaml['names'].items():
        if cls_name not in class_mapping:
            class_mapping[cls_name] = len(class_names)
            class_names.append(cls_name)
    
    print(f"\n✅ Total classes: {len(class_names)}")
    print(f"Classes: {', '.join(class_names[:5])}... (showing first 5)")
    
    # Convert and copy datasets
    total_train = 0
    total_val = 0
    
    # 1. Process PlantDoc - use more for training
    print("\n🔄 Processing PlantDoc dataset...")
    train_count = convert_supervisely_to_yolo(
        PLANTDOC_DIR / "train" / "img",
        PLANTDOC_DIR / "train" / "ann",
        OUTPUT_DIR / "train" / "images",
        OUTPUT_DIR / "train" / "labels",
        class_mapping
    )
    # Use only 10% of test set for validation to maximize training data
    val_count = convert_supervisely_to_yolo(
        PLANTDOC_DIR / "test" / "img",
        PLANTDOC_DIR / "test" / "ann",
        OUTPUT_DIR / "val" / "images",
        OUTPUT_DIR / "val" / "labels",
        class_mapping
    )
    total_train += train_count
    total_val += val_count
    print(f"  PlantDoc: {train_count} train, {val_count} val")
    
    # 2. Process Rice Dataset - use ALL images
    print("\n🔄 Processing Rice dataset...")
    # Train set
    rice_train_count = convert_supervisely_to_yolo(
        RICE_DIR / "train" / "img",
        RICE_DIR / "train" / "ann",
        OUTPUT_DIR / "train" / "images",
        OUTPUT_DIR / "train" / "labels",
        class_mapping
    )
    # Add valid set to training for maximum data
    rice_valid_count = convert_supervisely_to_yolo(
        RICE_DIR / "valid" / "img",
        RICE_DIR / "valid" / "ann",
        OUTPUT_DIR / "train" / "images",
        OUTPUT_DIR / "train" / "labels",
        class_mapping
    )
    # Use only test for validation
    rice_val_count = convert_supervisely_to_yolo(
        RICE_DIR / "test" / "img",
        RICE_DIR / "test" / "ann",
        OUTPUT_DIR / "val" / "images",
        OUTPUT_DIR / "val" / "labels",
        class_mapping
    )
    train_count = rice_train_count + rice_valid_count
    val_count = rice_val_count
    total_train += train_count
    total_val += val_count
    print(f"  Rice: {train_count} train ({rice_train_count} + {rice_valid_count}), {val_count} val")
    
    # 3. Process Wheat Dataset (already in YOLO format) - use ALL images
    print("\n🔄 Processing Wheat dataset...")
    
    # Process all wheat folders
    wheat_folders = [
        ("train", OUTPUT_DIR / "train"),
        ("valid", OUTPUT_DIR / "train"),  # Add valid to training
        ("test", OUTPUT_DIR / "train"),   # Add test to training
    ]
    
    wheat_train_total = 0
    for folder_name, output_dir in wheat_folders:
        wheat_img = WHEAT_DIR / folder_name / "images"
        wheat_lbl = WHEAT_DIR / folder_name / "labels"
        
        if wheat_img.exists() and wheat_lbl.exists():
            folder_count = 0
            for img_file in wheat_img.glob("*.*"):
                label_file = wheat_lbl / (img_file.stem + '.txt')
                if label_file.exists():
                    # Copy image with unique name to avoid conflicts
                    output_img_path = output_dir / "images" / img_file.name
                    if output_img_path.exists():
                        base = img_file.stem
                        ext = img_file.suffix
                        counter = 1
                        while output_img_path.exists():
                            output_img_path = output_dir / "images" / f"{base}_wheat{counter}{ext}"
                            counter += 1
                    
                    shutil.copy2(img_file, output_img_path)
                    
                    # Update class IDs in label file
                    with open(label_file, 'r') as f:
                        lines = f.readlines()
                    
                    updated_lines = []
                    for line in lines:
                        parts = line.strip().split()
                        if len(parts) >= 5:
                            old_class_id = int(parts[0])
                            wheat_class_name = wheat_yaml['names'][old_class_id]
                            new_class_id = class_mapping[wheat_class_name]
                            parts[0] = str(new_class_id)
                            updated_lines.append(' '.join(parts))
                    
                    if updated_lines:
                        with open(output_dir / "labels" / (output_img_path.stem + '.txt'), 'w') as f:
                            f.write('\n'.join(updated_lines))
                        
                        folder_count += 1
            
            print(f"    Added {folder_count} images from {folder_name}")
            wheat_train_total += folder_count
    
    # Use a small portion of PlantDoc test for validation
    val_count = 50  # We already have some validation images
    train_count = wheat_train_total
    
    total_train += train_count
    print(f"  Wheat: {train_count} train (all folders combined)")
    
    # Create data.yaml
    print("\n📝 Creating data.yaml...")
    data_yaml = {
        'path': str(OUTPUT_DIR.absolute()),
        'train': 'train/images',
        'val': 'val/images',
        'nc': len(class_names),
        'names': {i: name for i, name in enumerate(class_names)}
    }
    
    with open(OUTPUT_DIR / 'data.yaml', 'w') as f:
        yaml.dump(data_yaml, f, default_flow_style=False)
    
    # Save class names to text file
    with open(OUTPUT_DIR / 'labels.txt', 'w') as f:
        f.write('\n'.join(class_names))
    
    print("\n" + "="*60)
    print("DATASET PREPARATION COMPLETE")
    print("="*60)
    print(f"📊 Total training images: {total_train}")
    print(f"📊 Total validation images: {total_val}")
    print(f"📊 Total classes: {len(class_names)}")
    print(f"📁 Dataset location: {OUTPUT_DIR}")
    print("="*60)
    
    return OUTPUT_DIR / 'data.yaml', class_names


def train_model(data_yaml, class_names):
    """
    Train YOLOv8n model with optimized hyperparameters
    """
    print("\n" + "="*60)
    print("TRAINING YOLOV8N MODEL")
    print("="*60)
    
    # Initialize YOLOv8n (nano - fastest and lightest)
    print("\n📥 Loading YOLOv8n base model...")
    model = YOLO('yolov8n.pt')
    
    # Training parameters optimized for high accuracy and speed
    print("\n🚀 Starting training...")
    print(f"  Epochs: 100")
    print(f"  Image size: 640")
    print(f"  Batch size: 16 (auto)")
    print(f"  Device: GPU if available, else CPU")
    print(f"  Classes: {len(class_names)}")
    
    results = model.train(
        data=str(data_yaml),
        epochs=100,
        imgsz=640,
        batch=16,
        name='agriscan_combined',
        project=str(BASE_DIR / 'models'),
        
        # Optimization parameters for high accuracy
        optimizer='AdamW',  # AdamW optimizer for better convergence
        lr0=0.001,  # Initial learning rate
        lrf=0.01,  # Final learning rate factor
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        
        # Data augmentation for better generalization
        hsv_h=0.015,  # HSV-Hue augmentation
        hsv_s=0.7,    # HSV-Saturation augmentation
        hsv_v=0.4,    # HSV-Value augmentation
        degrees=0.0,   # Rotation augmentation
        translate=0.1, # Translation augmentation
        scale=0.5,     # Scale augmentation
        shear=0.0,     # Shear augmentation
        perspective=0.0,  # Perspective augmentation
        flipud=0.0,    # Flip up-down probability
        fliplr=0.5,    # Flip left-right probability
        mosaic=1.0,    # Mosaic augmentation probability
        mixup=0.0,     # MixUp augmentation probability
        copy_paste=0.0,  # Copy-paste augmentation
        
        # Performance parameters
        patience=50,   # Early stopping patience
        save=True,     # Save checkpoints
        save_period=10,  # Save every 10 epochs
        cache=False,   # Don't cache images (saves memory)
        device='',     # Auto-select device
        workers=8,     # Number of workers
        exist_ok=True,
        pretrained=True,
        verbose=True,
        seed=0,
        deterministic=True,
        single_cls=False,
        rect=False,
        cos_lr=True,  # Cosine learning rate scheduler
        close_mosaic=10,  # Disable mosaic in last 10 epochs
        amp=True,  # Automatic Mixed Precision
        fraction=1.0,
        profile=False,
        overlap_mask=True,
        mask_ratio=4,
        dropout=0.0,
        val=True,
        plots=True
    )
    
    print("\n✅ Training completed!")
    
    # Get best model path
    best_model_path = MODEL_OUTPUT_DIR / 'weights' / 'best.pt'
    
    # Print training metrics
    print("\n" + "="*60)
    print("TRAINING METRICS")
    print("="*60)
    
    if results is not None:
        print(f"  Best model: {best_model_path}")
        
    return best_model_path


def export_to_tflite(model_path):
    """
    Export trained model to TFLite format for mobile deployment
    """
    print("\n" + "="*60)
    print("EXPORTING TO TFLITE")
    print("="*60)
    
    try:
        # Load best model
        print("\n📥 Loading best model...")
        model = YOLO(str(model_path))
        
        # Export to TFLite
        print("🔄 Exporting to TFLite format...")
        print("  This may take a few minutes...")
        
        tflite_path = model.export(
            format='tflite',
            imgsz=640,
            optimize=True,  # Optimize for mobile
            int8=False,  # Use float16 for better accuracy
            dynamic=False,
            simplify=True,
            nms=True  # Include NMS in the model
        )
        
        print(f"\n✅ TFLite model exported: {tflite_path}")
        
        return tflite_path
        
    except Exception as e:
        print(f"\n❌ Error exporting to TFLite: {e}")
        print("  The .pt model is still available and can be used.")
        return None


def validate_model(model_path, data_yaml):
    """
    Validate model on validation set
    """
    print("\n" + "="*60)
    print("VALIDATING MODEL")
    print("="*60)
    
    try:
        model = YOLO(str(model_path))
        
        print("\n🔄 Running validation...")
        results = model.val(data=str(data_yaml))
        
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60)
        print(f"  mAP50: {results.box.map50:.4f}")
        print(f"  mAP50-95: {results.box.map:.4f}")
        print(f"  Precision: {results.box.mp:.4f}")
        print(f"  Recall: {results.box.mr:.4f}")
        print("="*60)
        
        return results
        
    except Exception as e:
        print(f"\n❌ Error validating model: {e}")
        return None


def update_flask_config(model_path, class_names):
    """
    Update Flask configuration to use new model
    """
    print("\n" + "="*60)
    print("UPDATING FLASK CONFIGURATION")
    print("="*60)
    
    # Copy labels to api directory
    labels_path = BASE_DIR / "api" / "labels.txt"
    print(f"\n📝 Updating labels file: {labels_path}")
    with open(labels_path, 'w') as f:
        f.write('\n'.join(class_names))
    
    print(f"✅ Labels file updated with {len(class_names)} classes")
    
    print("\n💡 Manual step required:")
    print(f"  Update config.py MODEL_PATH to: {model_path}")
    print("="*60)


def main():
    """
    Main training pipeline
    """
    print("\n" + "="*60)
    print("AGRISCAN - COMBINED MODEL TRAINING")
    print("="*60)
    print("  Datasets: PlantDoc + Rice + Wheat")
    print("  Model: YOLOv8n (lightweight)")
    print("  Epochs: 100")
    print("  Export: TFLite")
    print("="*60)
    
    try:
        # Step 1: Prepare unified dataset
        data_yaml, class_names = prepare_unified_dataset()
        
        # Step 2: Train model
        best_model_path = train_model(data_yaml, class_names)
        
        # Step 3: Validate model
        validate_model(best_model_path, data_yaml)
        
        # Step 4: Export to TFLite
        tflite_path = export_to_tflite(best_model_path)
        
        # Step 5: Update Flask configuration
        update_flask_config(best_model_path, class_names)
        
        print("\n" + "="*60)
        print("🎉 TRAINING PIPELINE COMPLETE!")
        print("="*60)
        print(f"  ✅ Model trained: {best_model_path}")
        if tflite_path:
            print(f"  ✅ TFLite exported: {tflite_path}")
        print(f"  ✅ Classes: {len(class_names)}")
        print(f"  ✅ Dataset: {OUTPUT_DIR}")
        print("\n  Next steps:")
        print(f"    1. Update config.py MODEL_PATH")
        print("    2. Restart Flask server")
        print("    3. Test detection with new model")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error in training pipeline: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
