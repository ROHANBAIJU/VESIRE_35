import json

# Complete disease knowledge for all 34 disease classes detected by the model
disease_data = {
    "Apple leaf": {
        "name": "Healthy Apple Leaf",
        "scientific_name": "Malus domestica",
        "description": "This is a healthy apple leaf showing no signs of disease or pest damage.",
        "symptoms": ["Vibrant green color", "No spots or lesions", "Proper leaf structure"],
        "treatment": {
            "organic": ["No treatment needed", "Continue regular care"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Maintain proper spacing", "Regular pruning"]
        },
        "prevention": ["Continue good practices", "Regular inspection"],
        "severity": "none",
        "affected_plants": ["Apple"]
    },
    "Apple rust leaf": {
        "name": "Apple Rust Leaf",
        "scientific_name": "Gymnosporangium juniperi-virginianae",
        "description": "Cedar-apple rust causes distinctive orange spots on apple leaves.",
        "symptoms": ["Bright orange spots", "Tube-like projections on leaf undersides", "Premature leaf drop"],
        "treatment": {
            "organic": ["Remove nearby cedar trees", "Apply sulfur fungicides", "Use neem oil"],
            "chemical": ["Apply myclobutanil", "Use propiconazole"],
            "cultural": ["Plant resistant varieties", "Improve air circulation"]
        },
        "prevention": ["Choose resistant cultivars", "Avoid planting near cedar"],
        "severity": "medium",
        "affected_plants": ["Apple", "Cedar"]
    },
    "Apple Scab Leaf": {
        "name": "Apple Scab Leaf",
        "scientific_name": "Venturia inaequalis",
        "description": "Apple scab is one of the most serious diseases of apple trees.",
        "symptoms": ["Olive-green to brown velvety spots", "Leaves curl and fall prematurely", "Scabby lesions on fruit"],
        "treatment": {
            "organic": ["Apply sulfur sprays", "Use copper fungicides", "Remove fallen leaves"],
            "chemical": ["Apply captan or mancozeb", "Use myclobutanil"],
            "cultural": ["Prune for air circulation", "Rake fallen leaves"]
        },
        "prevention": ["Plant resistant varieties", "Begin preventive sprays at bud break"],
        "severity": "high",
        "affected_plants": ["Apple", "Pear"]
    },
    "Bell_pepper leaf": {
        "name": "Healthy Bell Pepper Leaf",
        "scientific_name": "Capsicum annuum",
        "description": "A healthy bell pepper leaf with vibrant green coloration.",
        "symptoms": ["Deep green color", "Smooth surface", "No spots or discoloration"],
        "treatment": {
            "organic": ["No treatment needed", "Continue balanced fertilization"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Proper spacing", "Water at base"]
        },
        "prevention": ["Maintain healthy conditions", "Regular inspection"],
        "severity": "none",
        "affected_plants": ["Bell Pepper"]
    },
    "Bell_pepper leaf spot": {
        "name": "Bell Pepper Leaf Spot",
        "scientific_name": "Xanthomonas campestris pv. vesicatoria",
        "description": "Bacterial leaf spot causes leaf drop and reduced fruit quality.",
        "symptoms": ["Small dark brown spots with yellow halos", "Leaves yellow and drop", "Raised spots on fruits"],
        "treatment": {
            "organic": ["Apply copper bactericides", "Remove infected plants", "Use hydrogen peroxide spray"],
            "chemical": ["Apply copper hydroxide", "Use copper sulfate"],
            "cultural": ["Remove infected parts", "Avoid overhead watering"]
        },
        "prevention": ["Use disease-free seeds", "Rotate crops 3 years minimum"],
        "severity": "medium",
        "affected_plants": ["Bell pepper", "Tomato"]
    },
    "Blueberry leaf": {
        "name": "Healthy Blueberry Leaf",
        "scientific_name": "Vaccinium spp.",
        "description": "A healthy blueberry leaf with proper color.",
        "symptoms": ["Rich green color", "Smooth surface", "No spots"],
        "treatment": {
            "organic": ["No treatment needed", "Maintain acidic soil"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Maintain mulch", "Ensure consistent moisture"]
        },
        "prevention": ["Maintain soil acidity", "Good drainage"],
        "severity": "none",
        "affected_plants": ["Blueberry"]
    },
    "Cherry leaf": {
        "name": "Healthy Cherry Leaf",
        "scientific_name": "Prunus avium",
        "description": "A healthy cherry leaf with normal coloration.",
        "symptoms": ["Bright green color", "No spots", "Proper structure"],
        "treatment": {
            "organic": ["No treatment needed", "Continue care"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Proper pruning", "Good air circulation"]
        },
        "prevention": ["Maintain tree health", "Regular monitoring"],
        "severity": "none",
        "affected_plants": ["Cherry"]
    },
    "Corn Gray leaf spot": {
        "name": "Corn Gray Leaf Spot",
        "scientific_name": "Cercospora zeae-maydis",
        "description": "Gray leaf spot causes rectangular lesions on corn leaves.",
        "symptoms": ["Rectangular gray-tan lesions", "Lesions parallel to veins", "Premature leaf death"],
        "treatment": {
            "organic": ["Remove infected leaves", "Apply copper fungicides"],
            "chemical": ["Apply azoxystrobin", "Use triazole fungicides"],
            "cultural": ["Plant resistant hybrids", "Rotate crops"]
        },
        "prevention": ["Choose resistant hybrids", "Bury crop debris"],
        "severity": "medium",
        "affected_plants": ["Corn"]
    },
    "Corn leaf blight": {
        "name": "Corn Leaf Blight",
        "scientific_name": "Exserohilum turcicum",
        "description": "Northern corn leaf blight reduces yield significantly.",
        "symptoms": ["Long elliptical gray-green lesions", "Lesions merge on leaves", "Premature leaf death"],
        "treatment": {
            "organic": ["Apply sulfur fungicides", "Use copper fungicides"],
            "chemical": ["Apply azoxystrobin", "Use propiconazole"],
            "cultural": ["Plant resistant hybrids", "Bury crop residue"]
        },
        "prevention": ["Choose resistant varieties", "Crop rotation"],
        "severity": "medium",
        "affected_plants": ["Corn"]
    },
    "Corn rust leaf": {
        "name": "Corn Rust Leaf",
        "scientific_name": "Puccinia sorghi",
        "description": "Common rust produces pustules on corn leaves.",
        "symptoms": ["Small reddish-brown pustules", "Pustules on both surfaces", "Yellowing"],
        "treatment": {
            "organic": ["Apply sulfur fungicides", "Use neem oil"],
            "chemical": ["Apply propiconazole", "Use strobilurin fungicides"],
            "cultural": ["Plant resistant hybrids", "Adequate spacing"]
        },
        "prevention": ["Choose resistant varieties", "Monitor regularly"],
        "severity": "low",
        "affected_plants": ["Corn"]
    },
    "grape leaf": {
        "name": "Healthy Grape Leaf",
        "scientific_name": "Vitis vinifera",
        "description": "A healthy grape leaf with proper color.",
        "symptoms": ["Vibrant green", "No spots", "Proper lobed structure"],
        "treatment": {
            "organic": ["No treatment needed", "Continue care"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Proper training", "Good air circulation"]
        },
        "prevention": ["Maintain vine health", "Regular monitoring"],
        "severity": "none",
        "affected_plants": ["Grape"]
    },
    "grape leaf black rot": {
        "name": "Grape Leaf Black Rot",
        "scientific_name": "Guignardia bidwellii",
        "description": "Black rot is one of the most serious grape diseases.",
        "symptoms": ["Circular reddish-brown spots", "Tan centers with dark margins", "Black pycnidia in centers", "Berries shrivel into mummies"],
        "treatment": {
            "organic": ["Apply copper fungicides", "Use sulfur sprays", "Remove infected parts"],
            "chemical": ["Apply mancozeb", "Use myclobutanil", "Apply chlorothalonil"],
            "cultural": ["Prune for air circulation", "Remove infected leaves"]
        },
        "prevention": ["Remove mummified berries", "Apply dormant copper sprays", "Monitor weather"],
        "severity": "high",
        "affected_plants": ["Grape"]
    },
    "Peach leaf": {
        "name": "Healthy Peach Leaf",
        "scientific_name": "Prunus persica",
        "description": "A healthy peach leaf with normal coloration.",
        "symptoms": ["Dark green color", "Smooth surface", "No curling"],
        "treatment": {
            "organic": ["No treatment needed", "Continue care"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Proper pruning", "Remove fallen leaves"]
        },
        "prevention": ["Maintain tree health", "Regular inspection"],
        "severity": "none",
        "affected_plants": ["Peach"]
    },
    "Potato leaf": {
        "name": "Healthy Potato Leaf",
        "scientific_name": "Solanum tuberosum",
        "description": "A healthy potato leaf with normal green color.",
        "symptoms": ["Rich green color", "No spots", "Proper compound structure"],
        "treatment": {
            "organic": ["No treatment needed", "Continue care"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Hill soil", "Consistent moisture"]
        },
        "prevention": ["Use certified seed", "Crop rotation"],
        "severity": "none",
        "affected_plants": ["Potato"]
    },
    "Potato leaf early blight": {
        "name": "Potato Leaf Early Blight",
        "scientific_name": "Alternaria solani",
        "description": "Early blight causes premature defoliation in potatoes.",
        "symptoms": ["Dark brown spots with concentric rings", "Yellow halo", "Leaves die from bottom up"],
        "treatment": {
            "organic": ["Apply copper fungicides", "Use sulfur", "Remove infected foliage"],
            "chemical": ["Apply mancozeb", "Use chlorothalonil", "Apply azoxystrobin"],
            "cultural": ["Hill soil", "Mulch", "Space plants"]
        },
        "prevention": ["Use certified seed", "Rotate crops 3-4 years", "Destroy residue"],
        "severity": "medium",
        "affected_plants": ["Potato"]
    },
    "Potato leaf late blight": {
        "name": "Potato Leaf Late Blight",
        "scientific_name": "Phytophthora infestans",
        "description": "Late blight is the most devastating potato disease.",
        "symptoms": ["Water-soaked spots turn brown-black", "White mold on undersides", "Rapid foliage death", "Tuber rot"],
        "treatment": {
            "organic": ["Apply copper immediately", "Remove and burn infected plants"],
            "chemical": ["Apply chlorothalonil", "Use metalaxyl", "Apply dimethomorph"],
            "cultural": ["Destroy volunteers", "Hill soil high", "Avoid overhead watering"]
        },
        "prevention": ["Plant resistant varieties", "Monitor weather", "Spray before rain"],
        "severity": "high",
        "affected_plants": ["Potato", "Tomato"]
    },
    "Raspberry leaf": {
        "name": "Healthy Raspberry Leaf",
        "scientific_name": "Rubus idaeus",
        "description": "A healthy raspberry leaf with proper color.",
        "symptoms": ["Green with silvery undersides", "Compound leaves", "No spots"],
        "treatment": {
            "organic": ["No treatment needed", "Continue care"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Proper pruning", "Remove old canes"]
        },
        "prevention": ["Good air circulation", "Regular inspection"],
        "severity": "none",
        "affected_plants": ["Raspberry"]
    },
    "Soyabean leaf": {
        "name": "Healthy Soybean Leaf",
        "scientific_name": "Glycine max",
        "description": "A healthy soybean leaf with proper trifoliate structure.",
        "symptoms": ["Dark green color", "Trifoliate structure", "No spots"],
        "treatment": {
            "organic": ["No treatment needed", "Continue care"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Proper spacing", "Good weed control"]
        },
        "prevention": ["Use quality seed", "Crop rotation"],
        "severity": "none",
        "affected_plants": ["Soybean"]
    },
    "Squash Powdery mildew leaf": {
        "name": "Squash Powdery Mildew",
        "scientific_name": "Podosphaera xanthii",
        "description": "Powdery mildew appears as white powdery spots on leaves.",
        "symptoms": ["White powdery spots", "Spots merge to cover leaf", "Yellowing", "Premature death"],
        "treatment": {
            "organic": ["Apply sulfur fungicides", "Use baking soda spray", "Apply neem oil", "Milk spray"],
            "chemical": ["Apply myclobutanil", "Use potassium bicarbonate"],
            "cultural": ["Improve air circulation", "Avoid overhead watering"]
        },
        "prevention": ["Plant resistant varieties", "Good air circulation", "Water at base"],
        "severity": "medium",
        "affected_plants": ["Squash", "Cucumber", "Pumpkin"]
    },
    "Strawberry leaf": {
        "name": "Healthy Strawberry Leaf",
        "scientific_name": "Fragaria × ananassa",
        "description": "A healthy strawberry leaf with proper trifoliate structure.",
        "symptoms": ["Bright green color", "Trifoliate structure", "No spots"],
        "treatment": {
            "organic": ["No treatment needed", "Continue care"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Remove old leaves", "Maintain mulch"]
        },
        "prevention": ["Plant disease-free stock", "Good air circulation"],
        "severity": "none",
        "affected_plants": ["Strawberry"]
    },
    "Tomato Early blight leaf": {
        "name": "Tomato Early Blight",
        "scientific_name": "Alternaria solani",
        "description": "Early blight causes yield loss in tomatoes.",
        "symptoms": ["Dark brown spots with concentric rings", "Yellowing around spots", "Leaf drop from bottom", "Stem lesions"],
        "treatment": {
            "organic": ["Apply copper fungicides", "Use compost tea", "Remove infected leaves"],
            "chemical": ["Apply chlorothalonil", "Use mancozeb", "Apply azoxystrobin"],
            "cultural": ["Mulch plants", "Space adequately", "Water at base"]
        },
        "prevention": ["Disease-free transplants", "Rotate crops 3 years", "Remove debris"],
        "severity": "medium",
        "affected_plants": ["Tomato"]
    },
    "Tomato leaf": {
        "name": "Healthy Tomato Leaf",
        "scientific_name": "Solanum lycopersicum",
        "description": "A healthy tomato leaf with normal green color.",
        "symptoms": ["Rich green color", "Compound leaves", "No spots"],
        "treatment": {
            "organic": ["No treatment needed", "Continue care"],
            "chemical": ["No chemical treatment required"],
            "cultural": ["Stake and prune", "Water at base"]
        },
        "prevention": ["Use disease-free transplants", "Crop rotation"],
        "severity": "none",
        "affected_plants": ["Tomato"]
    },
    "Tomato leaf bacterial spot": {
        "name": "Tomato Bacterial Spot",
        "scientific_name": "Xanthomonas spp.",
        "description": "Bacterial spot affects leaves, stems, and fruits.",
        "symptoms": ["Small dark brown spots with yellow halos", "Greasy appearance", "Leaves yellow and drop", "Raised fruit spots"],
        "treatment": {
            "organic": ["Apply copper bactericides", "Remove infected plants", "Use hydrogen peroxide"],
            "chemical": ["Apply copper hydroxide", "Use copper sulfate", "Apply streptomycin"],
            "cultural": ["Remove infected parts", "Avoid overhead watering", "Disinfect tools"]
        },
        "prevention": ["Disease-free seeds", "Plant resistant varieties", "3-year rotation"],
        "severity": "medium",
        "affected_plants": ["Tomato", "Pepper"]
    },
    "Tomato leaf late blight": {
        "name": "Tomato Late Blight",
        "scientific_name": "Phytophthora infestans",
        "description": "Late blight can rapidly destroy entire tomato crops.",
        "symptoms": ["Dark brown to purplish-black spots", "White fuzzy growth on undersides", "Rapid yellowing and death", "Dark fruit spots"],
        "treatment": {
            "organic": ["Apply copper fungicides", "Remove infected parts immediately", "Use baking soda spray"],
            "chemical": ["Apply chlorothalonil", "Use mancozeb", "Apply metalaxyl"],
            "cultural": ["Improve air circulation", "Water at base", "Remove weeds"]
        },
        "prevention": ["Plant resistant varieties", "Avoid planting near potatoes", "Apply mulch", "Monitor weather"],
        "severity": "high",
        "affected_plants": ["Tomato", "Potato"]
    },
    "Tomato leaf mosaic virus": {
        "name": "Tomato Mosaic Virus",
        "scientific_name": "Tomato mosaic virus (ToMV)",
        "description": "Tomato mosaic virus causes mottled patterns on leaves.",
        "symptoms": ["Mottled light and dark green pattern", "Distorted fernlike leaves", "Stunted growth", "Yellow fruit streaking"],
        "treatment": {
            "organic": ["Remove infected plants immediately", "Disinfect tools with bleach", "Wash hands", "No cure available"],
            "chemical": ["No chemical treatment for viruses", "Control aphid vectors"],
            "cultural": ["Remove infected plants", "Disinfect equipment", "Control insects"]
        },
        "prevention": ["Use virus-free seeds", "Plant resistant varieties", "Wash hands", "Disinfect tools"],
        "severity": "high",
        "affected_plants": ["Tomato", "Pepper"]
    },
    "Tomato leaf yellow virus": {
        "name": "Tomato Yellow Leaf Curl Virus",
        "scientific_name": "Tomato yellow leaf curl virus (TYLCV)",
        "description": "TYLCV transmitted by whiteflies causes severe yellowing.",
        "symptoms": ["Upward curling leaf margins", "Yellowing leaf edges", "Severely stunted growth", "Reduced flowering"],
        "treatment": {
            "organic": ["Remove infected plants", "Control whiteflies with neem oil", "Use yellow sticky traps"],
            "chemical": ["No chemical cure", "Apply imidacloprid for whiteflies"],
            "cultural": ["Use reflective mulches", "Remove infected plants", "Install insect screening"]
        },
        "prevention": ["Plant resistant varieties", "Control whiteflies", "Use insect netting", "Remove weeds"],
        "severity": "high",
        "affected_plants": ["Tomato", "Bean", "Pepper"]
    },
    "Tomato mold leaf": {
        "name": "Tomato Leaf Mold",
        "scientific_name": "Passalora fulva",
        "description": "Leaf mold primarily affects greenhouse tomatoes.",
        "symptoms": ["Pale yellow spots on upper surface", "Olive-green fuzzy mold on undersides", "Spots turn brown", "Leaves wilt"],
        "treatment": {
            "organic": ["Improve air circulation", "Apply copper fungicides", "Use sulfur"],
            "chemical": ["Apply chlorothalonil", "Use mancozeb"],
            "cultural": ["Reduce humidity below 85%", "Increase ventilation", "Space plants"]
        },
        "prevention": ["Plant resistant varieties", "Maintain low humidity", "Good ventilation"],
        "severity": "medium",
        "affected_plants": ["Tomato"]
    },
    "Tomato Septoria leaf spot": {
        "name": "Tomato Septoria Leaf Spot",
        "scientific_name": "Septoria lycopersici",
        "description": "Septoria leaf spot causes numerous small spots on leaves.",
        "symptoms": ["Small circular spots with dark borders", "Gray centers with black specks", "Spots start on lower leaves", "Premature leaf drop"],
        "treatment": {
            "organic": ["Apply copper fungicides", "Remove infected leaves", "Use sulfur"],
            "chemical": ["Apply chlorothalonil", "Use mancozeb"],
            "cultural": ["Mulch to prevent splash", "Remove lower leaves", "Stake plants"]
        },
        "prevention": ["Disease-free transplants", "Rotate crops 3 years", "Remove debris"],
        "severity": "medium",
        "affected_plants": ["Tomato"]
    },
    "Tomato two spotted spider mites leaf": {
        "name": "Two Spotted Spider Mites",
        "scientific_name": "Tetranychus urticae",
        "description": "Spider mites feed on plant sap causing stippling.",
        "symptoms": ["Fine yellow speckling", "Fine webbing on undersides", "Leaves turn bronze", "Premature leaf drop"],
        "treatment": {
            "organic": ["Spray with strong water", "Apply neem oil", "Use predatory mites", "Apply horticultural oil"],
            "chemical": ["Apply abamectin", "Use bifenthrin", "Apply miticides"],
            "cultural": ["Increase humidity", "Remove infested leaves", "Avoid drought stress"]
        },
        "prevention": ["Monitor regularly", "Maintain moisture", "Avoid excessive nitrogen"],
        "severity": "medium",
        "affected_plants": ["Tomato", "Bean", "Cucumber"]
    },
    "Bacterial_Blight": {
        "name": "Bacterial Blight",
        "scientific_name": "Xanthomonas oryzae pv. oryzae",
        "description": "Bacterial blight is a serious disease affecting rice.",
        "symptoms": ["Water-soaked lesions", "Yellow to white-gray stripes", "Wilting", "Milky bacterial ooze"],
        "treatment": {
            "organic": ["Remove and burn infected plants", "Apply copper bactericides"],
            "chemical": ["Apply copper compounds", "Use streptomycin sulfate"],
            "cultural": ["Use resistant varieties", "Avoid mechanical injury", "Balance nitrogen"]
        },
        "prevention": ["Plant resistant varieties", "Use disease-free seeds", "Proper water management"],
        "severity": "high",
        "affected_plants": ["Rice", "Wheat"]
    },
    "Brown_Spot": {
        "name": "Brown Spot",
        "scientific_name": "Bipolaris oryzae",
        "description": "Brown spot affects rice causing brown lesions.",
        "symptoms": ["Small circular brown spots with gray centers", "Yellow halos", "Discolored grains"],
        "treatment": {
            "organic": ["Apply sulfur fungicides", "Use copper fungicides"],
            "chemical": ["Apply mancozeb", "Use propiconazole", "Treat seeds"],
            "cultural": ["Balance soil fertility", "Avoid water stress", "Remove stubble"]
        },
        "prevention": ["Plant resistant varieties", "Use healthy seeds", "Balanced fertilization"],
        "severity": "medium",
        "affected_plants": ["Rice"]
    },
    "Rice_Blast": {
        "name": "Rice Blast",
        "scientific_name": "Magnaporthe oryzae",
        "description": "Rice blast is the most serious disease of rice worldwide.",
        "symptoms": ["Diamond-shaped lesions with gray centers", "Lesions on nodes", "Neck rot", "Unfilled grains"],
        "treatment": {
            "organic": ["Apply sulfur fungicides", "Use copper compounds", "Apply silicon"],
            "chemical": ["Apply tricyclazole", "Use carbendazim", "Apply at tillering"],
            "cultural": ["Plant resistant varieties", "Avoid excessive nitrogen", "Proper water depth"]
        },
        "prevention": ["Plant resistant varieties", "Disease-free seeds", "Balance nitrogen"],
        "severity": "high",
        "affected_plants": ["Rice", "Wheat"]
    },
    "Septoria": {
        "name": "Septoria Leaf Blotch",
        "scientific_name": "Septoria tritici",
        "description": "Septoria leaf blotch is a major wheat disease.",
        "symptoms": ["Brown to tan blotches", "Small black pycnidia in lesions", "Lesions between veins", "Lower leaves first"],
        "treatment": {
            "organic": ["Apply copper fungicides", "Remove lower leaves"],
            "chemical": ["Apply propiconazole", "Use strobilurin fungicides", "Apply chlorothalonil"],
            "cultural": ["Plant resistant varieties", "Bury residue", "Rotate crops"]
        },
        "prevention": ["Choose resistant varieties", "Crop rotation", "Bury debris"],
        "severity": "medium",
        "affected_plants": ["Wheat", "Barley"]
    },
    "Stripe Rust": {
        "name": "Stripe Rust",
        "scientific_name": "Puccinia striiformis",
        "description": "Stripe rust produces yellow-orange stripes on wheat leaves.",
        "symptoms": ["Yellow-orange pustules in stripes", "Pustules parallel to veins", "Premature yellowing", "Reduced grain fill"],
        "treatment": {
            "organic": ["Apply sulfur fungicides", "Remove infected material", "Use resistant varieties"],
            "chemical": ["Apply tebuconazole", "Use propiconazole", "Apply at first rust sign"],
            "cultural": ["Plant resistant varieties", "Destroy volunteers", "Avoid early planting"]
        },
        "prevention": ["Plant resistant varieties (most effective)", "Monitor forecasts", "Destroy volunteers"],
        "severity": "high",
        "affected_plants": ["Wheat", "Barley", "Rye"]
    }
}

# Save to JSON file
with open('disease_knowledge.json', 'w', encoding='utf-8') as f:
    json.dump(disease_data, f, indent=2, ensure_ascii=False)

print("✅ Complete disease_knowledge.json created with all 34 disease classes!")
print("📊 Total diseases:", len(disease_data))
