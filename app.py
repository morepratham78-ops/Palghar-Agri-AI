"""
🌾 PALGHAR AGRI AI - Smart Farming Assistant
A complete, farmer-friendly agricultural AI web application for Maharashtra.
"""
import streamlit as st
import os
import sys
from datetime import datetime, date

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import TRANSLATIONS, PALGHAR_LOCATIONS, COMMON_CROPS, GOVT_SCHEMES, BASE_DIR
from database import (
    login_user, register_user, update_user_language,
    get_user_crops, add_crop, delete_crop,
    save_diagnosis, get_diagnosis_history,
)

# ── Page Config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PALGHAR AGRI AI | पालघर कृषी AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── Custom CSS ─────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
    <style>
    /* Clean natural green and white theme */
    :root {
        --primary: #2e7d32;
        --primary-light: #4caf50;
        --primary-dark: #1b5e20;
        --bg-light: #f7faf5;
        --white: #ffffff;
    }
    
    .stApp {
        background-color: #f7faf5;
        color: #1b381e;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Farmer Banner */
    .welcome-banner {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 60%, #43a047 100%);
        color: white !important;
        padding: 26px 30px;
        border-radius: 18px;
        margin-bottom: 22px;
        box-shadow: 0 4px 14px rgba(27, 94, 32, 0.22);
    }
    .welcome-banner h1 {
        color: white !important;
        font-size: 30px;
        font-weight: 700;
        margin: 0 0 6px 0;
    }
    .welcome-banner p {
        color: #e8f5e9 !important;
        font-size: 16px;
        margin: 0;
    }
    
    /* Large farmer navigation buttons */
    .stButton > button {
        background-color: #2e7d32 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #1b5e20 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.18) !important;
    }
    
    /* White Content Cards */
    .info-card {
        background: white;
        border-radius: 14px;
        padding: 18px 22px;
        margin: 12px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e2ebd8;
        border-left: 6px solid #2e7d32;
    }
    
    /* Weather Card */
    .weather-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #dcedc8 100%);
        border-radius: 18px;
        padding: 26px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.12);
        border: 1px solid #c8e6c9;
        margin-bottom: 18px;
    }
    .weather-temp {
        font-size: 52px;
        font-weight: 800;
        color: #1b5e20;
        line-height: 1.1;
    }
    
    /* Disease Result Cards */
    .disease-card {
        background: white;
        border-radius: 14px;
        padding: 22px;
        margin: 14px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07);
    }
    .disease-healthy {
        border-left: 8px solid #2e7d32;
    }
    .disease-warning {
        border-left: 8px solid #f57c00;
    }
    .disease-danger {
        border-left: 8px solid #d32f2f;
    }
    
    /* Scheme Card */
    .scheme-card {
        background: white;
        border-radius: 14px;
        padding: 20px;
        margin: 14px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e8f0fe;
        border-left: 6px solid #1976d2;
    }
    
    /* 7-Day Forecast pill */
    .forecast-day {
        background: white;
        border-radius: 12px;
        padding: 14px 10px;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border: 1px solid #e8f5e9;
    }
    
    /* Sidebar branding */
    section[data-testid="stSidebar"] {
        background-color: #1b5e20 !important;
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #ffffff !important;
    }
    
    /* Demo badge */
    .demo-badge {
        display: inline-block;
        background: #e8f5e9;
        color: #1b5e20;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        border: 1px solid #a5d6a7;
    }
    
    /* Clean headers */
    h1, h2, h3 {
        color: #1b5e20 !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ── Helper Functions ───────────────────────────────────────────────────
def t(key: str) -> str:
    """Get localized text string."""
    lang = st.session_state.get("lang", "mr")
    return TRANSLATIONS.get(lang, TRANSLATIONS.get("en", {})).get(key, key)


def init_session():
    """Initialize session state defaults."""
    defaults = {
        "lang": "mr",  # Default Marathi for Maharashtra farmers
        "page": "home",
        "user": None,
        "logged_in": False,
        "chat_history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def set_page(page: str):
    """Navigate to target page."""
    st.session_state.page = page


# ── Auth & Login / Register ────────────────────────────────────────────
def render_login_page():
    """Render Login & Registration screen with one-click quick login for testing."""
    st.markdown(f"""
    <div class="welcome-banner">
        <h1>🌾 PALGHAR AGRI AI</h1>
        <p>{t('app_subtitle')} — पालघर व महाराष्ट्रातील शेतकऱ्यांचा हक्काचा AI साथीदार</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language switcher right at login
    lang_cols = st.columns([1, 1, 1, 3])
    with lang_cols[0]:
        if st.button("मराठी", use_container_width=True, type="primary" if st.session_state.lang == "mr" else "secondary"):
            st.session_state.lang = "mr"
            st.rerun()
    with lang_cols[1]:
        if st.button("हिंदी", use_container_width=True, type="primary" if st.session_state.lang == "hi" else "secondary"):
            st.session_state.lang = "hi"
            st.rerun()
    with lang_cols[2]:
        if st.button("English", use_container_width=True, type="primary" if st.session_state.lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab_login, tab_register, tab_quick = st.tabs([
        f"🔑 {t('login')}", f"📝 {t('register')}", "⚡ Quick Access / झटपट प्रवेश"
    ])
    
    with tab_login:
        with st.form("login_form"):
            username = st.text_input(t("username"), placeholder="farmer")
            password = st.text_input(t("password"), type="password")
            submitted = st.form_submit_button(t("login"), use_container_width=True)
            
            if submitted:
                if username and password:
                    user = login_user(username, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.logged_in = True
                        st.session_state.lang = user.get("language") or st.session_state.lang
                        st.success(t("login_success"))
                        st.rerun()
                    else:
                        st.error(t("login_failed"))
                else:
                    st.warning("Please fill username and password")
                    
    with tab_register:
        with st.form("register_form"):
            new_user = st.text_input(t("username"), placeholder="e.g. suresh_patil")
            new_pass = st.text_input(t("password"), type="password")
            full_name = st.text_input(t("full_name"), placeholder="सुरेश पाटील / Suresh Patil")
            phone = st.text_input(t("phone"), placeholder="98XXXXXXXX")
            village = st.text_input(t("village"), placeholder="वाडा / Wada, Palghar")
            
            submitted = st.form_submit_button(t("register"), use_container_width=True)
            if submitted:
                if new_user and new_pass:
                    ok, msg = register_user(new_user, new_pass, full_name, phone, village)
                    if ok:
                        st.success(t("register_success"))
                    else:
                        st.error(t(msg))
                else:
                    st.warning("Please enter username and password")
                    
    with tab_quick:
        st.info("💡 **Farmer Account:** Use pre-configured account or browse as Guest instantly.")
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            if st.button("👨‍🌾 Login as Farmer (Ramesh Patil - Palghar)", use_container_width=True):
                user = login_user("farmer", "farmer123")
                if user:
                    st.session_state.user = user
                    st.session_state.logged_in = True
                    st.session_state.lang = "mr"
                    st.rerun()
        with col_q2:
            if st.button("👀 Continue as Guest / अतिथी म्हणून पाहा", use_container_width=True):
                st.session_state.user = {
                    "id": 0, "username": "guest", "full_name": "शेतकरी मित्र (Guest)", 
                    "village": "Palghar", "phone": "N/A"
                }
                st.session_state.logged_in = True
                st.rerun()


# ── Sidebar ────────────────────────────────────────────────────────────
def render_sidebar():
    """Render farmer sidebar navigation with language toggle and active user info."""
    with st.sidebar:
        st.markdown("### 🌾 PALGHAR AGRI AI")
        st.caption("पालघर कृषी सहाय्यक प्रणाली")
        
        # Language selector
        lang_options = {"मराठी": "mr", "हिंदी": "hi", "English": "en"}
        rev_lang = {v: k for k, v in lang_options.items()}
        curr_label = rev_lang.get(st.session_state.lang, "मराठी")
        
        selected_label = st.selectbox(
            f"🌐 {t('language')}",
            options=list(lang_options.keys()),
            index=list(lang_options.keys()).index(curr_label),
        )
        new_lang = lang_options[selected_label]
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            if st.session_state.logged_in and st.session_state.user and st.session_state.user["id"] > 0:
                update_user_language(st.session_state.user["id"], new_lang)
            st.rerun()
            
        st.markdown("---")
        
        # Navigation items
        nav_items = [
            ("🏠", "home", "Home / मुख्यपृष्ठ"),
            ("🔬", "crop_doctor", t("crop_doctor")),
            ("🤖", "advisor", t("advisor")),
            ("🌤️", "weather", t("weather")),
            ("📊", "market", t("market")),
            ("🏛️", "schemes", t("schemes")),
            ("🌱", "my_farm", t("my_farm")),
            ("👤", "profile", t("profile")),
        ]
        
        for icon, page_key, label in nav_items:
            is_active = st.session_state.page == page_key
            btn_label = f"{icon}  {label}"
            if st.button(
                btn_label, 
                key=f"sb_{page_key}", 
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                set_page(page_key)
                st.rerun()
                
        st.markdown("---")
        
        # User details & Logout
        if st.session_state.logged_in and st.session_state.user:
            u = st.session_state.user
            st.markdown(f"**👤 {u.get('full_name') or u.get('username')}**")
            st.caption(f"📍 {u.get('village', 'Palghar')}")
            
            if st.button(f"🚪 {t('logout')}", use_container_width=True):
                st.session_state.user = None
                st.session_state.logged_in = False
                st.session_state.page = "home"
                st.session_state.chat_history = []
                st.rerun()


# ── Home Page ──────────────────────────────────────────────────────────
def render_home():
    """Render home dashboard with quick weather summary and large buttons."""
    user = st.session_state.user or {}
    name = user.get("full_name") or user.get("username") or "शेतकरी मित्र"
    
    st.markdown(f"""
    <div class="welcome-banner">
        <h1>🌾 {t('app_title')}</h1>
        <p style="font-size: 20px; font-weight: 600; margin-bottom: 4px;">नमस्कार, {name}!</p>
        <p>{t('welcome_msg')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 6 Core features in high-visibility 3x2 grid
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="info-card">
            <h3>🔬 Crop Doctor</h3>
            <p>पिकाचा फोटो काढून रोग ओळखा, लक्षणे आणि खात्रीशीर उपाय मिळवा.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"👉 {t('crop_doctor')}", key="btn_h_doctor", use_container_width=True):
            set_page("crop_doctor")
            st.rerun()
            
    with c2:
        st.markdown("""
        <div class="info-card">
            <h3>🤖 AI Advisor</h3>
            <p>स्थानिक शेती सल्लागार (Llama 3.2). मराठी, हिंदी, इंग्रजीत बोला आणि विचारा.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"👉 {t('advisor')}", key="btn_h_advisor", use_container_width=True):
            set_page("advisor")
            st.rerun()
            
    with c3:
        st.markdown("""
        <div class="info-card">
            <h3>🌤️ Weather</h3>
            <p>पालघर हवामान अंदाज आणि हवामानानुसार प्रत्यक्ष शेती सल्ला.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"👉 {t('weather')}", key="btn_h_weather", use_container_width=True):
            set_page("weather")
            st.rerun()
            
    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("""
        <div class="info-card">
            <h3>📊 Market & MSP</h3>
            <p>महाराष्ट्र कृषी बाजारभाव आणि अधिकृत सरकारी हमीभाव (MSP 2024-25).</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"👉 {t('market')}", key="btn_h_market", use_container_width=True):
            set_page("market")
            st.rerun()
            
    with c5:
        st.markdown("""
        <div class="info-card">
            <h3>🏛️ Govt Schemes</h3>
            <p>PM-KISAN, नमो शेतकरी योजना, पीक विमा आणि KCC योजनांची माहिती.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"👉 {t('schemes')}", key="btn_h_schemes", use_container_width=True):
            set_page("schemes")
            st.rerun()
            
    with c6:
        st.markdown("""
        <div class="info-card">
            <h3>🌱 My Farm</h3>
            <p>तुमच्या शेतातील पिके, क्षेत्रफळ, पेरणी तारीख आणि नोंदींची नोंद ठेवा.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"👉 {t('my_farm')}", key="btn_h_myfarm", use_container_width=True):
            set_page("my_farm")
            st.rerun()


# ── Crop Doctor Page ───────────────────────────────────────────────────
def render_crop_doctor():
    """Crop Doctor: Genuine PlantVillage ResNet Vision Model inference."""
    st.markdown(f"## {t('crop_doctor')}")
    st.markdown(f"*{t('crop_doctor_desc')}*")
    
    # One-click sample test leaves for instant evaluation
    st.markdown("##### 🧪 Quick Test Samples / नमुना पान निवडून त्वरित तपासा:")
    scol1, scol2, scol3 = st.columns([1, 1, 2])
    
    sample_to_use = None
    samples_dir = os.path.join(BASE_DIR, "sample_images")
    
    with scol1:
        if st.button("🍃 Test Diseased Leaf Sample", use_container_width=True):
            sample_path = os.path.join(samples_dir, "diseased_leaf_sample.jpg")
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    sample_to_use = f.read()
    with scol2:
        if st.button("🌿 Test Healthy Leaf Sample", use_container_width=True):
            sample_path = os.path.join(samples_dir, "healthy_leaf_sample.jpg")
            if os.path.exists(sample_path):
                with open(sample_path, "rb") as f:
                    sample_to_use = f.read()
                    
    st.markdown("---")
    
    # Upload or Camera
    up_col, cam_col = st.columns(2)
    with up_col:
        uploaded_file = st.file_uploader(
            f"📁 {t('upload_image')}",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload clear photo of plant leaf or stem"
        )
    with cam_col:
        camera_file = st.camera_input(f"📷 {t('take_photo')}")
        
    image_bytes = None
    if sample_to_use is not None:
        image_bytes = sample_to_use
    elif uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
    elif camera_file is not None:
        image_bytes = camera_file.getvalue()
        
    if image_bytes is not None:
        col_img, col_res = st.columns([1, 1.2])
        
        with col_img:
            st.image(image_bytes, caption="Uploaded Crop Image", use_container_width=True)
            
        with col_res:
            with st.spinner(t("analyzing")):
                from disease_detection import predict_disease, get_disease_info
                result = predict_disease(image_bytes)
                
            if not result.get("success"):
                st.error(f"❌ {result.get('error', 'Prediction failed')}")
                return
                
            lang = st.session_state.lang
            disease_class = result["predicted_class"]
            conf = result["confidence"]
            conf_pct = round(conf * 100, 1)
            is_healthy = result["is_healthy"]
            
            # Fetch structured symptoms, treatment, prevention
            info = get_disease_info(disease_class, lang)
            disease_name = info.get("name") or result["disease_raw"]
            
            # Confidence banner
            if is_healthy:
                st.markdown(f"""
                <div class="disease-card disease-healthy">
                    <h3 style="color: #2e7d32; margin-top: 0;">✅ {t('healthy')}</h3>
                    <p style="font-size: 16px; margin: 4px 0;"><strong>Crop:</strong> {result['crop']}</p>
                    <p style="font-size: 16px; margin: 4px 0;"><strong>{t('confidence')}:</strong> <span class="demo-badge">{conf_pct}%</span></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                card_class = "disease-danger" if conf >= 0.7 else "disease-warning"
                st.markdown(f"""
                <div class="disease-card {card_class}">
                    <h3 style="color: #c62828; margin-top: 0;">🔴 {t('disease_detected')}</h3>
                    <h4 style="margin: 4px 0; color: #1b5e20;">{disease_name}</h4>
                    <p style="font-size: 15px; margin: 4px 0;"><strong>Crop:</strong> {result['crop']}</p>
                    <p style="font-size: 15px; margin: 4px 0;"><strong>{t('confidence')}:</strong> <span class="demo-badge">{conf_pct}%</span></p>
                </div>
                """, unsafe_allow_html=True)
                
            if conf < 0.55:
                st.warning(t("low_confidence_warning"))
                
            # Audio guidance (gTTS in Marathi/Hindi/English)
            from voice_service import text_to_speech, get_audio_html
            spoken_text = f"{disease_name}. {info.get('treatment', '')[:250]}"
            audio_path = text_to_speech(spoken_text, lang)
            if audio_path:
                st.markdown(f"**🔊 {t('voice_output')}:**")
                st.markdown(get_audio_html(audio_path), unsafe_allow_html=True)
                
            # Details Tabs
            tab_sym, tab_treat, tab_prev, tab_top3 = st.tabs([
                f"🔍 {t('symptoms')}", f"💊 {t('treatment')}", f"🛡️ {t('prevention')}", "📊 Top 3 Candidates"
            ])
            
            with tab_sym:
                st.write(info.get("symptoms") or "No specific symptoms reported.")
            with tab_treat:
                st.write(info.get("treatment") or "Consult local Krishi Vigyan Kendra.")
            with tab_prev:
                st.write(info.get("prevention") or "Practice clean farming and crop rotation.")
            with tab_top3:
                for idx, cand in enumerate(result.get("top3", [])):
                    cand_name = cand["class"].replace("___", " → ").replace("_", " ")
                    st.write(f"**{idx+1}. {cand_name}**: {cand['confidence']*100:.1f}%")
                    
            # Auto save diagnosis in farmer profile
            if st.session_state.logged_in and st.session_state.user:
                save_diagnosis(
                    st.session_state.user["id"],
                    "",
                    f"{result['crop']} - {disease_name}",
                    conf
                )


# ── AI Advisor Page ────────────────────────────────────────────────────
def render_advisor():
    """Multilingual AI Advisor with Ollama (Llama 3.2), Voice Input, and Spoken Responses."""
    st.markdown(f"## {t('advisor')}")
    st.markdown("स्थानिक शेती तज्ज्ञ — Llama 3.2 द्वारे समर्थित (मराठी, हिंदी व इंग्रजी)")
    
    from ai_advisor import is_ollama_available, ask_advisor_streaming, get_best_model_name
    from voice_service import get_web_speech_component_html, speech_to_text, text_to_speech, get_audio_html
    
    lang = st.session_state.lang
    ollama_ok = is_ollama_available()
    
    if not ollama_ok:
        st.warning(t("ollama_not_available"))
        st.info("Ollama is installed on your machine. Run `ollama serve` in a terminal to enable real-time local intelligence.")
    else:
        active_model = get_best_model_name()
        st.caption(f"⚡ Active AI Model: `{active_model}` (Local & Private)")
        
    # Voice assistant widget (Web Speech API)
    st.markdown("##### 🎙️ Voice Assistant / आवाजाद्वारे बोला:")
    st.components.v1.html(get_web_speech_component_html(lang), height=145)
    
    # Audio file upload fallback for voice input
    with st.expander("📁 Or upload voice audio recording (WAV / Audio file):"):
        audio_upload = st.file_uploader("Upload Audio", type=["wav", "flac"], key="audio_stt_file")
        if audio_upload is not None:
            with st.spinner("Transcribing your voice..."):
                stt_res = speech_to_text(audio_upload.getvalue(), lang)
                if stt_res.get("success"):
                    st.success(f"Recognized: **{stt_res['text']}**")
                    if st.button("Ask this question", key="btn_ask_stt"):
                        st.session_state.advisor_question = stt_res["text"]
                        st.rerun()
                else:
                    st.error(f"Voice recognition error: {stt_res.get('error')}")
                    
    st.markdown("---")
    
    # Quick question suggestions
    quick_questions = {
        "mr": [
            "पालघरमध्ये खरीप हंगामात भाताची कोणती जात लावावी?",
            "डहाणूच्या चिकू बागेत बुरशी व कीड नियंत्रण कसे करावे?",
            "टोमॅटो पिकावर करपा रोगासाठी सेंद्रिय उपाय काय आहेत?",
            "नाचणी (रागी) पिकाचे खत व्यवस्थापन कसे करावे?"
        ],
        "hi": [
            "पालघर में खरीफ मौसम के लिए धान की उत्तम किस्में कौन सी हैं?",
            "चीकू के बाग में फफूंद और कीट नियंत्रण कैसे करें?",
            "टमाटर में झुलसा रोग के लिए जैविक उपचार क्या हैं?",
            "नाचणी (रागी) फसल में खाद प्रबंधन कैसे करें?"
        ],
        "en": [
            "Which rice variety is best for Palghar Kharif season?",
            "How to manage pests in Dahanu Chickoo orchards?",
            "What are organic treatments for tomato early blight?",
            "What is the fertilizer schedule for Nagli (Ragi)?"
        ]
    }
    
    st.markdown(f"**💡 Quick Questions:**")
    q_cols = st.columns(2)
    for i, q in enumerate(quick_questions.get(lang, quick_questions["mr"])):
        with q_cols[i % 2]:
            if st.button(q, key=f"qq_{i}", use_container_width=True):
                st.session_state.advisor_question = q
                st.rerun()
                
    st.markdown("---")
    
    # Chat message history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    for msg in st.session_state.chat_history:
        role = msg["role"]
        with st.chat_message(role):
            st.markdown(msg["content"])
            if role == "assistant" and msg.get("audio"):
                st.markdown(msg["audio"], unsafe_allow_html=True)
                
    # Chat input
    user_input = st.chat_input(t("ask_question"))
    if "advisor_question" in st.session_state:
        user_input = st.session_state.advisor_question
        del st.session_state.advisor_question
        
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            if not ollama_ok:
                resp_text = t("ollama_not_available")
                st.warning(resp_text)
                audio_html = ""
            else:
                placeholder = st.empty()
                full_response = ""
                for chunk in ask_advisor_streaming(user_input, lang=lang):
                    full_response += chunk
                    placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                resp_text = full_response
                
                # Generate voice readout
                audio_path = text_to_speech(resp_text[:400], lang)
                audio_html = get_audio_html(audio_path) if audio_path else ""
                if audio_html:
                    st.markdown(f"**🔊 {t('voice_output')}**")
                    st.markdown(audio_html, unsafe_allow_html=True)
                    
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": resp_text,
            "audio": audio_html
        })


# ── Weather Page ───────────────────────────────────────────────────────
def render_weather():
    """Real-time Weather intelligence and agricultural advisory."""
    st.markdown(f"## {t('weather')}")
    st.caption("पालघर आणि महाराष्ट्रातील तालुक्यांचे प्रत्यक्ष हवामान व शेती सल्ला")
    
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        location = st.selectbox(
            t("select_location"),
            options=list(PALGHAR_LOCATIONS.keys()),
            index=0,
        )
        
    coords = PALGHAR_LOCATIONS[location]
    
    from weather_service import get_weather, get_farming_advice_from_weather, get_weather_emoji
    
    with st.spinner(t("loading")):
        weather_data = get_weather(coords["lat"], coords["lon"])
        
    if not weather_data:
        st.error(t("error"))
        return
        
    current = weather_data["current"]
    
    # Hero Weather Card
    st.markdown(f"""
    <div class="weather-card">
        <div style="font-size: 20px; font-weight: 600; color: #1b5e20; margin-bottom: 4px;">📍 {location}</div>
        <div class="weather-temp">{current['temperature']}°C</div>
        <div style="font-size: 20px; font-weight: 500; margin-top: 6px;">{current['description']}</div>
        <div style="margin-top: 14px; font-size: 15px; color: #2e7d32; font-weight: 600;">
            💧 {t('humidity')}: {current['humidity']}% &nbsp;|&nbsp; 
            🌧️ {t('rainfall')}: {current['precipitation']} mm &nbsp;|&nbsp; 
            💨 {t('wind_speed')}: {current['wind_speed']} km/h
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Farming Advice based on weather conditions
    lang = st.session_state.lang
    advice_list = get_farming_advice_from_weather(weather_data, lang)
    
    if advice_list:
        st.markdown(f"### 🌾 {t('farming_advice')}")
        for adv in advice_list:
            st.markdown(f"""
            <div class="info-card">
                <strong>{adv}</strong>
            </div>
            """, unsafe_allow_html=True)
            
    # 7-Day Forecast Grid
    st.markdown(f"### 📅 {t('forecast')}")
    forecast = weather_data.get("forecast", [])
    if forecast:
        fcols = st.columns(min(len(forecast), 7))
        for i, day in enumerate(forecast[:7]):
            with fcols[i]:
                day_obj = datetime.strptime(day["date"], "%Y-%m-%d")
                day_name = day_obj.strftime("%a")
                date_str = day_obj.strftime("%d %b")
                emoji = get_weather_emoji(day.get("weather_code", 0))
                
                st.markdown(f"""
                <div class="forecast-day">
                    <div style="font-weight: 700; color: #1b5e20;">{day_name}</div>
                    <div style="font-size: 12px; color: #777;">{date_str}</div>
                    <div style="font-size: 28px; margin: 4px 0;">{emoji}</div>
                    <div style="font-size: 14px; font-weight: 600;">🔺{day['temp_max']:.0f}° 🔻{day['temp_min']:.0f}°</div>
                    <div style="font-size: 12px; color: #43a047; font-weight: 500;">🌧️ {day['precipitation']:.1f} mm</div>
                </div>
                """, unsafe_allow_html=True)


# ── Market Prices Page ─────────────────────────────────────────────────
def render_market():
    """Market prices: Mandi Live Prices + Official Govt. Minimum Support Price (MSP)."""
    st.markdown(f"## {t('market')}")
    st.caption("अधिकृत हमीभाव (MSP 2024-25) आणि कृषी बाजारभाव (Agmarknet)")
    
    from market_service import get_market_prices, get_msp_data, COMMON_COMMODITIES, MAHARASHTRA_MARKETS
    
    tab_msp, tab_mandi = st.tabs([
        "🏛️ शासकीय हमीभाव (Govt. MSP 2024-25)",
        "🌾 कृषी उत्पन्न बाजार समिती भाव (Live APMC Mandi)"
    ])
    
    with tab_msp:
        st.markdown("##### 🇮🇳 भारत सरकार अधिकृत किमान आधारभूत किंमत (MSP - 2024-2025 हंगाम):")
        st.caption("किंमत: रुपये प्रति क्विंटल (Rs. per Quintal)")
        
        search_msp = st.text_input("🔍 हमीभाव शोधा (उदा. भात, सोयाबीन, तूर / Rice, Soybean, Cotton):", key="search_msp_input")
        msp_records = get_msp_data(search_msp)
        
        cols = st.columns(2)
        for i, item in enumerate(msp_records):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="info-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="font-size: 16px; color: #1b5e20;">{item['commodity']}</strong><br>
                            <span style="font-size: 13px; color: #666;">{item['category']}</span>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 22px; font-weight: 800; color: #2e7d32;">₹{item['msp']:,}</div>
                            <span style="font-size: 12px; color: #777;">प्रति क्विंटल</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
    with tab_mandi:
        st.markdown("##### 📍 महाराष्ट्र APMC बाजारभाव शोधा:")
        c1, c2 = st.columns(2)
        with c1:
            commodity = st.selectbox(
                t("select_crop"),
                options=[""] + COMMON_COMMODITIES,
                format_func=lambda x: "All Commodities / सर्व पिके" if x == "" else x
            )
        with c2:
            market = st.selectbox(
                "Market / बाजार समिती",
                options=[""] + MAHARASHTRA_MARKETS,
                format_func=lambda x: "All Markets / सर्व बाजार" if x == "" else x
            )
            
        if st.button(f"🔍 {t('search')}", key="btn_mandi_search", use_container_width=True):
            with st.spinner("Connecting to National Agmarknet portal..."):
                mandi_res = get_market_prices(commodity=commodity, market=market)
                
            if mandi_res.get("success") and mandi_res.get("records"):
                st.success(f"Found {len(mandi_res['records'])} live market arrivals:")
                for rec in mandi_res["records"]:
                    st.markdown(f"""
                    <div class="info-card">
                        <div style="display: flex; justify-content: space-between; flex-wrap: wrap;">
                            <div>
                                <strong style="font-size: 16px;">🌾 {rec.get('commodity')}</strong><br>
                                <span>📍 {rec.get('market')}, {rec.get('district', '')}</span><br>
                                <span style="font-size: 12px; color: #888;">📅 {rec.get('arrival_date')}</span>
                            </div>
                            <div style="text-align: right;">
                                <div>किमान: <strong>₹{rec.get('min_price')}</strong></div>
                                <div>कमाल: <strong>₹{rec.get('max_price')}</strong></div>
                                <div style="color: #2e7d32; font-weight: bold; font-size: 18px;">सरासरी: ₹{rec.get('modal_price')}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                err_msg = mandi_res.get("error", "No data")
                st.warning(f"ℹ️ {err_msg}")
                st.info("""
                **अधिकृत थेट पोर्टल:**
                - 🌐 [महाराष्ट्र राज्य कृषी पणन मंडळ (MSAMB)](https://www.msamb.com)
                - 🌐 [Agmarknet National Portal](https://agmarknet.gov.in)
                """)


# ── Government Schemes Page ────────────────────────────────────────────
def render_schemes():
    """Government schemes with verified eligibility and application links."""
    st.markdown(f"## {t('schemes')}")
    st.caption("शेतकऱ्यांसाठी केंद्र व महाराष्ट्र राज्य शासनाच्या कल्याणकारी योजना")
    
    lang = st.session_state.lang
    for sc in GOVT_SCHEMES:
        info = sc.get(lang) or sc.get("mr") or sc.get("en", {})
        
        st.markdown(f"""
        <div class="scheme-card">
            <h3 style="color: #1565c0; margin-top: 0;">🏛️ {info.get('name')}</h3>
            <p style="font-size: 15px; font-weight: 500;">{info.get('description')}</p>
            <p><strong>पात्रता / Eligibility:</strong> {info.get('eligibility')}</p>
            <p><strong>अर्ज कसा करावा / How to apply:</strong> {info.get('how_to_apply')}</p>
            <a href="{info.get('website')}" target="_blank" style="text-decoration: none; color: #1565c0; font-weight: 600;">
                🔗 अधिकृत पोर्टलला भेट द्या ({info.get('website')}) ↗
            </a>
        </div>
        """, unsafe_allow_html=True)


# ── My Farm Page ───────────────────────────────────────────────────────
def render_my_farm():
    """Farm management for farmers to maintain crop records."""
    st.markdown(f"## {t('my_farm')}")
    st.caption("माझ्या शेतातील पिके, पेरणी आणि क्षेत्रफळाचे व्यवस्थापन")
    
    if not st.session_state.logged_in or not st.session_state.user:
        st.warning("कृपया शेताची माहिती व्यवस्थापित करण्यासाठी लॉगिन करा.")
        return
        
    user_id = st.session_state.user["id"]
    
    with st.expander(f"➕ {t('add_crop')}", expanded=True):
        with st.form("form_add_crop"):
            c_name = st.selectbox(t("crop_name"), COMMON_CROPS)
            col_a, col_d = st.columns(2)
            with col_a:
                c_area = st.number_input(t("area"), min_value=0.1, max_value=500.0, value=1.0, step=0.5)
            with col_d:
                c_date = st.date_input(t("sowing_date"), value=date.today())
            c_notes = st.text_input(t("notes"), placeholder="उदा. वाडा कोलम तांदूळ, ठिबक सिंचन")
            
            if st.form_submit_button(f"💾 {t('add_crop')}", use_container_width=True):
                add_crop(user_id, c_name, c_area, str(c_date), c_notes)
                st.success("पीक यशस्वीरीत्या नोंदवले गेले!")
                st.rerun()
                
    st.markdown("### 📋 नोंदवलेली पिके:")
    crops = get_user_crops(user_id)
    if not crops:
        st.info("अद्याप कोणतेही पीक नोंदवलेले नाही. वरील फॉर्म भरून तुमचे पहिले पीक जोडा!")
    else:
        for crop in crops:
            c1, c2 = st.columns([5, 1])
            with c1:
                st.markdown(f"""
                <div class="info-card">
                    <strong style="font-size: 17px; color: #1b5e20;">🌱 {crop['crop_name']}</strong><br>
                    <span>📐 <strong>क्षेत्र:</strong> {crop['area_acres']} एकर &nbsp;|&nbsp; 📅 <strong>पेरणी:</strong> {crop['sowing_date']}</span>
                    {f"<br><span style='color: #666;'>📝 {crop['notes']}</span>" if crop.get('notes') else ""}
                </div>
                """, unsafe_allow_html=True)
            with c2:
                if st.button("🗑️", key=f"del_{crop['id']}", help="Delete crop"):
                    delete_crop(crop["id"], user_id)
                    st.rerun()


# ── Profile Page ───────────────────────────────────────────────────────
def render_profile():
    """User profile, diagnosis history, and logout."""
    st.markdown(f"## {t('profile')}")
    
    if not st.session_state.logged_in or not st.session_state.user:
        st.warning("कृपया लॉगिन करा.")
        return
        
    u = st.session_state.user
    st.markdown(f"""
    <div class="info-card">
        <h3 style="margin-top: 0; color: #1b5e20;">👤 {u.get('full_name') or u.get('username')}</h3>
        <p><strong>{t('username')}:</strong> {u.get('username')}</p>
        <p><strong>{t('village')}:</strong> {u.get('village', 'Palghar')}</p>
        <p><strong>{t('phone')}:</strong> {u.get('phone', 'N/A')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Diagnosis history
    st.markdown("### 🔬 रोग निदान इतिहास (Recent Diagnoses):")
    history = get_diagnosis_history(u["id"])
    if not history:
        st.info("अद्याप कोणतीही रोग तपासणी नोंदवलेली नाही. पिकाचा फोटो काढून 'Crop Doctor' वापरा!")
    else:
        for item in history:
            conf_val = item.get("confidence") or 0.0
            st.markdown(f"""
            <div class="info-card">
                <strong>🌾 {item.get('disease_name')}</strong><br>
                <span>📅 {item.get('created_at')} &nbsp;|&nbsp; विश्वासार्हता: <strong>{conf_val*100:.1f}%</strong></span>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("---")
    if st.button(f"🚪 {t('logout')}", use_container_width=True, type="primary"):
        st.session_state.user = None
        st.session_state.logged_in = False
        st.session_state.page = "home"
        st.session_state.chat_history = []
        st.rerun()


# ── Main Controller ────────────────────────────────────────────────────
def main():
    init_session()
    inject_css()
    
    if not st.session_state.logged_in:
        render_login_page()
        return
        
    render_sidebar()
    
    page = st.session_state.page
    page_map = {
        "home": render_home,
        "crop_doctor": render_crop_doctor,
        "advisor": render_advisor,
        "weather": render_weather,
        "market": render_market,
        "schemes": render_schemes,
        "my_farm": render_my_farm,
        "profile": render_profile,
    }
    
    handler = page_map.get(page, render_home)
    handler()


if __name__ == "__main__":
    main()
