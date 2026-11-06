import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("AI Chatbot")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Automatically fetch active chat models from your Groq account
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
selected_model = st.sidebar.selectbox("Select AI Model", available_models, index=0)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, concise AI assistant."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        completion = client.chat.completions.create(
            model=selected_model,
            messages=st.session_state.messages,
        )
        reply = completion.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)
    except Exception as e:
        st.error(f"API Error: {e}")
