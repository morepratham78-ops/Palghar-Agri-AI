"""
Configuration and translations for PALGHAR AGRI AI
"""
import os

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "palghar_agri.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
AUDIO_DIR = os.path.join(BASE_DIR, "audio_cache")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# ── API endpoints (free, no key needed) ────────────────────────────────
WEATHER_API = "https://api.open-meteo.com/v1/forecast"
AGMARKNET_API = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

# ── Ollama ─────────────────────────────────────────────────────────────
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2"

# ── Disease detection model ────────────────────────────────────────────
# We'll use a ResNet-based model fine-tuned on PlantVillage dataset
DISEASE_MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(DISEASE_MODEL_DIR, exist_ok=True)

# ── PlantVillage class labels (38 classes) ─────────────────────────────
PLANT_DISEASE_CLASSES = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy',
    'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)',
    'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy',
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
    'Raspberry___healthy', 'Rice___Brown_spot', 'Rice___Hispa', 'Rice___Leaf_Blast', 'Rice___healthy',
    'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy',
    'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight',
    'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy',
]

# ── Palghar / Maharashtra specific locations ──────────────────────────
PALGHAR_LOCATIONS = {
    "Palghar": {"lat": 19.6967, "lon": 72.7699},
    "Dahanu": {"lat": 19.9833, "lon": 72.7333},
    "Vasai": {"lat": 19.3919, "lon": 72.8397},
    "Boisar": {"lat": 19.8000, "lon": 72.7500},
    "Wada": {"lat": 19.6500, "lon": 73.1500},
    "Jawhar": {"lat": 19.9167, "lon": 73.2167},
    "Mokhada": {"lat": 19.8667, "lon": 73.3167},
    "Talasari": {"lat": 20.1000, "lon": 72.7000},
    "Vikramgad": {"lat": 19.8000, "lon": 73.1000},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Pune": {"lat": 18.5204, "lon": 73.8567},
    "Nashik": {"lat": 20.0000, "lon": 73.7800},
    "Nagpur": {"lat": 21.1458, "lon": 79.0882},
    "Kolhapur": {"lat": 16.7050, "lon": 74.2433},
}

