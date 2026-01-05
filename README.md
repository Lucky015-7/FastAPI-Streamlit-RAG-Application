[![Python CI](https://github.com/Lucky015-7/FastAPI-Streamlit-RAG-Application/actions/workflows/ci.yml/badge.svg)](https://github.com/Lucky015-7/FastAPI-Streamlit-RAG-Application/actions/workflows/ci.yml)
🚀 Multi-User RAG Chatbot

Production-Grade Document Intelligence with FastAPI, Streamlit & Groq

A high-performance, cloud-proven Retrieval-Augmented Generation (RAG) system enabling real-time, multi-user conversations with PDF and DOCX documents.
Built using a modular, containerized architecture and powered by Groq + LLaMA-3.3-70B for ultra-low-latency inference.

✨ Core Features

⚡ Ultra-Fast Inference
Leveraging Groq’s LLaMA-3.3-70B for near-instant, context-aware responses.

📂 Multi-Format Document Intelligence
Upload, embed, and chat with PDF & DOCX files seamlessly.

🧠 Persistent Conversational Memory
SQLite-backed chat history enables coherent multi-turn dialogue across sessions.

🔒 Privacy-First Vector Search
Local HuggingFace embeddings (all-MiniLM-L6-v2) with a self-hosted ChromaDB vector store.

🐳 Fully Containerized
Orchestrated with Docker Compose for reproducible, environment-safe deployments.

☁️ Cloud-Proven on AWS
Successfully deployed and tested on AWS EC2 with production networking.

🛠️ Developer-Friendly API
Interactive Swagger UI for instant backend testing and exploration.

🏗️ Architecture Overview

The application is split into two independent services for scalability and clean separation of concerns:

/api  → FastAPI Backend
       • Document ingestion & chunking
       • Vector store management
       • RAG chain orchestration

/app  → Streamlit Frontend
       • Document upload & management
       • Real-time conversational UI

🐳 Run with Docker (Recommended)

Docker Compose is the recommended way to run the application, handling networking and dependencies automatically.

1️⃣ Prerequisites

Docker & Docker Compose

Groq API Key → https://console.groq.com

2️⃣ Configuration

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

# Optional: LangSmith Tracing
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=Multi-User-RAG-App

3️⃣ Launch Services
docker compose up -d --build


🔹 FastAPI Backend: http://localhost:8000

🔹 Swagger Docs: http://localhost:8000/docs

🔹 Streamlit UI: http://localhost:8501

☁️ AWS EC2 Deployment
Security Group (Inbound Rules)

Allow the following ports (0.0.0.0/0):

Port	Purpose
8000	FastAPI Backend
8501	Streamlit Frontend
22	SSH Access
Deployment Commands
git clone https://github.com/Lucky015-7/FastAPI-Streamlit-RAG-Application.git
cd FastAPI-Streamlit-RAG-Application
docker compose up -d --build


Your RAG chatbot is now live on AWS 🚀

🛠️ Manual Installation (Local Testing)

⚠️ Run commands from the project root to support absolute imports (e.g. from api.utils...)

Install Dependencies
pip install -r requirements.txt

Terminal 1 — Backend
uvicorn api.main:app --reload

Terminal 2 — Frontend
streamlit run app/streamlit_app.py

📁 Project Structure
├── api/                     # FastAPI Backend Package
│   ├── main.py              # Entry point (api.main:app)
│   ├── langchain_utils.py   # RAG chains & logic
│   ├── chroma_utils.py      # Vector store utilities
│   └── Dockerfile
│
├── app/                     # Streamlit Frontend
│   ├── streamlit_app.py     # UI & API integration
│   └── Dockerfile
│
├── docker-compose.yml       # Multi-service orchestration
├── requirements.txt         # Dependencies (NumPy < 2.0 pinned)
└── rag_app.db               # SQLite chat history

🧠 Tech Stack

LLMs & AI: Groq (LLaMA-3.3), LangChain, HuggingFace, ChromaDB
Backend: Python, FastAPI, Uvicorn, SQLite
Frontend: Streamlit
DevOps & Cloud: Docker, Docker Compose, AWS EC2, Ubuntu Linux

📄 License

Licensed under the MIT License.


