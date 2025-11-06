"""
Test script to verify multilingual RAG responses
Tests English, Hindi, and Kannada language support
"""
import requests
import json

BASE_URL = "http://10.190.144.95:5000"

def test_language(disease_name, language, language_name):
    """Test RAG response in specific language"""
    print(f"\n{'='*70}")
    print(f"Testing {language_name} ({language}) for: {disease_name}")
    print('='*70)
    
    url = f"{BASE_URL}/api/diagnose/{disease_name}"
    params = {
        'language': language,
        'use_cache': 'false'  # Force online LLM to test language feature
    }
    
    try:
        response = requests.get(url, params=params, timeout=60)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data['success']:
                disease = data['disease']
                source = data['source']
                
                print(f"✅ Source: {source}")
                print(f"\n📝 Name: {disease['name']}")
                print(f"🔬 Scientific: {disease.get('scientific_name', 'N/A')}")
                print(f"\n📖 Description preview:")
                description = disease.get('description', 'N/A')
                print(f"   {description[:200]}..." if len(description) > 200 else f"   {description}")
                
                print(f"\n🔍 First symptom:")
                symptoms = disease.get('symptoms', [])
                if symptoms:
                    print(f"   {symptoms[0]}")
                
                print(f"\n💊 First organic treatment:")
                treatment = disease.get('treatment', {})
                organic = treatment.get('organic', [])
                if organic:
                    print(f"   {organic[0]}")
                
                print(f"\n🌱 First care recommendation:")
                care = disease.get('care_recommendations', [])
                if care:
                    print(f"   {care[0]}")
                
                # Check if response is actually in the requested language
                # Simple heuristic: check for non-ASCII characters for Hindi/Kannada
                has_unicode = any(ord(char) > 127 for char in description)
                
                if language in ['hi', 'kn']:
                    if has_unicode:
                        print(f"\n✅ Response appears to be in native script ({language_name})")
                    else:
                        print(f"\n⚠️  Warning: Response might not be in {language_name} - no native script detected")
                else:
                    print(f"\n✅ Response is in English")
                    
            else:
                print(f"❌ Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    print("\n" + "="*70)
    print("🌐 MULTILINGUAL RAG TEST")
    print("Testing language support for disease diagnosis")
    print("="*70)
    
    # Test disease - using a common one that should work
    disease = "Tomato leaf late blight"
    
    # Test English
    test_language(disease, 'en', 'English')
    
    # Test Hindi
    test_language(disease, 'hi', 'Hindi (हिंदी)')
    
    # Test Kannada
    test_language(disease, 'kn', 'Kannada (ಕನ್ನಡ)')
    
    print("\n" + "="*70)
    print("Test complete!")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
