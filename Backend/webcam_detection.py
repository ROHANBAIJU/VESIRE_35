"""
AgriScan - Live Webcam Detection with AR Overlay
Real-time plant disease detection with AI model + Gemini RAG diagnosis
"""

import cv2
import numpy as np
import requests
import base64
import json
import time
import os
from datetime import datetime
from pathlib import Path
import threading
from queue import Queue
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent / '.env')

# ============================================================================
# Configuration
# ============================================================================

# Backend API
API_BASE_URL = "http://127.0.0.1:5000/api"

# Gemini API - Load from environment variable
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Detection settings
CONFIDENCE_THRESHOLD = 0.5
DETECTION_INTERVAL = 2.0  # Detect every 2 seconds
FRAME_SIZE = (1280, 720)  # Webcam resolution

# UI Colors (BGR format for OpenCV)
COLOR_BOX = (0, 0, 255)  # Red
COLOR_TEXT = (255, 255, 255)  # White
COLOR_BG = (0, 0, 0)  # Black
COLOR_SUCCESS = (0, 255, 0)  # Green
COLOR_WARNING = (0, 165, 255)  # Orange

# ============================================================================
# Initialize Gemini with Model Fallback
# ============================================================================

# Validate API key
if not GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY not found in .env file!")
    print("   Gemini diagnosis will be unavailable.")
    print("   Please add GEMINI_API_KEY to Backend/.env file")
else:
    print(f"✅ Gemini API key loaded from .env file")

genai.configure(api_key=GEMINI_API_KEY)

# Try multiple models in order of preference (current available models)
primary_models = [
    'models/gemini-2.5-flash',
    'models/gemini-2.0-flash',
    'models/gemini-flash-latest',
    'models/gemini-2.5-pro'
]

gemini_model = None
last_error = None

print("\n" + "="*80)
print("🚀 AgriScan - Live Webcam Detection System")
print("="*80)
print(f"📊 Backend API: {API_BASE_URL}")
print(f"🤖 Gemini API: Testing models...")

# Test each model with a simple prompt
for model_name in primary_models:
    try:
        test_model = genai.GenerativeModel(model_name)
        test_response = test_model.generate_content('Return token OK').text
        if test_response:
            gemini_model = test_model
            print(f"✅ Using Gemini model: {model_name}")
            break
    except Exception as e:
        last_error = e
        print(f"⚠️  {model_name} unavailable: {str(e)[:100]}")
        continue

if not gemini_model:
    print(f"❌ All Gemini models failed")
    print("⚠️  Continuing without Gemini diagnosis...")
    gemini_model = None

print(f"📹 Webcam: Initializing...")
print("="*80 + "\n")

# ============================================================================
# Helper Functions
# ============================================================================

def encode_frame_to_base64(frame):
    """Convert frame to base64 for API"""
    _, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{jpg_as_text}"

