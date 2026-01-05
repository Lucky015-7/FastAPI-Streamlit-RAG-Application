import numpy as np
import os
import uuid
import shutil
import logging
import sys
from dotenv import load_dotenv

# FastAPI and Pydantic imports
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse

# --- SMART IMPORT BLOCK ---
# This allows the code to run from the root (Docker) OR from inside /api (Local)
try:
    from api.chroma_utils import index_document_to_chroma, delete_doc_from_chroma
    from api.db_utils import (
        insert_application_logs, get_chat_history, get_all_documents,
        insert_document_record, delete_document_record
    )
    from api.langchain_utils import get_rag_chain
    from api.pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
except ModuleNotFoundError:
    from chroma_utils import index_document_to_chroma, delete_doc_from_chroma
    from db_utils import (
        insert_application_logs, get_chat_history, get_all_documents,
        insert_document_record, delete_document_record
    )
    from langchain_utils import get_rag_chain
    from pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest

# Load variables from .env file
load_dotenv()

# NumPy 2.x Compatibility Fix (Important for Torch/Langchain)
if int(np.__version__.split('.')[0]) >= 2:
    os.environ["NUMPY_EXPERIMENTAL_ARRAY_FUNCTION"] = "0"

# 1. Advanced Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Chatbot Production API")

# 2. Global Exception Handler


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
        chat_history = get_chat_history(session_id)
        rag_chain = get_rag_chain(query_input.model.value)

        result = rag_chain.invoke({
            "input": query_input.question,
            "chat_history": chat_history
        })

        answer = result.get(
            'answer', "I'm sorry, I couldn't generate an answer.")
        sources = list(set([doc.metadata.get('filename', 'Unknown')
                       for doc in result.get('context', [])]))

        insert_application_logs(
            session_id, query_input.question, answer, query_input.model.value)

        return QueryResponse(
            answer=answer,
            session_id=session_id,
            model=query_input.model,
            sources=sources
        )

    except Exception as e:
        logger.error(f"Error in /chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to process chat request.")


@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = ['.pdf', '.docx']
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

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
            delete_document_record(file_id)
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
    logger.info(f"Deletion Request for File ID: {request.file_id}")
    chroma_success = delete_doc_from_chroma(request.file_id)
    if chroma_success:
        db_success = delete_document_record(request.file_id)
        if db_success:
            return {"message": f"Successfully deleted document {request.file_id}"}

    raise HTTPException(
        status_code=500, detail="System failed to delete the document.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
