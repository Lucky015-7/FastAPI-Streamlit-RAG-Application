import streamlit as st
from api_utils import get_api_response


def display_chat_interface():
    # 1. Display existing messages from the session history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 2. Accept new user input
    if prompt := st.chat_input("Ask about your data..."):
        # Add user message to state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 3. Generate response from the FastAPI backend
        with st.spinner("Generating response (Groq/Llama-3.3)..."):
            response = get_api_response(
                prompt, st.session_state.session_id, st.session_state.model)

            if response:
                # Update session state with the backend response
                st.session_state.session_id = response.get('session_id')
                st.session_state.messages.append(
                    {"role": "assistant", "content": response['answer']})

                # Display the assistant's message
                with st.chat_message("assistant"):
                    st.markdown(response['answer'])

                    # 4. ADDED: Traceability Expander (from reference project)
                    with st.expander("Details & Metadata"):
                        st.subheader("Final Answer")
                        st.code(response['answer'])

                        st.subheader("Model Configuration")
                        st.info(f"Using: {response['model']}")

                        st.subheader("Session Tracking")
                        st.info(f"ID: {response['session_id']}")
            else:
                # Error handling if the API is unreachable
                st.error(
                    "Failed to get a response from the API. Please ensure your FastAPI server is running.")