# ── UI Translations ───────────────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "app_title": "🌾 PALGHAR AGRI AI",
        "app_subtitle": "Smart Farming Assistant",
        "welcome": "Welcome, Farmer!",
        "welcome_msg": "Your smart farming assistant for crop health, weather, market prices and more.",
        "crop_doctor": "🔬 Crop Doctor",
        "crop_doctor_desc": "Upload a photo of your crop to detect diseases",
        "weather": "🌤️ Weather",
        "weather_desc": "Check weather forecast for your area",
        "advisor": "🤖 AI Advisor",
        "advisor_desc": "Ask any farming question",
        "market": "📊 Market Prices",
        "market_desc": "Check current crop prices",
        "schemes": "🏛️ Govt. Schemes",
        "schemes_desc": "Government schemes for farmers",
        "my_farm": "🌱 My Farm",
        "my_farm_desc": "Manage your farm information",
        "profile": "👤 Profile",
        "language": "Language",
        "upload_image": "Upload crop photo",
        "take_photo": "Take a photo",
        "analyzing": "Analyzing your crop...",
        "disease_detected": "Disease Detected",
        "confidence": "Confidence",
        "healthy": "Your crop looks healthy! ✅",
        "symptoms": "Symptoms",
        "treatment": "Treatment",
        "prevention": "Prevention",
        "low_confidence_warning": "⚠️ The model is not very confident about this prediction. Please consult a local agriculture expert.",
        "ask_question": "Type your farming question here...",
        "send": "Send",
        "listening": "🎤 Listening...",
        "speak": "🔊 Listen",
        "select_location": "Select your location",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "rainfall": "Rainfall",
        "wind_speed": "Wind Speed",
        "farming_advice": "Farming Advice",
        "today": "Today",
        "forecast": "7-Day Forecast",
        "crop_name": "Crop Name",
        "area": "Area (acres)",
        "sowing_date": "Sowing Date",
        "add_crop": "Add Crop",
        "my_crops": "My Crops",
        "delete": "Delete",
        "login": "Login",
        "logout": "Logout",
        "register": "Register",
        "username": "Username",
        "password": "Password",
        "full_name": "Full Name",
        "phone": "Phone Number",
        "village": "Village / Town",
        "login_success": "Login successful!",
        "login_failed": "Invalid username or password",
        "register_success": "Registration successful! Please login.",
        "already_exists": "Username already exists",
        "search": "Search",
        "no_data": "No data available at the moment. Please try again later.",
        "loading": "Loading...",
        "error": "Something went wrong. Please try again.",
        "ollama_not_available": "AI advisor is not available right now. Please make sure Ollama is running.",
        "voice_input": "🎤 Speak",
        "voice_output": "🔊 Listen to answer",
        "select_crop": "Select Crop",
        "notes": "Notes",
        "save": "Save",
    },
    "hi": {
        "app_title": "🌾 पालघर कृषि AI",
        "app_subtitle": "स्मार्ट खेती सहायक",
        "welcome": "स्वागत है, किसान भाई!",
        "welcome_msg": "फसल स्वास्थ्य, मौसम, बाज़ार भाव और अन्य जानकारी के लिए आपका स्मार्ट खेती सहायक।",
        "crop_doctor": "🔬 फसल डॉक्टर",
        "crop_doctor_desc": "बीमारी पहचानने के लिए फसल की फोटो अपलोड करें",
        "weather": "🌤️ मौसम",
        "weather_desc": "अपने क्षेत्र का मौसम पूर्वानुमान देखें",
        "advisor": "🤖 AI सलाहकार",
        "advisor_desc": "खेती से जुड़ा कोई भी सवाल पूछें",
        "market": "📊 बाज़ार भाव",
        "market_desc": "फसलों के वर्तमान भाव देखें",
        "schemes": "🏛️ सरकारी योजनाएं",
        "schemes_desc": "किसानों के लिए सरकारी योजनाएं",
        "my_farm": "🌱 मेरा खेत",
        "my_farm_desc": "अपने खेत की जानकारी प्रबंधित करें",
        "profile": "👤 प्रोफ़ाइल",
        "language": "भाषा",
        "upload_image": "फसल की फोटो अपलोड करें",
        "take_photo": "फोटो लें",
        "analyzing": "आपकी फसल की जांच हो रही है...",
        "disease_detected": "बीमारी पहचानी गई",
        "confidence": "विश्वसनीयता",
        "healthy": "आपकी फसल स्वस्थ दिख रही है! ✅",
        "symptoms": "लक्षण",
        "treatment": "उपचार",
        "prevention": "रोकथाम",
        "low_confidence_warning": "⚠️ मॉडल को इस भविष्यवाणी पर ज़्यादा विश्वास नहीं है। कृपया स्थानीय कृषि विशेषज्ञ से संपर्क करें।",
        "ask_question": "अपना खेती का सवाल यहाँ लिखें...",
        "send": "भेजें",
        "listening": "🎤 सुन रहा हूँ...",
        "speak": "🔊 सुनें",
        "select_location": "अपना स्थान चुनें",
        "temperature": "तापमान",
        "humidity": "नमी",
        "rainfall": "बारिश",
        "wind_speed": "हवा की गति",
        "farming_advice": "खेती की सलाह",
        "today": "आज",
        "forecast": "7 दिन का पूर्वानुमान",
        "crop_name": "फसल का नाम",
        "area": "क्षेत्र (एकड़)",
        "sowing_date": "बुवाई की तारीख",
        "add_crop": "फसल जोड़ें",
        "my_crops": "मेरी फसलें",
        "delete": "हटाएं",
        "login": "लॉगिन",
        "logout": "लॉगआउट",
        "register": "पंजीकरण",
        "username": "यूज़रनेम",
        "password": "पासवर्ड",
        "full_name": "पूरा नाम",
        "phone": "फ़ोन नंबर",
        "village": "गाँव / शहर",
        "login_success": "लॉगिन सफल!",
        "login_failed": "गलत यूज़रनेम या पासवर्ड",
        "register_success": "पंजीकरण सफल! कृपया लॉगिन करें।",
        "already_exists": "यह यूज़रनेम पहले से मौजूद है",
        "search": "खोजें",
        "no_data": "अभी कोई जानकारी उपलब्ध नहीं है। कृपया बाद में पुनः प्रयास करें।",
        "loading": "लोड हो रहा है...",
        "error": "कुछ गड़बड़ हो गई। कृपया पुनः प्रयास करें।",
        "ollama_not_available": "AI सलाहकार अभी उपलब्ध नहीं है। कृपया सुनिश्चित करें कि Ollama चल रहा है।",
        "voice_input": "🎤 बोलें",
        "voice_output": "🔊 जवाब सुनें",
        "select_crop": "फसल चुनें",
        "notes": "नोट्स",
        "save": "सहेजें",
    },
    "mr": {
        "app_title": "🌾 पालघर कृषी AI",
        "app_subtitle": "स्मार्ट शेती सहाय्यक",
        "welcome": "स्वागत आहे, शेतकरी बंधू!",
        "welcome_msg": "पीक आरोग्य, हवामान, बाजारभाव आणि इतर माहितीसाठी तुमचा स्मार्ट शेती सहाय्यक.",
        "crop_doctor": "🔬 पीक डॉक्टर",
        "crop_doctor_desc": "रोग ओळखण्यासाठी पिकाचा फोटो अपलोड करा",
        "weather": "🌤️ हवामान",
        "weather_desc": "तुमच्या भागाचा हवामान अंदाज पहा",
        "advisor": "🤖 AI सल्लागार",
        "advisor_desc": "शेतीबद्दल कोणताही प्रश्न विचारा",
        "market": "📊 बाजारभाव",
        "market_desc": "पिकांचे सध्याचे भाव पहा",
        "schemes": "🏛️ सरकारी योजना",
        "schemes_desc": "शेतकऱ्यांसाठी सरकारी योजना",
        "my_farm": "🌱 माझं शेत",
        "my_farm_desc": "तुमच्या शेताची माहिती व्यवस्थापित करा",
        "profile": "👤 प्रोफाईल",
        "language": "भाषा",
        "upload_image": "पिकाचा फोटो अपलोड करा",
        "take_photo": "फोटो काढा",
        "analyzing": "तुमच्या पिकाची तपासणी होत आहे...",
        "disease_detected": "रोग ओळखला गेला",
        "confidence": "विश्वासार्हता",
        "healthy": "तुमचं पीक निरोगी दिसत आहे! ✅",
        "symptoms": "लक्षणे",
        "treatment": "उपचार",
        "prevention": "प्रतिबंध",
        "low_confidence_warning": "⚠️ मॉडेलला या अंदाजावर फारसा विश्वास नाही. कृपया स्थानिक कृषी तज्ञांशी संपर्क साधा.",
        "ask_question": "तुमचा शेतीचा प्रश्न इथे लिहा...",
        "send": "पाठवा",
        "listening": "🎤 ऐकत आहे...",
        "speak": "🔊 ऐका",
        "select_location": "तुमचं ठिकाण निवडा",
        "temperature": "तापमान",
        "humidity": "आर्द्रता",
        "rainfall": "पाऊस",
        "wind_speed": "वाऱ्याचा वेग",
        "farming_advice": "शेतीचा सल्ला",
        "today": "आज",
        "forecast": "7 दिवसांचा अंदाज",
        "crop_name": "पिकाचे नाव",
        "area": "क्षेत्र (एकर)",
        "sowing_date": "पेरणीची तारीख",
        "add_crop": "पीक जोडा",
        "my_crops": "माझी पिके",
        "delete": "काढून टाका",
        "login": "लॉगिन",
        "logout": "लॉगआउट",
        "register": "नोंदणी",
        "username": "यूज़रनेम",
        "password": "पासवर्ड",
        "full_name": "पूर्ण नाव",
        "phone": "फोन नंबर",
        "village": "गाव / शहर",
        "login_success": "लॉगिन यशस्वी!",
        "login_failed": "चुकीचं यूज़रनेम किंवा पासवर्ड",
        "register_success": "नोंदणी यशस्वी! कृपया लॉगिन करा.",
        "already_exists": "हे यूज़रनेम आधीपासून अस्तित्वात आहे",
        "search": "शोधा",
        "no_data": "सध्या माहिती उपलब्ध नाही. कृपया नंतर पुन्हा प्रयत्न करा.",
        "loading": "लोड होत आहे...",
        "error": "काहीतरी चूक झाली. कृपया पुन्हा प्रयत्न करा.",
        "ollama_not_available": "AI सल्लागार सध्या उपलब्ध नाही. कृपया Ollama चालू असल्याची खात्री करा.",
        "voice_input": "🎤 बोला",
        "voice_output": "🔊 उत्तर ऐका",
        "select_crop": "पीक निवडा",
        "notes": "नोट्स",
        "save": "जतन करा",
    },
}

