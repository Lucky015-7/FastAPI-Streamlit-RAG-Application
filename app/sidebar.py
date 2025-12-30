import streamlit as st
from api_utils import upload_document, list_documents, delete_document


def display_sidebar():
    # 1. Model Selection (Updated for your Groq Model)
    st.sidebar.header("Configuration")
    # We use your Llama model instead of GPT-4
    model_options = ["llama-3.3-70b-versatile"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

    # 2. Upload Document Section (With Spinner and Success Messages)
    st.sidebar.header("Upload Document")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a file", type=["pdf", "docx"])

    if uploaded_file is not None:
        if st.sidebar.button("Upload & Index"):
            with st.spinner("Processing document..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(
                        f"File '{uploaded_file.name}' indexed successfully!")
                    # Refresh the document list automatically after upload
                    st.session_state.documents = list_documents()

    # 3. Document List Section
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing..."):
            st.session_state.documents = list_documents()

    # Initialize document list in session state if not already there
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()

    documents = st.session_state.documents

    if documents:
        # Display each document currently in the system
        for doc in documents:
            # We show the filename and ID so the user knows what is indexed
            st.sidebar.text(f" {doc['filename']} (ID: {doc['id']})")

        # 4. Delete Document Section (Critical for management)
        st.sidebar.subheader("Delete Document")

        # Create a dropdown to select which file to delete by its ID
        selected_file_id = st.sidebar.selectbox(
            "Select file to remove",
            options=[doc['id'] for doc in documents],
            format_func=lambda x: next(doc['filename']
                                       for doc in documents if doc['id'] == x)
        )

        if st.sidebar.button("Delete Selected Document"):
            with st.spinner("Deleting from system..."):
                delete_response = delete_document(selected_file_id)
                # Note: Even if delete_response is an empty dict, we refresh on success
                st.sidebar.success(f"Document {selected_file_id} removed.")
                st.session_state.documents = list_documents()  # Refresh list after deletion
                st.rerun()  # Refresh the whole UI to clear deleted items
    else:
        st.sidebar.info("No documents uploaded yet.")
