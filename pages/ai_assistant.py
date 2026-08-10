import streamlit as st

from utils.ai_helper import ask_ai


def show_ai_assistant():

    st.header("🤖 AI Study Assistant")

    st.write(
        "Ask questions, understand difficult concepts, "
        "and get help with your studies."
    )

    st.divider()

    # -------------------------
    # CHAT HISTORY
    # -------------------------

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # -------------------------
    # DISPLAY PREVIOUS MESSAGES
    # -------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # -------------------------
    # USER INPUT
    # -------------------------

    question = st.chat_input(
        "Ask me anything about your studies..."
    )

    if question:

        # Add user message
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        # Get AI response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = ask_ai(question)

            st.markdown(answer)

        # Save AI response
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

    # -------------------------
    # CLEAR CHAT
    # -------------------------

    if st.button("🗑️ Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()