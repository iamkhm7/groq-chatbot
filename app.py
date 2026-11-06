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
        padding: 6px 16px;
        font-size: 0.95rem;
        font-weight: 600;
        color: {text_color};
        background: {input_bg};
        box-shadow: 2px 3px 0px {brand_border};
        transition: all 0.3s ease;
    }}

    /* Button Styling */
    div.stButton > button {{
        background: {pill_bg} !important;
        backdrop-filter: blur(10px) !important;
        color: {text_color} !important;
        border: 1px solid {card_border} !important;
        border-radius: 999px !important;
        padding: 0.4rem 1rem !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06) !important;
        transition: all 0.22s ease !important;
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

# 4. Logo on Top-Left
st.markdown("""
<div class="fixed-top-nav">
    <div class="pointer-events-auto">
        <div class="logo-badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
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
div[data-testid="stDialog"] div[role="dialog"] {{
    background: {bg_color} !important;
    border-radius: 24px !important;
}}
div[data-testid="stDialog"] div[role="dialog"] h2 {{
    font-family: 'Patrick Hand SC', cursive !important;
    font-size: 1.5rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: {text_color} !important;
    text-align: center;
    width: fit-content;
    margin: 0 auto !important;
    padding: 0.35rem 1.6rem !important;
    border: 4px solid transparent;
    border-radius: 999px;
    background:
        linear-gradient({bg_color}, {bg_color}) padding-box,
        linear-gradient(90deg, #e0678f, #f9a8c0) border-box;
}}
.dev-card {{
    font-family: 'Patrick Hand SC', cursive;
    color: {text_color};
    padding: 0.5rem 0.4rem 0.2rem 0.4rem;
}}
.dev-name {{
    font-size: 1.6rem;
    letter-spacing: 0.05em;
    line-height: 1.5;
}}
.dev-info {{
    font-size: 1.25rem;
    letter-spacing: 0.06em;
    line-height: 1.55;
    margin-top: 0.6rem;
}}
.dev-more {{
    text-align: center;
    margin: 1.6rem 0 1.2rem 0;
}}
.dev-more summary {{
    display: inline-block;
    list-style: none;
    cursor: pointer;
    background: #cbd5e1;
    color: #131b2e;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem;
    padding: 0.55rem 1.4rem;
    border-radius: 999px;
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
    gap: 14px;
    margin-top: 0.4rem;
}}
.dev-social a {{
    display: flex;
    align-items: center;
    gap: 6px;
    color: {text_color} !important;
    text-decoration: none !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
}}
.dev-social a:hover {{ opacity: 0.7; }}
</style>
<div class="dev-card">
<div class="dev-name">Kamrul Hasan Maruf</div>
<div class="dev-name">(Maruf MD Kamrul Hasan)</div>
<div class="dev-info">2617308<br>Department of Artificial Intelligence<br>Kyungdong University Global<br>South Korea</div>
<details class="dev-more"><summary>More</summary><div class="dev-extra">Built with Streamlit and Groq (Llama 3.1).</div></details>
<div class="dev-social">
<a href="https://github.com/iamkhm7" target="_blank"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>GitHub</a>
<a href="https://instagram.com/_iamkhm_" target="_blank"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.3" cy="6.7" r="1" fill="currentColor" stroke="none"/></svg>Instagram</a>
<a href="https://facebook.com/iamkhm" target="_blank"><svg width="26" height="26" viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="currentColor"/><path d="M13.5 22v-8h2.7l.4-3.1h-3.1V8.9c0-.9.3-1.5 1.6-1.5h1.7V4.6c-.3 0-1.3-.1-2.4-.1-2.4 0-4 1.4-4 4.1v2.3H7.7V14h2.7v8z" fill="{bg_color}"/></svg>facebook</a>
</div>
</div>
""", unsafe_allow_html=True)


# 6. Top-Right Buttons (Dark Mode Toggle & Developer Info)
_, btn_col1, btn_col2 = st.columns([3.8, 1.1, 1.1])

with btn_col1:
    toggle_label = "☀️ Light" if st.session_state.dark_mode else "🌙 Dark"
    if st.button(toggle_label, use_container_width=True, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

with btn_col2:
    if st.button("👨‍💻 Developer", use_container_width=True, key="dev_btn"):
        show_developer()

# 7. Groq Connection & System Prompt
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
MODEL = "llama-3.1-8b-instant"

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

# 8. Landing View (no conversation yet)
if len(st.session_state.messages) == 1:
    st.markdown('<div class="hero-heading">Let\'s create a startup.</div>', unsafe_allow_html=True)

    inline_input = st.chat_input("Pitch your startup idea or ask a question...")
    if inline_input:
        user_prompt = inline_input

    st.write("")
    row1 = st.columns(2)
    row2 = st.columns(2)

    if row1[0].button("💡 Brainstorm Idea", use_container_width=True, key="qa_brainstorm"):
        user_prompt = "Help me brainstorm a high-potential SaaS startup idea for university students."
    if row1[1].button("🔍 Validate with SWOT", use_container_width=True, key="qa_swot"):
        user_prompt = "Conduct a rigorous SWOT analysis for an AI-powered personal productivity app."
    if row2[0].button("🗺️ 30-Day Roadmap", use_container_width=True, key="qa_roadmap"):
        user_prompt = "Create a lean 30-day MVP launch roadmap for a new startup concept."
    if row2[1].button("📊 Pitch Deck Outline", use_container_width=True, key="qa_pitch"):
        user_prompt = "Give me a 10-slide seed pitch deck structure for investors."

# 9. Active Chat View
else:
    top_c1, top_c2 = st.columns([5, 1])
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

    # Show the new question right away (history above was rendered before it existed)
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
            st.session_state.messages.pop()  # drop the unanswered prompt
            st.error(f"API Error: {e}")

    if reply:
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()  # redraw cleanly in the active chat layout
