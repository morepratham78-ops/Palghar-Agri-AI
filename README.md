# 🌾 PALGHAR AGRI AI

A complete, farmer-friendly agricultural AI web application built specifically for farmers in **Palghar** and Maharashtra, India.

---

## 🌟 Core Features & Implementation

### 1. 🔬 Crop Doctor (MVP)
- **Computer Vision Model**: Local, genuine **PlantVillage ResNet-18** model (`models/plantvillage-resnet18/`) fine-tuned across 38 crop disease classes.
- **Genuine Predictions**: Delivers real image-based classification, exact confidence percentages, crop name, symptoms, chemical treatments, and organic prevention advice.
- **Low Confidence Safeguard**: Transparently alerts farmers when prediction confidence is below 55% and directs them to the nearest Krishi Vigyan Kendra (KVK).
- **Audio Output**: Voice readout of the diagnosis and treatment in Marathi, Hindi, or English.
- **Instant Test Samples**: One-click test sample leaves (Healthy vs Diseased) built directly into the UI for instant testing.

### 2. 🤖 Multilingual AI Advisor
- **Local LLM**: Integrated with local **Ollama** running `llama3.2:3b` / `llama3.2:latest` (private, offline-capable).
- **Multilingual**: Full prompt tuning for **Marathi (मराठी)**, **Hindi (हिंदी)**, and **English**, specialized for Maharashtra crops (Rice/Wada Kolam, Chickoo/Dahanu, Nagli, Mango, Tomato, Cashew).
- **Streaming Response**: Real-time token streaming with farmer-friendly quick suggestion questions.

### 3. 🎙️ Voice Assistant
- **Speech Input**: Embedded **Web Speech API** widget (`mr-IN`, `hi-IN`, `en-IN`) for one-tap voice input directly from browser microphones (mobile & desktop), plus an audio file transcription fallback via `speech_recognition`.
- **Speech Output**: Automated audio player generation via Google Text-To-Speech (`gTTS`) in Marathi, Hindi, and English with persistent audio caching.

### 4. 🌤️ Weather Intelligence
- **Real-Time Data**: Live weather from Open-Meteo API for Palghar district and surrounding talukas (Dahanu, Vasai, Boisar, Wada, Jawhar, Mokhada, etc.).
- **Farming Advisory**: Contextual recommendations triggered by real temperature, humidity, rainfall forecasts, and wind speed.
- **7-Day Forecast**: Visual daily forecast with temperature swings, rainfall expectations, and weather icons.

### 5. 🏛️ Government Schemes
- Verified, up-to-date state and central farmer schemes:
  - **PM-KISAN** (₹6,000/yr)
  - **Namo Shetkari Mahasanman Nidhi** (Maharashtra state top-up ₹6,000/yr = ₹12,000/yr total)
  - **PM Fasal Bima Yojana** (Low premium crop insurance)
  - **Kisan Credit Card (KCC)** (Subsidized farm credit up to ₹3 Lakh)
  - **Soil Health Card Scheme** (Free soil nutrient testing)
  - **PM Kisan Maandhan Yojana** (Old-age farmer pension)
- Includes eligibility criteria, application steps, and direct official portal links.

### 6. 📊 Market Prices & Official MSP
- **Live APMC Mandi Data**: Queries open government Agmarknet data (`data.gov.in`) with graceful fallback to official portals (`msamb.com`, `agmarknet.gov.in`).
- **Official Government MSP**: 21 official Kharif & Rabi 2024-25 Minimum Support Price benchmarks (Paddy, Jowar, Bajra, Nagli, Soybean, Cotton, Tur, etc.) with instant search.

### 7. 🌱 My Farm Management
- SQLite-backed farm and crop tracker.
- Farmers can record crop varieties, area in acres, sowing dates, and custom agronomic notes.
- Instant deletion and record updating.

### 8. 👤 Profile & Authentication
- Secure SQLite user management with salted SHA-256 password hashing.
- Persistent session state, language preferences, and recent crop diagnosis logs.
- Quick farmer demo login (`farmer` / `farmer123`) and seamless guest browsing.

---

## 🚀 Running the Application

The app is already running live at:
- **Local URL**: [http://localhost:8501](http://localhost:8501)

To run or restart manually:
```bash
cd "C:\Users\Pratham\.gemini\antigravity\scratch\palghar-agri-ai"
python -m streamlit run app.py --server.port 8501 --server.headless true
```

To run the automated verification test suite:
```bash
python test_app.py
```