# ── Disease info database (verified agricultural knowledge) ────────────
DISEASE_INFO = {
    "Apple___Apple_scab": {
        "en": {
            "name": "Apple Scab",
            "symptoms": "Dark, olive-green spots on leaves. Velvety or corky spots on fruit surface. Leaves may curl and drop early.",
            "treatment": "Apply fungicides like Mancozeb or Captan at green tip stage. Remove and destroy fallen leaves. Prune trees for better air circulation.",
            "prevention": "Plant resistant varieties. Maintain good orchard sanitation. Apply preventive fungicide sprays before rainy season."
        },
        "hi": {
            "name": "सेब का पपड़ी रोग",
            "symptoms": "पत्तियों पर गहरे जैतूनी-हरे धब्बे। फल की सतह पर मखमली या कॉर्की धब्बे। पत्तियाँ मुड़ सकती हैं और जल्दी गिर सकती हैं।",
            "treatment": "हरी कली अवस्था में मैंकोज़ेब या कैप्टन जैसी फफूंदनाशक दवा छिड़कें। गिरी हुई पत्तियाँ हटाकर नष्ट करें। बेहतर हवा के लिए पेड़ों की छँटाई करें।",
            "prevention": "प्रतिरोधी किस्में लगाएं। बगीचे की अच्छी सफ़ाई रखें। बारिश के मौसम से पहले निवारक फफूंदनाशक छिड़काव करें।"
        },
        "mr": {
            "name": "सफरचंद खरपटी रोग",
            "symptoms": "पानांवर गडद ऑलिव्ह-हिरवे डाग. फळाच्या पृष्ठभागावर मखमली किंवा कॉर्की डाग. पाने गुंडाळू शकतात आणि लवकर गळू शकतात.",
            "treatment": "हिरव्या कळी अवस्थेत मॅन्कोझेब किंवा कॅप्टन सारखी बुरशीनाशक फवारणी करा. गळालेली पाने गोळा करून नष्ट करा. हवा खेळण्यासाठी झाडांची छाटणी करा.",
            "prevention": "प्रतिरोधक जाती लावा. बागेची स्वच्छता ठेवा. पावसाळ्यापूर्वी प्रतिबंधात्मक बुरशीनाशक फवारणी करा."
        }
    },
    "Tomato___Late_blight": {
        "en": {
            "name": "Tomato Late Blight",
            "symptoms": "Large, irregular dark brown or black water-soaked spots on leaves. White fungal growth under leaves. Fruit develops firm brown lesions.",
            "treatment": "Apply copper-based fungicides (Bordeaux mixture). Remove and destroy infected plants immediately. Spray Metalaxyl or Mancozeb.",
            "prevention": "Avoid overhead irrigation. Use disease-free seeds. Ensure good spacing between plants. Rotate crops every season."
        },
        "hi": {
            "name": "टमाटर का झुलसा रोग",
            "symptoms": "पत्तियों पर बड़े, अनियमित गहरे भूरे या काले पानी भरे धब्बे। पत्तियों के नीचे सफेद फफूंद। फल पर सख्त भूरे घाव।",
            "treatment": "तांबा आधारित फफूंदनाशक (बोर्डो मिश्रण) का छिड़काव करें। संक्रमित पौधों को तुरंत हटाकर नष्ट करें। मेटालैक्सिल या मैंकोज़ेब का छिड़काव करें।",
            "prevention": "ऊपर से सिंचाई न करें। रोग मुक्त बीज का उपयोग करें। पौधों के बीच अच्छी दूरी रखें। हर मौसम में फसल चक्र अपनाएं।"
        },
        "mr": {
            "name": "टोमॅटो करपा रोग",
            "symptoms": "पानांवर मोठे, अनियमित गडद तपकिरी किंवा काळे पाणी भरलेले डाग. पानांच्या खाली पांढरी बुरशी. फळावर कठीण तपकिरी जखमा.",
            "treatment": "तांबे आधारित बुरशीनाशक (बोर्डो मिश्रण) फवारा. बाधित झाडे ताबडतोब काढून नष्ट करा. मेटालॅक्सिल किंवा मॅन्कोझेब फवारा.",
            "prevention": "वरून पाणी देणे टाळा. रोगमुक्त बियाणे वापरा. झाडांमध्ये चांगलं अंतर ठेवा. दर हंगामात पीक फेरपालट करा."
        }
    },
    "Tomato___Early_blight": {
        "en": {
            "name": "Tomato Early Blight",
            "symptoms": "Dark brown spots with concentric rings (target-like pattern) on lower leaves first. Leaves turn yellow and drop. Fruit may show dark leathery spots.",
            "treatment": "Apply Mancozeb or Chlorothalonil fungicide every 7-10 days. Remove infected lower leaves. Mulch around plants to prevent soil splash.",
            "prevention": "Use certified disease-free seeds. Practice 2-3 year crop rotation. Avoid wetting leaves during irrigation. Stake plants for air circulation."
        },
        "hi": {
            "name": "टमाटर का अगेती झुलसा",
            "symptoms": "निचली पत्तियों पर पहले गहरे भूरे धब्बे जिनमें गोलाकार छल्ले (निशाना जैसा) दिखते हैं। पत्तियाँ पीली होकर गिरती हैं। फल पर गहरे चमड़ी जैसे धब्बे।",
            "treatment": "हर 7-10 दिन में मैंकोज़ेब या क्लोरोथैलोनिल फफूंदनाशक छिड़कें। संक्रमित निचली पत्तियाँ हटाएं। मिट्टी के छींटे रोकने के लिए मल्च बिछाएं।",
            "prevention": "प्रमाणित रोग मुक्त बीज का उपयोग करें। 2-3 साल का फसल चक्र अपनाएं। सिंचाई में पत्तियाँ गीली न करें। हवा के लिए पौधों को सहारा दें।"
        },
        "mr": {
            "name": "टोमॅटो लवकर करपा",
            "symptoms": "खालच्या पानांवर आधी गडद तपकिरी डाग ज्यात गोलाकार कडे (निशाणासारखे) दिसतात. पाने पिवळी होऊन गळतात. फळावर गडद चामड्यासारखे डाग.",
            "treatment": "दर 7-10 दिवसांनी मॅन्कोझेब किंवा क्लोरोथॅलोनिल बुरशीनाशक फवारा. बाधित खालची पाने काढा. मातीचे शिंतोडे रोखण्यासाठी आच्छादन करा.",
            "prevention": "प्रमाणित रोगमुक्त बियाणे वापरा. 2-3 वर्षांचा पीक फेरपालट करा. पाणी देताना पाने ओली करू नका. हवा खेळण्यासाठी झाडांना आधार द्या."
        }
    },
    "Potato___Early_blight": {
        "en": {
            "name": "Potato Early Blight",
            "symptoms": "Brown to black spots with concentric rings on older leaves. Spots may merge causing large dead areas. Tubers may show dark sunken spots.",
            "treatment": "Spray Mancozeb or Chlorothalonil at first sign of disease. Remove heavily infected leaves. Ensure adequate potassium fertilization.",
            "prevention": "Use resistant varieties like Kufri Jyoti. Practice crop rotation. Plant certified seed potatoes. Avoid planting in poorly drained soil."
        },
        "hi": {
            "name": "आलू का अगेती झुलसा",
            "symptoms": "पुरानी पत्तियों पर भूरे से काले धब्बे जिनमें गोलाकार छल्ले होते हैं। धब्बे मिलकर बड़े मृत क्षेत्र बनाते हैं। कंदों पर गहरे धंसे धब्बे।",
            "treatment": "रोग के पहले लक्षण पर मैंकोज़ेब या क्लोरोथैलोनिल छिड़कें। बहुत संक्रमित पत्तियाँ हटाएं। पर्याप्त पोटाश खाद दें।",
            "prevention": "कुफरी ज्योति जैसी प्रतिरोधी किस्में लगाएं। फसल चक्र अपनाएं। प्रमाणित बीज आलू लगाएं। खराब जल निकास वाली मिट्टी से बचें।"
        },
        "mr": {
            "name": "बटाटा लवकर करपा",
            "symptoms": "जुन्या पानांवर गोलाकार कड्यांसह तपकिरी ते काळे डाग. डाग एकत्र येऊन मोठे मृत भाग तयार होतात. कंदांवर गडद बुडालेले डाग.",
            "treatment": "रोगाच्या पहिल्या लक्षणावर मॅन्कोझेब किंवा क्लोरोथॅलोनिल फवारा. जास्त बाधित पाने काढा. पुरेसे पोटॅश खत द्या.",
            "prevention": "कुफरी ज्योती सारख्या प्रतिरोधक जाती लावा. पीक फेरपालट करा. प्रमाणित बियाणे बटाटे लावा. खराब निचऱ्याच्या जमिनीत लागवड टाळा."
        }
    },
    "Potato___Late_blight": {
        "en": {
            "name": "Potato Late Blight",
            "symptoms": "Dark water-soaked spots on leaves that spread rapidly. White fuzzy growth under leaves in humid weather. Tubers rot with reddish-brown granular flesh.",
            "treatment": "Apply Metalaxyl + Mancozeb immediately. Destroy all infected plant material. Do not harvest in wet conditions.",
            "prevention": "Plant resistant varieties. Avoid overhead irrigation. Hill up soil around plants. Monitor fields closely in cool wet weather."
        },
        "hi": {
            "name": "आलू का पछेती झुलसा",
            "symptoms": "पत्तियों पर गहरे पानी भरे धब्बे जो तेज़ी से फैलते हैं। नमी में पत्तियों के नीचे सफेद रोएंदार फफूंद। कंद सड़कर लाल-भूरे दानेदार गूदे वाले हो जाते हैं।",
            "treatment": "तुरंत मेटालैक्सिल + मैंकोज़ेब छिड़कें। सभी संक्रमित पौधे नष्ट करें। गीली स्थिति में कटाई न करें।",
            "prevention": "प्रतिरोधी किस्में लगाएं। ऊपर से सिंचाई न करें। पौधों के चारों ओर मिट्टी चढ़ाएं। ठंडे नम मौसम में खेत की बारीकी से निगरानी करें।"
        },
        "mr": {
            "name": "बटाटा उशीरा करपा",
            "symptoms": "पानांवर गडद पाणी भरलेले डाग जे वेगाने पसरतात. दमट हवामानात पानांखाली पांढरी रोयासारखी बुरशी. कंद सडून लाल-तपकिरी दाणेदार गर होतो.",
            "treatment": "ताबडतोब मेटालॅक्सिल + मॅन्कोझेब फवारा. सर्व बाधित रोपे नष्ट करा. ओल्या परिस्थितीत काढणी करू नका.",
            "prevention": "प्रतिरोधक जाती लावा. वरून पाणी देणे टाळा. झाडांभोवती माती चढवा. थंड ओल्या हवामानात शेताची बारकाईने तपासणी करा."
        }
    },
    "Corn_(maize)___Common_rust_": {
        "en": {
            "name": "Corn Common Rust",
            "symptoms": "Small reddish-brown raised pustules on both leaf surfaces. Pustules release powdery rust-colored spores when rubbed.",
            "treatment": "Apply fungicides like Propiconazole or Mancozeb if infection is severe and early. Usually not needed if infection occurs late in the season.",
            "prevention": "Plant rust-resistant hybrids. Early planting reduces infection risk. Monitor fields regularly during humid weather."
        },
        "hi": {
            "name": "मक्का सामान्य रतुआ रोग",
            "symptoms": "पत्तियों के दोनों तरफ छोटे लाल-भूरे उभरे हुए दाने। रगड़ने पर जंग के रंग के पाउडर जैसे बीजाणु निकलते हैं।",
            "treatment": "गंभीर और शुरुआती संक्रमण में प्रोपिकोनाज़ोल या मैंकोज़ेब फफूंदनाशक छिड़कें। मौसम में देर से संक्रमण होने पर आमतौर पर ज़रूरत नहीं।",
            "prevention": "रतुआ प्रतिरोधी संकर किस्में लगाएं। जल्दी बुवाई से संक्रमण का खतरा कम होता है। नमी वाले मौसम में खेत की नियमित निगरानी करें।"
        },
        "mr": {
            "name": "मका सामान्य तांबेरा रोग",
            "symptoms": "पानांच्या दोन्ही बाजूंवर लहान लाल-तपकिरी उभारलेले पुटकुळे. चोळल्यावर गंजासारख्या रंगाचे पावडर बीजाणू बाहेर येतात.",
            "treatment": "गंभीर आणि सुरुवातीच्या बाधेसाठी प्रोपिकोनॅझोल किंवा मॅन्कोझेब बुरशीनाशक फवारा. हंगामात उशीरा बाधा झाल्यास सहसा गरज नाही.",
            "prevention": "तांबेरा प्रतिरोधक संकरित जाती लावा. लवकर पेरणीने बाधेचा धोका कमी होतो. दमट हवामानात शेताची नियमित तपासणी करा."
        }
    },
    "Rice___Leaf_Blast": {
        "en": {
            "name": "Rice Leaf Blast",
            "symptoms": "Diamond-shaped lesions with gray centers and brown borders on leaves. Spots can kill entire leaves. Neck blast can break panicles.",
            "treatment": "Apply Tricyclazole or Isoprothiolane fungicide. Drain standing water. Apply potassium and reduce nitrogen fertilizer.",
            "prevention": "Use resistant varieties (like Pusa Basmati 1509). Avoid excessive nitrogen. Maintain proper water management. Space seedlings adequately."
        },
        "hi": {
            "name": "धान का ब्लास्ट रोग",
            "symptoms": "पत्तियों पर भूरी किनारी वाले हीरे के आकार के हल्के भूरे धब्बे। धब्बे पूरी पत्ती को मार सकते हैं। गर्दन ब्लास्ट बालियों को तोड़ सकता है।",
            "treatment": "ट्राइसाइक्लाज़ोल या आइसोप्रोथियोलेन फफूंदनाशक छिड़कें। खड़ा पानी निकालें। पोटाश दें और नाइट्रोजन खाद कम करें।",
            "prevention": "प्रतिरोधी किस्में (जैसे पूसा बासमती 1509) लगाएं। अत्यधिक नाइट्रोजन से बचें। उचित जल प्रबंधन रखें। पौधों में पर्याप्त दूरी रखें।"
        },
        "mr": {
            "name": "भात करपा (ब्लास्ट) रोग",
            "symptoms": "पानांवर तपकिरी कडा असलेले हिऱ्याच्या आकाराचे राखाडी डाग. डाग संपूर्ण पान मारू शकतात. मानेचा करपा लोंब्या तोडू शकतो.",
            "treatment": "ट्रायसायक्लॅझोल किंवा आयसोप्रोथिओलेन बुरशीनाशक फवारा. साचलेलं पाणी काढा. पोटॅश द्या आणि नायट्रोजन खत कमी करा.",
            "prevention": "प्रतिरोधक जाती (जसे पुसा बासमती 1509) लावा. जास्त नायट्रोजन टाळा. योग्य पाणी व्यवस्थापन ठेवा. रोपांमध्ये पुरेसं अंतर ठेवा."
        }
    },
    "Rice___Brown_spot": {
        "en": {
            "name": "Rice Brown Spot",
            "symptoms": "Oval brown spots on leaves with gray or white centers. Seeds may be discolored. Severe infection causes poor grain filling.",
            "treatment": "Spray Mancozeb or Propiconazole. Apply balanced fertilizers especially potash. Use seed treatment with Carbendazim before sowing.",
            "prevention": "Use certified disease-free seeds. Maintain balanced soil nutrition. Avoid water stress. Practice crop rotation."
        },
        "hi": {
            "name": "धान का भूरा धब्बा रोग",
            "symptoms": "पत्तियों पर भूरे अंडाकार धब्बे जिनके केंद्र में भूरा या सफेद होता है। बीज रंगहीन हो सकते हैं। गंभीर संक्रमण से दाने खराब भरते हैं।",
            "treatment": "मैंकोज़ेब या प्रोपिकोनाज़ोल छिड़कें। संतुलित खाद विशेषकर पोटाश दें। बुवाई से पहले कार्बेन्डाजिम से बीजोपचार करें।",
            "prevention": "प्रमाणित रोग मुक्त बीज का उपयोग करें। मिट्टी में संतुलित पोषण रखें। पानी की कमी न होने दें। फसल चक्र अपनाएं।"
        },
        "mr": {
            "name": "भात तपकिरी ठिपका रोग",
            "symptoms": "पानांवर राखाडी किंवा पांढऱ्या मध्यभागी असलेले अंडाकृती तपकिरी डाग. बियाणे रंगहीन होऊ शकतात. गंभीर बाधेमुळे दाणे नीट भरत नाहीत.",
            "treatment": "मॅन्कोझेब किंवा प्रोपिकोनॅझोल फवारा. संतुलित खते विशेषतः पोटॅश द्या. पेरणीपूर्वी कार्बेन्डॅझिम ने बीजप्रक्रिया करा.",
            "prevention": "प्रमाणित रोगमुक्त बियाणे वापरा. जमिनीत संतुलित पोषण ठेवा. पाण्याचा ताण येऊ देऊ नका. पीक फेरपालट करा."
        }
    },
    "Grape___Black_rot": {
        "en": {
            "name": "Grape Black Rot",
            "symptoms": "Circular reddish-brown spots on leaves. Fruit turns brown then black and shrivels into hard mummies. Shoots may show elongated dark lesions.",
            "treatment": "Apply Mancozeb or Myclobutanil before bloom and after petal fall. Remove all mummified fruit from vines and ground.",
            "prevention": "Prune for good air circulation. Remove and destroy all mummified berries. Maintain regular spray schedule during wet periods."
        },
        "hi": {
            "name": "अंगूर का काला सड़न रोग",
            "symptoms": "पत्तियों पर गोलाकार लालिमा-भूरे धब्बे। फल भूरे फिर काले होकर सूखकर सख्त हो जाते हैं। टहनियों पर लंबे गहरे घाव।",
            "treatment": "फूल आने से पहले और पंखुड़ी गिरने के बाद मैंकोज़ेब या मायक्लोब्यूटानिल छिड़कें। सभी ममीफाइड फल बेलों और ज़मीन से हटाएं।",
            "prevention": "अच्छी हवा के लिए छँटाई करें। सभी सूखे सड़े दानें हटाकर नष्ट करें। गीले मौसम में नियमित छिड़काव करें।"
        },
        "mr": {
            "name": "द्राक्ष काळा कुज रोग",
            "symptoms": "पानांवर गोलाकार लालसर-तपकिरी डाग. फळे तपकिरी मग काळी होऊन आटून कठीण ममी बनतात. फांद्यांवर लांबट गडद जखमा.",
            "treatment": "फुलोऱ्यापूर्वी आणि पाकळ्या गळल्यानंतर मॅन्कोझेब किंवा मायक्लोब्यूटॅनिल फवारा. वेलांवरील आणि जमिनीवरील सर्व ममीफाइड फळे काढा.",
            "prevention": "हवा खेळण्यासाठी छाटणी करा. सर्व सुकलेली कुजलेली फळे काढून नष्ट करा. ओल्या हवामानात नियमित फवारणी करा."
        }
    },
    "Pepper,_bell___Bacterial_spot": {
        "en": {
            "name": "Bell Pepper Bacterial Spot",
            "symptoms": "Small dark water-soaked spots on leaves that enlarge and turn brown. Raised scabby spots on fruit. Severe defoliation possible.",
            "treatment": "Apply copper-based bactericides. Remove and destroy infected plants. Avoid working in wet fields.",
            "prevention": "Use disease-free seeds and transplants. Practice crop rotation with non-solanaceous crops. Avoid overhead irrigation."
        },
        "hi": {
            "name": "शिमला मिर्च का जीवाणु धब्बा रोग",
            "symptoms": "पत्तियों पर छोटे गहरे पानी भरे धब्बे जो बड़े होकर भूरे हो जाते हैं। फल पर उभरे पपड़ीदार धब्बे। गंभीर पत्ती झड़ना संभव।",
            "treatment": "तांबा आधारित जीवाणुनाशक छिड़कें। संक्रमित पौधे हटाकर नष्ट करें। गीले खेत में काम करने से बचें।",
            "prevention": "रोग मुक्त बीज और पौध का उपयोग करें। गैर-सोलेनेसी फसलों के साथ फसल चक्र अपनाएं। ऊपर से सिंचाई न करें।"
        },
        "mr": {
            "name": "ढोबळी मिरची जिवाणू ठिपका रोग",
            "symptoms": "पानांवर लहान गडद पाणी भरलेले डाग जे मोठे होऊन तपकिरी होतात. फळावर उभरलेले खरपटी डाग. गंभीर पानगळ शक्य.",
            "treatment": "तांबे आधारित जिवाणूनाशक फवारा. बाधित झाडे काढून नष्ट करा. ओल्या शेतात काम करणे टाळा.",
            "prevention": "रोगमुक्त बियाणे आणि रोपे वापरा. सोलॅनेसी नसलेल्या पिकांसोबत पीक फेरपालट करा. वरून पाणी देणे टाळा."
        }
    },
}

