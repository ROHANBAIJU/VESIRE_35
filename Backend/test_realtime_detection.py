"""
AgriScan - Real-time Detection Test with Bounding Boxes
Test the trained model with webcam showing fast bounding boxes and confidence scores
"""

import cv2
import time
from pathlib import Path
from ultralytics import YOLO
import numpy as np
from collections import defaultdict, Counter

# Paths
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "models" / "agriscan_combined" / "weights" / "best.pt"
LABELS_PATH = BASE_DIR / "api" / "labels.txt"

# Colors for bounding boxes (BGR format)
COLORS = [
    (255, 0, 0),      # Blue
    (0, 255, 0),      # Green
    (0, 0, 255),      # Red
    (255, 255, 0),    # Cyan
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Yellow
    (128, 0, 255),    # Purple
    (255, 128, 0),    # Orange
    (0, 128, 255),    # Sky Blue
    (128, 255, 0),    # Lime
]


def load_class_names():
    """Load class names from labels file"""
    with open(LABELS_PATH, 'r') as f:
        return [line.strip() for line in f.readlines()]


def draw_detections(frame, results, class_names, conf_threshold=0.5):
    """
    Draw bounding boxes with labels and confidence scores on frame
    
    Args:
        frame: Input frame
        results: YOLO detection results
        class_names: List of class names
        conf_threshold: Minimum confidence threshold
    
    Returns:
        Tuple of (annotated frame, detection count)
    """
    annotated_frame = frame.copy()
    
    # Get detections
    boxes = results[0].boxes
    
    if boxes is None or len(boxes) == 0:
        return annotated_frame, 0
    
    detection_count = 0
    
    for box in boxes:
        # Get confidence
        confidence = float(box.conf[0])
        
        # Skip if below threshold
        if confidence < conf_threshold:
            continue
        
        # Get coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        
        # Get class
        class_id = int(box.cls[0])
        class_name = class_names[class_id] if class_id < len(class_names) else f"Class_{class_id}"
        
        # Choose color based on class
        color = COLORS[class_id % len(COLORS)]
        
        # Draw bounding box (thicker for better visibility)
        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 3)
        
        # Prepare label with confidence
        label = f"{class_name}: {confidence:.2%}"
        
        # Get text size for background rectangle
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
        
        # Draw background rectangle for text
        cv2.rectangle(
            annotated_frame,
            (x1, y1 - text_height - 10),
            (x1 + text_width + 10, y1),
            color,
            -1  # Filled rectangle
        )
        
        # Draw text
        cv2.putText(
            annotated_frame,
            label,
            (x1 + 5, y1 - 5),
            font,
            font_scale,
            (255, 255, 255),  # White text
            thickness,
            cv2.LINE_AA
        )
        
        detection_count += 1
    
    return annotated_frame, detection_count


