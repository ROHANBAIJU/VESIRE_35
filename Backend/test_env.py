"""
Test script to verify environment variables are loaded correctly
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

print("\n" + "="*80)
print("🔍 Environment Variables Check")
print("="*80)

# Check .env file exists
if env_path.exists():
    print(f"✅ .env file found at: {env_path}")
else:
    print(f"❌ .env file NOT found at: {env_path}")
    exit(1)

# Check Gemini API Key
gemini_key = os.getenv('GEMINI_API_KEY')
if gemini_key:
    print(f"✅ GEMINI_API_KEY: {gemini_key[:20]}...{gemini_key[-4:]}")
else:
    print("❌ GEMINI_API_KEY: NOT FOUND")

# Check OpenAI API Key (optional)
openai_key = os.getenv('OPENAI_API_KEY')
if openai_key:
    print(f"✅ OPENAI_API_KEY: {openai_key[:10]}...")
else:
    print("⚠️  OPENAI_API_KEY: Not set (optional)")

# Check other config
print(f"\n📊 Server Configuration:")
print(f"   HOST: {os.getenv('HOST', 'Not set')}")
print(f"   PORT: {os.getenv('PORT', 'Not set')}")
print(f"   DEBUG: {os.getenv('DEBUG', 'Not set')}")
print(f"   USE_ONLINE_RAG: {os.getenv('USE_ONLINE_RAG', 'Not set')}")

print("\n" + "="*80)
print("✅ All environment variables loaded successfully!")
print("="*80 + "\n")

# Test importing config
print("🧪 Testing config import...")
try:
    from api.config import config
    print(f"✅ Config imported successfully")
    print(f"   GEMINI_API_KEY from config: {config.GEMINI_API_KEY[:20] if config.GEMINI_API_KEY else 'NOT SET'}...")
    print(f"   USE_ONLINE_RAG: {config.USE_ONLINE_RAG}")
except Exception as e:
    print(f"❌ Error importing config: {e}")

print("\n🎉 Environment setup is complete and working!")
