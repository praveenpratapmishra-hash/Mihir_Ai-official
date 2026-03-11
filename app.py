import streamlit as st
import google.generativeai as genai
import requests
import PIL.Image

# --- 1. AI CONFIG (YOUR KEY) ---
genai.configure(api_key="AIzaSyCzKdc2QkS1l9KkypD7GcRZeToDKtyH5I4")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. THE ULTIMATE GEMINI LOOK (CSS) ---
st.set_page_config(page_title="Mihir AI", layout="centered")

st.markdown("""
    <style>
    /* Sabse upar ki patti aur Streamlit menu hide karo */
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration, div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* Robot/User face hide karo */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    
    /* Chat Box styling (Gemini style) */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 5px 0px !important;
        margin-left: -20px !important;
    }

    /* "Browse Files" text hatao aur sirf (+) icon rakho */
    [data-testid="stFileUploader"] section > label, [data-testid="stFileUploaderDropzoneInstructions"] {display: none !important;}
    [data-testid="stFileUploader"] section { border: none !important; padding: 0 !important; }

    /* Input Bar & Plus Button position */
    .stChatInputContainer { position: fixed !important; bottom: 25px !important; left: 65px !important; right: 15px !important; z-index: 1000; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 27px !important; left: 10px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 24px; color: white; background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
    }
    
    /* 4 Boxes Styling */
    .stButton button { width: 100%; border-radius: 10px; background-color: #1e1e1e; color: white; border: 1px solid #4A90E2; height: 50px; font-weight: bold; }
    
    /* Mihir AI Title */
    .app-title { text-align: center; font-size: 32px; font-weight: bold; color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []

# --- 4. TOP UI (Title & 4 Boxes) ---
if not st.session_state.messages:
    st.markdown("<div class='app-title'>Mihir AI</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Solve Problem"): st.session_state.temp = "Help me solve a problem."
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create a photo of "
    with col2:
        if st.button("✨ Horoscope"): st.session_state.temp = "Aaj ka rashifal batao."
        if st.button("☸️ Kundali"): st.session_state.temp = "Kundali reading karein."

# Display Chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])

# --- 5. INPUT & LOGIC ---
up_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Ask Mihir AI...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or up_file:
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyzing image..."})
    with st.chat_message("user"): st.markdown(prompt if prompt else "Analyzing image...")

    with st.chat_message("assistant"):
        try:
            if any(x in (prompt or "").lower() for x in ["create", "photo", "banao", "image"]):
                url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "content": "Ye rahi aapki photo!", "img": url})
            else:
                if up_file:
                    res = model.generate_content([prompt if prompt else "What is in this photo?", PIL.Image.open(up_file)])
                else:
                    res = model.generate_content(f"You are Mihir AI, a friendly boy. Reply in Hinglish: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except:
            st.error("Dost, server busy hai, ek baar phir try karo!")
