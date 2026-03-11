import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
import PIL.Image

# --- 1. CONFIG & YOUR API KEY ---
st.set_page_config(page_title="Mihir AI", layout="centered")

# Aapki di hui API key yahan set hai
genai.configure(api_key="AIzaSyCzKdc2QkS1l9KkypD7GcRZeToDKtyH5I4")
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_image(prompt):
    return f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"

# --- 2. CSS (NO BROWSE FILE, NO GITHUB/STREAMLIT STRIP) ---
st.markdown("""
    <style>
    /* 1. GitHub aur Streamlit ki patti (Header/Footer/Menu) hide karo */
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration, div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* 2. "Browse Files" text aur icons hide karo */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    section[data-testid="stFileUploader"] > label {display: none !important;} /* "Browse files" label hide */
    div[data-testid="stFileUploaderDropzoneInstructions"] {display: none !important;} /* Dropzone text hide */

    /* 3. Clean Gemini Chat Look */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 5px 0px !important;
    }

    /* 4. Plus (+) Button aur Chat Input placement */
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

    /* Padding taaki ads ke liye jagah rahe */
    .main .block-container { padding-bottom: 120px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ---
if "messages" not in st.session_state: st.session_state.messages = []
if "photo_count" not in st.session_state: st.session_state.photo_count = 0

# --- 4. CHAT DISPLAY ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img_url" in m: st.image(m["img_url"])
        st.markdown(m["content"])

# --- 5. INPUT ---
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Dost Mihir se baat karein...")

if prompt or uploaded_file:
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analysis"})
    
    with st.chat_message("assistant"):
        try:
            if any(x in (prompt or "").lower() for x in ["create", "photo", "banao", "image"]):
                if st.session_state.photo_count >= 5:
                    st.error("Dost, limit khatam! Watch ad and restart app.")
                    st.stop()
                url = generate_image(prompt)
                st.image(url)
                st.session_state.messages.append({"role":"assistant", "content":"", "img_url":url})
                st.session_state.photo_count += 1
            else:
                if uploaded_file:
                    res = model.generate_content([prompt if prompt else "Analyze", PIL.Image.open(uploaded_file)])
                else:
                    res = model.generate_content(f"You are Mihir AI, a friendly boy. Reply in Hinglish: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role":"assistant", "content":res.text})
        except:
            st.error("Dost, ek baar phir se koshish karein!")
