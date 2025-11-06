# Vesire AR: Offline AI Disease Diagnoser

**An offline-first, AI-powered Augmented Reality diagnostic tool designed to empower smallholder farmers by providing instant, on-device crop disease analysis.**

[![Hackathon Badge](https://img.shields.io/badge/SJBIT-Hackathon%202025-blue.svg)](https://sjbit.edu.in/)
[![Flutter Badge](https://img.shields.io/badge/Built%20with-Flutter-02569B.svg)](https://flutter.dev)
[![AI Badge](https://img.shields.io/badge/AI%20Model-TensorFlow%20Lite-FF6F00.svg)](https://www.tensorflow.org/lite)

---

## 🧠 Team VESIRE — SJBIT Hackathon 2025

Hello! We're **VESIRE**, a passionate student team participating in the SJBIT Hackathon 2025.  
We're excited to innovate, collaborate, and build something that creates real-world impact.


### 👥 Team Members
- **Ananya** — Team Lead  
- **Sruthi**  
- **Joel**  
- **Srijan**  
- **Rohan**

We’re a team driven by curiosity, collaboration, and creativity — all set to make **AgriScan AR** a game-changing project for farmers.

---

## 📖 Project Summary

Smallholder farmers face significant yield loss due to crop diseases, often lacking access to timely expert advice or reliable internet for diagnostic apps.  
**AgriScan AR** solves this problem by putting a powerful AI diagnostician directly in their hands—no internet required.

By leveraging **on-device machine learning** and a **pragmatic Augmented Reality (AR)** interface, the app performs real-time object detection on the live camera feed.  
It visually highlights disease symptoms with overlays and provides immediate, actionable treatment tips from a local offline database, all in the farmer's local language.

---

## ✨ Core Features

### Core (Offline) MVP
* **Real-Time Disease Detection:** Uses the live camera feed to instantly identify and locate crop diseases.  
* **AR Symptom Highlighting:** Draws "Augmented Reality" bounding boxes directly onto the screen, pinpointing the detected symptoms.  
* **100% Offline Functionality:** The AI model (TFLite) and treatment database (`sqflite`) run entirely on-device.  
* **Offline Treatment Database:** Provides practical, instant treatment tips.  
* **Localized UI:** Supports local languages (e.g., Kannada) for accessibility.

### Bonus (Online) Feature
* **Advanced AI Tips (RAG):** An optional "Learn More" button that, *if online*, uses a Firebase Cloud Function and Gemini API (RAG) to generate region-specific advice.

---

## 🏗️ Architecture & How It Works

### Core Offline Flow (On-Device)
1. **Camera Input:** The user points their phone at a plant. The Flutter `camera` plugin streams video frames.  
2. **AI Inference:** Each frame is fed into a locally-stored **TFLite model** (e.g., YOLOv5 or EfficientDet).  
3. **On-Device Processing:** The model outputs bounding boxes (e.g., `[Tomato_Blight, x:50, y:100, w:200, h:150]`).  
4. **AR Overlay:** Flutter’s `Stack` widget draws boxes/labels over the camera view for a pragmatic AR effect.  
5. **Offline Data:** When tapped, the app queries a local **`sqflite`** DB to fetch stored treatment tips.

### Optional Online Flow (Cloud)
1. **User Action:** User taps “Get Advanced AI Tips.”  
2. **Cloud Function:** Calls a **Firebase Cloud Function** written in Python.  
3. **GenAI RAG:** Uses **Gemini API** with RAG to produce a detailed context-aware answer.  
4. **Display:** Sends the result back to the app to display rich text to the user.

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Flutter & Dart | Cross-platform app |
| **On-Device AI** | TensorFlow Lite (`tflite_flutter`) | Offline AI inference |
| **AR Layer** | `camera` + `Stack` | Real-time “pragmatic AR” |
| **Offline DB** | `sqflite` / `hive` | Disease & treatment storage |
| **Localization** | `flutter_localizations` (`intl`) | Local language support |
| **AI Model** | Python + TensorFlow/Keras | Model training |
| **Cloud Backend** | Firebase Cloud Functions | Online RAG feature |
| **GenAI** | Gemini API | AI-powered recommendations |

---

## 🚀 Running the Project

### Prerequisites
* [Flutter SDK](https://flutter.dev/docs/get-started/install)
* [Python 3.9+](https://www.python.org/downloads/)
* [Firebase CLI](https://firebase.google.com/docs/cli)
* Physical Android/iOS device (for AR)

---

### Part 1: Run the Offline App
####### STARTING THE PROJECT NOW
```bash


git clone https://github.com/your-username/agriscan-ar.git
cd agriscan-ar
flutter pub get
flutter run
