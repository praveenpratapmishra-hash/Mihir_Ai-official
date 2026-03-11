import streamlit as st
import google.generativeai as genai

# --- 1. PREMIUM LOOK (No Credits, No Menus) ---
st.set_page_config(page_title="Mihir AI", page_icon="🤖", layout="centered")

hide_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #0E1117; color: white;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# --- 2. API SETUP ---
genai.configure(api_key="AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Mihir AI</h1>", unsafe_allow_html=True)

# 4 BOXES (Saamne dikhne wale)
if len(st.session_state.messages) == 0:
    st.write("Hello! Main Mihir AI hoon. Main aapki kya madad kar sakta hoon?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("☸️ Kundali Analysis"): st.session_state.temp_input = "Analyze my Kundali"
        if st.button("🧠 Solve Math/Logic"): st.session_state.temp_input = "Solve this problem"
    with col2:
        if st.button("📚 Study Guide"): st.session_state.temp_input = "Explain this topic"
        if st.button("✨ Daily Horoscope"): st.session_state.temp_input = "Tell my horoscope"

# Chat History Display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Logic
prompt = st.chat_input("Ask Mihir AI anything...")
if "temp_input" in st.session_state:
    prompt = st.session_state.pop("temp_input")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
