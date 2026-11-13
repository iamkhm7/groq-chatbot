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
    theme_vars = """
    :root {
        --bg-color: #0b0f19;
        --text-color: #f8fafc;
        --muted-text: #94a3b8;
        --card-bg: rgba(30, 41, 59, 0.72);
        --card-border: rgba(148, 163, 184, 0.16);
        --input-bg: rgba(15, 23, 42, 0.88);
        --pill-bg: rgba(30, 41, 59, 0.75);
        --footer-bg: rgba(11, 15, 25, 0.85);
        --brand-border: #818cf8;
        --placeholder-color: #64748b;
        --scheme: dark;
        --input-border: rgba(129, 140, 248, 0.28);
        --grid-color: rgba(255, 255, 255, 0.04);
    }
    """
    bg_color = "#0b0f19"
    text_color = "#f8fafc"
    muted_text = "#94a3b8"
    pill_bg = "rgba(30, 41, 59, 0.75)"
    card_border = "rgba(148, 163, 184, 0.16)"
else:
    theme_vars = """
    :root {
        --bg-color: #f8f9fc;
        --text-color: #0f172a;
        --muted-text: #64748b;
        --card-bg: rgba(255, 255, 255, 0.82);
        --card-border: rgba(226, 232, 240, 0.95);
        --input-bg: rgba(255, 255, 255, 0.95);
        --pill-bg: rgba(255, 255, 255, 0.80);
        --footer-bg: rgba(248, 249, 252, 0.85);
        --brand-border: #1e293b;
        --placeholder-color: #94a3b8;
        --scheme: light;
        --input-border: rgba(99, 102, 241, 0.22);
        --grid-color: rgba(15, 23, 42, 0.04);
    }
    """
    bg_color = "#f8f9fc"
    text_color = "#0f172a"
    muted_text = "#64748b"
    pill_bg = "rgba(255, 255, 255, 0.80)"
    card_border = "rgba(226, 232, 240, 0.95)"

st.markdown(f"<style>{theme_vars}</style>", unsafe_allow_html=True)

