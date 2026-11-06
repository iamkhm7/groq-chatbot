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

# 3. Dynamic Custom CSS & Layout Styling
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
            rgba(167, 139, 250, 0.45) 38%,
            rgba(129, 140, 248, 0.35) 62%,
            transparent 78%
        );
        filter: blur(52px);
        z-index: 0;
        pointer-events: none;
        animation: auroraFloat 7s ease-in-out infinite alternate;
    }}

    @keyframes auroraFloat {{
        0% {{ transform: translateX(-50%) scale(0.96) translateY(8px); opacity: 0.7; }}
        100% {{ transform: translateX(-50%) scale(1.05) translateY(-10px); opacity: 0.95; }}
    }}

    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(14px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .block-container {{
        position: relative;
        z-index: 2;
        padding-top: 6.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 760px !important;
    }}

    /* Fixed Header Anchored to Top Corners */
    .fixed-top-nav {{
        position: fixed;
        top: 20px;
        left: 28px;
        right: 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 99999;
        pointer-events: none;
    }}

    .pointer-events-auto {{
        pointer-events: auto;
    }}

    .logo-badge {{
        display: flex;
        align-items: center;
        gap: 8px;
        border: 1.5px solid {brand_border};
        border-radius: 999px;
