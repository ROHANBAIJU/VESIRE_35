import 'package:flutter/material.dart';

class AppLocalizations {
  final Locale locale;

  AppLocalizations(this.locale);

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  static final Map<String, Map<String, String>> _localizedValues = {
    'en': {
      // Home Screen
      'welcome': 'WELCOME',
      'home': 'Home',
      'search': 'Search',
      'scan': 'Scan',
      'analytics': 'Analytics',
      'history': 'History',
      'profile': 'Profile',
      
      // Stats Cards
      'totalScans': 'Total scans this week',
      'healthyPlants': 'Healthy Plants',
      'diseasedPlants': 'Diseased plants',
      'commonDisease': 'Most common disease',
      'blight': 'Blight',
      
      // Weather
      'windy': 'Windy',
      'humidity': 'Humidity',
      
      // Quick Actions
      'quickActions': 'Quick Actions',
      'scanPlant': 'Scan',
      'garden': 'Garden',
      'myGarden': 'My Garden',
      'guide': 'Guide',
      'plantGuide': 'Plant Guide',
      'plantGuides': 'Plant Guides',
      'community': 'Community',
      
      // Garden Screen
      'allPlants': 'All Plants',
      'needsCare': 'Needs Care',
      'addPlant': 'Add Plant',
      
      // Guide Screen
      'mostCommonDisease': 'Most common disease',
      
      // Tips
      'tipWateringTitle': 'Watering Tips',
      'tipWateringDesc': 'Water early morning or late evening for best absorption',
      'tipSunlightTitle': 'Sunlight Requirements',
      'tipSunlightDesc': 'Most plants need 6-8 hours of sunlight daily',
      'tipSoilTitle': 'Soil Health',
      'tipSoilDesc': 'Check soil moisture before watering to prevent overwatering',
      
      // Recent Activity
      'recentActivity': 'Recent Activity',
      'scannedHoursAgo': 'Scanned 2 hours ago',
      'scannedYesterday': 'Scanned yesterday',
      'healthy': 'Healthy - No diseases detected',
      'diseaseDetected': 'Disease detected - Powdery Mildew',
      'tomatoPlant': 'Tomato Plant',
      'roseBush': 'Rose Bush',
      
      // Plant Care Tips
      'plantCareTips': 'Plant Care Tips',
      'wateringSchedule': '💧 Watering Schedule',
      'wateringTip': 'Water your plants early morning or late evening for best absorption.',
      'sunlightRequirements': '☀️ Sunlight Requirements',
      'sunlightTip': 'Most plants need 6-8 hours of sunlight daily for healthy growth.',
      'soilHealth': '🌱 Soil Health',
      'soilTip': 'Check soil moisture before watering. Overwatering can harm roots.',
      
      // Language
      'selectLanguage': 'Select Language',
      'english': 'English',
      'hindi': 'Hindi',
      'kannada': 'Kannada',
      
      // Login Screen
      'loginTitle': 'Welcome Back',
      'loginSubtitle': 'Sign in to continue',
      'email': 'Email',
      'password': 'Password',
      'forgotPassword': 'Forgot Password?',
      'login': 'Login',
      'signInWith': 'Or sign in with',
      'dontHaveAccount': "Don't have an account?",
      'signUp': 'Sign Up',
      
      // Profile
      'myProfile': 'My Profile',
      'settings': 'Settings',
      'notifications': 'Notifications',
      'language': 'Language',
      'about': 'About',
      'logout': 'Logout',
      'scans': 'Scans',
      'plants': 'Plants',
      'achievements': 'Achievements',
      
      // Scan Screen
      'analysisReady': 'AI Analysis Ready! Tap to view',
      'scanningDiseases': 'Scanning for diseases...',
      'tapToStartDetection': 'Tap to start detection',
      'noDetections': 'No detections in this frame',
      'diseaseDetectedMessage': 'Disease detected but detailed information is not available in the knowledge base.',
      'consultExpert': 'Consult a local agricultural expert for treatment recommendations',
      'errorFetchingDiagnosis': 'Error fetching diagnosis information. Please check your connection.',
      'retryScanning': 'Retry scanning or consult a local agricultural expert',
    },
    'hi': {
      // Home Screen
      'welcome': 'स्वागत है',
      'home': 'होम',
      'search': 'खोज',
      'scan': 'स्कैन',
      'analytics': 'विश्लेषण',
      'history': 'इतिहास',
      'profile': 'प्रोफ़ाइल',
      
      // Stats Cards
      'totalScans': 'इस सप्ताह कुल स्कैन',
      'healthyPlants': 'स्वस्थ पौधे',
      'diseasedPlants': 'रोगग्रस्त पौधे',
      'commonDisease': 'सबसे आम बीमारी',
      'blight': 'झुलसा',
      
      // Weather
      'windy': 'हवादार',
      'humidity': 'नमी',
      
      // Quick Actions
      'quickActions': 'त्वरित कार्य',
      'scanPlant': 'स्कैन',
      'garden': 'बगीचा',
      'myGarden': 'मेरा बगीचा',
      'guide': 'गाइड',
      'plantGuide': 'पौधों की गाइड',
      'plantGuides': 'पौधों की गाइड',
      'community': 'समुदाय',
      
      // Garden Screen
      'allPlants': 'सभी पौधे',
      'needsCare': 'देखभाल की जरूरत',
      'addPlant': 'पौधा जोड़ें',
      
      // Guide Screen
      'mostCommonDisease': 'सबसे आम बीमारी',
      
      // Tips
      'tipWateringTitle': 'पानी देने के टिप्स',
      'tipWateringDesc': 'बेहतर अवशोषण के लिए सुबह जल्दी या शाम को पानी दें',
      'tipSunlightTitle': 'धूप की आवश्यकता',
      'tipSunlightDesc': 'अधिकांश पौधों को रोजाना 6-8 घंटे धूप की आवश्यकता होती है',
      'tipSoilTitle': 'मिट्टी का स्वास्थ्य',
      'tipSoilDesc': 'अधिक पानी से बचने के लिए पानी देने से पहले मिट्टी की नमी जांचें',
      
      // Recent Activity
      'recentActivity': 'हाल की गतिविधि',
      'scannedHoursAgo': '2 घंटे पहले स्कैन किया',
      'scannedYesterday': 'कल स्कैन किया',
      'healthy': 'स्वस्थ - कोई बीमारी नहीं',
      'diseaseDetected': 'रोग पाया गया - पाउडरी मिल्ड्यू',
      'tomatoPlant': 'टमाटर का पौधा',
      'roseBush': 'गुलाब की झाड़ी',
      
      // Plant Care Tips
      'plantCareTips': 'पौधों की देखभाल टिप्स',
      'wateringSchedule': '💧 पानी का समय',
      'wateringTip': 'बेहतर अवशोषण के लिए सुबह जल्दी या शाम को पौधों को पानी दें।',
      'sunlightRequirements': '☀️ धूप की आवश्यकता',
      'sunlightTip': 'अधिकांश पौधों को स्वस्थ विकास के लिए रोजाना 6-8 घंटे धूप की आवश्यकता होती है।',
      'soilHealth': '🌱 मिट्टी का स्वास्थ्य',
      'soilTip': 'पानी देने से पहले मिट्टी की नमी जांचें। अधिक पानी जड़ों को नुकसान पहुंचा सकता है।',
      
      // Language
      'selectLanguage': 'भाषा चुनें',
      'english': 'अंग्रेज़ी',
      'hindi': 'हिंदी',
      'kannada': 'ಕನ್ನಡ',
      
      // Login Screen
      'loginTitle': 'वापसी पर स्वागत है',
      'loginSubtitle': 'जारी रखने के लिए साइन इन करें',
      'email': 'ईमेल',
      'password': 'पासवर्ड',
      'forgotPassword': 'पासवर्ड भूल गए?',
      'login': 'लॉगिन',
      'signInWith': 'या साइन इन करें',
      'dontHaveAccount': 'खाता नहीं है?',
      'signUp': 'साइन अप',
      
      // Profile
      'myProfile': 'मेरा प्रोफ़ाइल',
      'settings': 'सेटिंग्स',
      'notifications': 'सूचनाएं',
      'language': 'भाषा',
      'about': 'के बारे में',
      'logout': 'लॉगआउट',
      'scans': 'स्कैन',
      'plants': 'पौधे',
      'achievements': 'उपलब्धियां',
      
      // Scan Screen
      'analysisReady': 'एआई विश्लेषण तैयार! देखने के लिए टैप करें',
      'scanningDiseases': 'रोगों के लिए स्कैन कर रहे हैं...',
      'tapToStartDetection': 'पहचान शुरू करने के लिए टैप करें',
      'noDetections': 'इस फ्रेम में कोई पहचान नहीं',
      'diseaseDetectedMessage': 'रोग पाया गया लेकिन विस्तृत जानकारी उपलब्ध नहीं है।',
      'consultExpert': 'उपचार सिफारिशों के लिए स्थानीय कृषि विशेषज्ञ से परामर्श करें',
      'errorFetchingDiagnosis': 'निदान जानकारी प्राप्त करने में त्रुटि। कृपया अपना कनेक्शन जांचें।',
      'retryScanning': 'फिर से स्कैन करें या स्थानीय कृषि विशेषज्ञ से परामर्श करें',
    },
    'kn': {
      // Home Screen
      'welcome': 'ಸ್ವಾಗತ',
      'home': 'ಮುಖಪುಟ',
      'search': 'ಹುಡುಕಿ',
      'scan': 'ಸ್ಕ್ಯಾನ್',
      'analytics': 'ವಿಶ್ಲೇಷಣೆ',
      'history': 'ಇತಿಹಾಸ',
      'profile': 'ಪ್ರೊಫೈಲ್',
      
      // Stats Cards
      'totalScans': 'ಈ ವಾರದ ಒಟ್ಟು ಸ್ಕ್ಯಾನ್‌ಗಳು',
      'healthyPlants': 'ಆರೋಗ್ಯಕರ ಸಸ್ಯಗಳು',
      'diseasedPlants': 'ರೋಗಗ್ರಸ್ತ ಸಸ್ಯಗಳು',
      'commonDisease': 'ಅತ್ಯಂತ ಸಾಮಾನ್ಯ ರೋಗ',
      'blight': 'ಬ್ಲೈಟ್',
      
      // Weather
      'windy': 'ಗಾಳಿಯುಕ್ತ',
      'humidity': 'ತೇವಾಂಶ',
      
      // Quick Actions
      'quickActions': 'ತ್ವರಿತ ಕ್ರಿಯೆಗಳು',
      'scanPlant': 'ಸ್ಕ್ಯಾನ್',
      'garden': 'ತೋಟ',
      'myGarden': 'ನನ್ನ ತೋಟ',
      'guide': 'ಮಾರ್ಗದರ್ಶಿ',
      'plantGuide': 'ಸಸ್ಯ ಮಾರ್ಗದರ್ಶಿ',
      'plantGuides': 'ಸಸ್ಯ ಮಾರ್ಗದರ್ಶಿಗಳು',
      'community': 'ಸಮುದಾಯ',
      
      // Garden Screen
      'allPlants': 'ಎಲ್ಲಾ ಸಸ್ಯಗಳು',
      'needsCare': 'ಆರೈಕೆ ಬೇಕು',
      'addPlant': 'ಸಸ್ಯ ಸೇರಿಸಿ',
      
      // Guide Screen
      'mostCommonDisease': 'ಅತ್ಯಂತ ಸಾಮಾನ್ಯ ರೋಗ',
      
      // Tips
      'tipWateringTitle': 'ನೀರುಣಿಸುವ ಸಲಹೆಗಳು',
      'tipWateringDesc': 'ಉತ್ತಮ ಹೀರಿಕೊಳ್ಳುವಿಕೆಗಾಗಿ ಮುಂಜಾನೆ ಅಥವಾ ಸಂಜೆ ನೀರು ಹಾಕಿ',
      'tipSunlightTitle': 'ಸೂರ್ಯನ ಬೆಳಕಿನ ಅವಶ್ಯಕತೆಗಳು',
      'tipSunlightDesc': 'ಹೆಚ್ಚಿನ ಸಸ್ಯಗಳಿಗೆ ದಿನಕ್ಕೆ 6-8 ಗಂಟೆ ಸೂರ್ಯನ ಬೆಳಕು ಬೇಕಾಗುತ್ತದೆ',
      'tipSoilTitle': 'ಮಣ್ಣಿನ ಆರೋಗ್ಯ',
      'tipSoilDesc': 'ಅತಿಯಾದ ನೀರು ತಪ್ಪಿಸಲು ನೀರು ಹಾಕುವ ಮೊದಲು ಮಣ್ಣಿನ ತೇವಾಂಶ ಪರಿಶೀಲಿಸಿ',
      
      // Recent Activity
      'recentActivity': 'ಇತ್ತೀಚಿನ ಚಟುವಟಿಕೆ',
      'scannedHoursAgo': '2 ಗಂಟೆಗಳ ಹಿಂದೆ ಸ್ಕ್ಯಾನ್ ಮಾಡಲಾಗಿದೆ',
      'scannedYesterday': 'ನಿನ್ನೆ ಸ್ಕ್ಯಾನ್ ಮಾಡಲಾಗಿದೆ',
      'healthy': 'ಆರೋಗ್ಯಕರ - ಯಾವುದೇ ರೋಗಗಳಿಲ್ಲ',
      'diseaseDetected': 'ರೋಗ ಪತ್ತೆಯಾಗಿದೆ - ಪೌಡರಿ ಮಿಲ್ಡ್ಯೂ',
      'tomatoPlant': 'ಟೊಮೇಟೊ ಗಿಡ',
      'roseBush': 'ಗುಲಾಬಿ ಗಿಡ',
      
      // Plant Care Tips
      'plantCareTips': 'ಸಸ್ಯ ಆರೈಕೆ ಸಲಹೆಗಳು',
      'wateringSchedule': '💧 ನೀರುಣಿಸುವ ವೇಳಾಪಟ್ಟಿ',
      'wateringTip': 'ಉತ್ತಮ ಹೀರಿಕೊಳ್ಳುವಿಕೆಗಾಗಿ ಮುಂಜಾನೆ ಅಥವಾ ಸಂಜೆ ನಿಮ್ಮ ಸಸ್ಯಗಳಿಗೆ ನೀರು ಹಾಕಿ.',
      'sunlightRequirements': '☀️ ಸೂರ್ಯನ ಬೆಳಕಿನ ಅವಶ್ಯಕತೆಗಳು',
      'sunlightTip': 'ಹೆಚ್ಚಿನ ಸಸ್ಯಗಳಿಗೆ ಆರೋಗ್ಯಕರ ಬೆಳವಣಿಗೆಗೆ ದಿನಕ್ಕೆ 6-8 ಗಂಟೆ ಸೂರ್ಯನ ಬೆಳಕು ಬೇಕಾಗುತ್ತದೆ.',
      'soilHealth': '🌱 ಮಣ್ಣಿನ ಆರೋಗ್ಯ',
      'soilTip': 'ನೀರು ಹಾಕುವ ಮೊದಲು ಮಣ್ಣಿನ ತೇವಾಂಶವನ್ನು ಪರಿಶೀಲಿಸಿ. ಅತಿಯಾದ ನೀರು ಬೇರುಗಳಿಗೆ ಹಾನಿ ಮಾಡಬಹುದು.',
      
      // Language
      'selectLanguage': 'ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ',
      'english': 'ಇಂಗ್ಲಿಷ್',
      'hindi': 'हिंदी',
      'kannada': 'ಕನ್ನಡ',
      
      // Login Screen
      'loginTitle': 'ಮರಳಿ ಸ್ವಾಗತ',
      'loginSubtitle': 'ಮುಂದುವರಿಸಲು ಸೈನ್ ಇನ್ ಮಾಡಿ',
      'email': 'ಇಮೇಲ್',
      'password': 'ಪಾಸ್‌ವರ್ಡ್',
      'forgotPassword': 'ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿರುವಿರಾ?',
      'login': 'ಲಾಗಿನ್',
      'signInWith': 'ಅಥವಾ ಸೈನ್ ಇನ್ ಮಾಡಿ',
      'dontHaveAccount': 'ಖಾತೆ ಇಲ್ಲವೇ?',
      'signUp': 'ಸೈನ್ ಅಪ್',
      
      // Profile
      'myProfile': 'ನನ್ನ ಪ್ರೊಫೈಲ್',
      'settings': 'ಸೆಟ್ಟಿಂಗ್‌ಗಳು',
      'notifications': 'ಅಧಿಸೂಚನೆಗಳು',
      'language': 'ಭಾಷೆ',
      'about': 'ಬಗ್ಗೆ',
      'logout': 'ಲಾಗ್ಔಟ್',
      'scans': 'ಸ್ಕ್ಯಾನ್‌ಗಳು',
      'plants': 'ಸಸ್ಯಗಳು',
      'achievements': 'ಸಾಧನೆಗಳು',
      
      // Scan Screen
      'analysisReady': 'AI ವಿಶ್ಲೇಷಣೆ ಸಿದ್ಧವಾಗಿದೆ! ನೋಡಲು ಟ್ಯಾಪ್ ಮಾಡಿ',
      'scanningDiseases': 'ರೋಗಗಳಿಗಾಗಿ ಸ್ಕ್ಯಾನ್ ಮಾಡುತ್ತಿದೆ...',
      'tapToStartDetection': 'ಪತ್ತೆ ಪ್ರಾರಂಭಿಸಲು ಟ್ಯಾಪ್ ಮಾಡಿ',
      'noDetections': 'ಈ ಫ್ರೇಮ್‌ನಲ್ಲಿ ಯಾವುದೇ ಪತ್ತೆಯಾಗಿಲ್ಲ',
      'diseaseDetectedMessage': 'ರೋಗ ಪತ್ತೆಯಾಗಿದೆ ಆದರೆ ವಿವರ ಮಾಹಿತಿ ಲಭ್ಯವಿಲ್ಲ.',
      'consultExpert': 'ಚಿಕಿತ್ಸೆ ಶಿಫಾರಸುಗಳಿಗಾಗಿ ಸ್ಥಳೀಯ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ',
      'errorFetchingDiagnosis': 'ರೋಗನಿರ್ಣಯ ಮಾಹಿತಿ ಪಡೆಯುವಲ್ಲಿ ದೋಷ. ದಯವಿಟ್ಟು ನಿಮ್ಮ ಸಂಪರ್ಕವನ್ನು ಪರಿಶೀಲಿಸಿ.',
      'retryScanning': 'ಮತ್ತೆ ಸ್ಕ್ಯಾನ್ ಮಾಡಿ ಅಥವಾ ಸ್ಥಳೀಯ ಕೃಷಿ ತಜ್ಞರನ್ನು ಸಂಪರ್ಕಿಸಿ',
    },
  };

  String translate(String key) {
    return _localizedValues[locale.languageCode]?[key] ?? key;
  }
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) {
    return ['en', 'hi', 'kn'].contains(locale.languageCode);
  }

  @override
  Future<AppLocalizations> load(Locale locale) async {
    return AppLocalizations(locale);
  }

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}
