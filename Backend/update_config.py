"""
AgriScan - Update Configuration for New Model
Updates the Flask configuration to use the newly trained combined model
"""

from pathlib import Path
import shutil

# Paths
BASE_DIR = Path(__file__).parent
API_DIR = BASE_DIR / "api"
CONFIG_FILE = API_DIR / "config.py"
MODEL_DIR = BASE_DIR / "models" / "agriscan_combined" / "weights"
DATASET_DIR = BASE_DIR / "unified_dataset"


def update_config():
    """Update config.py with new model paths"""
    print("\n" + "="*60)
    print("UPDATING FLASK CONFIGURATION")
    print("="*60)
    
    # Check if model exists
    model_path = MODEL_DIR / "best.pt"
    if not model_path.exists():
        print(f"\n❌ Model not found: {model_path}")
        return False
    
    # Check if labels exist
    labels_src = DATASET_DIR / "labels.txt"
    if not labels_src.exists():
        print(f"\n❌ Labels not found: {labels_src}")
        return False
    
    # Copy labels to api directory
    labels_dst = API_DIR / "labels.txt"
    print(f"\n📋 Copying labels to: {labels_dst}")
    shutil.copy2(labels_src, labels_dst)
    print("  ✅ Labels copied")
    
    # Read current config
    with open(CONFIG_FILE, 'r') as f:
        config_content = f.read()
    
    # Update MODEL_PATH
    old_model_line = "    MODEL_PATH = MODELS_DIR / 'agriscan_plantdoc' / 'weights' / 'best.pt'"
    new_model_line = "    MODEL_PATH = MODELS_DIR / 'agriscan_combined' / 'weights' / 'best.pt'"
    
    if old_model_line in config_content:
        config_content = config_content.replace(old_model_line, new_model_line)
        print(f"\n✏️  Updated MODEL_PATH")
    else:
        print("\n⚠️  Could not find MODEL_PATH line to update")
        print("  Please manually update config.py:")
        print(f"    MODEL_PATH = MODELS_DIR / 'agriscan_combined' / 'weights' / 'best.pt'")
    
    # Update LABELS_PATH
    old_labels_line = "    LABELS_PATH = BASE_DIR / 'yolo_dataset' / 'labels.txt'"
    new_labels_line = "    LABELS_PATH = API_DIR / 'labels.txt'"
    
    if old_labels_line in config_content:
        # Need to add API_DIR first
        if "API_DIR = " not in config_content:
            # Add API_DIR definition after BASE_DIR
            base_dir_line = "    BASE_DIR = Path(__file__).parent.parent"
            if base_dir_line in config_content:
                config_content = config_content.replace(
                    base_dir_line,
                    base_dir_line + "\n    API_DIR = Path(__file__).parent"
                )
        
        config_content = config_content.replace(old_labels_line, new_labels_line)
        print(f"✏️  Updated LABELS_PATH")
    else:
        print("\n⚠️  Could not find LABELS_PATH line to update")
        print("  Please manually update config.py:")
        print(f"    LABELS_PATH = API_DIR / 'labels.txt'")
    
    # Write updated config
    with open(CONFIG_FILE, 'w') as f:
        f.write(config_content)
    
    print("\n✅ Configuration updated successfully!")
    
    # Print model info
    with open(labels_dst, 'r') as f:
        num_classes = len(f.readlines())
    
    print("\n" + "="*60)
    print("NEW MODEL CONFIGURATION")
    print("="*60)
    print(f"  Model: {model_path}")
    print(f"  Labels: {labels_dst}")
    print(f"  Classes: {num_classes}")
    print("="*60)
    
    return True


def verify_setup():
    """Verify that everything is set up correctly"""
    print("\n" + "="*60)
    print("VERIFYING SETUP")
    print("="*60)
    
    checks = []
    
    # Check model
    model_path = MODEL_DIR / "best.pt"
    if model_path.exists():
        print(f"  ✅ Model exists: {model_path}")
        checks.append(True)
    else:
        print(f"  ❌ Model missing: {model_path}")
        checks.append(False)
    
    # Check labels
    labels_path = API_DIR / "labels.txt"
    if labels_path.exists():
        print(f"  ✅ Labels exist: {labels_path}")
        checks.append(True)
    else:
        print(f"  ❌ Labels missing: {labels_path}")
        checks.append(False)
    
    # Check config
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            content = f.read()
            if 'agriscan_combined' in content:
                print(f"  ✅ Config updated: {CONFIG_FILE}")
                checks.append(True)
            else:
                print(f"  ⚠️  Config may need manual update: {CONFIG_FILE}")
                checks.append(False)
    else:
        print(f"  ❌ Config missing: {CONFIG_FILE}")
        checks.append(False)
    
    print("="*60)
    
    return all(checks)


def main():
    """Main update pipeline"""
    print("\n" + "="*60)
    print("AGRISCAN - CONFIGURATION UPDATE")
    print("="*60)
    
    # Update config
    success = update_config()
    
    if success:
        # Verify setup
        if verify_setup():
            print("\n🎉 Configuration update complete!")
            print("\n  Next steps:")
            print("    1. Restart Flask server")
            print("    2. Test detection with: python test_combined_model.py")
            print("    3. Try the API with: python test_api.py")
        else:
            print("\n⚠️  Some verification checks failed")
            print("  Please review the errors above")
    else:
        print("\n❌ Configuration update failed")
        print("  Please check the errors above")


if __name__ == "__main__":
    main()
