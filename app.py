import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
import PIL.Image

# --- 1. FUNCTIONS ---
def generate_image(prompt):
    # Flux model for superfast & high-quality images
    return f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"

# --- 2. UI & CSS (MOBILE OPTIMIZED) ---
st.set_page_config(page_title="Mihir AI Dost", layout="centered")

st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #131314; color: #e3e3e3;}

    /* Chat Input Container Fix */
    .stChatInputContainer {
        position: fixed !important;
        bottom: 30px !important;
        left: 60px !important; /* Space for Plus button */
        right: 10px !important;
        z-index: 1000;
        background: transparent !important;
    }

    /* Minimalist Plus (+) Button */
    [data-testid="stFileUploader"] {
        position: fixed !important;
        bottom: 32px !important;
        left: 10px !important;
        width: 45px !important;
        z-index: 1001;
    }
    [data-testid="stFileUploaderSection"] {padding: 0; min-height: 0; border: none;}
    [data-testid="stFileUploader"] section > div {display: none;}
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 24px; color: white;
        background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.5);
    }

    /* Spacing for messages so they don't hide behind input */
    .main .block-container {
        padding-bottom: 120px !important;
        padding-top: 20px !important;
    }

    /* Button Styling */
    .stButton button {
        width: 100%;
        border-radius: 10px;
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #4A90E2;
    }
    
    /* Gallery Image Styling */
    .gallery-img { border-radius: 10px; margin-bottom: 10px; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "photo_gallery" not in st.session_state: st.session_state.photo_gallery = []
if "photo_count" not in st.session_state: st.session_state.photo_count = 0
if "ads_watched" not in st.session_state: st.session_state.ads_watched = 0

# --- 4. AI SETUP (FRIENDLY MODE) ---
genai.configure(api_key="AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I")
system_instruction = "Tumhara naam Mihir AI hai. Tum user ke sachi dost ho. Hamesha prem aur dosti se baat karo. Hello ka jawab dosti bhara aur bada pyara do."
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

# --- 5. MAIN INTERFACE ---

# 🖼️ Photo Gallery (Purani photos yahan dikhengi)
if st.session_state.photo_gallery:
    with st.expander("🖼️ My Gallery (All Created Photos)"):
        cols = st.columns(3)
        for idx, img_url in enumerate(st.session_state.photo_gallery):
            cols[idx % 3].image(img_url, use_column_width=True)

# 📦 Chaaro Action Boxes (Startup Screen)
if not st.session_state.messages:
    st.markdown("<h3 style='text-align: center; color: #4A90E2;'>Namaste Dost! ❤️</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Aaj kya karein? Main aapki har tarah se help karunga.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Solve Problem"): st.session_state.temp_prompt = "Dost, mujhe ek problem solve karni hai."
        if st.button("🎨 Create Photo"): st.session_state.temp_prompt = "Dost, ek mast photo banao."
    with col2:
        if st.button("✨ Horoscope"): st.session_state.temp_prompt = "Dost, aaj ka mera rashifal batao."
        if st.button("☸️ Kundali Reading"): st.session_state.temp_prompt = "Dost, meri kundali dekho."

# 💬 Chat Display
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img_url" in m: st.image(m["img_url"])
        if m["content"]: st.markdown(m["content"])

# --- 6. INPUT PROCESSING ---
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Apne dost Mihir se baat karein...")

# Button click handle karna
if "temp_prompt" in st.session_state:
    prompt = st.session_state.pop("temp_prompt")

if prompt or uploaded_file:
    # Image Generation check
    is_img_gen = any(x in (prompt or "").lower() for x in ["create", "generate", "photo", "image", "banao", "make"])
    
    # 💰 AD LIMIT LOGIC
    if is_img_gen and st.session_state.photo_count >= 5:
        if st.session_state.ads_watched < 2:
            st.error(f"Dost, 5 photos limit poori ho gayi hai. Please ad dekh kar support karein! ({st.session_state.ads_watched}/2)")
            if st.button("I watched the Ad"):
                st.session_state.ads_watched += 1
                st.rerun()
            st.stop()
        else:
            st.session_state.photo_count = 0
            st.session_state.ads_watched = 0

    # User side display
    user_msg = prompt if prompt else "Analyze this photo, friend."
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.markdown(user_msg)

    # Assistant side response
    with st.chat_message("assistant"):
        try:
            if is_img_gen:
                with st.spinner("Bas ek minute dost, photo bana raha hoon..."):
                    img_url = generate_image(prompt)
                    st.image(img_url)
                    st.session_state.photo_gallery.append(img_url)
                    
                    # Download link fetch
                    res = requests.get(img_url)
                    st.download_button("📥 Save to Gallery", data=BytesIO(res.content), file_name="mihir_ai.png")
                    
                    st.session_state.photo_count += 1
                    st.session_state.messages.append({"role": "assistant", "content": "", "img_url": img_url})
            else:
                # Conversational AI or Image Vision
                if uploaded_file:
                    img = PIL.Image.open(uploaded_file)
                    response = model.generate_content([prompt if prompt else "Dost, batao is photo mein kya hai?", img])
                else:
                    response = model.generate_content(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("Maaf karna dost, server mein thodi dikkat hai. Dubara koshish karein!")





