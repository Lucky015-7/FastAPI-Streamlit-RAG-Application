🚀 Multi-User RAG Chatbot
A high-performance, production-ready Retrieval-Augmented Generation (RAG) application. This project features a modular architecture with a FastAPI backend and a Streamlit frontend, designed for lightning-fast document intelligence using Groq and Llama-3.3.

✨ Features
⚡ Ultra-Fast Inference: Powered by Groq’s Llama-3.3-70b model for near-instant responses.

📂 Multi-Format Support: Upload and chat with PDF and DOCX documents.

🧠 Conversational Memory: Maintains chat history across sessions using SQLite for coherent, multi-turn dialogue.

🔒 Privacy-First: Uses local HuggingFace embeddings (all-MiniLM-L6-v2) and a local ChromaDB vector store.

🛠️ Interactive API Docs: Built-in Swagger UI for testing backend endpoints directly.

🏗️ Project Architecture
The project is split into two main components to ensure scalability and clean separation of concerns:

/api: The FastAPI backend. Handles document processing, vector storage management, and RAG chain logic.

/app: The Streamlit frontend. Provides a user-friendly interface for document management and real-time chatting.

🚀 Getting Started
1. Prerequisites
Python 3.10+

Groq API Key (Get one at console.groq.com)

2. Installation
Clone the repository and install the dependencies:

Bash

git clone https://github.com/Lucky015-7/FastAPI-Streamlit-RAG-Application.git
cd FastAPI-Streamlit-RAG-Application
pip install -r requirements.txt
3. Configuration
Create a .env file in the root directory and add your keys:

Code snippet

GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Multi-User-RAG-App
🏃 Running the Application
You will need to open two terminals in VS Code:

Terminal 1: Backend (FastAPI)
Bash

cd api
uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000. You can view the docs at /docs.

Terminal 2: Frontend (Streamlit)
Bash

cd app
streamlit run streamlit_app.py
The dashboard will open at http://localhost:8501.

📁 Folder Structure
Plaintext

├── api/                # FastAPI Backend
│   ├── main.py         # API Endpoints
│   ├── langchain_utils.py # RAG Logic & Chains
│   └── chroma_utils.py  # Vector Store Management
├── app/                # Streamlit Frontend
│   └── streamlit_app.py # UI & API Integration
├── chroma_db/          # Local Vector Database (Git ignored)
├── rag_app.db          # Chat History SQLite DB (Git ignored)
├── .env                # Environment Variables (Git ignored)
└── requirements.txt    # Project Dependencies
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.