def test_webcam_detection():
    """Test real-time detection with webcam"""
    print("\n" + "="*60)
    print("AGRISCAN - REAL-TIME DETECTION TEST")
    print("="*60)
    
    # Check if model exists
    if not MODEL_PATH.exists():
        print(f"\n❌ Model not found: {MODEL_PATH}")
        print("  Please run train_combined_model.py first")
        return
    
    # Load model
    print("\n📥 Loading model...")
    model = YOLO(str(MODEL_PATH))
    print(f"✅ Model loaded: {MODEL_PATH.name}")
    
    # Load class names
    class_names = load_class_names()
    print(f"✅ Loaded {len(class_names)} classes")
    
    # Open webcam
    print("\n📹 Opening webcam...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam")
        return
    
    # Set resolution to 1280x720 for better quality and larger display
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    print("✅ Webcam opened successfully")
    print("\n" + "="*60)
    print("CONTROLS")
    print("="*60)
    print("  Press 'q' or ESC to quit (exits fullscreen)")
    print("  Press 's' to save current frame")
    print("  Press '+' to increase confidence threshold")
    print("  Press '-' to decrease confidence threshold")
    print("  Press 'f' to toggle fullscreen")
    print("="*60)
    print("\n💡 TIP: Bounding boxes persist for ~0.5 seconds for smoother visualization")
    print("💡 TIP: Similar diseases (wheat rust vs corn rust) may get confused - this is normal!")
    print("="*60)
    
    # FPS calculation
    fps_list = []
    frame_count = 0
    conf_threshold = 0.5
    avg_fps = 0.0  # Initialize avg_fps
    
    # Temporal smoothing for bounding boxes - keep detections for longer
    detection_history = []  # Store last N frames of detections
    history_size = 15  # Keep detections for 15 frames (~0.5 seconds at 30fps)
    
    # Primary detection tracking
    class_occurrence_counter = Counter()  # Count occurrences of each class
    primary_detection_class = None  # The most frequently detected class
    primary_detection_bbox = None  # Bounding box of primary detection
    tracking_window_size = 45  # Look at last 45 frames (~1.5 seconds) to determine primary
    class_history = []  # Store class detections for each frame
    
    print("\n🚀 Starting real-time detection...")
    print("  (Bounding boxes will appear in RED, GREEN, BLUE, etc.)")
    print("  (Confidence scores shown as percentages)")
    print("  (Detections persist for smoother visualization)")
    print("  (🎯 PRIMARY DETECTION tracks the most frequently detected disease!)")
    print()
    
    # Create fullscreen window
    cv2.namedWindow('AgriScan - Disease Detection', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('AgriScan - Disease Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    try:
        while True:
            # Read frame
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Error: Could not read frame")
                break
            
            # Start timer for FPS
            start_time = time.time()
            
            # Run inference
            results = model(frame, conf=conf_threshold, verbose=False)
            
            # Get current frame detections
            current_detections = []
            current_frame_classes = []
            boxes = results[0].boxes
            
            if boxes is not None and len(boxes) > 0:
                for box in boxes:
                    confidence = float(box.conf[0])
                    if confidence >= conf_threshold:
                        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                        class_id = int(box.cls[0])
                        current_detections.append({
                            'bbox': (x1, y1, x2, y2),
                            'class_id': class_id,
                            'confidence': confidence,
                            'age': 0  # Fresh detection
                        })
                        current_frame_classes.append(class_id)
            
            # Update class history for primary detection tracking
            class_history.append(current_frame_classes)
            if len(class_history) > tracking_window_size:
                class_history.pop(0)
            
            # Update class occurrence counter
            class_occurrence_counter.clear()
            for frame_classes in class_history:
                for cls_id in frame_classes:
                    class_occurrence_counter[cls_id] += 1
            
            # Determine primary detection (most frequent class)
            if class_occurrence_counter:
                primary_detection_class = class_occurrence_counter.most_common(1)[0][0]
                
                # Find the bounding box of primary detection in current frame
                primary_detection_bbox = None
                for det in current_detections:
                    if det['class_id'] == primary_detection_class:
                        primary_detection_bbox = det['bbox']
                        break
            else:
                primary_detection_class = None
                primary_detection_bbox = None
            
            # Add current detections to history
            detection_history.append(current_detections)
            
            # Keep only last N frames
            if len(detection_history) > history_size:
                detection_history.pop(0)
            
            # Merge all detections from history with age-based opacity
            all_detections = []
            for frame_idx, frame_detections in enumerate(detection_history):
                age = len(detection_history) - frame_idx - 1
                for det in frame_detections:
                    det_copy = det.copy()
                    det_copy['age'] = age
                    all_detections.append(det_copy)
            
            # Draw all historical detections
            annotated_frame = frame.copy()
            detection_count = 0
            
            for det in all_detections:
                x1, y1, x2, y2 = det['bbox']
                class_id = det['class_id']
                confidence = det['confidence']
                age = det['age']
                
                # Check if this is the primary detection
                is_primary = (class_id == primary_detection_class and age == 0)
                
                # Calculate opacity based on age (newer = more opaque)
                opacity = max(0.3, 1.0 - (age / history_size))
                
                # Get class name
                class_name = class_names[class_id] if class_id < len(class_names) else f"Class_{class_id}"
                
                # Choose color based on class
                color = COLORS[class_id % len(COLORS)]
                
                # Apply opacity to color
                overlay = annotated_frame.copy()
                
                # Draw bounding box (EXTRA THICK for primary detection)
                box_thickness = 8 if is_primary else 4
                cv2.rectangle(overlay, (x1, y1), (x2, y2), color, box_thickness)
                
                # Add special marker for primary detection
                if is_primary:
                    # Draw "PRIMARY" label at top
                    primary_label = "🎯 PRIMARY DETECTION"
                    cv2.putText(
                        overlay,
                        primary_label,
                        (x1, y1 - 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 255, 0),  # Bright green
                        3,
                        cv2.LINE_AA
                    )
                    
                    # Add glow effect for primary detection
                    cv2.rectangle(overlay, (x1-5, y1-5), (x2+5, y2+5), (0, 255, 0), 3)
                
                # Prepare label with confidence
                label = f"{class_name}: {confidence:.1%}"
                
                # Get text size for background rectangle
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1.0 if is_primary else 0.9
                thickness = 3 if is_primary else 2
                (text_width, text_height), baseline = cv2.getTextSize(label, font, font_scale, thickness)
                
                # Draw background rectangle for text
                cv2.rectangle(
                    overlay,
                    (x1, y1 - text_height - 15),
                    (x1 + text_width + 15, y1),
                    color,
                    -1  # Filled rectangle
                )
                
                # Draw text
                cv2.putText(
                    overlay,
                    label,
                    (x1 + 7, y1 - 7),
                    font,
                    font_scale,
                    (255, 255, 255),  # White text
                    thickness,
                    cv2.LINE_AA
                )
                
                # Blend with original frame using opacity
                cv2.addWeighted(overlay, opacity, annotated_frame, 1 - opacity, 0, annotated_frame)
                
                if age == 0:  # Count only fresh detections
                    detection_count += 1
            
            # Calculate FPS
            inference_time = (time.time() - start_time) * 1000  # ms
            fps = 1000 / inference_time if inference_time > 0 else 0
            fps_list.append(fps)
            
            # Keep only last 30 FPS values for moving average
            if len(fps_list) > 30:
                fps_list.pop(0)
            
            avg_fps = sum(fps_list) / len(fps_list)
            
            # Draw info overlay with larger text for fullscreen
            info_y = 40
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1.2
            
            # Create semi-transparent background for info (larger to fit primary detection info)
            overlay_info = annotated_frame.copy()
            cv2.rectangle(overlay_info, (5, 5), (550, 235), (0, 0, 0), -1)
            cv2.addWeighted(overlay_info, 0.6, annotated_frame, 0.4, 0, annotated_frame)
            
            # FPS
            cv2.putText(
                annotated_frame,
                f"FPS: {avg_fps:.1f}",
                (15, info_y),
                font,
                font_scale,
                (0, 255, 0),
                3,
                cv2.LINE_AA
            )
            
            # Inference time
            cv2.putText(
                annotated_frame,
                f"Time: {inference_time:.1f}ms",
                (15, info_y + 45),
                font,
                font_scale,
                (0, 255, 0),
                3,
                cv2.LINE_AA
            )
            
            # Detections count
            cv2.putText(
                annotated_frame,
                f"Detections: {detection_count}",
                (15, info_y + 90),
                font,
                font_scale,
                (0, 255, 255),
                3,
                cv2.LINE_AA
            )
            
            # Confidence threshold
            cv2.putText(
                annotated_frame,
                f"Conf: {conf_threshold:.2f}",
                (15, info_y + 135),
                font,
                font_scale,
                (255, 255, 0),
                3,
                cv2.LINE_AA
            )
            
            # Primary detection info
            if primary_detection_class is not None:
                primary_class_name = class_names[primary_detection_class] if primary_detection_class < len(class_names) else f"Class_{primary_detection_class}"
                occurrence_count = class_occurrence_counter[primary_detection_class]
                cv2.putText(
                    annotated_frame,
                    f"Primary: {primary_class_name}",
                    (15, info_y + 180),
                    font,
                    font_scale,
                    (0, 255, 0),
                    3,
                    cv2.LINE_AA
                )
            else:
                cv2.putText(
                    annotated_frame,
                    "Primary: None",
                    (15, info_y + 180),
                    font,
                    font_scale,
                    (128, 128, 128),
                    3,
                    cv2.LINE_AA
                )
            
            # Show frame
            cv2.imshow('AgriScan - Disease Detection', annotated_frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q') or key == 27:  # 'q' or ESC
                print("\n👋 Quitting...")
                break
            elif key == ord('f'):
                # Toggle fullscreen
                current_state = cv2.getWindowProperty('AgriScan - Disease Detection', cv2.WND_PROP_FULLSCREEN)
                if current_state == cv2.WINDOW_FULLSCREEN:
                    cv2.setWindowProperty('AgriScan - Disease Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                    print("📐 Windowed mode")
                else:
                    cv2.setWindowProperty('AgriScan - Disease Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    print("🖥️  Fullscreen mode")
            elif key == ord('s'):
                # Save frame
                filename = f"detection_{int(time.time())}.jpg"
                cv2.imwrite(filename, annotated_frame)
                print(f"💾 Saved frame: {filename}")
            elif key == ord('+') or key == ord('='):
                conf_threshold = min(0.95, conf_threshold + 0.05)
                print(f"📊 Confidence threshold: {conf_threshold:.2f}")
            elif key == ord('-') or key == ord('_'):
                conf_threshold = max(0.05, conf_threshold - 0.05)
                print(f"📊 Confidence threshold: {conf_threshold:.2f}")
            
            frame_count += 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        
        # Print statistics
        print("\n" + "="*60)
        print("SESSION STATISTICS")
        print("="*60)
        print(f"  Total frames: {frame_count}")
        print(f"  Average FPS: {avg_fps:.2f}")
        print(f"  Average inference time: {1000/avg_fps:.2f}ms")
        print("="*60)


def test_image_detection(image_path):
    """Test detection on a single image"""
    print("\n" + "="*60)
    print("AGRISCAN - IMAGE DETECTION TEST")
    print("="*60)
    
    # Check if model exists
    if not MODEL_PATH.exists():
        print(f"\n❌ Model not found: {MODEL_PATH}")
        return
    
    # Load model
    print("\n📥 Loading model...")
    model = YOLO(str(MODEL_PATH))
    print(f"✅ Model loaded")
    
    # Load class names
    class_names = load_class_names()
    
    # Load image
    print(f"\n📷 Loading image: {image_path}")
    image = cv2.imread(str(image_path))
    
    if image is None:
        print("❌ Error: Could not load image")
        return
    
    print("✅ Image loaded")
    
    # Run inference
    print("\n🔄 Running detection...")
    start_time = time.time()
    results = model(image, conf=0.5, verbose=False)
    inference_time = (time.time() - start_time) * 1000
    
    # Draw detections
    annotated_image, detection_count = draw_detections(
        image, results, class_names, conf_threshold=0.5
    )
    
    print(f"✅ Detection complete in {inference_time:.2f}ms")
    print(f"📊 Found {detection_count} detections")
    
    # Display results
    print("\n🖼️  Displaying results...")
    cv2.imshow('AgriScan - Detection Results', annotated_image)
    print("  Press any key to close...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save result
    output_path = f"detection_result_{int(time.time())}.jpg"
    cv2.imwrite(output_path, annotated_image)
    print(f"\n💾 Saved result: {output_path}")


def main():
    """Main function"""
    import sys
    
    print("\n" + "="*60)
    print("AGRISCAN - FAST DETECTION WITH BOUNDING BOXES")
    print("="*60)
    print("  Model: YOLOv8n (Lightweight & Fast)")
    print("  Features:")
    print("    ✓ Real-time bounding boxes")
    print("    ✓ Confidence scores displayed")
    print("    ✓ Color-coded by class")
    print("    ✓ FPS counter")
    print("    ✓ Adjustable confidence threshold")
    print("="*60)
    
    # Check if image path provided
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_image_detection(image_path)
    else:
        test_webcam_detection()


if __name__ == "__main__":
    main()
