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

    /* Top Navigation Bar */
    .top-nav {{
        position: fixed;
        top: 22px;
        left: 32px;
        right: 32px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 100;
        animation: fadeUp 0.5s ease-out;
    }}
    .brand-wrap {{
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    .logo-badge {{
        display: flex;
        align-items: center;
        gap: 8px;
        border: 1.5px solid {brand_border};
        border-radius: 999px;
        padding: 5px 16px;
        font-size: 0.95rem;
        font-weight: 600;
        color: {text_color};
        background: {input_bg};
        box-shadow: 2px 3px 0px {brand_border};
        transition: all 0.3s ease;
    }}

    /* Style Streamlit button in top right */
    [data-testid="stHorizontalBlock"] {{
        align-items: center;
    }}
    div.stButton > button {{
        background: {pill_bg} !important;
        backdrop-filter: blur(10px) !important;
        color: {text_color} !important;
        border: 1px solid {card_border} !important;
        border-radius: 999px !important;
        padding: 0.42rem 0.95rem !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.22s ease !important;
        white-space: nowrap !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.15) !important;
        border-color: #818cf8 !important;
    }}

    /* Heading */
    .hero-heading {{
        font-family: 'Instrument Serif', Georgia, serif;
        font-size: 3.4rem;
        font-weight: 400;
        color: {text_color};
        text-align: center;
        margin-top: 8vh;
        margin-bottom: 1.8rem;
        letter-spacing: -0.02em;
        animation: fadeUp 0.6s ease-out 0.05s both;
    }}

    /* Chat Input Card */
    [data-testid="stChatInput"] {{
        background: {input_bg} !important;
        border-radius: 22px !important;
        border: 1px solid {card_border} !important;
        box-shadow: 0 14px 36px rgba(0, 0, 0, 0.08) !important;
        padding: 10px 14px 42px 14px !important;
        position: relative !important;
    }}
    [data-testid="stChatInput"] textarea {{
        color: {text_color} !important;
        font-size: 1rem !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}
    [data-testid="stChatInput"]::after {{
        content: "💡";
        position: absolute;
        bottom: 12px;
        left: 18px;
        font-size: 0.95rem;
        pointer-events: none;
    }}
    [data-testid="stChatInputSubmitButton"] {{
        background-color: {text_color} !important;
        color: {bg_color} !important;
        border-radius: 50% !important;
        width: 34px !important;
        height: 34px !important;
        position: absolute !important;
        bottom: 10px !important;
        right: 14px !important;
    }}

    /* Chat Messages */
    [data-testid="stChatMessage"] {{
        background: {card_bg} !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid {card_border} !important;
        border-radius: 18px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04) !important;
        color: {text_color} !important;
        animation: fadeUp 0.35s ease-out both;
    }}
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li, [data-testid="stChatMessage"] span {{
        color: {text_color} !important;
    }}

    /* Disclaimer & AI Notice */
    .disclaimer-footer {{
        position: fixed;
        bottom: 10px;
        left: 0;
        right: 0;
        text-align: center;
        font-size: 0.73rem;
        color: #94a3b8;
        z-index: 10;
        pointer-events: none;
        background: {footer_bg};
        padding: 4px;
    }}
</style>

<div class="aurora-bg"></div>
<div class="disclaimer-footer">
    ⚡ AI Notice: Content is AI-generated and can contain mistakes. Not professional business/legal advice. Human verification required.
</div>
""", unsafe_allow_html=True)

# 4. Top Header Layout (Logo on left, Toggle Button neatly in the top right)
top_col1, top_col2 = st.columns([4, 1])
with top_col1:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; padding-top: 4px;">
        <div class="logo-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            StartupMateAI
        </div>
    </div>
    """, unsafe_allow_html=True)

with top_col2:
    toggle_label = "☀️ Light" if st.session_state.dark_mode else "🌙 Dark"
    if st.button(toggle_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# 5. Groq Connection & System Prompt (Topic 84: Startup Co-Founder)
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

# 6. Landing View
if len(st.session_state.messages) == 1:
    with st.container():
        st.markdown('<div class="hero-heading">Let\'s create a startup.</div>', unsafe_allow_html=True)

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

# 7. Active Chat View
else:
    top_c1, top_c2 = st.columns([5, 1])
    with top_c2:
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

# 8. Response Generation
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
