from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime
from typing import List, Optional


class ModelName(str, Enum):
    LLAMA_3_3 = "llama-3.3-70b-versatile"


class QueryInput(BaseModel):
    question: str = Field(...,
                          description="The user's question to the assistant")
    session_id: Optional[str] = Field(
        default=None, description="The unique session ID for the chat history")
    model: ModelName = Field(default=ModelName.LLAMA_3_3)


class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName
    # ADDED: Optional list of document sources for better UI feedback
    sources: Optional[List[str]] = Field(
        default=[], description="List of filenames used to generate the answer")


class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime
    # ADDED: To help the UI display file size or type if needed
    file_size: Optional[int] = Field(
        default=None, description="Size of the file in bytes")


class DeleteFileRequest(BaseModel):
    file_id: int

# ADDED: A standard success/failure response model for general API actions


class MessageResponse(BaseModel):
    message: str
    status: str = "success"
