"""
AI Advisor service using Ollama with Llama 3.2.
Provides local, privacy-preserving, farmer-friendly agricultural advisory in Marathi, Hindi, and English.
"""
import requests
import json
from config import OLLAMA_URL, OLLAMA_MODEL


def get_available_models() -> list:
    """Get list of available Ollama models."""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        if resp.status_code == 200:
            return [m.get("name", "") for m in resp.json().get("models", [])]
        return []
    except Exception:
        return []


def get_best_model_name() -> str:
    """Find the best matching model installed in Ollama."""
    models = get_available_models()
    if not models:
        return OLLAMA_MODEL
        
    # Priority order
    priorities = [
        "llama3.2:latest",
        "llama3.2:3b",
        "llama3.2",
        "llama3.1:latest",
        "llama3.1:8b",
        "llama3:8b",
        "llama3:latest",
    ]
    for p in priorities:
        if p in models:
            return p
            
    # Substring matching for any llama3.2
    for m in models:
        if "llama3.2" in m:
            return m
    for m in models:
        if "llama3" in m:
            return m
            
    return models[0] if models else OLLAMA_MODEL


def is_ollama_available() -> bool:
    """Check if Ollama is running and has any compatible model."""
    try:
        models = get_available_models()
        return len(models) > 0
    except Exception:
        return False


def build_system_prompt(lang: str = "en", context: str = "") -> str:
    lang_instructions = {
        "en": "Respond strictly in simple English that an Indian farmer can understand easily.",
        "hi": "सरल और स्पष्ट हिंदी (देवनागरी लिपि) में जवाब दें जो एक सामान्य किसान आसानी से समझ सके।",
        "mr": "सोप्या आणि स्पष्ट मराठीत (देवनागरी लिपी) उत्तर द्या जे महाराष्ट्रातील शेतकरी सहज समजू शकेल.",
    }
    
    return f"""You are 'PALGHAR AGRI AI', an expert agricultural assistant specifically designed for farmers in Maharashtra, India (especially Palghar, Thane, Konkan and Western Maharashtra).
You provide highly practical, crop-specific, climate-aware guidance.

Language Requirement:
{lang_instructions.get(lang, lang_instructions['en'])}

Guidelines:
1. Provide concise, clear, and actionable answers (bullet points preferred for steps).
2. Consider local crops: Paddy (भात / धान), Nagli/Ragi (नाचणी), Mango (हापूस/केसर), Cashew (काजू), Chickoo (Dahanu Gholvad चिकू), Jasmine flowers, Vegetables (Tomato, Brinjal, Chilli), and Pulses.
3. Keep seasonal weather in mind (Konkan coastal rains, high humidity, red/laterite soils, coastal salinity).
4. Emphasize organic and low-cost natural farming practices alongside balanced chemical inputs when necessary.
5. If medical emergency or toxic chemical poisoning occurs, recommend immediate medical attention.
{f'Context information: {context}' if context else ''}"""


def ask_advisor(question: str, lang: str = "en", context: str = "") -> str:
    """Ask the AI advisor a farming question synchronously."""
    model_name = get_best_model_name()
    system_prompt = build_system_prompt(lang, context)

    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": question,
                "system": system_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.6,
                    "num_predict": 450,
                }
            },
            timeout=90,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return _get_offline_message(lang)
    except requests.exceptions.Timeout:
        return _get_timeout_message(lang)
    except Exception as e:
        return _get_error_message(lang, str(e))


def ask_advisor_streaming(question: str, lang: str = "en", context: str = ""):
    """Stream response from AI advisor in real-time."""
    model_name = get_best_model_name()
    system_prompt = build_system_prompt(lang, context)

    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": question,
                "system": system_prompt,
                "stream": True,
                "options": {
                    "temperature": 0.6,
                    "num_predict": 450,
                }
            },
            timeout=90,
            stream=True,
        )
        resp.raise_for_status()
        
        for line in resp.iter_lines():
            if line:
                try:
                    data = json.loads(line)
                    token = data.get("response", "")
                    if token:
                        yield token
                    if data.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue
    except requests.exceptions.ConnectionError:
        yield _get_offline_message(lang)
    except Exception as e:
        yield _get_error_message(lang, str(e))


def get_disease_advice(disease_name: str, crop: str, lang: str = "en") -> str:
    """Get AI-generated advisory about a detected disease."""
    prompts = {
        "en": f"A farmer's {crop} crop has been diagnosed with {disease_name}. Give practical immediate steps, organic treatments, and prevention tips for Maharashtra conditions.",
        "hi": f"एक किसान के {crop} की फसल में {disease_name} रोग पहचाना गया है। महाराष्ट्र की परिस्थितियों के अनुसार तुरंत किए जाने वाले उपाय, जैविक उपचार और रोकथाम के नुस्खे बताएं।",
        "mr": f"एका शेतकऱ्याच्या {crop} पिकात {disease_name} रोग आढळला आहे. महाराष्ट्रातील परिस्थितीनुसार तात्काळ उपाययोजना, सेंद्रिय औषधोपचार आणि पुढील काळजी याबद्दल मार्गदर्शन करा.",
    }
    return ask_advisor(prompts.get(lang, prompts["en"]), lang=lang)


def _get_offline_message(lang: str) -> str:
    msgs = {
        "en": "⚠️ AI Advisor is offline. Please make sure Ollama is running (`ollama serve`).",
        "hi": "⚠️ AI सलाहकार ऑफ़लाइन है। कृपया सुनिश्चित करें कि Ollama चल रहा है (`ollama serve`)।",
        "mr": "⚠️ AI सल्लागार सध्या ऑफलाइन आहे. कृपया Ollama सुरू असल्याची खात्री करा (`ollama serve`).",
    }
    return msgs.get(lang, msgs["en"])


def _get_timeout_message(lang: str) -> str:
    msgs = {
        "en": "⏱️ AI Advisor response timed out. Please try asking a shorter question.",
        "hi": "⏱️ AI सलाहकार से उत्तर प्राप्त करने में समय समाप्त हो गया। कृपया छोटा प्रश्न पूछें।",
        "mr": "⏱️ AI सल्लागाराकडून उत्तर मिळण्यास वेळ लागला. कृपया थोडक्यात प्रश्न विचारा.",
    }
    return msgs.get(lang, msgs["en"])


def _get_error_message(lang: str, error: str = "") -> str:
    msgs = {
        "en": f"❌ Error communicating with AI Advisor: {error}",
        "hi": f"❌ AI सलाहकार से संपर्क करने में समस्या: {error}",
        "mr": f"❌ AI सल्लागाराशी संवाद साधताना त्रुटी: {error}",
    }
    return msgs.get(lang, msgs["en"])
