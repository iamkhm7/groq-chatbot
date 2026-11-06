import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="StartupMateAI",
    page_icon="🟣",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS & Smooth Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

    /* Hide default Streamlit UI elements */
    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}

    /* Force crisp light background & dark slate text regardless of OS dark mode */
    .stApp {
        background-color: #f6f7fb !important;
        color: #131b2e !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        overflow-x: hidden;
    }

    /* Animated Bottom Aurora Glow Orb */
    .aurora-bg {
        position: fixed;
        bottom: -22vh;
        left: 50%;
        transform: translateX(-50%);
        width: 78vw;
        max-width: 960px;
        height: 62vh;
        background: radial-gradient(
            circle at 50% 65%,
            rgba(253, 186, 140, 0.75) 0%,
            rgba(167, 139, 250, 0.65) 38%,
            rgba(129, 140, 248, 0.45) 62%,
            rgba(246, 247, 251, 0) 78%
        );
        filter: blur(42px);
        z-index: 0;
        pointer-events: none;
        animation: auroraFloat 7s ease-in-out infinite alternate;
    }

    @keyframes auroraFloat {
        0% { transform: translateX(-50%) scale(0.96) translateY(8px); opacity: 0.88; }
        100% { transform: translateX(-50%) scale(1.05) translateY(-10px); opacity: 1; }
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes dotPulse {
        0%, 100% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.12); opacity: 1; }
    }

    /* Ensure Streamlit content sits above the aurora orb */
    .block-container {
        position: relative;
        z-index: 2;
        padding-top: 6.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 760px !important;
    }

    /* Fixed Top Navigation Bar */
    .top-nav {
        position: fixed;
        top: 22px;
        left: 32px;
        right: 32px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 100;
        animation: fadeUp 0.5s ease-out;
    }
    .brand-wrap {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-dot {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: linear-gradient(135deg, #c084fc, #f472b6);
        animation: dotPulse 3.5s ease-in-out infinite;
    }
    .brand-pill {
        border: 1.5px solid #131b2e;
        border-radius: 999px;
        padding: 4px 16px;
        font-size: 0.95rem;
        font-weight: 500;
        color: #131b2e;
        background: #f6f7fb;
        box-shadow: 2px 3px 0px #131b2e;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: pointer;
    }
    .brand-pill:hover {
        transform: translate(-1px, -1px);
        box-shadow: 3px 4px 0px #131b2e;
    }
    .nav-right {
        display: flex;
        align-items: center;
        gap: 14px;
        color: #64748b;
        font-size: 0.88rem;
        font-weight: 500;
    }
    .profile-circle {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        color: #131b2e;
        font-size: 0.85rem;
    }

    /* Centered Serif Greeting */
    .hero-heading {
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 3.6rem;
        font-weight: 400;
        color: #131b2e;
        text-align: center;
        margin-top: 8vh;
        margin-bottom: 1.8rem;
        letter-spacing: -0.02em;
        animation: fadeUp 0.6s ease-out 0.05s both;
    }

    /* White Rounded Chat Input Card */
    [data-testid="stChatInput"] {
        background: #ffffff !important;
        border-radius: 22px !important;
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
        box-shadow: 0 14px 36px rgba(19, 27, 46, 0.07) !important;
        padding: 10px 14px 42px 14px !important;
        position: relative !important;
        transition: box-shadow 0.25s ease, transform 0.25s ease !important;
        animation: fadeUp 0.65s ease-out 0.12s both;
    }
    [data-testid="stChatInput"]:focus-within {
        box-shadow: 0 18px 42px rgba(99, 102, 241, 0.13) !important;
        transform: translateY(-1px);
    }
    [data-testid="stChatInput"] > div {
        background: transparent !important;
        border: none !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #131b2e !important;
        font-size: 1rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* Decorative '+' icon inside the bottom-left of the input card */
    [data-testid="stChatInput"]::after {
        content: "+";
        position: absolute;
        bottom: 12px;
        left: 18px;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        color: #64748b;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.05rem;
        font-weight: 400;
        pointer-events: none;
    }

    /* Dark Circular Up-Arrow Submit Button */
    [data-testid="stChatInputSubmitButton"] {
        background-color: #131b2e !important;
        color: #ffffff !important;
        border-radius: 50% !important;
        width: 34px !important;
        height: 34px !important;
        position: absolute !important;
        bottom: 10px !important;
        right: 14px !important;
        transition: transform 0.2s ease, background-color 0.2s ease !important;
    }
    [data-testid="stChatInputSubmitButton"]:hover {
        transform: scale(1.08) !important;
        background-color: #2563eb !important;
    }
    [data-testid="stChatInputSubmitButton"] svg {
        fill: #ffffff !important;
    }

    /* Suggestion Pill Buttons */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.72) !important;
        backdrop-filter: blur(10px) !important;
        color: #1e293b !important;
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        border-radius: 999px !important;
        padding: 0.42rem 0.95rem !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 14px rgba(19, 27, 46, 0.05) !important;
        transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
        animation: fadeUp 0.7s ease-out 0.2s both;
        white-space: nowrap !important;
    }
    div.stButton > button:hover {
        background: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.12) !important;
        border-color: #c7d2fe !important;
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.82) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.95) !important;
        border-radius: 18px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 6px 20px rgba(19, 27, 46, 0.04) !important;
        color: #131b2e !important;
        animation: fadeUp 0.35s ease-out both;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {
        color: #131b2e !important;
    }

    /* Transparent bottom dock when chatting */
    [data-testid="stBottom"] {
        background: transparent !important;
    }
    [data-testid="stBottom"] > div {
        background: transparent !important;
    }

    /* Bottom Disclaimer Footer */
    .footer-note {
        position: fixed;
        bottom: 14px;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 0.76rem;
        color: #64748b;
        z-index: 10;
        pointer-events: none;
    }
