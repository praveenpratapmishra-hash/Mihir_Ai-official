import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
import PIL.Image

# --- 1. AI SETUP (Pakka Connection) ---
# Maine API logic ko try-except ke bahar rakha hai taaki error turant pakda jaye
GOOGLE_API_KEY = "AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_image(prompt):
    return f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"

# --- 2. CSS (SAB KUCH HIDE KARO) ---
st.set_page_config(page_title="Mihir AI", layout="centered")
st.markdown("""
    <style>
    /* 1. Purani branding aur menu mitao */
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    
    /* Manage App aur bottom menu hide karne ka ultimate tarika */
    div[class^="st-emotion-cache-10pw50"], div[class^="st-emotion-cache-1dp5vir"] {display: none !important;}
    footer {display: none !important;}

    /* 2. Icons aur Blue Boxes mitao (Gemini Look) */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 5px 0px !important;
        margin-bottom: 10px !important;
    }

    /* 3. Input Bar Layout */
    .stChatInputContainer {
        position: fixed !important; bottom: 25px !important;
        left: 65px !important; right: 15px !important; z-index: 1000;
    }
    [data-testid="stFileUploader"] {
        position: fixed !important; bottom: 27px !important; left: 10px !important;
        width: 45px !important; z-index: 1001;
    }
    [data-testid="stFileUploaderSection"] {padding: 0; min-height: 0; border: none;}
    [data-testid="stFileUploader"] section > div {display: none;}
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 24px; color: white;
        background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ---
if "messages" not in st.session_state: st.session_state.messages = []
if "photo_count" not in st.session_state: st.session_state.photo_count = 0

# --- 4. START SCREEN ---
if not st.session_state.messages:
    st.markdown("<h2 style='text-align: center;'>Mihir AI ❤️</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🧠 Solve Problem"): st.session_state.temp = "Dost, help me solve this."
    if c1.button("🎨 Create Photo"): st.session_state.temp = "Create a photo of "
    if c2.button("✨ Horoscope"): st.session_state.temp = "Aaj ka rashifal batao."
    if c2.button("☸️ Kundali"): st.session_state.temp = "Kundali reading karein."

# Display Messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img_url" in m: st.image(m["img_url"])
        st.markdown(m["content"])

# --- 5. INPUT ---
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Dost se baat karein...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or uploaded_file:
    is_img = any(x in (prompt or "").lower() for x in ["create", "photo", "banao", "image"])
    
    # User Msg
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analysis"})
    st.rerun()

# Assistant Response (Naye message par trigger hoga)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    user_prompt = st.session_state.messages[-1]["content"]
    with st.chat_message("assistant"):
        try:
            if any(x in user_prompt.lower() for x in ["create", "photo", "banao", "image"]):
                with st.spinner("🎨 Creating..."):
                    url = generate_image(user_prompt)
                    st.image(url)
                    st.download_button("📥 Save", requests.get(url).content, "photo.png")
                    st.session_state.messages.append({"role":"assistant", "content":"Photo taiyar hai!", "img_url":url})
            else:
                with st.spinner("Mihir is thinking..."):
                    if uploaded_file:
                        res = model.generate_content([user_prompt, PIL.Image.open(uploaded_file)])
                    else:
                        res = model.generate_content(f"Be a friendly Indian friend named Mihir. Reply in Hinglish: {user_prompt}")
                    st.markdown(res.text)
                    st.session_state.messages.append({"role":"assistant", "content":res.text})
        except Exception as e:
            st.error("Dost, API key refresh ki zaroorat hai ya internet slow hai. Dubara try karo!")
