import requests
import streamlit as st

# Using a variable makes it easy to change if you deploy to a real server later
BASE_URL = "http://localhost:8000"


def get_api_response(question, session_id, model):
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json'}
    payload = {"question": question, "model": model}
    if session_id:
        payload["session_id"] = session_id

    try:
        response = requests.post(
            f"{BASE_URL}/chat", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Chat Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None


def upload_document(file):
    try:
        files = {"file": (file.name, file, file.type)}
        response = requests.post(f"{BASE_URL}/upload-doc", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Upload Error: {str(e)}")
        return None


def list_documents():
    try:
        response = requests.get(f"{BASE_URL}/list-docs")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Could not fetch document list.")
            return []
    except Exception as e:
        st.error(f"List Error: {str(e)}")
        return []


def delete_document(file_id):
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json'}
    try:
        response = requests.post(
            f"{BASE_URL}/delete-doc", headers=headers, json={"file_id": file_id})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Delete failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"Delete Error: {str(e)}")
        return None
