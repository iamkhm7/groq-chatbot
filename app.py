import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="StartupMateAI - Your AI Co-Founder",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS & UI Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

    #MainMenu, header, footer {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}

    .stApp {
        background-color: #f6f7fb !important;
        color: #131b2e !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
        overflow-x: hidden;
    }

    /* Ambient Aurora Glow */
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

    .block-container {
        position: relative;
        z-index: 2;
        padding-top: 6.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 760px !important;
    }

    /* Top Navigation Bar */
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
    .logo-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        border: 1.5px solid #131b2e;
        border-radius: 999px;
        padding: 5px 16px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #131b2e;
        background: #f6f7fb;
        box-shadow: 2px 3px 0px #131b2e;
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

    /* Heading */
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

    /* Chat Input Card */
    [data-testid="stChatInput"] {
        background: #ffffff !important;
        border-radius: 22px !important;
        border: 1px solid rgba(226, 232, 240, 0.9) !important;
        box-shadow: 0 14px 36px rgba(19, 27, 46, 0.07) !important;
        padding: 10px 14px 42px 14px !important;
        position: relative !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #131b2e !important;
        font-size: 1rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    [data-testid="stChatInput"]::after {
        content: "💡";
        position: absolute;
        bottom: 12px;
        left: 18px;
        font-size: 0.95rem;
        pointer-events: none;
    }
    [data-testid="stChatInputSubmitButton"] {
        background-color: #131b2e !important;
        color: #ffffff !important;
        border-radius: 50% !important;
        width: 34px !important;
        height: 34px !important;
        position: absolute !important;
        bottom: 10px !important;
        right: 14px !important;
    }

    /* Suggestion Pills */
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
        transition: all 0.22s ease !important;
        white-space: nowrap !important;
    }
    div.stButton > button:hover {
        background: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.12) !important;
        border-color: #c7d2fe !important;
    }

    /* Chat Messages */
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
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {
        color: #131b2e !important;
    }

    /* Disclaimer & AI Notice */
    .disclaimer-footer {
        position: fixed;
        bottom: 10px;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 0.73rem;
        color: #64748b;
        z-index: 10;
        pointer-events: none;
        background: rgba(246, 247, 251, 0.85);
        padding: 4px;
    }
</style>

<div class="aurora-bg"></div>
<div class="top-nav">
    <div class="brand-wrap">
        <div class="logo-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            StartupMateAI
        </div>
    </div>
    <div class="nav-right">
        <span>History</span>
        <div class="profile-circle">👤</div>
    </div>
</div>
<div class="disclaimer-footer">
    ⚡ AI Notice: Content is AI-generated and can contain mistakes. Not professional business/legal advice. Human verification required.
</div>
""", unsafe_allow_html=True)

# 3. Groq Connection & System Prompt (Topic 84: Startup Co-Founder)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = (
    "You are StartupMateAI, an expert startup co-founder, business strategist, and venture mentor. "
    "Your objective is to help founders brainstorm ideas, test market viability, construct SWOT analyses, "
    "and build structured execution roadmaps. "
    "SAFETY & DISCLAIMER RULES:\n"
    "1. Always remind users that financial, legal, and tax projections are simulated and require professional verification.\n"
    "2. If a user mentions self-harm, danger, illegal activity, or severe distress, immediately stop business advice, express care, and instruct them to contact emergency services or trusted authorities.\n"
    "3. Be objective, constructive, and realistic in startup critique."
)

@st.cache_data(ttl=3600)
def get_model():
    return "llama-3.1-8b-instant"

selected_model = get_model()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

user_prompt = None

# 4. Landing View
if len(st.session_state.messages) == 1:
    with st.container():
        st.markdown('<div class="hero-heading">Where shall we build?</div>', unsafe_allow_html=True)

        inline_input = st.chat_input("Pitch your startup idea or ask a question...")
        if inline_input:
            user_prompt = inline_input

        st.write("")
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("💡 Brainstorm Idea", use_container_width=True):
            user_prompt = "Help me brainstorm a high-potential SaaS startup idea for university students."
        if c2.button("🔍 Validate with SWOT", use_container_width=True):
            user_prompt = "Conduct a rigorous SWOT analysis for an AI-powered personal productivity app."
        if c3.button("🗺️ 30-Day Roadmap", use_container_width=True):
            user_prompt = "Create a lean 30-day MVP launch roadmap for a new startup concept."
        if c4.button("📊 Pitch Deck Outline", use_container_width=True):
            user_prompt = "Give me a 10-slide seed pitch deck structure for investors."

# 5. Active Chat View
else:
    top_col1, top_col2 = st.columns([5, 1])
    with top_col2:
        if st.button("↺ New Pitch", use_container_width=True):
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

# 6. Response Generation
if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    if len(st.session_state.messages) == 2:
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_prompt)

    with st.chat_message("assistant", avatar="🚀"):
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
