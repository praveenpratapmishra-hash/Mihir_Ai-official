import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
import PIL.Image

# --- 1. FUNCTIONS ---
def generate_image(prompt):
    return f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"

# --- 2. UI & CSS ---
st.set_page_config(page_title="Mihir AI Dost", layout="centered")
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {background-color: #131314; color: #e3e3e3; margin-bottom: 110px !important;}
    
    /* Plus Button */
    [data-testid="stFileUploader"] { 
        width: 45px; position: fixed; bottom: 105px; left: 20px; z-index: 100; 
    }
    [data-testid="stFileUploaderSection"] {padding: 0; min-height: 0; border: none;}
    [data-testid="stFileUploader"] section > div {display: none;}
    [data-testid="stFileUploader"]::before {
        content: "＋"; font-size: 26px; color: white;
        background: #4A90E2; border-radius: 50%; width: 42px; height: 42px;
        display: flex; align-items: center; justify-content: center; cursor: pointer;
    }
    
    .stChatInputContainer { padding-bottom: 110px !important; margin-left: 55px !important; }
    .action-btn { width: 100%; height: 50px; background: #1e1e1e; border: 1px solid #4A90E2; color: white; border-radius: 10px; margin-bottom: 10px; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "photo_gallery" not in st.session_state: st.session_state.photo_gallery = []
if "photo_count" not in st.session_state: st.session_state.photo_count = 0
if "ads_watched" not in st.session_state: st.session_state.ads_watched = 0

# --- 4. AI SETUP ---
genai.configure(api_key="AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I")
system_instruction = "Tumhara naam Mihir AI hai. Tum user ke sachi dost ho. Prem se baat karo. Hello ka jawab dosti bhara do."
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_instruction)

# --- 5. APP INTERFACE ---

# 🖼️ Gallery Expander (Sabse upar)
if st.session_state.photo_gallery:
    with st.expander("🖼️ My Gallery (Purani Photos)"):
        cols = st.columns(3)
        for idx, img_url in enumerate(st.session_state.photo_gallery):
            cols[idx % 3].image(img_url, use_column_width=True)

# 📦 Chaaro Boxes (Khulte hi dikhenge)
if not st.session_state.messages:
    st.markdown("<h3 style='text-align: center; color: #4A90E2;'>Namaste Dost! Aaj kya karein?</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Solve Problem"): st.session_state.temp_prompt = "Dost, mujhe is problem ko solve karne mein help karo."
        if st.button("🎨 Create Photo"): st.session_state.temp_prompt = "Dost, ek bahut sundar photo banao."
    with col2:
        if st.button("✨ Horoscope"): st.session_state.temp_prompt = "Dost, mera aaj ka rashifal (horoscope) batao."
        if st.button("☸️ Kundali Reading"): st.session_state.temp_prompt = "Dost, meri kundali ke baare mein batao."

# 💬 Chat Display
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img_url" in m: st.image(m["img_url"])
        if m["content"]: st.markdown(m["content"])

# --- 6. INPUT LOGIC ---
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
prompt = st.chat_input("Mihir se baat karein...")

# Agar box par click kiya ho
if "temp_prompt" in st.session_state:
    prompt = st.session_state.pop("temp_prompt")

if prompt or uploaded_file:
    is_img_gen = any(x in (prompt or "").lower() for x in ["create", "generate", "photo", "image", "banao", "make"])
    
    # 5 Photo Limit
    if is_img_gen and st.session_state.photo_count >= 5:
        if st.session_state.ads_watched < 2:
            st.error(f"Dost, 5 photos poori ho gayi hain. Ad dekh kar help karo! ({st.session_state.ads_watched}/2)")
            if st.button("Ad Dekh Liya"): 
                st.session_state.ads_watched += 1
                st.rerun()
            st.stop()
        else:
            st.session_state.photo_count = 0
            st.session_state.ads_watched = 0

    user_msg = prompt if prompt else "Dost, ye photo dekho."
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"): st.markdown(user_msg)

    with st.chat_message("assistant"):
        try:
            if is_img_gen:
                with st.spinner("Aapke liye taiyar kar raha hoon..."):
                    img_url = generate_image(prompt)
                    st.image(img_url)
                    st.session_state.photo_gallery.append(img_url)
                    res = requests.get(img_url)
                    st.download_button("📥 Save to Gallery", data=BytesIO(res.content), file_name="mihir_ai.png")
                    st.session_state.photo_count += 1
                    st.session_state.messages.append({"role": "assistant", "content": "", "img_url": img_url})
            else:
                if uploaded_file:
                    img = PIL.Image.open(uploaded_file)
                    response = model.generate_content([prompt if prompt else "Batao dost ye kya hai?", img])
                else:
                    response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error("Dost, thodi problem aa rahi hai. Dubara try karo!")




