import streamlit as st
from groq import Groq

# ---------------------------------------------------------
# StartupMate AI — Streamlit redesign
# Keeps the existing Groq-powered chat and quick actions.
# ---------------------------------------------------------

st.set_page_config(
    page_title="StartupMate AI — Your AI Co-Founder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------- State -------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

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

# ------------------------- Theme -------------------------
if st.session_state.dark_mode:
    theme = {
        "bg": "#11111f",
        "surface": "rgba(31, 30, 49, .92)",
        "surface_soft": "rgba(39, 37, 60, .82)",
        "text": "#f7f5ff",
        "muted": "#aaa7c1",
        "border": "rgba(177, 164, 226, .18)",
        "input": "#211f35",
        "footer": "rgba(17, 17, 31, .92)",
        "grid": "rgba(255,255,255,.035)",
        "shadow": "rgba(0,0,0,.24)",
    }
else:
    theme = {
        "bg": "#faf9ff",
        "surface": "rgba(255,255,255,.88)",
        "surface_soft": "rgba(255,255,255,.72)",
        "text": "#19172b",
        "muted": "#77758d",
        "border": "rgba(111, 91, 166, .14)",
        "input": "#ffffff",
        "footer": "rgba(250,249,255,.9)",
        "grid": "rgba(34,24,70,.045)",
        "shadow": "rgba(76,55,132,.09)",
    }

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;1,500;1,600&display=swap');

    :root {{
        color-scheme: {"dark" if st.session_state.dark_mode else "light"};
        --bg: {theme["bg"]};
        --surface: {theme["surface"]};
        --surface-soft: {theme["surface_soft"]};
        --text: {theme["text"]};
        --muted: {theme["muted"]};
        --border: {theme["border"]};
        --input: {theme["input"]};
        --shadow: {theme["shadow"]};
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif !important;
    }}
    [data-testid="stAppViewContainer"] {{
        background-image:
          radial-gradient(ellipse at 17% 22%, rgba(173,145,255,.19), transparent 32%),
          radial-gradient(ellipse at 83% 30%, rgba(255,167,190,.17), transparent 31%),
          radial-gradient(var(--grid) 1px, transparent 1px) !important;
        background-size: auto, auto, 25px 25px !important;
    }}
    [data-testid="stHeader"], #MainMenu, footer {{visibility:hidden;}}
    [data-testid="stToolbar"] {{display:none;}}
    .block-container {{
        max-width: 1120px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 5rem !important;
    }}
    p, li, label, .stMarkdown {{ color: var(--text); }}
    .brand {{
        display:flex; align-items:center; gap:10px;
        color:var(--text); font-weight:800; letter-spacing:-.5px;
        font-size:17px; padding:8px 0;
    }}
    .brand-icon {{
        display:inline-flex; align-items:center; justify-content:center;
        width:36px; height:36px; border-radius:13px; color:white;
        background:linear-gradient(140deg,#7955ef,#bd55d7);
        box-shadow:0 7px 18px rgba(137,91,230,.28); font-size:18px;
    }}
    .topline {{
        border-bottom:1px solid var(--border);
        padding-bottom:13px; margin-bottom:20px;
    }}
    .hero {{
        text-align:center; padding:50px 10px 25px;
    }}
    .eyebrow {{
        display:inline-flex; align-items:center; gap:8px;
        padding:8px 14px; border-radius:999px;
        color:#8069dc; background:rgba(133,104,232,.10);
        border:1px solid rgba(133,104,232,.22);
        font-size:11px; font-weight:800; letter-spacing:.6px;
    }}
    .live-dot {{
        width:7px; height:7px; display:inline-block;
        border-radius:50%; background:#32c99a;
        box-shadow:0 0 0 4px rgba(50,201,154,.13);
    }}
    .hero h1 {{
        font-family:'Playfair Display', Georgia, serif;
        color:var(--text); font-size:clamp(43px,6.5vw,72px);
        line-height:1.08; letter-spacing:-1.9px;
        font-weight:500; margin:22px 0 12px;
    }}
    .hero h1 em {{
        font-weight:500; background:linear-gradient(100deg,#ff8b55,#a16be8);
        -webkit-background-clip:text; background-clip:text;
        -webkit-text-fill-color:transparent;
    }}
    .hero-sub {{
        color:var(--muted); font-size:15px; line-height:1.75;
        max-width:690px; margin:0 auto;
    }}
    .hero-joke {{
        color:var(--muted); font-size:11px; margin-top:11px;
    }}
    .section-label {{
        color:#9075e5; font-size:10px; font-weight:800;
        letter-spacing:1.6px; text-transform:uppercase;
        margin:23px 0 8px;
    }}
    .section-title {{
        color:var(--text); font-family:'Playfair Display',serif;
        font-size:29px; font-weight:500; margin:0 0 5px;
    }}
    .section-copy {{color:var(--muted);font-size:12px;line-height:1.6;}}
    .tool-card {{
        background:var(--surface); border:1px solid var(--border);
        border-radius:19px; padding:17px 16px 13px;
        min-height:135px; box-shadow:0 9px 28px var(--shadow);
        margin-bottom:8px; backdrop-filter:blur(12px);
    }}
    .tool-icon {{
        width:37px;height:37px;border-radius:12px;
        display:flex;align-items:center;justify-content:center;
        background:rgba(133,104,232,.12);font-size:18px;margin-bottom:12px;
    }}
    .tool-title {{font-size:13px;font-weight:800;color:var(--text);margin-bottom:5px;}}
    .tool-copy {{font-size:11px;line-height:1.55;color:var(--muted);}}
    div.stButton > button {{
        border:1px solid var(--border) !important;
        border-radius:999px !important;
        background:var(--surface) !important;
        color:var(--text) !important;
        font-family:'DM Sans',sans-serif !important;
        font-weight:700 !important; font-size:12px !important;
        min-height:39px !important;
        box-shadow:0 5px 15px var(--shadow) !important;
        transition:all .2s ease !important;
    }}
    div.stButton > button:hover {{
        border-color:#a58af2 !important;
        transform:translateY(-2px);
        box-shadow:0 9px 22px rgba(129,91,225,.16) !important;
    }}
    div.stButton > button[kind="primary"] {{
        background:linear-gradient(110deg,#8058ef,#bd4dd5) !important;
        color:white !important; border:0 !important;
    }}
    /* Floating chat composer: one minimal pill, no white footer slab */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"],
    .stChatFloatingInputContainer {{
        background:transparent !important;
        background-color:transparent !important;
        border:0 !important;
        box-shadow:none !important;
    }}
    [data-testid="stBottom"] {{
        padding:14px 18px 20px !important;
    }}
    [data-testid="stBottomBlockContainer"] {{
        max-width:980px !important;
        padding:0 !important;
    }}
    [data-testid="stChatInput"] {{
        background:var(--input) !important;
        background-color:var(--input) !important;
        border:1px solid rgba(137,111,220,.25) !important;
        border-radius:999px !important;
        box-shadow:0 12px 34px var(--shadow), 0 2px 8px rgba(90,65,160,.05) !important;
        padding:5px 9px 5px 20px !important;
        min-height:62px !important;
        transition:border-color .2s ease, box-shadow .2s ease !important;
    }}
    [data-testid="stChatInput"]:focus-within {{
        border-color:rgba(145,111,239,.72) !important;
        box-shadow:0 14px 38px var(--shadow), 0 0 0 3px rgba(145,111,239,.10) !important;
    }}
    [data-testid="stChatInput"] textarea {{
        color:var(--text) !important;
        caret-color:#9b72ef !important;
        font-family:'DM Sans',sans-serif !important;
        font-size:14px !important;
        line-height:1.5 !important;
        padding-top:12px !important;
        padding-bottom:10px !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color:var(--muted) !important; opacity:.9 !important;
    }}
    [data-testid="stChatInputSubmitButton"] {{
        background:linear-gradient(135deg,#8058ef,#c34fd5)!important;
        color:white!important;border:0!important;border-radius:50%!important;
        width:42px!important;height:42px!important;min-width:42px!important;
        box-shadow:0 5px 14px rgba(151,83,222,.28)!important;
        transition:transform .2s ease, box-shadow .2s ease!important;
    }}
    [data-testid="stChatInputSubmitButton"]:hover {{
        transform:translateY(-1px) scale(1.04);
        box-shadow:0 7px 18px rgba(151,83,222,.38)!important;
    }}

    /* Streamlit's native dialog must follow the selected theme */
    [data-testid="stDialog"] > div,
    [data-testid="stModal"] > div,
    div[role="dialog"] {{
        background:var(--surface) !important;
        color:var(--text) !important;
        border:1px solid var(--border) !important;
        border-radius:22px !important;
        box-shadow:0 24px 80px rgba(0,0,0,.24) !important;
    }}
    [data-testid="stDialog"] *,
    [data-testid="stModal"] *,
    div[role="dialog"] * {{
        color:var(--text);
    }}
    [data-testid="stDialog"] a,
    [data-testid="stModal"] a,
    div[role="dialog"] a {{
        color:#a58af2 !important;
        font-weight:700 !important;
    }}
    [data-testid="stDialog"] button,
    [data-testid="stModal"] button,
    div[role="dialog"] button {{
        color:var(--text) !important;
    }}
    [data-testid="stChatMessage"] {{
        background:var(--surface)!important;
        border:1px solid var(--border)!important;
        border-radius:18px!important;
        box-shadow:0 8px 25px var(--shadow)!important;
        padding:14px 18px!important;
    }}
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li {{color:var(--text)!important;}}
    .workspace-note {{
        border:1px solid var(--border); border-radius:18px;
        padding:16px 18px; background:var(--surface-soft);
        color:var(--muted); font-size:12px; line-height:1.7;
        margin:12px 0 18px;
    }}
    .disclaimer {{
        text-align:center; color:var(--muted); font-size:10px;
        border-top:1px solid var(--border); padding-top:15px; margin-top:28px;
    }}
    @media(max-width:700px) {{
        .block-container {{padding: .6rem 1rem 4rem !important;}}
        .hero {{padding:36px 0 18px;}}
        .hero h1 {{letter-spacing:-1px;}}
        .hero-sub {{font-size:13px;}}
        .tool-card {{min-height:145px;padding:14px 12px;}}
        .section-title {{font-size:25px;}}
    }}
    @media(prefers-reduced-motion:reduce) {{
        *,*::before,*::after {{animation:none!important;transition:none!important;}}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------- Header -------------------------
header_left, header_right = st.columns([5, 2], vertical_alignment="center")
with header_left:
    st.markdown(
        '<div class="brand"><span class="brand-icon">✦</span>'
        'StartupMate<span style="color:#956de8">AI</span></div>',
        unsafe_allow_html=True,
    )
with header_right:
    h1, h2 = st.columns(2)
    with h1:
        theme_label = "☀️ Light" if st.session_state.dark_mode else "🌙 Dark"
        if st.button(theme_label, use_container_width=True, key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    @st.dialog("A little about the builder")
    def show_developer():
        st.markdown(
            """
            <div style="text-align:center;line-height:1.9">
              <div style="font-size:25px;font-weight:800;color:var(--text)">Kamrul Hasan Maruf</div>
              <div style="color:#a58af2;font-weight:700">AI Student · StartupMate AI</div>
              <p>Department of Artificial Intelligence<br>
              Kyungdong University Global · South Korea</p>
              <p><b>Built with:</b> Streamlit + Groq AI</p>
              <p style="font-size:12px;color:var(--muted)">Making startup planning less intimidating—and slightly less boring.</p>
              <a style="color:#a58af2" href="https://github.com/iamkhm7" target="_blank">GitHub profile ↗</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with h2:
        if st.button("👨‍💻 Developer", use_container_width=True, key="developer_btn"):
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
        "button": "Brainstorm an idea",
        "prompt": "Help me brainstorm a high-potential startup idea. Ask concise clarifying questions if needed, then outline the problem, target users, solution, differentiator, and MVP.",
    },
    {
        "key": "swot",
        "icon": "🔎",
        "title": "SWOT Validator",
        "copy": "Find the strengths, weaknesses, opportunities and threats.",
        "button": "Run a SWOT analysis",
        "prompt": "Help me validate my startup idea with a rigorous SWOT analysis. If I have not provided an idea, ask me for it first. Separate known facts from assumptions.",
    },
    {
        "key": "roadmap",
        "icon": "🗺️",
        "title": "30-Day Roadmap",
        "copy": "Break the launch into small, achievable milestones.",
        "button": "Build a 30-day roadmap",
        "prompt": "Create a practical 30-day startup MVP roadmap with weekly milestones, daily or grouped tasks, deliverables, and validation checkpoints. Ask for the startup idea if it is missing.",
    },
    {
        "key": "pitch",
        "icon": "📊",
        "title": "Pitch Deck Builder",
        "copy": "Shape your idea into a clear investor presentation.",
        "button": "Create a pitch outline",
        "prompt": "Create a clear 10-slide startup pitch deck outline covering problem, solution, product, market, business model, traction or validation, competition, go-to-market, team, and ask. Ask for the startup idea if missing.",
    },
]

def queue_prompt(prompt: str):
    st.session_state.pending_prompt = prompt

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

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    user_input = st.chat_input("Pitch your idea or ask your co-founder anything…")
    if user_input:
        queue_prompt(user_input)

else:
    chat_header_left, chat_header_right = st.columns([5, 1])
    with chat_header_left:
        st.markdown('<div class="section-label">YOUR STARTUP WORKSPACE</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">The idea is in motion.</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-copy">Keep refining, questioning and building. Progress looks good on you.</div>', unsafe_allow_html=True)
    with chat_header_right:
        if st.button("↺ New chat", use_container_width=True, key="new_chat"):
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
                else:
                    st.warning("The model returned an empty response. Please try again.")
                    st.session_state.messages.pop()
            except Exception as exc:
                st.session_state.messages.pop()
                st.error(f"AI request failed: {exc}")
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
