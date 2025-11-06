"""
AgriScan - Test Combined Model
Test the trained combined model for accuracy and inference speed
"""

import time
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np
from tqdm import tqdm

# Paths
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "models" / "agriscan_combined" / "weights" / "best.pt"
DATASET_PATH = BASE_DIR / "unified_dataset"
LABELS_PATH = DATASET_PATH / "labels.txt"


def load_class_names():
    """Load class names"""
    with open(LABELS_PATH, 'r') as f:
        return [line.strip() for line in f.readlines()]


def test_inference_speed(model, num_iterations=100):
    """
    Test inference speed on random images
    """
    print("\n" + "="*60)
    print("TESTING INFERENCE SPEED")
    print("="*60)
    
    # Create random test images
    test_images = [np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8) for _ in range(num_iterations)]
    
    # Warmup
    print("\n🔥 Warming up...")
    for _ in range(10):
        _ = model(test_images[0], verbose=False)
    
    # Test inference speed
    print(f"⚡ Testing inference speed ({num_iterations} iterations)...")
    times = []
    
    for img in tqdm(test_images, desc="  Processing"):
        start_time = time.time()
        _ = model(img, verbose=False)
        inference_time = (time.time() - start_time) * 1000  # Convert to ms
        times.append(inference_time)
    
    # Calculate statistics
    avg_time = np.mean(times)
    min_time = np.min(times)
    max_time = np.max(times)
    std_time = np.std(times)
    fps = 1000 / avg_time
    
    print("\n" + "="*60)
    print("SPEED TEST RESULTS")
    print("="*60)
    print(f"  Average inference time: {avg_time:.2f} ms")
    print(f"  Min inference time: {min_time:.2f} ms")
    print(f"  Max inference time: {max_time:.2f} ms")
    print(f"  Std deviation: {std_time:.2f} ms")
    print(f"  FPS (frames per second): {fps:.2f}")
    print("="*60)
    
    return avg_time, fps


def test_on_validation_set(model, data_yaml):
    """
    Test model on validation set
    """
    print("\n" + "="*60)
    print("TESTING ON VALIDATION SET")
    print("="*60)
    
    print("\n🔄 Running validation...")
    results = model.val(data=str(data_yaml))
    
    print("\n" + "="*60)
    print("VALIDATION METRICS")
    print("="*60)
    print(f"  mAP50 (IoU=0.5): {results.box.map50:.4f}")
    print(f"  mAP50-95 (IoU=0.5:0.95): {results.box.map:.4f}")
    print(f"  Precision: {results.box.mp:.4f}")
    print(f"  Recall: {results.box.mr:.4f}")
    print(f"  F1-Score: {2 * (results.box.mp * results.box.mr) / (results.box.mp + results.box.mr):.4f}")
    print("="*60)
    
    return results


def test_on_sample_images(model, class_names, num_samples=5):
    """
    Test model on sample images from validation set
    """
    print("\n" + "="*60)
    print("TESTING ON SAMPLE IMAGES")
    print("="*60)
    
    val_img_dir = DATASET_PATH / "val" / "images"
    val_images = list(val_img_dir.glob("*.*"))[:num_samples]
    
    if not val_images:
        print("  ⚠️  No validation images found")
        return
    
    print(f"\n🖼️  Testing on {len(val_images)} sample images...")
    
    for img_path in val_images:
        print(f"\n  Image: {img_path.name}")
        
        # Run inference
        start_time = time.time()
        results = model(str(img_path), verbose=False)
        inference_time = (time.time() - start_time) * 1000
        
        # Get detections
        detections = results[0].boxes
        
        print(f"    Inference time: {inference_time:.2f} ms")
        print(f"    Detections: {len(detections)}")
        
        if len(detections) > 0:
            for i, box in enumerate(detections):
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = class_names[class_id] if class_id < len(class_names) else f"Class_{class_id}"
                print(f"      [{i+1}] {class_name}: {confidence:.2%}")


def analyze_model_size():
    """
    Analyze model file size
    """
    print("\n" + "="*60)
    print("MODEL SIZE ANALYSIS")
    print("="*60)
    
    if MODEL_PATH.exists():
        size_mb = MODEL_PATH.stat().st_size / (1024 * 1024)
        print(f"\n  Model file: {MODEL_PATH.name}")
        print(f"  Size: {size_mb:.2f} MB")
        
        # Check for TFLite model
        tflite_path = MODEL_PATH.parent / "best_saved_model" / "best_float16.tflite"
        if tflite_path.exists():
            tflite_size_mb = tflite_path.stat().st_size / (1024 * 1024)
            print(f"\n  TFLite file: {tflite_path.name}")
            print(f"  Size: {tflite_size_mb:.2f} MB")
            print(f"  Compression ratio: {size_mb / tflite_size_mb:.2f}x")
    else:
        print("  ⚠️  Model not found")
    
    print("="*60)


def main():
    """
    Main testing pipeline
    """
    print("\n" + "="*60)
    print("AGRISCAN - COMBINED MODEL TESTING")
    print("="*60)
    
    # Check if model exists
    if not MODEL_PATH.exists():
        print(f"\n❌ Model not found at: {MODEL_PATH}")
        print("  Please run train_combined_model.py first")
        return
    
    # Load model
    print("\n📥 Loading model...")
    model = YOLO(str(MODEL_PATH))
    print(f"✅ Model loaded: {MODEL_PATH.name}")
    
    # Load class names
    class_names = load_class_names()
    print(f"✅ Loaded {len(class_names)} classes")
    
    # 1. Analyze model size
    analyze_model_size()
    
    # 2. Test inference speed
    avg_time, fps = test_inference_speed(model)
    
    # 3. Test on validation set
    data_yaml = DATASET_PATH / "data.yaml"
    if data_yaml.exists():
        results = test_on_validation_set(model, data_yaml)
    else:
        print(f"\n⚠️  Data YAML not found: {data_yaml}")
    
    # 4. Test on sample images
    test_on_sample_images(model, class_names)
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 TESTING COMPLETE!")
    print("="*60)
    print(f"  ✅ Model: YOLOv8n")
    print(f"  ✅ Classes: {len(class_names)}")
    print(f"  ✅ Avg inference time: {avg_time:.2f} ms")
    print(f"  ✅ FPS: {fps:.2f}")
    
    # Performance rating
    if fps >= 30:
        rating = "EXCELLENT - Real-time capable"
    elif fps >= 15:
        rating = "GOOD - Suitable for most applications"
    elif fps >= 10:
        rating = "ACCEPTABLE - May need optimization"
    else:
        rating = "SLOW - Needs optimization or hardware upgrade"
    
    print(f"  ✅ Performance: {rating}")
    print("="*60)


if __name__ == "__main__":
    main()
