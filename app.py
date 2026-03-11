import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
import PIL.Image

# --- 1. CONFIG & YOUR API KEY ---
st.set_page_config(page_title="Mihir AI", layout="centered")
genai.configure(api_key="AIzaSyCzKdc2QkS1l9KkypD7GcRZeToDKtyH5I4")
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_image(prompt):
    return f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"

# --- 2. CSS (CLEAN LOOK, NO BRANDING, NO BROWSE TEXT) ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    
    /* Browse files text aur avatars hide karne ke liye */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    section[data-testid="stFileUploader"] > label {display: none !important;}
    div[data-testid="stFileUploaderDropzoneInstructions"] {display: none !important;}

    /* Buttons Styling */
    .stButton button {
        width: 100%;
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #4A90E2;
        border-radius: 10px;
        margin-bottom: 5px;
    }

    /* Input Bar Fix */
    .stChatInputContainer { position: fixed !important; bottom: 25px !important; left: 65px !important; right: 15px !important; z-index: 1000; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 27px !important; left: 10px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploaderSection"] {padding: 0; min-height: 0; border: none;}
    [data-testid="stFileUploader"] section > div {display: none;}
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 24px; color: white; background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []

# --- 4. THE 4 BUTTONS (App khulte hi dikhenge) ---
if not st.session_state.messages:
    st.markdown("<h2 style='text-align: center;'>Mihir AI ❤️</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Solve Problem"): st.session_state.temp = "Dost, help me solve this."
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create a beautiful photo of "
    with col2:
        if st.button("✨ Horoscope"): st.session_state.temp = "Aaj ka rashifal batao dost."
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Meri kundali ke baare mein batao."

# --- 5. CHAT DISPLAY ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img_url" in m: st.image(m["img_url"])
        st.markdown(m["content"])

# --- 6. INPUT LOGIC ---
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Dost Mihir se baat karein...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or uploaded_file:
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analysis"})
    with st.chat_message("assistant"):
        try:
            if any(x in (prompt or "").lower() for x in ["create", "photo", "banao", "image"]):
                url = generate_image(prompt)
                st.image(url)
                st.session_state.messages.append({"role":"assistant", "content":"Photo taiyar hai!", "img_url":url})
            else:
                if uploaded_file:
                    res = model.generate_content([prompt, PIL.Image.open(uploaded_file)])
                else:
                    res = model.generate_content(f"You are Mihir AI, a friendly boy. Reply in Hinglish: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role":"assistant", "content":res.text})
        except:
            st.error("Dost, ek baar phir se koshish karein!")