def detect_disease(frame):
    """Call backend API for disease detection"""
    try:
        # Encode frame
        base64_image = encode_frame_to_base64(frame)
        
        # API request
        payload = {
            "image": base64_image,
            "confidence_threshold": CONFIDENCE_THRESHOLD
        }
        
        response = requests.post(
            f"{API_BASE_URL}/detect",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API Error: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend! Is Flask server running?")
        return None
    except Exception as e:
        print(f"❌ Detection error: {e}")
        return None

def get_gemini_diagnosis_async(disease_name, result_queue):
    """Get disease diagnosis from Gemini RAG (runs in background thread)"""
    try:
        if not gemini_model:
            result_queue.put({
                'disease': disease_name,
                'diagnosis': "⚠️  Gemini diagnosis unavailable (model initialization failed)",
                'success': False
            })
            return
        
        prompt = f"""You are a plant pathology expert. Provide a concise diagnosis for: {disease_name}

Please provide:
1. Brief description (2-3 sentences)
2. Key symptoms (3-4 points)
3. Organic treatment (2-3 recommendations)
4. Chemical treatment (2-3 recommendations)
5. Prevention tips (2-3 points)

Keep it practical and farmer-friendly. Format as clear bullet points."""

        response = gemini_model.generate_content(prompt)
        
        result_queue.put({
            'disease': disease_name,
            'diagnosis': response.text,
            'success': True
        })
        
    except Exception as e:
        result_queue.put({
            'disease': disease_name,
            'diagnosis': f"❌ Diagnosis unavailable: {str(e)}",
            'success': False
        })

def draw_bounding_box(frame, detection, frame_width, frame_height):
    """Draw AR bounding box on frame"""
    box = detection['bounding_box']
    
    # Convert normalized coordinates to pixels
    x = box['x']
    y = box['y']
    width = box['width']
    height = box['height']
    
    # Calculate box corners (center point to top-left)
    x1 = int((x - width/2) * frame_width)
    y1 = int((y - height/2) * frame_height)
    x2 = int((x + width/2) * frame_width)
    y2 = int((y + height/2) * frame_height)
    
    # Ensure coordinates are within frame
    x1 = max(0, min(x1, frame_width))
    y1 = max(0, min(y1, frame_height))
    x2 = max(0, min(x2, frame_width))
    y2 = max(0, min(y2, frame_height))
    
    # Draw box
    cv2.rectangle(frame, (x1, y1), (x2, y2), COLOR_BOX, 3)
    
    # Draw semi-transparent overlay
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), COLOR_BOX, -1)
    cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
    
    # Prepare label text
    class_name = detection['class_name']
    confidence = detection['confidence']
    label = f"{class_name}"
    confidence_text = f"Confidence: {confidence*100:.1f}%"
    
    # Calculate label background size
    (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    (conf_w, conf_h), _ = cv2.getTextSize(confidence_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    
    max_width = max(label_w, conf_w) + 20
    total_height = label_h + conf_h + 20
    
    # Draw label background
    cv2.rectangle(frame, 
                  (x1, y1 - total_height - 10), 
                  (x1 + max_width, y1), 
                  COLOR_BG, -1)
    
    # Draw label text
    cv2.putText(frame, label, 
                (x1 + 5, y1 - conf_h - 15), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 2)
    
    # Draw confidence text
    confidence_color = COLOR_SUCCESS if confidence > 0.7 else COLOR_WARNING
    cv2.putText(frame, confidence_text, 
                (x1 + 5, y1 - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, confidence_color, 1)

def draw_status_panel(frame, status_text, color=COLOR_TEXT):
    """Draw status panel at top of frame"""
    height, width = frame.shape[:2]
    
    # Draw status bar background
    cv2.rectangle(frame, (0, 0), (width, 60), COLOR_BG, -1)
    
    # Draw status text
    cv2.putText(frame, status_text, (10, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

def draw_diagnosis_panel(frame, diagnosis_text):
    """Draw diagnosis panel at bottom of frame"""
    height, width = frame.shape[:2]
    
    # Split diagnosis into lines
    lines = diagnosis_text.split('\n')[:8]  # Max 8 lines
    
    # Calculate panel height
    line_height = 25
    panel_height = len(lines) * line_height + 20
    
    # Draw panel background
    cv2.rectangle(frame, 
                  (0, height - panel_height), 
                  (width, height), 
                  (0, 0, 0), -1)
    
    # Draw diagnosis text
    y_pos = height - panel_height + 20
    for line in lines:
        if len(line) > 100:  # Truncate long lines
            line = line[:97] + "..."
        cv2.putText(frame, line, (10, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        y_pos += line_height

def draw_instructions(frame):
    """Draw usage instructions"""
    height, width = frame.shape[:2]
    
    instructions = [
        "INSTRUCTIONS:",
        "1. Show a plant leaf to the camera",
        "2. Hold steady for 2 seconds",
        "3. Wait for AI detection",
        "4. See diagnosis below",
        "",
        "Press 'Q' to quit | Press 'S' to save screenshot"
    ]
    
    # Draw semi-transparent background
    cv2.rectangle(frame, (10, 80), (400, 80 + len(instructions)*25 + 10), 
                  COLOR_BG, -1)
    
    # Draw instructions
    y_pos = 100
    for instruction in instructions:
        color = COLOR_SUCCESS if instruction.startswith("Press") else COLOR_TEXT
        cv2.putText(frame, instruction, (15, y_pos), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        y_pos += 25

# ============================================================================
# Main Detection Loop
# ============================================================================

def main():
    """Main detection loop with webcam"""
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])
    
    if not cap.isOpened():
        print("❌ Error: Cannot open webcam!")
        return
    
    print("✅ Webcam initialized")
    print("\n" + "="*80)
    print("👀 Show a plant leaf to the camera...")
    print("="*80 + "\n")
    
    # Detection state
    last_detection_time = 0
    current_detections = []
    current_diagnosis = None
    current_disease = None
    status_message = "Ready - Show leaf to camera..."
    status_color = COLOR_SUCCESS
    show_instructions = True
    
    # Async diagnosis state
    diagnosis_queue = Queue()
    diagnosis_thread = None
    diagnosis_pending = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Cannot read frame!")
            break
        
        frame_height, frame_width = frame.shape[:2]
        current_time = time.time()
        
        # Check if diagnosis is ready (non-blocking)
        if not diagnosis_queue.empty():
            result = diagnosis_queue.get()
            if result['success']:
                current_diagnosis = result['diagnosis']
                current_disease = result['disease']
                print(f"✅ Diagnosis received for {result['disease']}")
                print(f"\n{result['diagnosis']}\n")
            else:
                current_diagnosis = result['diagnosis']
            diagnosis_pending = False
        
        # Perform detection at intervals
        if current_time - last_detection_time >= DETECTION_INTERVAL:
            status_message = "🔍 Analyzing image..."
            status_color = COLOR_WARNING
            
            # Draw current status
            display_frame = frame.copy()
            draw_status_panel(display_frame, status_message, status_color)
            if show_instructions:
                draw_instructions(display_frame)
            cv2.imshow('AgriScan - Live Detection', display_frame)
            cv2.waitKey(1)
            
            # Detect diseases
            print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Running detection...")
            result = detect_disease(frame)
            
            if result and result.get('success'):
                detections = result.get('detections', [])
                
                if len(detections) > 0:
                    # Disease detected!
                    show_instructions = False
                    current_detections = detections
                    
                    # Get first detection
                    detection = detections[0]
                    disease_name = detection['class_name']
                    confidence = detection['confidence']
                    
                    print(f"✅ Detected: {disease_name}")
                    print(f"   Confidence: {confidence*100:.1f}%")
                    print(f"   Total detections: {len(detections)}")
                    
                    status_message = f"✅ Detected: {disease_name} ({confidence*100:.1f}%)"
                    status_color = COLOR_SUCCESS
                    
                    # Get diagnosis if disease changed (async - non-blocking)
                    if disease_name != current_disease and not diagnosis_pending:
                        print(f"🤖 Getting diagnosis from Gemini (async)...")
                        diagnosis_pending = True
                        
                        # Start background thread for Gemini diagnosis
                        diagnosis_thread = threading.Thread(
                            target=get_gemini_diagnosis_async,
                            args=(disease_name, diagnosis_queue),
                            daemon=True
                        )
                        diagnosis_thread.start()
                        
                        # Show temporary message
                        current_diagnosis = "🔄 Getting AI diagnosis from Gemini... (this won't freeze the video!)"
                        current_disease = disease_name
                    
                else:
                    # No detections
                    current_detections = []
                    current_diagnosis = None
                    current_disease = None
                    show_instructions = True
                    
                    status_message = "⚠️ No disease detected - Show leaf closer or try different angle"
                    status_color = COLOR_WARNING
                    print("ℹ️  No disease detected in frame")
            
            else:
                # API error
                status_message = "❌ Backend error - Check if Flask server is running"
                status_color = (0, 0, 255)  # Red
                print("❌ Backend API error")
            
            last_detection_time = current_time
        
        # Draw UI
        display_frame = frame.copy()
        
        # Draw bounding boxes
        for detection in current_detections:
            draw_bounding_box(display_frame, detection, frame_width, frame_height)
        
        # Draw status panel
        draw_status_panel(display_frame, status_message, status_color)
        
        # Draw instructions or diagnosis
        if show_instructions:
            draw_instructions(display_frame)
        elif current_diagnosis:
            draw_diagnosis_panel(display_frame, current_diagnosis)
        
        # Show FPS
        cv2.putText(display_frame, f"FPS: {int(cap.get(cv2.CAP_PROP_FPS))}", 
                    (frame_width - 100, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)
        
        # Display frame
        cv2.imshow('AgriScan - Live Detection', display_frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == ord('Q'):
            # Quit
            print("\n👋 Exiting...")
            break
        
        elif key == ord('s') or key == ord('S'):
            # Save screenshot
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"detection_{timestamp}.jpg"
            cv2.imwrite(filename, display_frame)
            print(f"📸 Screenshot saved: {filename}")
            status_message = f"📸 Screenshot saved: {filename}"
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "="*80)
    print("✅ Session ended")
    print("="*80)

# ============================================================================
# Entry Point
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
