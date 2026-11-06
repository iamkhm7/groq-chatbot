import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("AI Chatbot")

# Reads your key securely from Streamlit's dashboard
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, concise AI assistant."}
    ]

# Show previous messages on screen
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages,
    )
    reply = completion.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
