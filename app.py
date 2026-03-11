import streamlit as st
import google.generativeai as genai

# --- 1. PREMIUM INTERFACE (Plus Icon & Clean Look) ---
st.set_page_config(page_title="Mihir AI", layout="centered")

st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: white;}
    
    /* Plus Icon Styling */
    .stFileUploader section {
        padding: 0 !important;
        min-height: unset !important;
    }
    .stFileUploader label {display: none;}
    
    /* Branding */
    .app-title {text-align: center; color: #4A90E2; font-size: 35px; font-weight: bold; margin-top: -50px;}
    .footer-text {text-align: center; font-size: 14px; color: #888; font-style: italic; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="app-title">Mihir AI</div>', unsafe_allow_html=True)

# API Setup
genai.configure(api_key="AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I")
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state: st.session_state.messages = []
if "p_limit" not in st.session_state: st.session_state.p_limit = 0

# --- 2. THE PLUS (+) ICON BUTTON ---
# Isse user ko sirf plus icon dikhega file attach karne ke liye
uploaded_file = st.file_uploader("➕", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")

# 4 Action Boxes
if len(st.session_state.messages) == 0:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Analyze my Kundali"
        if st.button("🧠 Problem Solver"): st.session_state.temp = "Solve this logic problem"
    with col2:
        if st.button("📚 Study Help"): st.session_state.temp = "Explain this study topic"
        if st.button("✨ Horoscope"): st.session_state.temp = "Tell my daily horoscope"

# Chat Display
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# --- 3. BRANDING & INPUT ---
st.markdown('<div class="footer-text">Powered by developer Mihir</div>', unsafe_allow_html=True)

prompt = st.chat_input("Ask Mihir AI anything...")

if st.session_state.p_limit >= 5:
    st.error("⚠️ 5 Photo Limit Reached! Watch 2 Ads to unlock.")
else:
    if "temp" in st.session_state: prompt = st.session_state.pop("temp")
    if prompt or uploaded_file:
        user_msg = prompt if prompt else "Attached File Analysis"
        if uploaded_file: st.session_state.p_limit += 1
        
        st.session_state.messages.append({"role": "user", "content": user_msg})
        with st.chat_message("user"): st.markdown(user_msg)
        
        with st.chat_message("assistant"):
            res = model.generate_content([user_msg, uploaded_file] if uploaded_file else user_msg)
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})

