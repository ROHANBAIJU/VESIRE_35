"""
Test script to list available Gemini models
"""
import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyDKCnXD1fuM22M0sYpc05DOAAaJmv3mXFo"

genai.configure(api_key=GEMINI_API_KEY)

print("Available Gemini Models:")
print("="*80)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Supported: {model.supported_generation_methods}")
            print()
except Exception as e:
    print(f"Error listing models: {e}")
