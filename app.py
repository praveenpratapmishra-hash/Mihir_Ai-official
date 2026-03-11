import streamlit as st
import google.generativeai as genai
import PIL.Image

# --- 1. AI CONFIG (Direct Key) ---
# Key ko direct configure kar rahe hain taaki connection error na aaye
API_KEY = "AIzaSyCzKdc2QkS1l9KkypD7GcRZeToDKtyH5I4"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. CLEAN LOOK CSS (NO BROWSE FILES, NO BRANDING) ---
st.set_page_config(page_title="Mihir AI", layout="centered")

st.markdown("""
    <style>
    /* Sabse upar ki patti aur Streamlit menu hide karo */
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton, .viewerBadge_container__1QS13, #stDecoration, div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* Browse files text aur tooltip hide karo */
    [data-testid="stFileUploader"] section > label, 
    [data-testid="stFileUploaderDropzoneInstructions"],
    .st-emotion-cache-1ae8k9e { display: none !important; }
    div[data-testid="stTooltipHoverTarget"] { display: none !important; }

    /* Clean Chat (No Face Icons) */
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; padding: 5px 0px !important; }

    /* Input Bar & Plus (+) Button Fix */
    .stChatInputContainer { position: fixed !important; bottom: 25px !important; left: 65px !important; right: 15px !important; z-index: 1000; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 27px !important; left: 10px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploaderSection"] {padding: 0; min-height: 0; border: none;}
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 24px; color: white; background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
    }

    /* 4 Buttons Grid */
    .stButton button { width: 100%; border-radius: 12px; background-color: #1e1e1e; color: white; border: 1px solid #4A90E2; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. UI LOGIC ---
if "messages" not in st.session_state: st.session_state.messages = []

# Title and 4 Buttons
if not st.session_state.messages:
    st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Mihir AI</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Solve Problem"): st.session_state.temp = "Dost, help me solve this."
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create a photo of "
    with col2:
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
    st.session_state.messages.append({"role": "user", "content": prompt if prompt else "Analyze this image"})
    with st.chat_message("assistant"):
        try:
            if any(x in (prompt or "").lower() for x in ["create", "photo", "banao", "image"]):
                url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "content": "Ye rahi photo!", "img": url})
            else:
                if up_file:
                    res = model.generate_content([prompt if prompt else "Analyze", PIL.Image.open(up_file)])
                else:
                    res = model.generate_content(f"You are Mihir AI, a friendly boy. Reply in Hinglish: {prompt}")
                st.markdown(res.text)
                st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.error("Dost, server connect nahi ho pa raha. Ek baar page Refresh karo!")

