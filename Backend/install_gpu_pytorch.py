"""
Install GPU-Enabled PyTorch for Faster Training
================================================

This script will install CUDA-enabled PyTorch to use your NVIDIA GPU for training.

Requirements:
- NVIDIA GPU (GTX 1050 or higher)
- NVIDIA drivers installed
- Windows 10/11

Run this if you want GPU acceleration for training!
"""

import subprocess
import sys

print("=" * 70)
print("🎮 GPU PyTorch Installer for AgriScan AR")
print("=" * 70)

print("\n⚠️  IMPORTANT: This requires an NVIDIA GPU")
print("   Check if you have NVIDIA GPU:")
print("   1. Open Device Manager")
print("   2. Look under 'Display adapters'")
print("   3. Should see 'NVIDIA' in the name")

response = input("\n❓ Do you have an NVIDIA GPU? (yes/no): ").strip().lower()

if response not in ['yes', 'y']:
    print("\n❌ GPU training requires NVIDIA GPU")
    print("   Current CPU training will work, just slower (~2-3 hours)")
    print("   Alternative: Use Google Colab for free GPU training")
    sys.exit(0)

print("\n📦 Installing CUDA-enabled PyTorch...")
print("   This will:")
print("   - Uninstall CPU-only PyTorch")
print("   - Install PyTorch with CUDA 12.1 support")
print("   - Enable GPU acceleration")

response = input("\n❓ Continue? (yes/no): ").strip().lower()

if response not in ['yes', 'y']:
    print("❌ Installation cancelled")
    sys.exit(0)

print("\n🔄 Installing... (this will take 5-10 minutes)")

# Uninstall old torch
print("\n1️⃣ Uninstalling CPU PyTorch...")
subprocess.run([
    sys.executable, "-m", "pip", "uninstall", "-y",
    "torch", "torchvision", "torchaudio"
])

# Install CUDA version
print("\n2️⃣ Installing GPU PyTorch with CUDA 12.1...")
subprocess.run([
    sys.executable, "-m", "pip", "install",
    "torch", "torchvision", "torchaudio",
    "--index-url", "https://download.pytorch.org/whl/cu121"
])

# Verify installation
print("\n✅ Installation complete! Verifying...")

import torch
print("\n🔍 GPU Status:")
print(f"   CUDA Available: {torch.cuda.is_available()}")
print(f"   GPU Count: {torch.cuda.device_count()}")

if torch.cuda.is_available():
    print(f"   GPU Name: {torch.cuda.get_device_name(0)}")
    print("\n🎉 SUCCESS! GPU is ready for training")
    print("   Training will be 10-50x faster!")
    print("\n🚀 Now run: python train_plantdoc_model.py")
else:
    print("\n⚠️  GPU not detected")
    print("   Possible issues:")
    print("   1. No NVIDIA GPU in system")
    print("   2. NVIDIA drivers not installed")
    print("   3. GPU not compatible with CUDA 12.1")
    print("\n💡 Try Google Colab for free GPU:")
    print("   https://colab.research.google.com/")

print("\n" + "=" * 70)
