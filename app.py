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
            'or pick one of the tools below. “I have no idea yet” is also a valid starting point. '
            '<br><b>Heads up:</b> I only talk startups and business, so no trivia, poems or homework!</div>',
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

        user_input = st.chat_input("Ask about startups or business…")
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

        user_input = st.chat_input("Ask about startups or business…")
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
                    api_messages = list(st.session_state.messages)
                    api_messages[-1] = {
                        **api_messages[-1],
                        "content": api_messages[-1]["content"] + SCOPE_REMINDER,
                    }
                    stream = client.chat.completions.create(
                        model=MODEL,
                        messages=api_messages,
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
if st.session_state.page == "home":
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
else:
    st.markdown(
        """
        <div class="notice-fixed">
          <span class="n-full">⚡ AI-generated content can contain mistakes. Not professional financial, legal or tax advice. Verify important decisions.</span>
          <span class="n-short">⚡ AI-generated, may contain mistakes. Verify before use.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
