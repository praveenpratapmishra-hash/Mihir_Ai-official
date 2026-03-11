import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
import PIL.Image

# --- 1. CONFIG & AI SETUP ---
st.set_page_config(page_title="Mihir AI", layout="centered")

# API Key yahan direct set hai
genai.configure(api_key="AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I")
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_image(prompt):
    return f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"

# --- 2. CSS (THE MAGIC FIX) ---
st.markdown("""
    <style>
    /* Sab kuch hide karo: Menu, Footer, Header, Manage App button */
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration, div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* 1. ICONS HATANA: User aur Assistant ke chehre hide karo */
    [data-testid="stChatMessageAvatarUser"], 
    [data-testid="stChatMessageAvatarAssistant"] {
        display: none !important;
    }

    /* 2. BOXES HATANA: Message ke piche ka background aur border khatam */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding-top: 0px !important;
        padding-bottom: 10px !important;
        margin-left: -30px !important; /* Text ko left align karne ke liye */
    }

    /* 3. INPUT BAR FIX: Mobile screen ke liye sahi jagah */
    .stChatInputContainer {
        position: fixed !important;
        bottom: 25px !important;
        left: 65px !important;
        right: 15px !important;
        z-index: 1000;
    }
    
    /* 4. PLUS (+) BUTTON: Minimalist circular design */
    [data-testid="stFileUploader"] {
        position: fixed !important; bottom: 27px !important; left: 10px !important;
        width: 45px !important; z-index: 1001;
    }
    [data-testid="stFileUploaderSection"] {padding: 0; min-height: 0; border: none;}
    [data-testid="stFileUploader"] section > div {display: none;}
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 24px; color: white;
        background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
    }

    /* Main Container Padding */
    .main .block-container { padding-bottom: 120px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC & HISTORY ---
if "messages" not in st.session_state: st.session_state.messages = []
if "photo_gallery" not in st.session_state: st.session_state.photo_gallery = []
if "photo_count" not in st.session_state: st.session_state.photo_count = 0

# --- 4. UI DISPLAY ---
if not st.session_state.messages:
    st.markdown("<h3 style='text-align: center;'>Mihir AI ❤️</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🧠 Solve Problem"): st.session_state.temp = "Solve this problem as a friend."
    if c1.button("🎨 Create Photo"): st.session_state.temp = "Create a high quality photo of "
    if c2.button("✨ Horoscope"): st.session_state.temp = "Aaj ka rashifal batao dost."
    if c2.button("☸️ Kundali"): st.session_state.temp = "Meri kundali ke baare mein batao."

# Chat messages display (Clean Text Only)
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img_url" in m: st.image(m["img_url"])
        st.markdown(m["content"])

# --- 5. INPUT HANDLING ---
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Dost Mihir se baat karein...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or uploaded_file:
    # Logic determine
    is_img = any(x in (prompt or "").lower() for x in ["create", "photo", "banao", "image", "generate"])
    
    # User message
    user_txt = prompt if prompt else "Analyze this photo"
    st.session_state.messages.append({"role": "user", "content": user_txt})
    with st.chat_message("user"): st.markdown(user_txt)

    with st.chat_message("assistant"):
        try:
            if is_img:
                if st.session_state.photo_count >= 5:
                    st.error("Dost, limit reached! Watch ad to unlock.")
                    st.stop()
                
                with st.spinner("🎨 Creating..."):
                    url = generate_image(prompt)
                    st.image(url)
                    st.session_state.photo_gallery.append(url)
                    st.download_button("📥 Save to Gallery", requests.get(url).content, "mihir_ai.png")
                    st.session_state.photo_count += 1
                    st.session_state.messages.append({"role": "assistant", "content": f"Aapki photo taiyar hai dost!", "img_url": url})
            else:
                with st.spinner("Thinking..."):
                    if uploaded_file:
                        res = model.generate_content([prompt if prompt else "Explain this image", PIL.Image.open(uploaded_file)])
                    else:
                        res = model.generate_content(f"You are Mihir AI, a very friendly person. Answer this warmly: {prompt}")
                    
                    st.markdown(res.text)
                    st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.info("Dost, ek baar phir se koshish karein, main taiyar hoon!")
