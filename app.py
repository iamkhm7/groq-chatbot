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
    div[data-testid="stHorizontalBlock"]:has(.brand) > div:last-child,
    div[data-testid="stHorizontalBlock"]:has(.ws-head) > div:last-child {
        flex: 0 0 auto !important; min-width: 0 !important; width: auto !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.brand) > div:last-child div.stButton,
    div[data-testid="stHorizontalBlock"]:has(.ws-head) > div:last-child div.stButton {
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
header_left, header_right = st.columns([4, 1.6], vertical_alignment="center")
with header_left:
    st.markdown(
        '<div class="brand"><span class="brand-icon">✦</span>'
        'StartupMate<span style="color:#956de8">AI</span></div>',
        unsafe_allow_html=True,
    )
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
