import streamlit as st
import google.generativeai as genai

# --- 1. SETTINGS & CSS FOR PLUS ICON ---
st.set_page_config(page_title="Mihir AI", layout="centered")

st.markdown("""
    <style>
    /* Hide Streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: white;}
    
    /* Mihir AI Title */
    .app-title {text-align: center; color: #4A90E2; font-size: 35px; font-weight: bold; margin-top: -60px;}
    .footer-text {text-align: center; font-size: 15px; color: #888; font-weight: bold; margin-top: 20px;}

    /* Magic to turn File Uploader into a Small Plus Icon */
    [data-testid="stFileUploader"] {
        width: 50px;
        float: left;
        margin-top: -45px;
    }
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
        min-height: unset !important;
        border: none !important;
        background: transparent !important;
    }
    [data-testid="stFileUploader"] label {display: none;}
    .stFileUploader span {display:none;}
    .stFileUploader svg {color: #4A90E2; width: 30px; height: 30px;}
    
    /* Adjusting the input area to make space for the icon */
    .stChatInputContainer {
        padding-left: 50px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Sabse upar Mihir AI
st.markdown('<div class="app-title">Mihir AI</div>', unsafe_allow_html=True)

# API Setup
genai.configure(api_key="AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I")
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []
if "p_limit" not in st.session_state: st.session_state.p_limit = 0

# --- 2. THE ATTACH BUTTON (Ab chota icon dikhega) ---
uploaded_file = st.file_uploader("➕", type=['png', 'jpg', 'jpeg', 'pdf'])

# 4 Action Boxes
if len(st.session_state.messages) == 0:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Analyze my Kundali"
        if st.button("🧠 Problem Solver"): st.session_state.temp = "Solve this problem"
    with col2:
        if st.button("📚 Study Help"): st.session_state.temp = "Help me with studies"
        if st.button("✨ Horoscope"): st.session_state.temp = "Tell my horoscope"

# Chat Display
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# --- 3. BRANDING & INPUT ---
st.markdown('<div class="footer-text"><i><b>Powered by developer Mihir</b></i></div>', unsafe_allow_html=True)

prompt = st.chat_input("Ask Mihir AI anything...")

# Business Logic
if st.session_state.p_limit >= 5:
    st.error("⚠️ 5 Photo Limit Reached!")
    if st.button("Unlock Now (Watch 2 Ads)"):
        st.session_state.p_limit = 0
        st.rerun()
else:
    if "temp" in st.session_state: prompt = st.session_state.pop("temp")
    if prompt or uploaded_file:
        user_msg = prompt if prompt else "Analyze this attachment"
        if uploaded_file: st.session_state.p_limit += 1
        st.session_state.messages.append({"role": "user", "content": user_msg})
        with st.chat_message("user"): st.markdown(user_msg)
        with st.chat_message("assistant"):
            res = model.generate_content([user_msg, uploaded_file] if uploaded_file else user_msg)
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})