# 3. Main Stylesheet & Animations
# NOTE: keep this whole block inside the triple quotes. Do not let an editor wrap lines inside it.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}

    .stApp {
        background-color: var(--bg-color) !important;
        background-image: radial-gradient(var(--grid-color) 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
        color: var(--text-color) !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        overflow-x: hidden;
        color-scheme: var(--scheme);
        transition: background-color 0.35s ease, color 0.35s ease;
    }

    /* Multi-Orb Animated Mesh Background */
    .aurora-container {
        position: fixed;
        inset: 0;
        overflow: hidden;
        z-index: 0;
        pointer-events: none;
    }
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(64px);
        opacity: 0.65;
    }
    .orb-1 {
        width: 42vw;
        height: 42vw;
        max-width: 520px;
        max-height: 520px;
        bottom: -12vh;
        left: 18%;
        background: radial-gradient(circle, rgba(168, 85, 247, 0.55) 0%, rgba(99, 102, 241, 0.25) 60%, transparent 80%);
        animation: floatOrb1 9s ease-in-out infinite alternate;
    }
    .orb-2 {
        width: 38vw;
        height: 38vw;
        max-width: 480px;
        max-height: 480px;
        bottom: -15vh;
        right: 16%;
        background: radial-gradient(circle, rgba(251, 146, 60, 0.50) 0%, rgba(236, 72, 153, 0.35) 55%, transparent 80%);
        animation: floatOrb2 11s ease-in-out infinite alternate;
    }
    .orb-3 {
        width: 28vw;
        height: 28vw;
        max-width: 360px;
        max-height: 360px;
        top: 12vh;
        left: 50%;
        transform: translateX(-50%);
        background: radial-gradient(circle, rgba(56, 189, 248, 0.28) 0%, rgba(129, 140, 248, 0.15) 60%, transparent 80%);
        animation: floatOrb3 8s ease-in-out infinite alternate;
    }

    @keyframes floatOrb1 {
        0% { transform: translate(0, 0) scale(0.95); }
        100% { transform: translate(-30px, -25px) scale(1.08); }
    }
    @keyframes floatOrb2 {
        0% { transform: translate(0, 0) scale(1.05); }
        100% { transform: translate(35px, -30px) scale(0.92); }
    }
    @keyframes floatOrb3 {
        0% { transform: translateX(-50%) translateY(0) scale(0.9); }
        100% { transform: translateX(-45%) translateY(20px) scale(1.1); }
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes pulseDot {
        0%, 100% { transform: scale(1); opacity: 1; box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.6); }
        50% { transform: scale(1.15); opacity: 0.85; box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    }

    .block-container {
        position: relative;
        z-index: 2;
        padding-top: 6.2rem !important;
        padding-bottom: 5.5rem !important;
        max-width: 760px !important;
    }

    /* Fixed Header Anchored to Top Corners */
    .fixed-top-nav {
        position: fixed;
        top: 20px;
        left: 28px;
        right: 28px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 99999;
        pointer-events: none;
    }

    .pointer-events-auto {
        pointer-events: auto;
    }

    .logo-badge {
        display: flex;
        align-items: center;
        gap: 9px;
        border: 1.5px solid var(--brand-border);
        border-radius: 999px;
        padding: 6px 16px 6px 12px;
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-color);
        background: var(--input-bg);
        backdrop-filter: blur(12px);
        box-shadow: 3px 3px 0px #6366f1;
        transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1);
        cursor: pointer;
    }
    .logo-badge:hover {
        transform: translate(-2px, -2px) scale(1.03);
        box-shadow: 5px 5px 0px #ec4899;
    }
    .logo-icon-circle {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366f1, #ec4899);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: white;
    }

    /* Button Styling */
    div.stButton > button {
        background: var(--pill-bg) !important;
        backdrop-filter: blur(12px) !important;
        color: var(--text-color) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 999px !important;
        padding: 0.42rem 1.05rem !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 10px 24px rgba(99, 102, 241, 0.22) !important;
        border-color: #818cf8 !important;
    }

    /* Hero Badge, Animated Gradient Heading & Subtitle */
    .hero-badge-wrap {
        display: flex;
        justify-content: center;
        margin-top: 5vh;
        margin-bottom: 0.8rem;
        animation: fadeUp 0.55s ease-out both;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 5px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(129, 140, 248, 0.35);
        color: #818cf8;
    }
    .live-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #10b981;
        animation: pulseDot 2s infinite;
    }

    .hero-heading {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: clamp(2.4rem, 9vw, 3.8rem);
        line-height: 1.08;
        font-weight: 400;
        color: var(--text-color);
        text-align: center;
        margin-bottom: 0.65rem;
        letter-spacing: -0.02em;
        animation: fadeUp 0.65s ease-out 0.08s both;
    }
    .gradient-word {
        font-style: italic;
        background: linear-gradient(90deg, #6366f1, #ec4899, #f59e0b, #6366f1);
        background-size: 250% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientFlow 5s linear infinite;
        padding-right: 4px;
    }
    .hero-subtitle {
        text-align: center;
        font-size: 0.96rem;
        color: var(--muted-text);
        margin-bottom: 1.8rem;
        animation: fadeUp 0.7s ease-out 0.14s both;
    }

    /* Chat Input: Interactive Glowing Pill */
    [data-testid="stChatInput"] {
        background: var(--input-bg) !important;
        backdrop-filter: blur(16px) !important;
        border-radius: 999px !important;
        border: 1.5px solid var(--input-border) !important;
        box-shadow: 0 14px 36px rgba(99, 102, 241, 0.12), 0 2px 6px rgba(0, 0, 0, 0.04) !important;
        padding: 6px 58px 6px 22px !important;
        position: relative !important;
        transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1) !important;
        animation: fadeUp 0.75s ease-out 0.18s backwards;
    }
    [data-testid="stChatInput"]:hover {
        border-color: rgba(168, 85, 247, 0.5) !important;
        box-shadow: 0 16px 40px rgba(168, 85, 247, 0.16) !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 18px 44px rgba(99, 102, 241, 0.22), 0 0 0 4px rgba(129, 140, 248, 0.18) !important;
        transform: translateY(-2px);
    }
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="base-input"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 999px !important;
    }
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        color: var(--text-color) !important;
        font-size: 1rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        padding: 0.65rem 0 !important;
        caret-color: #ec4899;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--placeholder-color) !important;
        opacity: 1 !important;
    }
    [data-testid="stChatInputSubmitButton"] {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        position: absolute !important;
        top: 50% !important;
        bottom: auto !important;
        right: 8px !important;
        transform: translateY(-50%);
        box-shadow: 0 4px 14px rgba(168, 85, 247, 0.4) !important;
        transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    [data-testid="stChatInputSubmitButton"]:hover {
        transform: translateY(-50%) scale(1.12) rotate(6deg) !important;
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.55) !important;
    }
    [data-testid="stChatInputSubmitButton"] svg {
        fill: #ffffff !important;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background: var(--card-bg) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 20px !important;
        padding: 16px 20px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 8px 26px rgba(0, 0, 0, 0.05) !important;
        color: var(--text-color) !important;
        animation: fadeUp 0.35s cubic-bezier(0.16, 1, 0.3, 1) backwards;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 30px rgba(99, 102, 241, 0.08) !important;
    }
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li, [data-testid="stChatMessage"] span {
        color: var(--text-color) !important;
    }

    div.stButton > button p {
        font-size: inherit !important;
        line-height: 1.25 !important;
        margin: 0 !important;
    }

    /* Quick-action chips */
    div[data-testid="stHorizontalBlock"]:has(.qa-marker) {
        flex-wrap: nowrap !important;
        justify-content: safe center;
        gap: 0.65rem !important;
        overflow-x: auto;
        padding: 14px 6px 30px 6px;
        scrollbar-width: none;
        animation: fadeUp 0.8s ease-out 0.24s backwards;
    }
    div[data-testid="stHorizontalBlock"]:has(.qa-marker)::-webkit-scrollbar { display: none; }
    div[data-testid="stHorizontalBlock"]:has(.qa-marker) > div {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: 0 !important;
    }
    div[data-testid="stElementContainer"]:has(.qa-marker),
    div.element-container:has(.qa-marker) {
        display: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.qa-marker) button {
        background: var(--pill-bg) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid var(--input-border) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
        color: var(--text-color) !important;
        padding: 0.5rem 1.15rem !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
        transition: all 0.28s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.qa-marker) button:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.14), rgba(236, 72, 153, 0.14)) !important;
        border-color: #a855f7 !important;
        box-shadow: 0 10px 22px rgba(168, 85, 247, 0.18) !important;
        transform: translateY(-3px) scale(1.03) !important;
    }

    /* Top-right button bar */
    div[data-testid="stHorizontalBlock"]:has(.topbar-marker) {
        position: fixed !important;
        top: 20px;
        right: 28px;
        width: 270px !important;
        max-width: calc(100vw - 200px);
        gap: 10px !important;
        flex-wrap: nowrap !important;
        z-index: 99999;
    }
    div[data-testid="stHorizontalBlock"]:has(.topbar-marker) > div {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        width: auto !important;
    }
    div[data-testid="stElementContainer"]:has(.topbar-marker),
    div.element-container:has(.topbar-marker) {
        display: none !important;
    }

    [data-testid="stBottom"], [data-testid="stBottom"] > div {
        background: transparent !important;
    }

    /* Disclaimer & AI Notice */
    .notice-short { display: none; }
    .disclaimer-footer {
        position: fixed;
        bottom: 10px;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 0.73rem;
        color: var(--muted-text);
        z-index: 10;
        pointer-events: none;
        background: var(--footer-bg);
        backdrop-filter: blur(8px);
        padding: 5px;
    }

    /* Phones */
    @media (max-width: 640px) {
        .orb { filter: blur(40px); animation: none; }
        .block-container {
            padding-top: 4.8rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 6rem !important;
        }
        .fixed-top-nav { top: 14px; left: 12px; right: 12px; }
        .logo-badge {
            padding: 5px 12px;
            font-size: 0.8rem;
            box-shadow: 2px 2px 0px #6366f1;
        }
        .logo-icon-circle { display: none; }
        div[data-testid="stHorizontalBlock"]:has(.topbar-marker) {
            top: 14px;
            right: 12px;
            width: 220px !important;
            max-width: none;
            gap: 6px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.topbar-marker) button {
            padding: 0.3rem 0.3rem !important;
            font-size: 0.72rem !important;
            white-space: nowrap !important;
        }
        .hero-badge-wrap { margin-top: 1.5vh; }
        .hero-heading { margin-bottom: 0.5rem; }
        .hero-subtitle { font-size: 0.85rem; margin-bottom: 1.2rem; }
        div[data-testid="stHorizontalBlock"]:has(.qa-marker) button {
            font-size: 0.8rem !important;
            padding: 0.42rem 0.95rem !important;
        }
        [data-testid="stChatInput"] { padding: 4px 52px 4px 16px !important; }
        [data-testid="stChatInput"] textarea { font-size: 0.92rem !important; }
        [data-testid="stChatMessage"] { padding: 12px 14px !important; }
        .notice-full { display: none; }
        .notice-short { display: inline; }
        .disclaimer-footer {
            bottom: 6px;
            font-size: 0.62rem;
            padding: 4px 76px 4px 10px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    }
    @media (max-width: 380px) {
        div[data-testid="stHorizontalBlock"]:has(.topbar-marker) { width: 200px !important; }
        div[data-testid="stHorizontalBlock"]:has(.topbar-marker) button { font-size: 0.66rem !important; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation: none !important; transition: none !important; }
    }
</style>

<div class="aurora-container">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
</div>
<div class="disclaimer-footer">
    <span class="notice-full">⚡ AI Notice: Content is AI-generated and can contain mistakes. Not professional business/legal advice. Human verification required.</span>
    <span class="notice-short">⚡ AI-generated, may contain mistakes. Verify before use.</span>
</div>
""", unsafe_allow_html=True)

# 4. Logo on Top-Left
st.markdown("""
<div class="fixed-top-nav">
    <div class="pointer-events-auto">
        <div class="logo-badge">
            <span class="logo-icon-circle">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            </span>
            StartupMateAI
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# 5. Developer Details Dialog (requires streamlit>=1.37)
@st.dialog("Developer Details")
def show_developer():
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Patrick+Hand+SC&display=swap');
div[role="dialog"] {{
    background: {bg_color} !important;
    border-radius: 26px !important;
    border: 1px solid {card_border} !important;
    box-shadow: 0 24px 60px rgba(99, 102, 241, 0.25) !important;
}}
div[role="dialog"] button[aria-label="Close"],
div[role="dialog"] button[aria-label="Close"] svg {{
    color: {text_color} !important;
}}
div[role="dialog"] h2 {{
    font-family: 'Patrick Hand SC', cursive !important;
    font-size: 1.55rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: {text_color} !important;
    text-align: center;
    width: fit-content;
    margin: 0 auto !important;
    padding: 0.35rem 1.6rem !important;
    border: 3px solid transparent;
    border-radius: 999px;
    background:
        linear-gradient({bg_color}, {bg_color}) padding-box,
        linear-gradient(90deg, #6366f1, #ec4899, #f59e0b) border-box;
}}
.dev-card {{
    font-family: 'Patrick Hand SC', cursive;
    color: {text_color} !important;
    background: {bg_color};
    border-radius: 18px;
    padding: 0.6rem 0.4rem 0.3rem 0.4rem;
    text-align: center;
}}
.dev-card div, .dev-card span, .dev-card a {{
    color: {text_color};
}}
.dev-name {{
    font-size: 1.65rem;
    letter-spacing: 0.05em;
    line-height: 1.45;
}}
.dev-info {{
    font-size: 1.25rem;
    letter-spacing: 0.06em;
    line-height: 1.55;
    margin-top: 0.6rem;
    color: {muted_text} !important;
}}
.dev-more {{
    text-align: center;
    margin: 1.4rem 0 1.2rem 0;
}}
.dev-more summary {{
    display: inline-block;
    list-style: none;
    cursor: pointer;
    background: linear-gradient(135deg, #6366f1, #ec4899);
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    padding: 0.5rem 1.4rem;
    border-radius: 999px;
    box-shadow: 0 4px 14px rgba(236, 72, 153, 0.3);
}}
.dev-more summary::-webkit-details-marker {{ display: none; }}
.dev-extra {{
    font-size: 1.1rem;
    letter-spacing: 0.04em;
    margin-top: 0.9rem;
}}
.dev-social {{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 0.6rem;
}}
.dev-social a {{
    display: flex;
    align-items: center;
    gap: 7px;
    color: {text_color} !important;
    background: {pill_bg};
    border: 1px solid {card_border};
    padding: 8px 14px;
    border-radius: 999px;
    text-decoration: none !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
}}
</style>
<div class="dev-card">
<div class="dev-name">Kamrul Hasan Maruf</div>
<div class="dev-name">(Maruf MD Kamrul Hasan)</div>
<div class="dev-info">2617308<br>Department of Artificial Intelligence<br>Kyungdong University Global<br>South Korea</div>
<details class="dev-more"><summary>✨ More Info</summary><div class="dev-extra">Built with Streamlit &amp; Groq AI for Topic 84.</div></details>
<div class="dev-social">
<a href="https://github.com/iamkhm7" target="_blank">GitHub</a>
<a href="https://instagram.com/_iamkhm_" target="_blank">Instagram</a>
<a href="https://facebook.com/iamkhm" target="_blank">Facebook</a>
</div>
</div>
""", unsafe_allow_html=True)


# 6. Top-Right Buttons
btn_col1, btn_col2 = st.columns(2)

with btn_col1:
    st.markdown('<div class="topbar-marker"></div>', unsafe_allow_html=True)
    toggle_label = "☀️ Light" if st.session_state.dark_mode else "🌙 Dark"
    if st.button(toggle_label, use_container_width=True, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

with btn_col2:
    if st.button("👨‍💻 Developer", use_container_width=True, key="dev_btn"):
        show_developer()

# 7. Groq Connection & System Prompt
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = (
    "You are StartupMateAI, an expert startup co-founder, business strategist, and venture mentor. "
    "Your objective is to help founders brainstorm ideas, test market viability, construct SWOT analyses, "
    "and build structured execution roadmaps. "
    "SAFETY & DISCLAIMER RULES:\n"
    "1. Always remind users that financial, legal, and tax projections are simulated and require professional verification.\n"
    "2. If a user mentions self-harm, danger, illegal activity, or severe distress, immediately stop business advice, express care, and instruct them to contact emergency services or trusted authorities.\n"
    "3. Be objective, constructive, and realistic in startup critique."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

user_prompt = None

# 8. Landing View
if len(st.session_state.messages) == 1:
    st.markdown("""
    <div class="hero-badge-wrap">
        <div class="hero-badge"><span class="live-dot"></span> AI Co-Founder • Idea to MVP</div>
    </div>
    <div class="hero-heading">Let's create a <span class="gradient-word">startup.</span></div>
    <div class="hero-subtitle">Brainstorm high-potential ventures, validate with SWOT, and map your 30-day launch.</div>
    """, unsafe_allow_html=True)

    inline_input = st.chat_input("Pitch your idea or ask anything...")
    if inline_input:
        user_prompt = inline_input

    st.write("")
    qa = st.columns(4)
    with qa[0]:
        st.markdown('<div class="qa-marker"></div>', unsafe_allow_html=True)

    if qa[0].button("💡 Brainstorm Idea", key="qa_brainstorm"):
        user_prompt = "Help me brainstorm a high-potential SaaS startup idea for university students."
    if qa[1].button("🔍 Validate with SWOT", key="qa_swot"):
        user_prompt = "Conduct a rigorous SWOT analysis for an AI-powered personal productivity app."
    if qa[2].button("🗺️ 30-Day Roadmap", key="qa_roadmap"):
        user_prompt = "Create a lean 30-day MVP launch roadmap for a new startup concept."
    if qa[3].button("📊 Pitch Deck", key="qa_pitch"):
        user_prompt = "Give me a 10-slide seed pitch deck structure for investors."

# 9. Active Chat View
else:
    _, top_c2 = st.columns([5, 1])
    with top_c2:
        if st.button("↺ New Pitch", use_container_width=True, key="new_pitch"):
            st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            avatar = "🧑‍💻" if msg["role"] == "user" else "🚀"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    docked_input = st.chat_input("Ask your co-founder anything...")
    if docked_input:
        user_prompt = docked_input

# 10. Response Generation
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_prompt)

    reply = None
    with st.chat_message("assistant", avatar="🚀"):
        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
                stream=True,
            )
            reply = st.write_stream(
                chunk.choices[0].delta.content or "" for chunk in stream
            )
        except Exception as e:
            st.session_state.messages.pop()
            st.error(f"API Error: {e}")

    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
