<div align="center">

# 🌿 AgriScan: AI-Powered Plant Disease Detection

**An offline-first, AI-powered Augmented Reality diagnostic tool designed to empower smallholder farmers by providing instant, on-device crop disease analysis.**

</div>

<div align="center">

[![SJBIT Hackathon](https://img.shields.io/badge/SJBIT-Hackathon%202025-4CAF50?style=for-the-badge&logo=google-scholar&logoColor=white)](https://sjbit.edu.in/)
[![Flutter](https://img.shields.io/badge/Flutter-3.35.6-02569B?style=for-the-badge&logo=flutter&logoColor=white)](https://flutter.dev)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-AI%20Detection-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://github.com/ultralytics/ultralytics)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

</div>

<div align="center">
  <img src="UI PICS FOR README/LOGO.jpg" alt="AgriScan Banner" width="500"/>
</div>

<p align="center">
  <strong>An AI-powered solution that brings expert plant disease diagnosis to farmers' fingertips — with offline support and real-time AR visualization.</strong>
</p>

<p align="center">
  <a href="#-features">📱 Features</a> •
  <a href="#️-architecture">🏗️ Architecture</a> •
  <a href="#-quick-start">🚀 Quick Start</a> •
  <a href="#-screenshots">📸 Screenshots</a> •
  <a href="#-team-vesire">👥 Team</a>
</p>

---

## 🧠 Team VESIRE — SJBIT Hackathon 2025

<div align="center">

Hello! We're **VESIRE**, a passionate student team participating in the SJBIT Hackathon 2025.  
We're excited to innovate, collaborate, and build something that creates real-world impact.

</div>

### 👥 Team Members
- **Ananya** — Team Lead
- **Sruthi**
- **Joel**
- **Srijan**
- **Rohan**

<div align="center">

| Role                | Member     | GitHub                                       |
| :------------------ | :--------- | :------------------------------------------- |
| 🎯 **Team Lead**    | **Ananya** | [@ananya](https://github.com/Ananya570-hub)                |
| 💻 **Developer**    | **Joel** | [@sruthi](https://github.com/joeljo777)                |
| 🎨 **UI/UX Designer** | **Sruthi**   | [@joel](https://github.com/Sruthi-SK1)                  |
| 🤖 **Frontend Dev**    | **Srijan** | [@srijan](https://github.com/srijansrivastava03)                |
| ⚙️ **Backend Dev**  | **Rohan**  | [@ROHANBAIJU](https://github.com/ROHANBAIJU) |

*A team driven by innovation, collaboration, and the vision to revolutionize agriculture with AI.*

</div>

---

## 📖 Project Summary

Smallholder farmers face significant yield loss due to crop diseases, often lacking access to timely expert advice or reliable internet for diagnostic apps.
**AgriScan AR** solves this problem by putting a powerful AI diagnostician directly in their hands—no internet required.

By leveraging **on-device machine learning** and a **pragmatic Augmented Reality (AR)** interface, the app performs real-time object detection on the live camera feed.
It visually highlights disease symptoms with overlays and provides immediate, actionable treatment tips from a local offline database, all in the farmer's local language.

### 🚨 The Challenge
- 🌾 Smallholder farmers lose **30-40% of crop yield** to diseases annually.
- 📱 Limited access to agricultural experts and diagnostic tools.
- 🌐 Unreliable internet connectivity in rural areas.
- 💰 High cost of traditional disease diagnosis methods.
- ⏰ Time-critical detection - diseases spread rapidly.

### 💡 Our Solution: AgriScan
**AgriScan** leverages cutting-edge AI and AR technology to provide **instant, accurate plant disease diagnosis** directly on farmers' smartphones — **with or without internet!**

<div align="center">

| 📷 Point Camera        | 🤖 AI Detection           | 🎯 AR Overlay                   | 💊 Get Treatment                     |
| :--------------------- | :------------------------ | :------------------------------ | :----------------------------------- |
| Aim at affected leaf | YOLOv8 identifies disease | Bounding boxes highlight symptoms | Instant diagnosis + AI recommendations |

</div>

---

## ✨ Core Features

### 🔥 Core Features (Offline Mode)
#### 🤖 **Real-Time AI Detection**
- YOLOv8-based disease recognition
- Detects 29+ plant diseases
- Confidence scoring (50%+ threshold)
- Sub-second inference time

#### 📱 **AR Visualization**
- Live camera feed with AR overlays
- Bounding boxes around diseases
- Real-time symptom highlighting
- Intuitive visual feedback

#### 💾 **100% Offline Support**
- On-device TFLite model (6MB)
- SQLite disease database
- No internet required for diagnosis
- Works in remote areas

#### 🗣️ **Multi-Language Support**
- Kannada, Hindi, Tamil support
- Local language UI
- Farmer-friendly interface
- Voice instructions (planned)

### 🌟 Advanced Features (Online Mode)
#### 🚀 **Gemini AI RAG Layer**
- Context-aware recommendations
- Region-specific treatment advice
- Advanced diagnosis insights
- Natural language responses

#### 📊 **Detection History**
- Track all detections
- Compare past diagnoses
- Disease trends over time
- Export reports

#### 🌐 **Cloud Sync (Optional)**
- Backup detection history
- Cross-device sync
- Community insights
- Expert consultation requests

#### 🔔 **Smart Notifications**
- Disease alerts
- Treatment reminders
- Weather-based warnings
- Best practice tips

---

## 🏗️ Architecture & How It Works

### System Overview
```
┌─────────────────────────────────────────────────────────────────┐
│                      📱 Flutter Mobile App                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │   Camera    │  │  AR Overlay  │  │  Local Database        │ │
│  │   Plugin    │→ │   (Stack)    │→ │  (SQLite)              │ │
│  └─────────────┘  └──────────────┘  └────────────────────────┘ │
│         ↓                                      ↑                 │
│  ┌─────────────────────────────────────────────┘                │
│  │           TFLite Model (YOLOv8)                              │
│  │           • 29 Disease Classes                               │
│  │           • 6MB Optimized Model                              │
│  └──────────────────────────────────────────────────────────────┤
│                                                                  │
│  Optional Online Features:                                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  🌐 REST API → Flask Backend → Gemini RAG → Response    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔄 Detection Flow
```
📷 Camera Feed → 🖼️ Frame Capture → 🤖 YOLOv8 Inference
                                           ↓
                            ┌──────────────┴──────────────┐
                            ↓                             ↓
                      Disease Detected              No Detection
                            ↓                             ↓
                    🎯 Draw AR Overlay            ⚠️ Show Message
                            ↓
                    📊 Get Treatment Info
                            ↓
                    ┌───────┴───────┐
                    ↓               ↓
              Online Mode      Offline Mode
                    ↓               ↓
            🚀 Gemini RAG    💾 Local DB
                    ↓               ↓
                    └───────┬───────┘
                            ↓
                    📱 Display Results
```

---

## 🛠️ Tech Stack

| Category       | Technology                               | Purpose                                  |
| :------------- | :--------------------------------------- | :--------------------------------------- |
| **Frontend**   | Flutter & Dart                           | Cross-platform app development           |
| **On-Device AI** | TensorFlow Lite (`tflite_flutter`)       | Offline AI inference on mobile           |
| **AR Layer**   | `camera` + `Stack` Widget                | Real-time "pragmatic AR" visualization   |
| **Offline DB** | `sqflite`                                | Local disease & treatment storage        |
| **Backend**    | Python, Flask                            | REST API for online features             |
| **AI Model**   | Ultralytics YOLOv8, PyTorch              | Model training and computer vision       |
| **GenAI**      | Google Gemini API                        | Advanced AI-powered recommendations (RAG)|

---

## 📸 Working

<div align="center">

### Dashboard, Garden, Plant Guide, Community.
<img src="UI PICS FOR README/IMG-20251107-WA0006.jpg" width="250" alt="Dashbord"/> <img src="UI PICS FOR README/IMG-20251107-WA0008.jpg" width="250" alt="Garden"/> <img src="UI PICS FOR README/IMG-20251107-WA0009.jpg" width="250" alt="Plant Guide"/> <img src="UI PICS FOR README/IMG-20251107-WA0010.jpg" width="250" alt="Community"/> 

### Real-Time Disease Detection, AR Visualization with Treatment Recommendations & Results
<img src="UI PICS FOR README/actual ar detection.jpg" width="250" alt="AR overlay"/> <img src="UI PICS FOR README/analysis.jpg" width="250" alt="Analytics"/> 

*Real-time plant disease detection with AR bounding boxes and instant diagnosis*

</div>

---

## 🚀 Quick Start

### Prerequisites
- **Flutter SDK 3.35+** ([Install](https://flutter.dev/docs/get-started/install))
- **Python 3.10+** ([Install](https://python.org))
- **Android Studio** or **Xcode** (for mobile development)
- **Physical Device** (recommended for camera + AR)

### 📱 Frontend Setup (Flutter App)
```bash
# Clone the repository
git clone https://github.com/ROHANBAIJU/VESIRE_35.git
cd VESIRE_35/ar_test_app

# Install dependencies
flutter pub get

# Set JAVA_HOME if not configured (Example for Windows PowerShell)
$env:JAVA_HOME = "C:\Program Files\Java\jdk-21"

# Run on connected device
flutter run
```

### ⚙️ Backend Setup (Flask API)
```bash
# Navigate to backend directory
cd Backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables by creating a .env file
# Add your Gemini API key to the .env file:
# GEMINI_API_KEY=your_gemini_api_key_here

# Run Flask server
python -m api.app
# Server starts at http://127.0.0.1:5000
```

### 🧪 Test Webcam Detection
```bash
# Run live webcam detection script (for desktop testing)
cd Backend
python webcam_detection.py

# Controls: 'q' or 'esc' to quit
```

---

## 📚 Documentation

| Document                                       | Description                                      |
| :--------------------------------------------- | :----------------------------------------------- |
| [API Documentation](Backend/API_DOCUMENTATION.md) | Complete REST API reference with 15+ endpoints   |
| [Architecture Guide](Backend/API_ARCHITECTURE.md) | System design and component details              |
| [Integration Guide](Backend/INTEGRATION_READY.md) | Flutter integration instructions               |
| [Quick Start Guide](Backend/QUICK_START.md)     | Getting started with the backend                 |
| [Environment Setup](Backend/ENV_SETUP_COMPLETE.md)| Environment variables configuration            |

---

## 🎯 Supported Diseases

<details>
<summary><b>📋 Click to see all 34 supported plant diseases</b></summary>

🍎 Apple (3):

Apple leaf
Apple rust leaf
Apple Scab Leaf
🌶 Bell Pepper (2):
4. Bell_pepper leaf
5. Bell_pepper leaf spot

🫐 Berries (4):
6. Blueberry leaf
7. Cherry leaf
8. Raspberry leaf
9. Strawberry leaf

🌽 Corn (3):
10. Corn Gray leaf spot
11. Corn leaf blight
12. Corn rust leaf

🍇 Grape (2):
13. grape leaf
14. grape leaf black rot

🍑 Peach (1):
15. Peach leaf

🥔 Potato (3):
16. Potato leaf
17. Potato leaf early blight
18. Potato leaf late blight

🫘 Soybean (1):
19. Soyabean leaf

🎃 Squash (1):
20. Squash Powdery mildew leaf

🍅 Tomato (9):
21. Tomato Early blight leaf
22. Tomato leaf
23. Tomato leaf bacterial spot
24. Tomato leaf late blight
25. Tomato leaf mosaic virus
26. Tomato leaf yellow virus
27. Tomato mold leaf
28. Tomato Septoria leaf spot
29. Tomato two spotted spider mites leaf

🌾 Rice (3):
30. Bacterial_Blight
31. Brown_Spot
32. Rice_Blast

🌾 Wheat (2):
33. Septoria
34. Stripe Rust

Total: 34 disease classes covering major crops (Apple, Tomato, Potato, Corn, Rice, Wheat, Grape, and other vegetables/fruits)
</details>

---

## 📊 Model Performance

| Metric       | Value     | Description                                         |
| :----------- | :-------- | :-------------------------------------------------- |
| **mAP@50**   | `66.6%`   | Mean Average Precision at IoU 0.5                   |
| **mAP@50-95**| `67.8%`   | Mean Average Precision at IoU 0.5-0.95              |
| **Precision**| `61%`   | Accuracy of positive predictions                  |
| **Recall**   | `64.1%`   | Ability to find all relevant instances            |
| **Model Size** | `5.95 MB` | Optimized for mobile deployment (TFLite)          |
| **Inference**| `~200ms`  | On mid-range Android devices                      |
| **Dataset**  | `3,000+(for training)`  | Images from the PlantDoc dataset across 34 classes|

---

## 🗺️ Roadmap

- [x] **Phase 1: MVP (Completed)**
  - [x] YOLOv8 model training & Flask REST API
  - [x] Flutter camera integration with AR overlay
  - [x] Offline SQLite database & Gemini RAG
  - [x] Real-time webcam detection with async diagnosis
- [x] **Phase 2: Enhancement (In Progress)**
  - [x] TFLite model export and on-device inference
  - [x] Multi-language support (Kannada, Hindi)
  - [x] Detection history and treatment UI
- [x] **Phase 3: Advanced Features (Planned)**
  - [ ] Voice input/output and weather alerts
  - [x] Community features and expert consultation

---

## 🤝 Contributing

We welcome contributions! Please fork the repository, create a feature branch, and open a pull request. See our development guidelines for more details.

## 📄 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 🙏 Acknowledgments
**SJBIT** • **PlantDoc Dataset** • **Ultralytics** • **Google** • **Flutter Team** • Our **Mentors & Advisors**

---

### 📞 Contact Team VESIRE

📧 **Email**: [teamvesire@sjbit.edu.in](mailto:teamvesire@sjbit.edu.in) | 🌐 **GitHub**: [@ROHANBAIJU/VESIRE_35](https://github.com/ROHANBAIJU/VESIRE_35) | 💬 **Issues**: [Report a Bug](https://github.com/ROHANBAIJU/VESIRE_35/issues)

[![GitHub stars](https://img.shields.io/github/stars/ROHANBAIJU/VESIRE_35?style=social)](https://github.com/ROHANBAIJU/VESIRE_35)
[![GitHub forks](https://img.shields.io/github/forks/ROHANBAIJU/VESIRE_35?style=social)](https://github.com/ROHANBAIJU/VESIRE_35/fork)

**Made with ❤️ by Team VESIRE for farmers worldwide**

🌾 *Empowering Agriculture Through AI* 🌾

</div>
