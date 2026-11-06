import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="StartupMateAI - Your AI Co-Founder",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Theme State Management
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Colors based on toggle state
if st.session_state.dark_mode:
    bg_color = "#0f172a"
    text_color = "#f8fafc"
    card_bg = "rgba(30, 41, 59, 0.85)"
    card_border = "rgba(255, 255, 255, 0.1)"
    input_bg = "#1e293b"
    pill_bg = "rgba(30, 41, 59, 0.8)"
    footer_bg = "rgba(15, 23, 42, 0.85)"
    brand_border = "#f8fafc"
else:
    bg_color = "#f6f7fb"
    text_color = "#131b2e"
    card_bg = "rgba(255, 255, 255, 0.82)"
    card_border = "rgba(255, 255, 255, 0.95)"
    input_bg = "#ffffff"
    pill_bg = "rgba(255, 255, 255, 0.72)"
    footer_bg = "rgba(246, 247, 251, 0.85)"
    brand_border = "#131b2e"

# 3. Dynamic Custom CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

    #MainMenu, header, footer {{visibility: hidden;}}
    [data-testid="stToolbar"] {{display: none;}}

    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        overflow-x: hidden;
        transition: background-color 0.3s ease, color 0.3s ease;
    }}

    /* Ambient Aurora Glow */
    .aurora-bg {{
        position: fixed;
        bottom: -22vh;
        left: 50%;
        transform: translateX(-50%);
        width: 78vw;
        max-width: 960px;
        height: 62vh;
        background: radial-gradient(
            circle at 50% 65%,
            rgba(253, 186, 140, 0.55) 0%,
            rgba(167, 139, 250,
