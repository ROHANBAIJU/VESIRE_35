"""
Test script for Primary Detection Integration with RAG
Tests the new /api/detect endpoint with primary detection tracking
"""

import requests
import base64
import json
from pathlib import Path

# API Configuration
API_URL = "http://localhost:5000"

def test_primary_detection_single_image():
    """Test single image detection with primary detection and auto-diagnosis"""
    print("\n" + "="*70)
    print("TEST 1: Single Image Detection with Primary Detection + RAG")
    print("="*70)
    
    # Load test image (use any image from test dataset)
    test_image_path = Path("DATASET/RICE DATASET/test/images/DSC_0008.JPG")
    
    if not test_image_path.exists():
        print(f"❌ Test image not found: {test_image_path}")
        return
    
    # Read and encode image
    with open(test_image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Prepare request
    payload = {
        "image": image_data,
        "confidence_threshold": 0.5,
        "track_primary": True,
        "auto_diagnose": True,
        "language": "en"
    }
    
    print(f"\n📤 Sending detection request...")
    print(f"   Image: {test_image_path.name}")
    print(f"   Tracking: Enabled")
    print(f"   Auto-diagnose: Enabled")
    
    # Send request
    response = requests.post(
        f"{API_URL}/api/detect",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n✅ Detection successful!")
        print(f"   Detection ID: {result.get('detection_id')}")
        print(f"   Total detections: {len(result['detections'])}")
        
        # Show all detections
        print(f"\n📊 All Detections:")
        for i, det in enumerate(result['detections']):
            print(f"   [{i+1}] {det['class_name']}: {det['confidence']:.2%}")
        
        # Show primary detection
        primary = result.get('primary_detection')
        if primary:
            print(f"\n🎯 PRIMARY DETECTION:")
            print(f"   Disease: {primary['class_name']}")
            print(f"   Confidence: {primary['confidence']:.2%}")
            
            stats = primary.get('tracking_stats', {})
            if stats:
                print(f"   Tracking Stats:")
                print(f"      Occurrences: {stats['occurrence_count']}/{stats['total_frames']} frames")
                print(f"      Percentage: {stats['occurrence_percentage']}%")
                print(f"      Stable: {stats['is_stable']}")
        
        # Show diagnosis
        diagnosis = result.get('diagnosis')
        if diagnosis:
            print(f"\n🔍 DIAGNOSIS (from RAG):")
            print(f"   Disease: {diagnosis['name']}")
            print(f"   Scientific Name: {diagnosis.get('scientific_name', 'N/A')}")
            print(f"   Severity: {diagnosis.get('severity', 'N/A')}")
            print(f"   Description: {diagnosis.get('description', 'N/A')[:100]}...")
            print(f"   Symptoms: {len(diagnosis.get('symptoms', []))} listed")
            print(f"   Treatment Options: {len(diagnosis.get('treatment', {}).get('organic', []))} organic methods")
        else:
            print(f"\n⚠️  No diagnosis available")
        
        # Show timing
        timing = result.get('timing', {})
        print(f"\n⏱️  Timing:")
        print(f"   Inference: {timing.get('inference', 0)*1000:.2f}ms")
        print(f"   Total: {timing.get('total', 0)*1000:.2f}ms")
        
    else:
        print(f"\n❌ Detection failed!")
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.text}")


def test_continuous_detection():
    """Test continuous detection endpoint (simulates multiple frames)"""
    print("\n" + "="*70)
    print("TEST 2: Continuous Detection (Simulating Real-time Detection)")
    print("="*70)
    
    # Use multiple images to simulate continuous detection
    test_images = list(Path("DATASET/RICE DATASET/test/images").glob("*.JPG"))[:5]
    
    if len(test_images) < 3:
        print("❌ Not enough test images")
        return
    
    print(f"\n📹 Simulating continuous detection with {len(test_images)} frames...")
    
    # Reset tracking first
    print("\n🔄 Resetting tracking history...")
    reset_response = requests.post(f"{API_URL}/api/detect/reset-tracking")
    if reset_response.status_code == 200:
        print("✅ Tracking reset successful")
    
    # Send multiple frames
    for i, image_path in enumerate(test_images):
        print(f"\n📸 Frame {i+1}/{len(test_images)}: {image_path.name}")
        
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Send to continuous detection endpoint
        payload = {
            "image": image_data,
            "confidence_threshold": 0.5,
            "language": "en",
            "min_stability": 3
        }
        
        response = requests.post(
            f"{API_URL}/api/detect/continuous",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            primary = result.get('primary_detection')
            is_stable = result.get('is_stable', False)
            
            print(f"   Detections: {len(result['detections'])}")
            
            if primary:
                stats = primary.get('tracking_stats', {})
                print(f"   Primary: {primary['class_name']} ({primary['confidence']:.1%})")
                print(f"   Tracking: {stats['occurrence_count']} occurrences, {stats['occurrence_percentage']}%")
                print(f"   Stable: {'✅ YES' if is_stable else '❌ No'}")
                
                if is_stable and result.get('diagnosis'):
                    print(f"   🔍 Diagnosis available: {result['diagnosis']['name']}")
        else:
            print(f"   ❌ Failed: {response.status_code}")


def test_info_endpoint():
    """Test API info endpoint to verify model status"""
    print("\n" + "="*70)
    print("TEST 3: API Info & Model Status")
    print("="*70)
    
    response = requests.get(f"{API_URL}/api/info")
    
    if response.status_code == 200:
        info = response.json()
        
        print(f"\n✅ API Information:")
        print(f"   Name: {info['name']}")
        print(f"   Version: {info['version']}")
        
        model_info = info.get('model_info', {})
        if model_info.get('loaded'):
            print(f"\n📊 Model Status:")
            print(f"   Loaded: ✅")
            print(f"   Model Path: {model_info['model_path']}")
            print(f"   Classes: {model_info['num_classes']}")
            print(f"   Confidence Threshold: {model_info['confidence_threshold']}")
        else:
            print(f"\n⚠️  Model not loaded!")
    else:
        print(f"❌ Failed to get API info: {response.status_code}")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 PRIMARY DETECTION + RAG INTEGRATION TESTS")
    print("="*70)
    print(f"API URL: {API_URL}")
    print("="*70)
    
    try:
        # Check if server is running
        response = requests.get(f"{API_URL}/api/health", timeout=2)
        if response.status_code == 200:
            print("✅ Flask server is running")
        else:
            print("⚠️  Server responded but health check failed")
    except requests.exceptions.ConnectionError:
        print("❌ Flask server is not running!")
        print("   Please start the server with: python api/app.py")
        return
    except requests.exceptions.Timeout:
        print("❌ Server connection timeout!")
        return
    
    # Run tests
    test_info_endpoint()
    test_primary_detection_single_image()
    test_continuous_detection()
    
    print("\n" + "="*70)
    print("🎉 All tests completed!")
    print("="*70)


if __name__ == "__main__":
    main()
