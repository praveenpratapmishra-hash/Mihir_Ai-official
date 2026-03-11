import streamlit as st
import google.generativeai as genai
import requests
import PIL.Image

# --- 1. AI CONFIG ---
genai.configure(api_key="AIzaSyCzKdc2QkS1l9KkypD7GcRZeToDKtyH5I4")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. CLEAN LOOK CSS ---
st.set_page_config(page_title="Mihir AI", layout="centered")

st.markdown("""
    <style>
    /* Sab pattiyaan aur branding hide karo */
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration, div[data-testid="stStatusWidget"] {display: none !important;}
    div[class^="st-emotion-cache-10pw50"], div[class^="st-emotion-cache-1dp5vir"] {display: none !important;}
    
    /* No Robot/User Face */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    
    /* Clean Gemini Chat */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 5px 0px !important;
        margin-left: -20px !important;
    }

    /* Browse files text hide - Only (+) Icon */
    [data-testid="stFileUploader"] section > label, [data-testid="stFileUploaderDropzoneInstructions"] {display: none !important;}
    [data-testid="stFileUploader"] section { border: none !important; padding: 0 !important; }

    /* Buttons Style */
    .stButton button {
        width: 100%;
        border-radius: 12px;
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #4A90E2;
        font-weight: bold;
        padding: 10px;
    }

    /* Input Bar Fix */
    .stChatInputContainer { position: fixed !important; bottom: 25px !important; left: 65px !important; right: 15px !important; z-index: 1000; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 27px !important; left: 10px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 24px; color: white; background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI (Mihir AI + 4 Buttons) ---
if "messages" not in st.session_state: st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Mihir AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Hello! Main aapki kya madad karun?</p>", unsafe_allow_html=True)
    
    # Chaaro Buttons ka Grid
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    with row1_col1:
        if st.button("🧠 Solve Problem"): st.session_state.temp = "Dost, help me solve this."
    with row1_col2:
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create a photo of "
    with row2_col1:
        if st.button("✨ Horoscope"): st.session_state.temp = "Aaj ka rashifal batao."
    with row2_col2:
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Meri kundali ke baare mein batao."

# Display Chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])

# --- 4. INPUT & LOGIC ---
up_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Ask Mihir AI...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or up_file:
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyze image"})
    with st.chat_message("user"): st.markdown(prompt if prompt else "Analyze image")

    with st.chat_message("assistant"):
        try:
            if any(x in (prompt or "").lower() for x in ["create", "photo", "banao", "image"]):
                url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "content": "Ye rahi photo!", "img": url})
            else:
                if up_file:
                    res = model.generate_content([prompt if prompt else "Batao ye kya hai?", PIL.Image.open(up_file)])
                else:
                    res = model.generate_content(f"Be a friendly Indian boy Mihir. Reply in Hinglish: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except:
            st.error("Dost, server me dikkat hai. Ek baar refresh karein!")

