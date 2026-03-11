import streamlit as st
import google.generativeai as genai
import requests
import PIL.Image

# --- 1. CONFIG & API ---
st.set_page_config(page_title="Mihir AI", layout="centered")
genai.configure(api_key="AIzaSyCzKdc2QkS1l9KkypD7GcRZeToDKtyH5I4")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. THE ULTIMATE CLEAN CSS (No Branding, No Faces) ---
st.markdown("""
    <style>
    /* 1. Patti aur Menu Hide */
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration, div[data-testid="stStatusWidget"] {display: none !important;}
    div[data-testid="stDecoration"] {display: none !important;}
    
    /* 2. No Robot/User Face (Gemini Style) */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    
    /* 3. Clean Chat Bubble */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 10px 0px !important;
        margin-left: -20px !important;
    }

    /* 4. Browse Text Hatana - Only Plus (+) Icon */
    [data-testid="stFileUploader"] section > label, [data-testid="stFileUploaderDropzoneInstructions"] {display: none !important;}
    [data-testid="stFileUploader"] section { border: none !important; padding: 0 !important; }

    /* 5. Plus Button aur Input placement */
    .stChatInputContainer { position: fixed !important; bottom: 25px !important; left: 65px !important; right: 15px !important; z-index: 1000; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 27px !important; left: 10px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 24px; color: white; background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center;
    }

    /* 6. 4 Buttons Style */
    .stButton button {
        width: 100%; border-radius: 12px; background-color: #1e1e1e;
        color: white; border: 1px solid #4A90E2; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI (Mihir AI Title & 4 Boxes) ---
if "messages" not in st.session_state: st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("<h1 style='text-align: center; color: #4A90E2; margin-top: -50px;'>Mihir AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Hello! Main aapki kya madad karun?</p>", unsafe_allow_html=True)
    
    # Grid for 4 Buttons
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🧠 Solve Problem"): st.session_state.temp = "Help me solve a problem."
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create a photo of "
    with c2:
        if st.button("✨ Horoscope"): st.session_state.temp = "Aaj ka rashifal batao."
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Meri kundali ke baare mein batao."

# Display Chat
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])

# --- 4. INPUT & AI ---
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
                st.session_state.messages.append({"role": "assistant", "content": "Photo taiyar hai!", "img": url})
            else:
                if up_file:
                    res = model.generate_content([prompt if prompt else "Describe this", PIL.Image.open(up_file)])
                else:
                    res = model.generate_content(f"Be a friendly Indian boy named Mihir. Reply in Hinglish: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except:
            st.error("Dost, ek baar refresh karein!")
