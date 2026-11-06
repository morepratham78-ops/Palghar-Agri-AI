"""
Voice service for PALGHAR AGRI AI.
Supports:
1. Text-To-Speech (TTS) via gTTS in Marathi (mr), Hindi (hi), and English (en).
2. Speech-To-Text (STT) via SpeechRecognition in mr-IN, hi-IN, and en-IN.
3. Web Speech API client-side component for direct mic access in web browsers.
"""
import os
import hashlib
import base64
import tempfile
from config import AUDIO_DIR


def text_to_speech(text: str, lang: str = "en") -> str | None:
    """Convert text to speech and return the audio file path.
    Uses gTTS (Google Text-to-Speech) with persistent caching.
    """
    if not text or not text.strip():
        return None
        
    try:
        from gtts import gTTS
        
        # Map our language codes to gTTS codes
        gtts_lang = {"en": "en", "hi": "hi", "mr": "mr"}.get(lang, "en")
        
        # Clean text slightly (strip markdown headers and asterisks for cleaner pronunciation)
        clean_text = text.replace("**", "").replace("#", "").replace("`", "")
        # Limit text length to first 600 characters for snappy voice response
        if len(clean_text) > 600:
            clean_text = clean_text[:600] + "..."
            
        # Cache audio by content hash to avoid regenerating identical audio
        text_hash = hashlib.md5(f"{clean_text}_{gtts_lang}".encode()).hexdigest()[:14]
        audio_path = os.path.join(AUDIO_DIR, f"tts_{text_hash}.mp3")
        
        if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
            return audio_path
        
        tts = gTTS(text=clean_text, lang=gtts_lang, slow=False)
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"TTS Error: {e}")
        return None


def get_audio_base64(audio_path: str) -> str | None:
    """Read audio file and return base64 encoded string."""
    try:
        if os.path.exists(audio_path):
            with open(audio_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    except Exception:
        pass
    return None


def get_audio_html(audio_path: str, autoplay: bool = False) -> str:
    """Generate HTML5 audio player for the given audio file."""
    audio_b64 = get_audio_base64(audio_path)
    if not audio_b64:
        return ""
    
    autoplay_attr = "autoplay" if autoplay else ""
    return f"""
    <div style="margin: 8px 0; padding: 4px 0;">
        <audio controls {autoplay_attr} style="width: 100%; height: 42px; border-radius: 8px;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            Your browser does not support audio playback.
        </audio>
    </div>
    """


def speech_to_text(audio_bytes: bytes, lang: str = "en") -> dict:
    """
    Transcribe audio bytes (e.g. from an audio recorder or uploaded audio file)
    using speech_recognition.
    """
    try:
        import speech_recognition as sr
        
        lang_code_map = {
            "mr": "mr-IN",
            "hi": "hi-IN",
            "en": "en-IN",
        }
        recog_lang = lang_code_map.get(lang, "en-IN")
        
        # Save temporary file for SpeechRecognition to read
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_path = tmp_file.name
            
        r = sr.Recognizer()
        with sr.AudioFile(tmp_path) as source:
            audio_data = r.record(source)
            
        text = r.recognize_google(audio_data, language=recog_lang)
        
        try:
            os.remove(tmp_path)
        except Exception:
            pass
            
        return {"success": True, "text": text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_web_speech_component_html(lang: str = "en") -> str:
    """
    Returns an embedded Web Speech API microphone widget.
    Farmers can click the mic button, speak in Marathi/Hindi/English,
    and it will recognize their speech directly with instant feedback.
    """
    lang_map = {
        "mr": ("mr-IN", "माइक वर टॅप करा आणि बोला...", "ऐकणे सुरू आहे..."),
        "hi": ("hi-IN", "माइक पर टैप करें और बोलें...", "सुनना चालू है..."),
        "en": ("en-IN", "Tap microphone and speak...", "Listening..."),
    }
    recog_code, prompt_text, listening_text = lang_map.get(lang, lang_map["en"])
    
    return f"""
    <div style="background: #ffffff; border: 2px solid #4caf50; border-radius: 12px; padding: 14px; margin: 12px 0;">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <button id="palghar-mic-btn" onclick="startPalgharSpeechRecognition()" 
                    style="background: #2e7d32; color: white; border: none; border-radius: 50%; width: 48px; height: 48px; font-size: 22px; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 3px 6px rgba(0,0,0,0.16); transition: 0.2s;">
                    🎤
                </button>
                <div>
                    <span id="palghar-status-text" style="font-weight: 600; color: #1b5e20; font-size: 15px;">{prompt_text}</span>
                    <div style="font-size: 12px; color: #666;">Language: {recog_code}</div>
                </div>
            </div>
            <button onclick="copyRecognizedText()" style="background: #e8f5e9; border: 1px solid #4caf50; color: #1b5e20; border-radius: 6px; padding: 6px 12px; font-size: 13px; cursor: pointer;">
                📋 Copy Text
            </button>
        </div>
        <div id="palghar-transcript-box" style="margin-top: 10px; min-height: 40px; background: #f9fbf8; border: 1px dashed #a5d6a7; border-radius: 8px; padding: 8px 12px; font-size: 14px; color: #2e7d32;">
            <em style="color: #888;">Spoken text will appear here / बोललेला मजकूर येथे येईल...</em>
        </div>
    </div>
    
    <script>
    var recognition = null;
    var isListening = false;
    
    function startPalgharSpeechRecognition() {{
        var btn = document.getElementById('palghar-mic-btn');
        var status = document.getElementById('palghar-status-text');
        var box = document.getElementById('palghar-transcript-box');
        
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
            status.innerText = "Speech recognition is not supported in this browser. Please use Google Chrome or Edge.";
            status.style.color = "#d32f2f";
            return;
        }}
        
        if (isListening && recognition) {{
            recognition.stop();
            return;
        }}
        
        var SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRec();
        recognition.lang = '{recog_code}';
        recognition.interimResults = true;
        recognition.continuous = false;
        
        recognition.onstart = function() {{
            isListening = true;
            btn.style.background = "#d32f2f";
            btn.innerHTML = "⏹️";
            status.innerText = "{listening_text}";
            status.style.color = "#d32f2f";
        }};
        
        recognition.onresult = function(event) {{
            var transcript = '';
            for (var i = event.resultIndex; i < event.results.length; ++i) {{
                transcript += event.results[i][0].transcript;
            }}
            box.innerText = transcript;
            box.style.color = "#1b5e20";
            box.style.fontWeight = "bold";
        }};
        
        recognition.onerror = function(event) {{
            isListening = false;
            btn.style.background = "#2e7d32";
            btn.innerHTML = "🎤";
            status.innerText = "Error: " + event.error;
            status.style.color = "#d32f2f";
        }};
        
        recognition.onend = function() {{
            isListening = false;
            btn.style.background = "#2e7d32";
            btn.innerHTML = "🎤";
            status.innerText = "{prompt_text}";
            status.style.color = "#1b5e20";
        }};
        
        recognition.start();
    }}
    
    function copyRecognizedText() {{
        var box = document.getElementById('palghar-transcript-box');
        var text = box.innerText;
        if (text && !text.includes("Spoken text will appear here")) {{
            navigator.clipboard.writeText(text);
            alert("Copied to clipboard! Paste it into the message box.");
        }}
    }}
    </script>
    """