</style>

<!-- Background Glowing Orb & Fixed Header -->
<div class="aurora-bg"></div>
<div class="top-nav">
    <div class="brand-wrap">
        <div class="brand-dot"></div>
        <div class="brand-pill">StartupMateAI</div>
    </div>
    <div class="nav-right">
        <span>History</span>
        <div class="profile-circle">👤</div>
    </div>
</div>
<div class="footer-note">StartupMateAI can make mistakes. Check anything important.</div>
""", unsafe_allow_html=True)

# 3. Connect to Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

@st.cache_data(ttl=3600)
def get_available_models():
    all_models = [
        m.id for m in client.models.list().data
        if not any(x in m.id.lower() for x in ["whisper", "tts", "guard", "orpheus", "safeguard"])
    ]
    preferred = [
        "llama-3.1-8b-instant",
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "openai/gpt-oss-20b",
        "qwen/qwen3-32b",
    ]
    return [m for m in preferred if m in all_models] + [m for m in all_models if m not in preferred]

available_models = get_available_models()
selected_model = available_models[0]

# 4. Initialize Conversation History
SYSTEM_PROMPT = (
    "You are StartupMateAI, an insightful, friendly, and practical AI co-founder and assistant. "
    "Help users brainstorm, validate ideas, draft emails, plan their week, and write clean code."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

user_prompt = None

# 5. Empty State ("Where shall we begin?" + Inline Card + 4 Pills)
if len(st.session_state.messages) == 1:
    with st.container():
        st.markdown('<div class="hero-heading">Where shall we begin?</div>', unsafe_allow_html=True)

        # Placing st.chat_input inside a container renders it inline in the center
        inline_input = st.chat_input("Ask anything")
        if inline_input:
            user_prompt = inline_input

        st.write("")  # Small spacing before pills
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("Explain something simply", use_container_width=True):
            user_prompt = "Explain how startup idea validation works in simple terms."
        if c2.button("Draft an email", use_container_width=True):
            user_prompt = "Help me draft a concise cold email to a potential startup co-founder or mentor."
        if c3.button("Plan my week", use_container_width=True):
            user_prompt = "Help me create a balanced weekly schedule for classes and building my startup project."
        if c4.button("Fix some code", use_container_width=True):
            user_prompt = "I have a bug in my code. Tell me what to paste so you can debug it."

# 6. Active Conversation State
else:
    top_col1, top_col2 = st.columns([5, 1])
    with top_col2:
        if st.button("↺ New", use_container_width=True):
            st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.rerun()

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            avatar = "🧑‍💻" if msg["role"] == "user" else "🟣"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    docked_input = st.chat_input("Ask anything")
    if docked_input:
        user_prompt = docked_input

# 7. Process New Prompt & Stream Response
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if len(st.session_state.messages) == 2:
        # Transition smoothly from the hero landing screen into the chat view
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_prompt)

    with st.chat_message("assistant", avatar="🟣"):
        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=st.session_state.messages,
                stream=True,
            )
            reply = st.write_stream(
                chunk.choices[0].delta.content or "" for chunk in stream
            )
            st.session_state.messages.append({"role": "assistant", "content": reply})
            if len(st.session_state.messages) == 3:
                st.rerun()
        except Exception as e:
            st.error(f"API Error: {e}")
