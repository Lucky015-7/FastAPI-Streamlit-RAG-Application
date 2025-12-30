from chroma_utils import index_document_to_chroma, delete_doc_from_chroma
from db_utils import (
    insert_application_logs,
    get_chat_history,
    get_all_documents,
    insert_document_record,
    delete_document_record
)
from langchain_utils import get_rag_chain
from pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from fastapi.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi import FastAPI
import os
import uuid
import shutil
import logging
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Now the rest of your imports can happen
# ...

# 1. Advanced Logging Configuration for Production Monitoring
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()  # Allows you to see activity in your terminal
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Chatbot Production API")

# 2. Global Exception Handler to prevent raw code exposure to users


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "message": "An internal server error occurred. Please check the logs."}
    )


@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id or str(uuid.uuid4())
    logger.info(
        f"Chat Request - Session: {session_id}, Model: {query_input.model.value}")

    try:
        # Retrieve history and initialize the chain
        chat_history = get_chat_history(session_id)
        rag_chain = get_rag_chain(query_input.model.value)

        # Invoke the chain (the result includes 'answer' and 'context')
        result = rag_chain.invoke({
            "input": query_input.question,
            "chat_history": chat_history
        })

        answer = result.get(
            'answer', "I'm sorry, I couldn't generate an answer.")

        # Extract unique source filenames from the retrieved document context
        sources = list(set([doc.metadata.get('filename', 'Unknown')
                       for doc in result.get('context', [])]))

        # Log and persist the interaction
        insert_application_logs(
            session_id, query_input.question, answer, query_input.model.value)

        return QueryResponse(
            answer=answer,
            session_id=session_id,
            model=query_input.model,
            sources=sources  # NEW: Tells the UI which files were used
        )

    except Exception as e:
        logger.error(f"Error in /chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to process chat request.")


@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    # 3. Enhanced File Validation (Security Best Practice)
    allowed_extensions = ['.pdf', '.docx']
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Use a unique temporary path to prevent name collisions
    temp_file_path = f"temp_{uuid.uuid4()}_{file.filename}"

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = insert_document_record(file.filename)
        success = index_document_to_chroma(temp_file_path, file_id)

        if success:
            logger.info(f"Successfully uploaded and indexed: {file.filename}")
            return {"message": "File indexed successfully.", "file_id": file_id}
        else:
            delete_document_record(file_id)  # Cleanup DB if indexing fails
            raise HTTPException(
                status_code=500, detail="Document indexing failed.")

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents():
    return get_all_documents()


@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    # 4. Atomic Deletion logic: Ensures consistency between Chroma and SQLite
    logger.info(f"Deletion Request for File ID: {request.file_id}")

    chroma_success = delete_doc_from_chroma(request.file_id)
    if chroma_success:
        db_success = delete_document_record(request.file_id)
        if db_success:
            return {"message": f"Successfully deleted document {request.file_id}"}

    raise HTTPException(
        status_code=500, detail="System failed to delete the document.")