# Generic fallback for diseases not in above database
GENERIC_DISEASE_ADVICE = {
    "en": {
        "symptoms": "Visible spots, discoloration, wilting, or abnormal growth patterns on the plant.",
        "treatment": "Consult your nearest Krishi Vigyan Kendra (KVK) or agricultural officer with a sample of the affected plant. General measures include removing infected parts and applying appropriate fungicide/pesticide.",
        "prevention": "Use certified seeds, practice crop rotation, maintain proper spacing, avoid waterlogging, and keep your fields clean."
    },
    "hi": {
        "symptoms": "पौधे पर दिखाई देने वाले धब्बे, रंग बदलना, मुरझाना, या असामान्य बढ़ोतरी के पैटर्न।",
        "treatment": "प्रभावित पौधे का नमूना लेकर अपने नज़दीकी कृषि विज्ञान केंद्र (KVK) या कृषि अधिकारी से संपर्क करें। सामान्य उपाय - संक्रमित हिस्से हटाएं और उचित फफूंदनाशक/कीटनाशक छिड़कें।",
        "prevention": "प्रमाणित बीज का उपयोग करें, फसल चक्र अपनाएं, उचित दूरी रखें, जलभराव से बचें और खेत साफ़ रखें।"
    },
    "mr": {
        "symptoms": "पिकावर दिसणारे डाग, रंग बदलणे, कोमेजणे किंवा असामान्य वाढीचे नमुने.",
        "treatment": "बाधित पिकाचा नमुना घेऊन जवळच्या कृषी विज्ञान केंद्र (KVK) किंवा कृषी अधिकाऱ्यांशी संपर्क साधा. सामान्य उपाय - बाधित भाग काढा आणि योग्य बुरशीनाशक/कीटकनाशक फवारा.",
        "prevention": "प्रमाणित बियाणे वापरा, पीक फेरपालट करा, योग्य अंतर ठेवा, पाणी साचू देऊ नका आणि शेत स्वच्छ ठेवा."
    }
}

