"""
Quick test for multilingual RAG - tests Hindi response
"""
import requests
import time

print("\n" + "="*70)
print("🌐 Testing Multilingual RAG (Hindi)")
print("="*70)

url = "http://10.190.144.95:5000/api/diagnose/Tomato leaf late blight"
params = {
    'language': 'hi',
    'use_cache': 'false'  # Force fresh response from Gemini
}

print(f"\n📡 Requesting diagnosis in Hindi...")
print(f"   URL: {url}")
print(f"   Language: Hindi (hi)")
print(f"   Waiting for Gemini API response...\n")

try:
    start = time.time()
    response = requests.get(url, params=params, timeout=120)
    elapsed = time.time() - start
    
    print(f"⏱️  Response time: {elapsed:.1f}s")
    print(f"📊 Status: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        
        if data['success']:
            disease = data['disease']
            source = data['source']
            
            print(f"✅ Success!")
            print(f"📌 Source: {source}")
            print(f"\n" + "-"*70)
            
            print(f"\n🏷️  Name: {disease['name']}")
            print(f"🔬 Scientific: {disease.get('scientific_name', 'N/A')}")
            
            print(f"\n📖 Description (Hindi):")
            description = disease.get('description', 'N/A')
            print(f"   {description}\n")
            
            print(f"🔍 Symptoms (Hindi):")
            symptoms = disease.get('symptoms', [])
            for i, symptom in enumerate(symptoms[:3], 1):
                print(f"   {i}. {symptom}")
            
            print(f"\n💊 Organic Treatment (Hindi):")
            treatment = disease.get('treatment', {})
            organic = treatment.get('organic', [])
            for i, method in enumerate(organic[:3], 1):
                print(f"   {i}. {method}")
            
            print(f"\n🌱 Care Recommendations (Hindi):")
            care = disease.get('care_recommendations', [])
            for i, rec in enumerate(care[:4], 1):
                print(f"   {i}. {rec}")
            
            # Check for Hindi script
            has_devanagari = any(
                '\u0900' <= char <= '\u097F' 
                for char in description
            )
            
            print(f"\n" + "-"*70)
            if has_devanagari:
                print("✅ MULTILINGUAL FEATURE WORKING! Response contains Hindi script (Devanagari)")
            else:
                print("⚠️  Warning: No Hindi script detected - check if Gemini API is configured")
            print("="*70 + "\n")
            
        else:
            print(f"❌ Error: {data.get('error')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Exception: {e}")
    print("\nMake sure:")
    print("1. Backend server is running (python app.py)")
    print("2. Gemini API key is configured in .env file")
    print("3. Network connection is available")
