import json

# Load the multilingual disease knowledge
with open('data/disease_knowledge.json', encoding='utf-8') as f:
    data = json.load(f)

print(f'✅ Total diseases: {len(data)}')

# Count translations
hi_count = sum(1 for d in data.values() if 'translations' in d and 'hi' in d['translations'])
kn_count = sum(1 for d in data.values() if 'translations' in d and 'kn' in d['translations'])

print(f'✅ Hindi translations: {hi_count}/{len(data)}')
print(f'✅ Kannada translations: {kn_count}/{len(data)}')

print(f'\n📝 Sample translations:')
print('='*60)

# Show sample for Tomato Late Blight
sample_key = 'Tomato leaf Late blight'
if sample_key in data:
    sample = data[sample_key]
    print(f'\nDisease: {sample_key}')
    print(f'  EN: {sample.get("name")}')
    if 'translations' in sample:
        if 'hi' in sample['translations']:
            print(f'  HI: {sample["translations"]["hi"]["name"]}')
        if 'kn' in sample['translations']:
            print(f'  KN: {sample["translations"]["kn"]["name"]}')

# Show sample for Wheat Brown Rust
sample_key2 = 'Wheat Brown rust'
if sample_key2 in data:
    sample = data[sample_key2]
    print(f'\nDisease: {sample_key2}')
    print(f'  EN: {sample.get("name")}')
    if 'translations' in sample:
        if 'hi' in sample['translations']:
            print(f'  HI: {sample["translations"]["hi"]["name"]}')
        if 'kn' in sample['translations']:
            print(f'  KN: {sample["translations"]["kn"]["name"]}')

print('\n' + '='*60)
print('🎉 Multilingual dataset verification complete!')
