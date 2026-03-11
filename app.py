import streamlit as st
import google.generativeai as genai
import socket
import requests

# --- 1. FUNCTIONS ---
def has_net():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except: return False

def generate_image(prompt):
    url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
    return url

# --- 2. UI & CUSTOM CSS (For (+) Button Look) ---
st.set_page_config(page_title="Mihir AI Pro", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #131314; color: #e3e3e3;}
    .app-title {text-align: center; font-size: 30px; font-weight: bold; color: #4A90E2; margin-top: -40px;}
    
    /* File Uploader ko chhota (+) button banane ka trick */
    [data-testid="stFileUploader"] {
        width: 45px;
        position: fixed;
        bottom: 95px;
        left: 20px;
        z-index: 100;
    }
    [data-testid="stFileUploaderSection"] {padding: 0; min-height: 0;}
    [data-testid="stFileUploader"] section > div {display: none;} /* "Drag and drop" text chhupane ke liye */
    
    /* Custom (+) Icon Style */
    [data-testid="stFileUploader"]::before {
        content: "＋";
        font-size: 24px;
        font-weight: bold;
        color: white;
        background: #303134;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
    }

    /* Typing Bar adjust karo taaki button ke upar na aaye */
    .stChatInputContainer {
        padding-bottom: 90px !important;
        margin-left: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

if not has_net():
    st.error("🚫 No Internet! Net ON kijiye Ads ke liye.")
    st.stop()

st.markdown('<div class="app-title">Mihir AI</div>', unsafe_allow_html=True)

# --- 3. AI SETUP ---
genai.configure(api_key="AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I")
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []

# Action Boxes
if not st.session_state.messages:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Solve Problem"): st.session_state.temp = "Solve this problem"
        if st.button("🎨 Create Photo"): st.session_state.temp = "GEN_IMAGE"
    with col2:
        if st.button("✨ Horoscope"): st.session_state.temp = "My Horoscope"
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Kundali Analysis"

# Display Chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img_url" in m: st.image(m["img_url"])
        else: st.markdown(m["content"])

# --- 4. INPUT ---
# Ye wahi plus button ban jayega
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Ask Mihir AI or Create Image...")

if "temp" in st.session_state:
    if st.session_state.temp == "GEN_IMAGE":
        st.info("🎨 Type what you want to create...")
        st.session_state.pop("temp")
    else: prompt = st.session_state.pop("temp")

if prompt or uploaded_file:
    is_image = any(x in prompt.lower() for x in ["create", "generate", "make a photo", "ki photo"]) if prompt else False
    user_msg = prompt if prompt else "Analyze this photo"
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.markdown(user_msg)

    with st.chat_message("assistant"):
        try:
            if is_image:
                img_url = generate_image(prompt)
                st.image(img_url)
                st.session_state.messages.append({"role": "assistant", "content": "Done!", "img_url": img_url})
            elif uploaded_file:
                res = model.generate_content([user_msg, uploaded_file])
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
            else:
                res = model.generate_content(user_msg)
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except: st.error("Try again later!")

st.markdown("<p style='text-align:center; color:#555;'>Developer: Mihir</p>", unsafe_allow_html=True)



