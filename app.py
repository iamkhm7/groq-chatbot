import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="Nova AI",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS (Hides Streamlit branding & styles the UI)
st.markdown("""
<style>
    /* Hide Streamlit top bar, menu, and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main background and font styling */
    .stApp {
        background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%);
        color: #f8fafc;
    }

    /* Custom Hero Header */
    .hero-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Chat message bubbles */
    [data-testid="stChatMessage"] {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown('<div class="hero-title">⚡ Nova AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Fast, intelligent answers powered by Groq</div>', unsafe_allow_html=True)

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

# 4. Sidebar Controls
with st.sidebar:
    st.subheader("⚙️ Chat Settings")
    available_models = get_available_models()
    selected_model = st.selectbox("AI Model", available_models, index=0)
    system_prompt = st.text_area(
        "Bot Personality",
        value="You are a helpful, witty, and concise AI assistant.",
        height=100
    )
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        st.rerun()

# 5. Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# 6. Starter Suggestion Buttons (Shown only when chat is empty)
user_prompt = None
if len(st.session_state.messages) == 1:
    st.write("✨ **Try asking:**")
    col1, col2 = st.columns(2)
    if col1.button("💡 Validate a startup idea", use_container_width=True):
        user_prompt = "Help me validate a new startup idea step by step."
    if col2.button("🐍 Write a Python script", use_container_width=True):
        user_prompt = "Write a clean Python script to automate file organization."

# 7. Render Existing Chat Messages with Custom Avatars
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "🧑‍💻" if msg["role"] == "user" else "⚡"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# 8. Chat Input & Live Streaming Response
chat_box_input = st.chat_input("Type your message here...")
prompt = user_prompt or chat_box_input

if prompt:
    st.session_state.messages[0]["content"] = system_prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        try:
            stream = client.chat.completions.create(
                model=selected_model,
                messages=st.session_state.messages,
                stream=True,
            )
            response_text = st.write_stream(
                chunk.choices[0].delta.content or "" for chunk in stream
            )
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"API Error: {e}")
