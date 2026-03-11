import streamlit as st
import google.generativeai as genai

# --- CONFIG & ADS SETUP ---
st.set_page_config(page_title="Mihir AI Pro", layout="centered")

# Ads styling
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .ad-box {background-color: #262730; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #4A90E2;}
    </style>
    """, unsafe_allow_html=True)

# API
genai.configure(api_key="AIzaSyCPFQf0hfAN6xHN-sRnU00UiSc1nDVsn2I")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- REWARD & LIMIT LOGIC ---
if "photo_count" not in st.session_state:
    st.session_state.photo_count = 0

# Title
st.markdown("<h1 style='text-align: center;'>🤖 Mihir AI Pro</h1>", unsafe_allow_html=True)

# TOP BANNER AD (Placeholder)
st.markdown(f'<div class="ad-box">💰 Banner Ad: {st.secrets.get("BANNER_ID", "ca-app-pub-3631540460014375/4130287701")}</div>', unsafe_allow_html=True)

# FILE UPLOADER (Universal Attach)
uploaded_file = st.file_uploader("📎 Kuch bhi attach karein (Photo/Doc)", type=['png', 'jpg', 'jpeg', 'pdf'])

if st.session_state.photo_count >= 5:
    st.warning("⚠️ Aapki 5 photos ki limit khatam ho gayi hai!")
    if st.button("📺 Watch 2 Reward Ads to get 5 More"):
        # Yahan Reward Ad ka logic APK conversion ke baad chalega
        st.session_state.photo_count = 0
        st.success("✅ Reward Added! Ab aap 5 photos aur bana sakte hain.")
        st.rerun()
else:
    # --- CHAT & SOLVER LOGIC ---
    if prompt := st.chat_input("Ask Mihir AI Universal Solver..."):
        # Image handling
        if uploaded_file:
            st.session_state.photo_count += 1
            # AI logic here...
        st.write(f"Remaining Free Photos: {5 - st.session_state.photo_count}")
