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

if st.session_state.dark_mode:
    bg_color = "#0b0f19"
    text_color = "#f8fafc"
    muted_text = "#94a3b8"
    card_bg = "rgba(30, 41, 59, 0.72)"
    card_border = "rgba(148, 163, 184, 0.16)"
    input_bg = "rgba(15, 23, 42, 0.88)"
    pill_bg = "rgba(30, 41, 59, 0.75)"
    footer_bg = "rgba(11, 15, 25, 0.85)"
    brand_border = "#818cf8"
    placeholder_color = "#64748b"
    scheme = "dark"
    input_border = "rgba(129, 140, 248, 0.28)"
    grid_color = "rgba(255, 255, 255, 0.04)"
else:
    bg_color = "#f8f9fc"
    text_color = "#0f172a"
    muted_text = "#64748b"
    card_bg = "rgba(255, 255, 255, 0.82)"
    card_border = "rgba(226, 232, 240, 0.95)"
    input_bg = "rgba(255, 255, 255, 0.95)"
    pill_bg = "rgba(255, 255, 255, 0.80)"
    footer_bg = "rgba(248, 249, 252, 0.85)"
    brand_border = "#1e293b"
    placeholder_color = "#94a3b8"
    scheme = "light"
    input_border = "rgba(99, 102, 241, 0.22)"
    grid_color = "rgba(15, 23, 42, 0.04)"

# 3. Dynamic Custom CSS & Modern Animations
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    #MainMenu, header, footer {{visibility: hidden;}}
    [data-testid="stToolbar"] {{display: none;}}

    .stApp {{
        background-color: {bg_color} !important;
        background-image: radial-gradient({grid_color} 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
        color: {text_color} !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        overflow-x: hidden;
        color-scheme: {scheme};
        transition: background-color 0.35s ease, color 0.35s ease;
    }}

    /* Multi-Orb Animated Mesh Background */
    .aurora-container {{
        position: fixed;
        inset: 0;
        overflow: hidden;
        z-index: 0;
        pointer-events: none;
    }}
    .orb {{
        position: absolute;
        border-radius: 50%;
        filter: blur(64px);
        opacity: 0.65;
    }}
    .orb-1 {{
        width: 42vw;
        height: 42vw;
        max-width: 520px;
        max-height: 520px;
        bottom: -12vh;
        left: 18%;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.55) 0%, rgba(99, 102, 241, 0.25) 60%, transparent 80%);
        animation: floatOrb1 9s ease-in-out infinite alternate;
    }}
    .orb-2 {{
        width:
