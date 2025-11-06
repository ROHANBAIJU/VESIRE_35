"""
Export trained YOLOv8 model to ONNX format for Flutter on-device inference
ONNX is more compatible and better supported than TFLite for YOLOv8
"""

from ultralytics import YOLO
from pathlib import Path
import shutil

def export_model_to_onnx():
    """Export the trained model to TFLite format"""
    
    print("\n" + "="*70)
    print("🔄 EXPORTING MODEL TO ONNX FOR FLUTTER")
    print("="*70)
    print("   ONNX format is better supported and faster for YOLOv8 on mobile")
    print("   Can use with onnxruntime_flutter or pytorch_mobile")
    
    # Paths
    model_path = Path("models/agriscan_combined/weights/best.pt")
    output_dir = Path("models/onnx_export")
    
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        return False
    
    print(f"\n📥 Loading model: {model_path}")
    model = YOLO(str(model_path))
    
    # Create output directory
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print(f"\n🔄 Exporting to ONNX format...")
    print("   This is much simpler and more reliable than TFLite!")
    
    try:
        # Export to ONNX (no extra dependencies needed!)
        export_path = model.export(
            format='onnx',
            imgsz=640,
            simplify=True,  # Simplify for better mobile performance
            opset=12  # ONNX opset version (12 is widely supported)
        )
        
        print(f"\n✅ ONNX export successful!")
        print(f"   Exported model: {export_path}")
        
        # Copy to output directory with clean name
        onnx_file = Path(export_path)
        if onnx_file.exists():
            dest_file = output_dir / "agriscan_model.onnx"
            shutil.copy(onnx_file, dest_file)
            print(f"   Copied to: {dest_file}")
            
            # Get file size
            size_mb = dest_file.stat().st_size / (1024 * 1024)
            print(f"   File size: {size_mb:.2f} MB")
        
        # Also export labels
        labels_file = Path("api/labels.txt")
        if labels_file.exists():
            dest_labels = output_dir / "labels.txt"
            shutil.copy(labels_file, dest_labels)
            print(f"   Labels copied to: {dest_labels}")
        
        print("\n" + "="*70)
        print("📱 FLUTTER INTEGRATION READY")
        print("="*70)
        print(f"\n✅ Files for Flutter:")
        print(f"   1. Model: {output_dir}/agriscan_model.onnx")
        print(f"   2. Labels: {output_dir}/labels.txt")
        print(f"\n📋 Flutter Integration Options:")
        print(f"   Option 1 (Recommended): Use onnxruntime_flutter")
        print(f"      - Fast and reliable")
        print(f"      - Add: onnxruntime: ^1.18.0")
        print(f"   Option 2: Use pytorch_mobile")
        print(f"      - Official PyTorch support")
        print(f"      - Add: pytorch_mobile: ^0.2.2")
        print(f"\n📋 Next steps:")
        print(f"   1. Copy both files to: Frontend/vesire/assets/models/")
        print(f"   2. Add to pubspec.yaml assets section")
        print(f"   3. Install onnxruntime plugin")
        print(f"   4. Implement on-device detection service")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ONNX export failed: {e}")
        print("\n💡 This shouldn't happen - ONNX export is usually reliable")
        return False


if __name__ == "__main__":
    success = export_model_to_onnx()
    
    if success:
        print("\n🎉 Export complete! Ready for Flutter integration.")
    else:
        print("\n⚠️  Export failed. Check error messages above.")
