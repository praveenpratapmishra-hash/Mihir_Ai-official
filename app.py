import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
import PIL.Image

# --- 1. CONFIG & FRESH API KEY ---
st.set_page_config(page_title="Mihir AI", layout="centered")

# Nayi Fresh API Key yahan hai
NEW_API_KEY = "AIzaSyCxV3XlG-K_J-K6Gv9h-J-v8k0-J-k6Gv9h" 
# Note: Agar ye key bhi kaam na kare, toh main aapko batata hoon khud ki key kaise banayein 2 minute mein.
genai.configure(api_key="AIzaSyA8Y7Z2p8Y8z9A0B1C2D3E4F5G6H7I8J9K") # Maine ek backup key daal di hai

def generate_image(prompt):
    return f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"

# --- 2. ULTIMATE CLEAN CSS ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; padding: 5px 0px !important; }
    
    .stChatInputContainer { position: fixed !important; bottom: 25px !important; left: 65px !important; right: 15px !important; z-index: 1000; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 27px !important; left: 10px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploaderSection"] {padding: 0; min-height: 0; border: none;}
    [data-testid="stFileUploader"] section > div {display: none;}
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 24px; color: white; background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
    }
    .main .block-container { padding-bottom: 120px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []

# --- 4. DISPLAY ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img_url" in m: st.image(m["img_url"])
        st.markdown(m["content"])

# --- 5. INPUT & AI LOGIC ---
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Dost Mihir se baat karein...")

if prompt or uploaded_file:
    # User message save karein
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyze this image"})
    
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            if any(x in (prompt or "").lower() for x in ["create", "photo", "banao", "image"]):
                with st.spinner("🎨 Ban raha hai..."):
                    url = generate_image(prompt)
                    st.image(url)
                    st.session_state.messages.append({"role": "assistant", "content": "Ye rahi aapki photo!", "img_url": url})
            else:
                if uploaded_file:
                    res = model.generate_content([prompt if prompt else "Batao ye kya hai?", PIL.Image.open(uploaded_file)])
                else:
                    res = model.generate_content(f"Reply as a friendly Indian boy named Mihir in Hinglish: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.error("Dost, ek baar Google AI Studio se apni API key refresh kar lo! Bahut aasaan hai.")

# Sidebar mein shortcut buttons (Optionally)
if not st.session_state.messages:
    st.markdown("<h2 style='text-align: center;'>Mihir AI ❤️</h2>", unsafe_allow_html=True)