# ── Government Schemes (Verified data) ─────────────────────────────────
GOVT_SCHEMES = [
    {
        "en": {
            "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
            "description": "₹6,000 per year in 3 installments of ₹2,000 directly to farmer's bank account.",
            "eligibility": "All landholding farmer families.",
            "how_to_apply": "Visit pmkisan.gov.in or contact your local Talathi/Patwari office.",
            "website": "https://pmkisan.gov.in"
        },
        "hi": {
            "name": "PM-KISAN (प्रधानमंत्री किसान सम्मान निधि)",
            "description": "किसान के बैंक खाते में सीधे ₹2,000 की 3 किस्तों में प्रति वर्ष ₹6,000।",
            "eligibility": "सभी भूमिधारक किसान परिवार।",
            "how_to_apply": "pmkisan.gov.in पर जाएं या अपने स्थानीय तलाठी/पटवारी कार्यालय से संपर्क करें।",
            "website": "https://pmkisan.gov.in"
        },
        "mr": {
            "name": "PM-KISAN (प्रधानमंत्री किसान सन्मान निधी)",
            "description": "शेतकऱ्याच्या बँक खात्यात थेट ₹2,000 च्या 3 हप्त्यांमध्ये वार्षिक ₹6,000.",
            "eligibility": "सर्व जमीनधारक शेतकरी कुटुंबे.",
            "how_to_apply": "pmkisan.gov.in ला भेट द्या किंवा तुमच्या स्थानिक तलाठी कार्यालयाशी संपर्क साधा.",
            "website": "https://pmkisan.gov.in"
        }
    },
    {
        "en": {
            "name": "PM Fasal Bima Yojana (Crop Insurance)",
            "description": "Crop insurance at very low premium: 2% for Kharif, 1.5% for Rabi, 5% for commercial crops.",
            "eligibility": "All farmers growing notified crops in notified areas.",
            "how_to_apply": "Apply through your bank, CSC center, or pmfby.gov.in before the deadline each season.",
            "website": "https://pmfby.gov.in"
        },
        "hi": {
            "name": "PM फसल बीमा योजना",
            "description": "बहुत कम प्रीमियम पर फसल बीमा: खरीफ 2%, रबी 1.5%, व्यावसायिक फसलें 5%।",
            "eligibility": "अधिसूचित क्षेत्रों में अधिसूचित फसलें उगाने वाले सभी किसान।",
            "how_to_apply": "हर मौसम की समय सीमा से पहले अपने बैंक, CSC केंद्र या pmfby.gov.in के माध्यम से आवेदन करें।",
            "website": "https://pmfby.gov.in"
        },
        "mr": {
            "name": "PM पीक विमा योजना",
            "description": "अत्यंत कमी प्रीमियमवर पीक विमा: खरीप 2%, रब्बी 1.5%, नगदी पिके 5%.",
            "eligibility": "अधिसूचित क्षेत्रात अधिसूचित पिके घेणारे सर्व शेतकरी.",
            "how_to_apply": "प्रत्येक हंगामाच्या अंतिम तारखेपूर्वी तुमच्या बँक, CSC केंद्र किंवा pmfby.gov.in द्वारे अर्ज करा.",
            "website": "https://pmfby.gov.in"
        }
    },
    {
        "en": {
            "name": "Kisan Credit Card (KCC)",
            "description": "Affordable credit up to ₹3 lakh at 4% interest (with subsidy) for crop cultivation, post-harvest, and farm maintenance.",
            "eligibility": "All farmers, sharecroppers, tenant farmers, and self-help groups.",
            "how_to_apply": "Apply at your nearest bank (Nationalized, Cooperative, or Regional Rural Bank) with land records.",
            "website": "https://www.pmkisan.gov.in/KCC"
        },
        "hi": {
            "name": "किसान क्रेडिट कार्ड (KCC)",
            "description": "फसल खेती, कटाई के बाद और खेत रखरखाव के लिए 4% ब्याज (सब्सिडी के साथ) पर ₹3 लाख तक सस्ता ऋण।",
            "eligibility": "सभी किसान, बटाईदार, काश्तकार, और स्वयं सहायता समूह।",
            "how_to_apply": "भूमि रिकॉर्ड के साथ अपने नज़दीकी बैंक (राष्ट्रीयकृत, सहकारी, या क्षेत्रीय ग्रामीण बैंक) में आवेदन करें।",
            "website": "https://www.pmkisan.gov.in/KCC"
        },
        "mr": {
            "name": "किसान क्रेडिट कार्ड (KCC)",
            "description": "पीक लागवड, काढणीनंतर आणि शेत देखभालीसाठी 4% व्याजदराने (अनुदानासह) ₹3 लाखांपर्यंत स्वस्त कर्ज.",
            "eligibility": "सर्व शेतकरी, भागीदार शेतकरी, भाडेकरू शेतकरी आणि बचत गट.",
            "how_to_apply": "जमीन रेकॉर्डसह तुमच्या जवळच्या बँकेत (राष्ट्रीयीकृत, सहकारी किंवा प्रादेशिक ग्रामीण बँक) अर्ज करा.",
            "website": "https://www.pmkisan.gov.in/KCC"
        }
    },
    {
        "en": {
            "name": "Soil Health Card Scheme",
            "description": "Free soil testing and recommendations for fertilizers and nutrients every 2 years.",
            "eligibility": "All farmers.",
            "how_to_apply": "Contact your nearest KVK or agriculture department. Collect soil sample and submit for testing.",
            "website": "https://soilhealth.dac.gov.in"
        },
        "hi": {
            "name": "मृदा स्वास्थ्य कार्ड योजना",
            "description": "हर 2 साल में मुफ्त मिट्टी परीक्षण और खाद एवं पोषक तत्वों की सिफारिशें।",
            "eligibility": "सभी किसान।",
            "how_to_apply": "अपने नज़दीकी KVK या कृषि विभाग से संपर्क करें। मिट्टी का नमूना लेकर परीक्षण के लिए जमा करें।",
            "website": "https://soilhealth.dac.gov.in"
        },
        "mr": {
            "name": "मृदा आरोग्य पत्रिका योजना",
            "description": "दर 2 वर्षांनी मोफत माती परीक्षण आणि खतं व पोषक तत्वांच्या शिफारसी.",
            "eligibility": "सर्व शेतकरी.",
            "how_to_apply": "तुमच्या जवळच्या KVK किंवा कृषी विभागाशी संपर्क साधा. मातीचा नमुना घेऊन तपासणीसाठी जमा करा.",
            "website": "https://soilhealth.dac.gov.in"
        }
    },
    {
        "en": {
            "name": "Maharashtra Shetkari Yojana (Namo Shetkari Mahasanman Nidhi)",
            "description": "₹6,000 per year additional to PM-KISAN (total ₹12,000/year) from Maharashtra state government.",
            "eligibility": "All eligible PM-KISAN beneficiary farmers in Maharashtra.",
            "how_to_apply": "No separate application. Automatically paid to PM-KISAN beneficiaries in Maharashtra.",
            "website": "https://nsmny.mahait.org"
        },
        "hi": {
            "name": "महाराष्ट्र शेतकरी योजना (नमो शेतकरी महासन्मान निधी)",
            "description": "PM-KISAN के अतिरिक्त प्रति वर्ष ₹6,000 (कुल ₹12,000/वर्ष) महाराष्ट्र राज्य सरकार से।",
            "eligibility": "महाराष्ट्र में सभी पात्र PM-KISAN लाभार्थी किसान।",
            "how_to_apply": "अलग आवेदन की आवश्यकता नहीं। महाराष्ट्र में PM-KISAN लाभार्थियों को स्वचालित भुगतान।",
            "website": "https://nsmny.mahait.org"
        },
        "mr": {
            "name": "नमो शेतकरी महासन्मान निधी योजना",
            "description": "PM-KISAN व्यतिरिक्त वार्षिक ₹6,000 (एकूण ₹12,000/वर्ष) महाराष्ट्र राज्य सरकारकडून.",
            "eligibility": "महाराष्ट्रातील सर्व पात्र PM-KISAN लाभार्थी शेतकरी.",
            "how_to_apply": "वेगळ्या अर्जाची गरज नाही. महाराष्ट्रातील PM-KISAN लाभार्थ्यांना स्वयंचलित भुगतान.",
            "website": "https://nsmny.mahait.org"
        }
    },
    {
        "en": {
            "name": "PM Kisan Maandhan Yojana (Pension)",
            "description": "₹3,000 monthly pension after age 60. Farmer contributes ₹55-200/month based on entry age.",
            "eligibility": "Small and marginal farmers aged 18-40 with cultivable land up to 2 hectares.",
            "how_to_apply": "Visit nearest CSC center or pmkmy.gov.in with Aadhaar and bank details.",
            "website": "https://pmkmy.gov.in"
        },
        "hi": {
            "name": "PM किसान मानधन योजना (पेंशन)",
            "description": "60 वर्ष की आयु के बाद ₹3,000 मासिक पेंशन। किसान प्रवेश आयु के अनुसार ₹55-200/माह योगदान करता है।",
            "eligibility": "2 हेक्टेयर तक खेती योग्य भूमि वाले 18-40 आयु के छोटे और सीमांत किसान।",
            "how_to_apply": "आधार और बैंक विवरण के साथ नज़दीकी CSC केंद्र या pmkmy.gov.in पर जाएं।",
            "website": "https://pmkmy.gov.in"
        },
        "mr": {
            "name": "PM किसान मानधन योजना (पेन्शन)",
            "description": "60 वर्षांनंतर दरमहा ₹3,000 पेन्शन. शेतकरी प्रवेश वयानुसार दरमहा ₹55-200 योगदान देतो.",
            "eligibility": "2 हेक्टरपर्यंत लागवडयोग्य जमीन असलेले 18-40 वयोगटातील अल्प आणि सीमांत शेतकरी.",
            "how_to_apply": "आधार आणि बँक तपशीलांसह जवळच्या CSC केंद्राला भेट द्या किंवा pmkmy.gov.in वर जा.",
            "website": "https://pmkmy.gov.in"
        }
    },
]

# ── Common crops in Palghar/Maharashtra ────────────────────────────────
COMMON_CROPS = [
    "Rice / भात / धान", "Wheat / गहू / गेहूं", "Jowar / ज्वारी / ज्वार",
    "Bajra / बाजरी / बाजरा", "Maize / मका / मक्का", "Ragi / नाचणी / रागी",
    "Tur (Pigeon Pea) / तूर / तूर दाल", "Moong / मूग / मूंग",
    "Urad / उडीद / उड़द", "Groundnut / भुईमूग / मूंगफली",
    "Soybean / सोयाबीन", "Cotton / कापूस / कपास",
    "Sugarcane / ऊस / गन्ना", "Onion / कांदा / प्याज़",
    "Tomato / टोमॅटो / टमाटर", "Potato / बटाटा / आलू",
    "Chilli / मिरची / मिर्च", "Banana / केळी / केला",
    "Mango / आंबा / आम", "Coconut / नारळ / नारियल",
    "Cashew / काजू", "Chickoo / चिकू", "Grapes / द्राक्षे / अंगूर",
    "Other / इतर / अन्य"
]
