import streamlit as st
import google.generativeai as genai

# --- 1. FULL CLEAN LOOK (No Platform Branding) ---
st.set_page_config(page_title="Mihir AI Pro", layout="centered")

st.markdown("""
    <style>
    /* Sab kuch hide karo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: white;}
    
    /* Mihir AI Title Styling */
    .app-title {
        text-align: center; 
        color: #4A90E2; 
        font-size: 40px; 
        font-weight: bold;
        margin-top: -50px;
    }
    
    /* Powered by Branding */
    .footer-branding {
        text-align: center;
        font-size: 14px;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Sabse upar Mihir AI
st.markdown('<div class="app-title">Mihir AI</div>', unsafe_allow_html=True)

# API Setup
genai.configure(api_key="AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I")
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []
if "photo_count" not in st.session_state:
    st.session_state.photo_count = 0

# --- 2. ADS & ATTACHMENT ---
uploaded_file = st.file_uploader("📎 Kuch bhi attach karein", type=['png', 'jpg', 'jpeg', 'pdf'])

# 4 BOXES
if len(st.session_state.messages) == 0:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Analyze my Kundali"
        if st.button("🧠 Solve Problem"): st.session_state.temp = "Solve this problem"
    with col2:
        if st.button("📚 Study Help"): st.session_state.temp = "Help me with studies"
        if st.button("✨ Horoscope"): st.session_state.temp = "Tell my horoscope"

# Chat History
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# --- 3. POWERED BY BRANDING (Input bar se pehle) ---
st.markdown('<div class="footer-branding"><i><b>Powered by developer Mihir</b></i></div>', unsafe_allow_html=True)

# Input Bar
prompt = st.chat_input("Ask Mihir AI...")

# Business Logic (Ads & Limits)
if st.session_state.photo_count >= 5:
    st.warning("⚠️ 5 photo limit reached! Watch Reward Ad to continue.")
    # APK conversion ke baad yahan reward ad trigger hoga
else:
    if "temp" in st.session_state: prompt = st.session_state.pop("temp")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
