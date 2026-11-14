import random

import streamlit as st
from groq import Groq

# ---------------------------------------------------------
# StartupMate AI — Streamlit app (light theme, phone-optimized)
# NOTE: keep every CSS block inside its triple quotes.
# Do not let an editor wrap lines inside them.
# ---------------------------------------------------------

st.set_page_config(
    page_title="StartupMate AI — Your AI Co-Founder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------- State -------------------------
SYSTEM_PROMPT = (
    "You are StartupMateAI, an expert startup co-founder, business strategist, "
    "and venture mentor. Help founders brainstorm ideas, test market viability, "
    "construct SWOT analyses, and build structured execution roadmaps. "
    "Be objective, constructive, practical, and realistic. Use clear headings "
    "and actionable steps when useful. Do not pretend assumptions are verified facts. "
    "SAFETY & DISCLAIMER RULES:\n"
    "1. Remind users that financial, legal, and tax projections are simulated "
    "and require professional verification.\n"
    "2. If a user mentions self-harm, danger, illegal activity, or severe distress, "
    "stop business advice, respond supportively, and direct them to emergency "
    "services or trusted authorities as appropriate.\n"
    "3. Never guarantee business success, funding, revenue, or market demand."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "page" not in st.session_state:
    st.session_state.page = "home"  # "home" first, then "app"

# ------------------------- Styles -------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;1,500;1,600&display=swap');

    :root {
        color-scheme: light;
        --bg: #f6f4fb;
        --surface: rgba(255, 255, 255, .86);
        --surface-soft: rgba(255, 255, 255, .70);
        --text: #19172b;
        --muted: #5f5d78;
        --border: rgba(111, 91, 166, .16);
        --input: #ffffff;
        --shadow: rgba(76, 55, 132, .10);
        --dialog-bg: #fdfcff;
    }

    html, body {
        background: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ---------- Background: glowing orange > pink > violet "sunrise" on a soft lavender base ---------- */
    .stApp {
        background-color: var(--bg) !important;
        background-image:
            /* fine grain, like the reference designs */
            url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='100%' height='100%' filter='url(%23n)' opacity='.09'/></svg>"),
            /* the sunrise glow: orange core, then coral, pink, violet */
            radial-gradient(122% 80% at 50% -22%,
                rgba(255, 140, 40, .96) 0%,
                rgba(255, 106, 80, .74) 24%,
                rgba(240, 80, 150, .50) 44%,
                rgba(156, 98, 240, .27) 62%,
                transparent 80%),
            /* soft violet and peach washes at the sides, cool lavender-blue at the bottom */
            radial-gradient(46% 38% at 0% 34%, rgba(150, 100, 240, .26), transparent 72%),
            radial-gradient(46% 38% at 100% 38%, rgba(255, 150, 175, .26), transparent 72%),
            radial-gradient(70% 40% at 50% 108%, rgba(130, 145, 255, .30), transparent 72%) !important;
        background-size: 220px 220px, 100% 100%, 100% 100%, 100% 100%, 100% 100% !important;
        background-repeat: repeat, no-repeat, no-repeat, no-repeat, no-repeat !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    [data-testid="stHeader"], #MainMenu, footer { visibility: hidden; }
    [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none; }

    .block-container {
        max-width: 1120px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 7rem !important;
    }
    p, li, label { color: var(--text); }

    /* ---------- Header ---------- */
    .brand {
        display: flex; align-items: center; gap: 10px;
        color: var(--text); font-weight: 800; letter-spacing: -.5px;
        font-size: 17px; padding: 8px 0;
    }
    .brand-icon {
        display: inline-flex; align-items: center; justify-content: center;
        width: 36px; height: 36px; border-radius: 13px; color: white;
        background: linear-gradient(140deg, #7955ef, #bd55d7);
        box-shadow: 0 7px 18px rgba(137, 91, 230, .28); font-size: 18px;
    }
    .topline {
        border-bottom: 1px solid var(--border);
        padding-bottom: 6px; margin-bottom: 14px;
    }
    /* Header rows (brand + button, workspace title + button) stay on ONE line on phones */
    div[data-testid="stHorizontalBlock"]:has(.brand),
    div[data-testid="stHorizontalBlock"]:has(.ws-head) {
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: .5rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.brand) > div:first-child,
    div[data-testid="stHorizontalBlock"]:has(.ws-head) > div:first-child {
        flex: 1 1 auto !important; min-width: 0 !important; width: auto !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.brand) > div:not(:first-child),
    div[data-testid="stHorizontalBlock"]:has(.ws-head) > div:not(:first-child) {
        flex: 0 0 auto !important; min-width: 0 !important; width: auto !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.brand) > div:not(:first-child) div.stButton,
    div[data-testid="stHorizontalBlock"]:has(.ws-head) > div:not(:first-child) div.stButton {
        display: flex; justify-content: flex-end;
    }

    /* ---------- Hero ---------- */
    .hero { text-align: center; padding: 44px 10px 22px; }
    .eyebrow {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 8px 14px; border-radius: 999px;
        color: #7a63d6; background: rgba(133, 104, 232, .10);
        border: 1px solid rgba(133, 104, 232, .22);
        font-size: 11px; font-weight: 800; letter-spacing: .6px;
    }
    .live-dot {
        width: 7px; height: 7px; display: inline-block; flex: none;
        border-radius: 50%; background: #32c99a;
        box-shadow: 0 0 0 4px rgba(50, 201, 154, .15);
    }
    .hero h1 {
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--text); font-size: clamp(36px, 6.5vw, 72px);
        line-height: 1.08; letter-spacing: -1.9px;
        font-weight: 500; margin: 22px 0 12px;
        text-wrap: balance;
    }
    .hero h1 em {
        font-weight: 500; background: linear-gradient(100deg, #ea580c, #a63fd9);
        -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent; padding-right: 4px;
    }
    .hero-sub {
        color: var(--muted); font-size: 15px; line-height: 1.75;
        max-width: 690px; margin: 0 auto;
    }
    .hero-joke { color: var(--muted); font-size: 11.5px; margin-top: 11px; }

    .workspace-note {
        border: 1px solid var(--border); border-radius: 18px;
        padding: 16px 18px; background: var(--surface-soft);
        backdrop-filter: blur(10px);
        color: var(--muted); font-size: 12.5px; line-height: 1.7;
        margin: 12px 0 18px;
    }

    .section-label {
        color: #8a6fe0; font-size: 10px; font-weight: 800;
        letter-spacing: 1.6px; text-transform: uppercase; margin: 14px 0 6px;
    }
    .section-title {
        color: var(--text); font-family: 'Playfair Display', serif;
        font-size: 29px; font-weight: 500; margin: 0 0 5px;
    }
    .section-copy { color: var(--muted); font-size: 12.5px; line-height: 1.6; }

    /* ---------- Tool cards ---------- */
    .tool-card {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 19px; padding: 17px 16px 13px;
        min-height: 135px; box-shadow: 0 9px 28px var(--shadow);
        margin-bottom: 0; backdrop-filter: blur(12px);
    }
    div[data-testid="stHorizontalBlock"]:has(.tool-card) [data-testid="stVerticalBlock"] { gap: .5rem !important; }
    .tool-icon {
        width: 37px; height: 37px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        background: rgba(133, 104, 232, .12); font-size: 18px; margin-bottom: 12px;
    }
    .tool-title { font-size: 13px; font-weight: 800; color: var(--text); margin-bottom: 5px; }
    .tool-copy { font-size: 11.5px; line-height: 1.55; color: var(--muted); }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        border: 1px solid var(--border) !important;
        border-radius: 999px !important;
        background: var(--surface) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important; font-size: 12.5px !important;
        min-height: 40px !important;
        box-shadow: 0 5px 15px var(--shadow) !important;
        transition: all .2s ease !important;
    }
    div.stButton > button:hover {
        border-color: #a58af2 !important;
        transform: translateY(-2px);
        box-shadow: 0 9px 22px rgba(129, 91, 225, .18) !important;
    }
    div.stButton > button p { font-size: inherit !important; margin: 0 !important; }

    /* ---------- Floating chat composer: one minimal pill ---------- */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"],
    .stChatFloatingInputContainer {
        background: transparent !important;
        background-color: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }
    [data-testid="stBottom"] { padding: 14px 18px 20px !important; }
    [data-testid="stBottomBlockContainer"] { max-width: 880px !important; padding: 0 !important; }

    [data-testid="stChatInput"] {
        background: var(--input) !important;
        background-color: var(--input) !important;
        border: 1px solid rgba(137, 111, 220, .28) !important;
        border-radius: 999px !important;
        box-shadow: 0 12px 34px var(--shadow), 0 2px 8px rgba(90, 65, 160, .05) !important;
        padding: 5px 9px 5px 20px !important;
        min-height: 62px !important;
        transition: border-color .2s ease, box-shadow .2s ease !important;
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(145, 111, 239, .75) !important;
        box-shadow: 0 14px 38px var(--shadow), 0 0 0 3px rgba(145, 111, 239, .12) !important;
    }
    /* Streamlit/BaseWeb draw a separate surface inside the shell: make every inner layer transparent */
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] > div > div,
    [data-testid="stChatInput"] form,
    [data-testid="stChatInput"] [data-baseweb="textarea"],
    [data-testid="stChatInput"] [data-baseweb="base-input"],
    [data-testid="stChatInput"] [data-baseweb="input"],
    [data-testid="stChatInput"] textarea {
        background: transparent !important;
        background-color: transparent !important;
        border: 0 !important;
        outline: 0 !important;
        box-shadow: none !important;
    }
    [data-testid="stChatInput"] textarea {
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        caret-color: #9b72ef !important;
        resize: none !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 15px !important;
        line-height: 1.5 !important;
        padding-top: 12px !important;
        padding-bottom: 10px !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--muted) !important;
        -webkit-text-fill-color: var(--muted) !important;
        opacity: .9 !important;
    }
    [data-testid="stChatInputSubmitButton"] {
        background: linear-gradient(135deg, #8058ef, #c34fd5) !important;
        color: white !important; border: 0 !important; border-radius: 50% !important;
        width: 42px !important; height: 42px !important; min-width: 42px !important;
        box-shadow: 0 5px 14px rgba(151, 83, 222, .28) !important;
        transition: transform .2s ease, box-shadow .2s ease !important;
    }
    [data-testid="stChatInputSubmitButton"]:hover {
        transform: translateY(-1px) scale(1.04);
        box-shadow: 0 7px 18px rgba(151, 83, 222, .38) !important;
    }

    /* ---------- Chat messages ---------- */
    [data-testid="stChatMessage"] {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 25px var(--shadow) !important;
        padding: 14px 18px !important;
        max-width: 880px; margin-left: auto; margin-right: auto;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li { color: var(--text) !important; }

    /* ---------- Dialog ---------- */
    [data-testid="stDialog"] > div,
    [data-testid="stModal"] > div,
    div[role="dialog"] {
        background: var(--dialog-bg) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 22px !important;
        box-shadow: 0 24px 80px rgba(60, 40, 120, .28) !important;
    }
    [data-testid="stDialog"] *,
    [data-testid="stModal"] *,
    div[role="dialog"] * { color: var(--text); }
    [data-testid="stDialog"] a,
    [data-testid="stModal"] a,
    div[role="dialog"] a { color: #8058ef !important; font-weight: 700 !important; }
    [data-testid="stDialog"] button,
    [data-testid="stModal"] button,
    div[role="dialog"] button { color: var(--text) !important; }
    [data-testid="stDialog"] a.dev-link,
    [data-testid="stModal"] a.dev-link,
    div[role="dialog"] a.dev-link { color: #ffffff !important; }

    /* ---------- Homepage ---------- */
    .rotator {
        display: inline-flex; align-items: center; gap: .55rem;
        margin-top: 20px; padding: .6rem 1.1rem; border-radius: 999px;
        background: var(--surface); border: 1px solid var(--border);
        box-shadow: 0 8px 22px var(--shadow); backdrop-filter: blur(10px);
        font-size: 14px; font-weight: 700; color: var(--text);
    }
    .rot-label { color: var(--muted); font-weight: 600; }
    .rot-window { display: inline-block; height: 1.5em; width: 15em; overflow: hidden; text-align: left; vertical-align: middle; }
    .rot-list { display: block; animation: rotateWords 11s cubic-bezier(.65, 0, .35, 1) infinite; }
    .rot-list span { display: block; height: 1.5em; line-height: 1.5em; white-space: nowrap; color: #8058ef; }
    @keyframes rotateWords {
        0%, 20%  { transform: translateY(0); }
        25%, 45% { transform: translateY(-20%); }
        50%, 70% { transform: translateY(-40%); }
        75%, 95% { transform: translateY(-60%); }
        100%     { transform: translateY(-80%); }
    }
    @keyframes popIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* CTA rows (the buttons are real Streamlit buttons) */
    div[data-testid="stHorizontalBlock"]:has(.cta-marker) {
        flex-wrap: nowrap !important; justify-content: center; gap: .7rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.cta-marker) > div {
        flex: 0 0 auto !important; width: auto !important; min-width: 0 !important;
    }
    div[data-testid="stElementContainer"]:has(.cta-marker),
    div.element-container:has(.cta-marker) { display: none !important; }
    div[data-testid="stHorizontalBlock"]:has(.cta-marker) button {
        min-height: 48px !important; padding: .4rem 1.4rem !important; font-size: 14px !important;
    }
    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(110deg, #8058ef, #bd4dd5) !important;
        color: #ffffff !important; border: 0 !important;
        box-shadow: 0 10px 26px rgba(137, 91, 230, .38) !important;
    }
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[data-testid="stBaseButton-primary"]:hover {
        box-shadow: 0 14px 32px rgba(189, 77, 213, .45) !important;
    }
    .fineprint { text-align: center; font-size: 11.5px; color: var(--muted); margin-top: 6px; line-height: 1.6; }

    /* Chat preview card */
    .peek {
        max-width: 560px; margin: 28px auto 0; text-align: left; overflow: hidden;
        border-radius: 22px; background: var(--surface); border: 1px solid var(--border);
        box-shadow: 0 18px 46px var(--shadow); backdrop-filter: blur(14px);
    }
    .peek-bar {
        display: flex; align-items: center; gap: 6px; padding: 11px 14px;
        border-bottom: 1px solid var(--border); font-size: 11px; font-weight: 700; color: var(--muted);
    }
    .peek-bar i { width: 9px; height: 9px; border-radius: 50%; display: inline-block; flex: none; }
    .peek-bar i:nth-child(1) { background: #ff6b6b; }
    .peek-bar i:nth-child(2) { background: #ffd166; }
    .peek-bar i:nth-child(3) { background: #4cd9a0; }
    .peek-bar span { margin-left: 6px; }
    .peek-body { padding: 16px 14px 18px; display: flex; flex-direction: column; gap: 10px; }
    .bubble { max-width: 84%; padding: 10px 13px; border-radius: 16px; font-size: 13px; line-height: 1.55; }
    .bubble.you { align-self: flex-end; background: linear-gradient(110deg, #8058ef, #bd4dd5); color: #fff; border-bottom-right-radius: 5px; }
    .bubble.bot { align-self: flex-start; background: #f3effd; color: var(--text); border-bottom-left-radius: 5px; }
    .peek-body .bubble:nth-child(1) { animation: popIn .5s ease-out .2s backwards; }
    .peek-body .bubble:nth-child(2) { animation: popIn .5s ease-out 1.1s backwards; }
    .peek-body .bubble:nth-child(3) { animation: popIn .5s ease-out 2.0s backwards; }
    .peek-body .bubble:nth-child(4) { animation: popIn .5s ease-out 2.9s backwards; }

    /* Stats, features, steps, closing */
    .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 34px; }
    .stat {
        background: var(--surface-soft); border: 1px solid var(--border); border-radius: 18px;
        padding: 14px 12px; text-align: center; backdrop-filter: blur(10px);
    }
    .stat b {
        display: block; font-family: 'Playfair Display', serif; font-size: 30px; font-weight: 600; line-height: 1.15;
        background: linear-gradient(100deg, #ea580c, #a63fd9); -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat span { display: block; font-size: 11.5px; color: var(--muted); margin-top: 3px; line-height: 1.4; }
    .home-section { margin-top: 54px; text-align: center; }
    .home-section .section-copy { max-width: 560px; margin: 0 auto 18px; }
    .feat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; text-align: left; }
    .steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; text-align: left; }
    .feat, .step {
        background: var(--surface); border: 1px solid var(--border); border-radius: 19px;
        padding: 17px 16px 16px; box-shadow: 0 9px 28px var(--shadow); backdrop-filter: blur(12px);
        transition: transform .2s ease, box-shadow .2s ease;
    }
    .feat:hover, .step:hover { transform: translateY(-3px); box-shadow: 0 14px 34px rgba(129, 91, 225, .16); }
    .step-num {
        font-family: 'Playfair Display', serif; font-style: italic; font-size: 36px; line-height: 1; margin-bottom: 8px;
        background: linear-gradient(100deg, #ea580c, #a63fd9); -webkit-background-clip: text; background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .closing { margin: 58px auto 14px; max-width: 640px; text-align: center; }
    .closing h2 {
        font-family: 'Playfair Display', serif; font-weight: 500; letter-spacing: -1px;
        font-size: clamp(30px, 5vw, 44px); line-height: 1.1; margin: 0 0 8px; color: var(--text);
    }
    .closing p { color: var(--muted); font-size: 14.5px; margin: 0 0 18px; }

    /* ---------- Footer ---------- */
    .disclaimer {
        text-align: center; color: var(--muted); font-size: 10.5px; line-height: 1.6;
        border-top: 1px solid var(--border); padding-top: 15px; margin-top: 28px;
    }

    @media (min-width: 701px) and (max-height: 820px) {
        .hero { padding: 22px 10px 8px; }
        .hero h1 { font-size: clamp(36px, 5vw, 54px); margin: 14px 0 8px; }
        .hero-joke { display: none; }
        .workspace-note { margin: 4px 0 12px; padding: 12px 16px; }
    }

    /* ---------- Phones ---------- */
    @media (max-width: 700px) {
        .block-container { padding: .8rem .9rem 8rem !important; }
        .brand { font-size: 16px; }
        .brand-icon { width: 32px; height: 32px; border-radius: 11px; font-size: 16px; }
        div[data-testid="stHorizontalBlock"]:has(.brand) button { font-size: 11.5px !important; padding: .2rem .8rem !important; }
        div[data-testid="stHorizontalBlock"]:has(.ws-head) button { font-size: 11.5px !important; padding: .2rem .8rem !important; }

        .hero { padding: 26px 0 14px; }
        .hero h1 { font-size: clamp(34px, 10vw, 44px); letter-spacing: -1px; margin: 16px 0 10px; }
        .hero-sub { font-size: 13.5px; line-height: 1.65; }
        .hero-joke { display: none; }
        .eyebrow { font-size: 10px; padding: 7px 12px; }
        .workspace-note { font-size: 12px; padding: 12px 14px; margin: 8px 0 14px; }

        /* Tool cards: a tidy 2 x 2 grid instead of four stacked cards */
        div[data-testid="stHorizontalBlock"]:has(.tool-card) {
            flex-wrap: wrap !important;
            gap: .6rem !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.tool-card) > div {
            flex: 1 1 calc(50% - .6rem) !important;
            min-width: calc(50% - .6rem) !important;
            width: calc(50% - .6rem) !important;
        }
        .tool-card { min-height: 132px; padding: 14px 12px 11px; border-radius: 17px; }
        .tool-icon { width: 33px; height: 33px; font-size: 16px; margin-bottom: 9px; }
        .tool-title { font-size: 12.5px; }
        .tool-copy { font-size: 10.5px; }
        div.stButton > button { min-height: 38px !important; font-size: 11.5px !important; }

        .section-title { font-size: 24px; }

        [data-testid="stBottom"] { padding: 8px 12px calc(12px + env(safe-area-inset-bottom)) !important; }
        [data-testid="stChatInput"] { min-height: 54px !important; padding: 3px 7px 3px 16px !important; }
        /* 16px stops iPhones from zooming the page when the box is tapped */
        [data-testid="stChatInput"] textarea { font-size: 16px !important; padding-top: 10px !important; padding-bottom: 8px !important; }
        [data-testid="stChatInputSubmitButton"] { width: 38px !important; height: 38px !important; min-width: 38px !important; }
        [data-testid="stChatMessage"] { padding: 12px 14px !important; border-radius: 16px !important; }
    }
    @media (max-width: 700px) {
        .rotator { font-size: 12.5px; padding: .5rem .9rem; gap: .4rem; }
        .rot-window { width: 14.5em; }
        div[data-testid="stHorizontalBlock"]:has(.cta-marker) { gap: .55rem !important; }
        div[data-testid="stHorizontalBlock"]:has(.cta-marker) button { min-height: 44px !important; padding: .35rem 1rem !important; font-size: 13px !important; }
        .peek { margin-top: 22px; border-radius: 18px; }
        .bubble { font-size: 12.5px; max-width: 90%; }
        .stats { grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 26px; }
        .stat b { font-size: 26px; }
        .home-section { margin-top: 40px; }
        .feat-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
        .steps { grid-template-columns: 1fr; gap: 10px; }
        .feat { padding: 14px 12px; border-radius: 17px; }
        .step { padding: 14px 16px; border-radius: 17px; }
        .step-num { font-size: 30px; }
        .closing { margin-top: 42px; }
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation: none !important; transition: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------- Developer dialog (requires streamlit>=1.37) -------------------------
@st.dialog("Meet the team")
def show_developer():
    st.markdown(
        """
        <style>
          .dev-profile { color: var(--text) !important; text-align: center; line-height: 1.65; }
          .dev-kicker {
            display: inline-block; margin: 2px 0 12px; padding: 5px 11px;
            border: 1px solid rgba(153, 119, 239, .28); border-radius: 999px;
            color: #8058ef !important; background: rgba(153, 119, 239, .10);
            font-size: 10px; font-weight: 800; letter-spacing: 1.1px; text-transform: uppercase;
          }
          .dev-name {
            color: var(--text) !important; font-size: 23px; font-weight: 800;
            letter-spacing: -.5px; line-height: 1.25; margin: 3px 0 5px;
          }
          .dev-role { color: #8058ef !important; font-size: 13px; font-weight: 700; margin-bottom: 13px; }
          .dev-education { color: var(--muted) !important; font-size: 13px; line-height: 1.8; margin: 0 0 17px; }
          .dev-link {
            display: inline-flex; align-items: center; justify-content: center;
            margin: 2px 0 20px; padding: 9px 17px; border-radius: 999px;
            background: linear-gradient(110deg, #8058ef, #bd4dd5);
            color: #fff !important; font-size: 12px; font-weight: 800;
            text-decoration: none !important; box-shadow: 0 7px 18px rgba(137, 91, 230, .22);
          }
          .dev-divider { height: 1px; width: 100%; background: var(--border); margin: 2px 0 15px; }
          .team-heading {
            color: var(--text) !important; text-align: left; font-size: 12px;
            font-weight: 800; letter-spacing: .4px; margin: 0 0 10px;
          }
          .team-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; text-align: left; }
          .team-member {
            border: 1px solid var(--border); border-radius: 12px; background: var(--surface-soft);
            color: var(--text) !important; padding: 10px 11px; font-size: 12px; font-weight: 700;
          }
          .team-member span {
            display: block; color: var(--muted) !important; font-size: 9px; font-weight: 600;
            letter-spacing: .7px; text-transform: uppercase; margin-bottom: 3px;
          }
          @media (max-width: 480px) {
            .team-grid { grid-template-columns: 1fr; }
            .dev-name { font-size: 20px; }
          }
        </style>

        <div class="dev-profile">
          <div class="dev-kicker">StartupMate AI · Project Team</div>
          <div class="dev-name">MARUF MD KAMRUL HASAN</div>
          <div class="dev-role">Main Developer</div>
          <p class="dev-education">
            Student<br>
            Department of Artificial Intelligence<br>
            Kyungdong University Global
          </p>
          <a class="dev-link" href="https://linktr.ee/iamkhm" target="_blank" rel="noopener noreferrer">
            More about the developer ↗
          </a>

          <div class="dev-divider"></div>
          <div class="team-heading">OTHER PROJECT MEMBERS</div>
          <div class="team-grid">
            <div class="team-member"><span>Project member</span>Sirjan Batala</div>
            <div class="team-member"><span>Project member</span>Ahmed Md Kazi Rakesh</div>
            <div class="team-member"><span>Project member</span>Manish Dubey</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------------- Header -------------------------
on_home = st.session_state.page == "home"
if on_home:
    header_left, header_right = st.columns([4, 1.6], vertical_alignment="center")
    home_slot = None
else:
    header_left, home_slot, header_right = st.columns([3.1, 1.15, 1.7], vertical_alignment="center")

with header_left:
    st.markdown(
        '<div class="brand"><span class="brand-icon">✦</span>'
        'StartupMate<span style="color:#956de8">AI</span></div>',
        unsafe_allow_html=True,
    )
if home_slot is not None:
    with home_slot:
        if st.button("🏠 Home", key="home_btn"):
            st.session_state.page = "home"
            st.rerun()
with header_right:
    if st.button("👨‍💻 Developer", key="developer_btn"):
        show_developer()

st.markdown('<div class="topline"></div>', unsafe_allow_html=True)

# ------------------------- Groq client -------------------------
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    client = None

MODEL = "openai/gpt-oss-20b"

QUICK_ACTIONS = [
    {
        "key": "brainstorm",
        "icon": "💡",
        "title": "Idea Brainstormer",
        "copy": "Turn a half-formed thought into a startup concept.",
        "button": "Brainstorm",
        "prompt": "Help me brainstorm a high-potential startup idea. Ask concise clarifying questions if needed, then outline the problem, target users, solution, differentiator, and MVP.",
    },
    {
        "key": "swot",
        "icon": "🔎",
        "title": "SWOT Validator",
        "copy": "Find strengths, weaknesses, opportunities and threats.",
        "button": "Run SWOT",
        "prompt": "Help me validate my startup idea with a rigorous SWOT analysis. If I have not provided an idea, ask me for it first. Separate known facts from assumptions.",
    },
    {
        "key": "roadmap",
        "icon": "🗺️",
        "title": "30-Day Roadmap",
        "copy": "Break the launch into small, achievable milestones.",
        "button": "Build roadmap",
        "prompt": "Create a practical 30-day startup MVP roadmap with weekly milestones, daily or grouped tasks, deliverables, and validation checkpoints. Ask for the startup idea if it is missing.",
    },
    {
        "key": "pitch",
        "icon": "📊",
        "title": "Pitch Deck Builder",
        "copy": "Shape your idea into a clear investor presentation.",
        "button": "Pitch outline",
        "prompt": "Create a clear 10-slide startup pitch deck outline covering problem, solution, product, market, business model, traction or validation, competition, go-to-market, team, and ask. Ask for the startup idea if missing.",
    },
]


def queue_prompt(prompt: str):
    st.session_state.pending_prompt = prompt


SURPRISE_PROMPTS = [
    "Surprise me! Pitch one genuinely creative startup idea that solves an everyday annoyance. Give it a catchy name and tagline, then honestly critique it.",
    "I'm feeling bold. Invent a quirky but viable startup idea for university students, then outline the problem, target users, and a tiny MVP I could build this weekend.",
    "Roll the dice: give me three very different startup ideas (one boring-but-profitable, one weird-but-promising, one ambitious), then tell me which one you would back and why.",
    "Pretend we are co-founders at our very first brainstorm. Pitch me an unexpected startup idea, then ask me three sharp questions to test it.",
]


def open_app(prompt=None):
    st.session_state.page = "app"
    if prompt:
        queue_prompt(prompt)
    st.rerun()


def cta_row(prefix: str, start_label: str):
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="cta-marker"></div>', unsafe_allow_html=True)
        start_clicked = st.button(start_label, key=f"{prefix}_start", type="primary")
    with right:
        surprise_clicked = st.button("🎲 Surprise me", key=f"{prefix}_surprise")
    if start_clicked:
        open_app()
    if surprise_clicked:
        open_app(random.choice(SURPRISE_PROMPTS))


def render_home():
    st.markdown(
        """
<section class="hero">
<div class="eyebrow"><span class="live-dot"></span> POSITION FILLED · AI CO-FOUNDER</div>
<h1>Hey there, <em>future founder.</em></h1>
<div class="hero-sub">I'm <b>StartupMate AI</b>, the co-founder who works for free, never steals your Wi-Fi, and has never once said "let's circle back."</div>
<div class="rotator"><span class="rot-label">Ask me to</span><span class="rot-window"><span class="rot-list"><span>brainstorm at 3 a.m.</span><span>roast your business plan</span><span>survive your 47th pivot</span><span>draft a 30-day roadmap</span><span>brainstorm at 3 a.m.</span></span></span></div>
</section>
""",
        unsafe_allow_html=True,
    )

    cta_row("top", "🚀 Start building")
    st.markdown(
        '<div class="fineprint">No sign-up. No credit card. No awkward small talk.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="peek">
<div class="peek-bar"><i></i><i></i><i></i><span>StartupMate AI · online (and caffeinated)</span></div>
<div class="peek-body">
<div class="bubble you">I want to start a business but I have zero ideas. Help?</div>
<div class="bubble bot">Perfect, a blank canvas! 🎨 Let's start with problems that annoy <i>you</i>. What did you complain about this week?</div>
<div class="bubble you">...My landlord's Wi-Fi.</div>
<div class="bubble bot">Great. Pain is the seed of every startup. ☕ Now, who else is suffering? Let's find your first 10 customers.</div>
</div>
</div>
<div class="stats">
<div class="stat"><b>0%</b><span>equity requested</span></div>
<div class="stat"><b>24/7</b><span>online, no snack breaks</span></div>
<div class="stat"><b>∞</b><span>patience for pivots</span></div>
<div class="stat"><b>0</b><span>hoodies required</span></div>
</div>
<div class="home-section">
<div class="section-label">WHAT I'M GOOD AT</div>
<div class="section-title">Four superpowers. Zero capes.</div>
<div class="section-copy">Pick one, or just start typing. I don't judge. (I mildly judge. Constructively.)</div>
<div class="feat-grid">
<div class="feat"><div class="tool-icon">💡</div><div class="tool-title">Idea Brainstormer</div><div class="tool-copy">Turns "I have a vague feeling" into an actual concept.</div></div>
<div class="feat"><div class="tool-icon">🔎</div><div class="tool-title">SWOT Validator</div><div class="tool-copy">Honest feedback, kindly delivered. Supportive, not delusional.</div></div>
<div class="feat"><div class="tool-icon">🗺️</div><div class="tool-title">30-Day Roadmap</div><div class="tool-copy">Because "someday" is not a deadline.</div></div>
<div class="feat"><div class="tool-icon">📊</div><div class="tool-title">Pitch Deck Builder</div><div class="tool-copy">Ten slides. Zero clip art. (Okay, maybe one.)</div></div>
</div>
</div>
<div class="home-section">
<div class="section-label">HOW IT WORKS</div>
<div class="section-title">Three steps. One mild existential crisis.</div>
<div class="section-copy">Okay, we're kidding about the crisis.</div>
<div class="steps">
<div class="step"><div class="step-num">1</div><div class="tool-title">Tell me your idea</div><div class="tool-copy">Or admit you don't have one. That's a perfectly good starting point.</div></div>
<div class="step"><div class="step-num">2</div><div class="tool-title">I poke holes (lovingly)</div><div class="tool-copy">SWOT, sharp questions, and a gentle reality check. Free of charge.</div></div>
<div class="step"><div class="step-num">3</div><div class="tool-title">You leave with a plan</div><div class="tool-copy">An actual roadmap. Not just vibes and a new logo.</div></div>
</div>
</div>
<div class="closing">
<h2>Ready when you are.</h2>
<p>The spreadsheets are already warming up.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    cta_row("bottom", "🚀 Let's go")
    st.markdown(
        '<div class="fineprint">By clicking start you agree to dream big and double-check the numbers.<br>'
        "I'm an AI, not your lawyer, accountant, or fortune teller.</div>",
        unsafe_allow_html=True,
    )


# ------------------------- Router -------------------------
if st.session_state.page == "home":
    render_home()
else:
    # ------------------------- Landing / chat -------------------------
    is_landing = len(st.session_state.messages) == 1

    if is_landing:
        st.markdown(
            """
            <section class="hero">
              <div class="eyebrow"><span class="live-dot"></span> YOUR AI CO-FOUNDER · IDEA TO MVP</div>
              <h1>Let's build your <em>big idea.</em></h1>
              <div class="hero-sub">
                Brainstorm, validate and plan your next move with an AI co-founder
                that works for equity-free enthusiasm.
              </div>
              <div class="hero-joke">You bring the idea. We'll bring the spreadsheets. Nobody has to wear a hoodie.</div>
            </section>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="workspace-note">✦ <b>Start anywhere:</b> pitch a rough idea, describe a problem, '
            'or pick one of the tools below. “I have no idea yet” is also a valid starting point.</div>',
            unsafe_allow_html=True,
        )

        cols = st.columns(4, gap="small")
        for col, action in zip(cols, QUICK_ACTIONS):
            with col:
                st.markdown(
                    f"""
                    <div class="tool-card">
                      <div class="tool-icon">{action["icon"]}</div>
                      <div class="tool-title">{action["title"]}</div>
                      <div class="tool-copy">{action["copy"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(action["button"], key=f'quick_{action["key"]}', use_container_width=True):
                    queue_prompt(action["prompt"])

        user_input = st.chat_input("Pitch your idea or ask anything…")
        if user_input:
            queue_prompt(user_input)

    else:
        head_left, head_right = st.columns([4, 1.4], vertical_alignment="center")
        with head_left:
            st.markdown(
                '<div class="ws-head">'
                '<div class="section-label">YOUR STARTUP WORKSPACE</div>'
                '<div class="section-title">The idea is in motion.</div>'
                '<div class="section-copy">Keep refining, questioning and building.</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        with head_right:
            if st.button("↺ New chat", key="new_chat"):
                st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                st.session_state.pending_prompt = None
                st.rerun()

        for msg in st.session_state.messages:
            if msg["role"] != "system":
                avatar = "🧑‍💻" if msg["role"] == "user" else "🚀"
                with st.chat_message(msg["role"], avatar=avatar):
                    st.markdown(msg["content"])

        user_input = st.chat_input("Ask your co-founder anything…")
        if user_input:
            queue_prompt(user_input)

    # ------------------------- Generate response -------------------------
    prompt = st.session_state.pending_prompt
    if prompt:
        st.session_state.pending_prompt = None
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        succeeded = False
        with st.chat_message("assistant", avatar="🚀"):
            if client is None:
                st.error(
                    "Groq is not configured. Add GROQ_API_KEY to your Streamlit secrets "
                    "before using AI generation."
                )
                st.session_state.messages.pop()
            else:
                try:
                    stream = client.chat.completions.create(
                        model=MODEL,
                        messages=st.session_state.messages,
                        stream=True,
                    )
                    reply = st.write_stream(
                        chunk.choices[0].delta.content or "" for chunk in stream
                    )
                    if reply:
                        st.session_state.messages.append(
                            {"role": "assistant", "content": reply}
                        )
                        succeeded = True
                    else:
                        st.warning("The model returned an empty response. Please try again.")
                        st.session_state.messages.pop()
                except Exception as exc:
                    st.session_state.messages.pop()
                    st.error(f"AI request failed: {exc}")

        # Only rerun on success, so error messages stay visible instead of vanishing.
        if succeeded:
            st.rerun()

# ------------------------- Footer -------------------------
st.markdown(
    """
    <div class="disclaimer">
      ⚡ AI-generated content can contain mistakes. Financial, legal and tax information
      is not professional advice. Verify important decisions with qualified professionals.
      <br><br>
      <span style="opacity:.8">StartupMate AI · Built for bold ideas and realistic to-do lists.</span>
    </div>
    """,
    unsafe_allow_html=True,
)
