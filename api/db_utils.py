import sqlite3
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage

DB_NAME = "rag_app.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    """Initializes both the log and document store tables in a single call."""
    conn = get_db_connection()
    # Table for chat history and session tracking
    conn.execute('''CREATE TABLE IF NOT EXISTS application_logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     session_id TEXT, user_query TEXT, gpt_response TEXT,
                     model TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Table for tracking uploaded documents
    conn.execute('''CREATE TABLE IF NOT EXISTS document_store
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     filename TEXT, upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()


def insert_application_logs(session_id, user_query, gpt_response, model):
    conn = get_db_connection()
    conn.execute('INSERT INTO application_logs (session_id, user_query, gpt_response, model) VALUES (?, ?, ?, ?)',
                 (session_id, user_query, gpt_response, model))
    conn.commit()
    conn.close()


def get_chat_history(session_id):
    """Returns chat history as a list of LangChain message objects for the RAG chain."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT user_query, gpt_response FROM application_logs WHERE session_id = ? ORDER BY created_at', (session_id,))
    history = []
    for row in cursor.fetchall():
        # Using objects (HumanMessage/AIMessage) is best for LangChain's latest LCEL logic
        history.append(HumanMessage(content=row['user_query']))
        history.append(AIMessage(content=row['gpt_response']))
    conn.close()
    return history


def insert_document_record(filename):
    """Registers a new document and returns its unique database ID."""
    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO document_store (filename) VALUES (?)', (filename,))
    file_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return file_id


def get_all_documents():
    """Fetches all indexed documents, sorted by most recent upload."""
    conn = get_db_connection()
    # Sorting ensures the newest files appear at the top of your Streamlit sidebar
    docs = conn.execute(
        'SELECT id, filename, upload_timestamp FROM document_store ORDER BY upload_timestamp DESC').fetchall()
    conn.close()
    return [dict(doc) for doc in docs]


def delete_document_record(file_id):
    """Removes a document record from the SQL database. 
    Note: Ensure you also delete from Chroma in your main logic."""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM document_store WHERE id = ?', (file_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting record: {e}")
        return False


# CRITICAL: Always initialize tables when the script is imported
create_tables()
