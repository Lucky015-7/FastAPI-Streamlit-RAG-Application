import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Initialize Embeddings & Vectorstore
embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="./chroma_db",
                     embedding_function=embedding_function)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, length_function=len)


def load_and_split_document(file_path: str) -> List[Document]:
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    return text_splitter.split_documents(loader.load())


def index_document_to_chroma(file_path: str, file_id: int) -> bool:
    try:
        splits = load_and_split_document(file_path)
        for split in splits:
            split.metadata['file_id'] = file_id
        vectorstore.add_documents(splits)
        return True
    except Exception as e:
        print(f"Error indexing document: {e}")
        return False


def delete_doc_from_chroma(file_id: int):
    try:
        # Check if chunks exist before deletion (from referencing project)
        docs = vectorstore.get(where={"file_id": file_id})
        if len(docs.get('ids', [])) > 0:
            vectorstore._collection.delete(where={"file_id": file_id})
        return True
    except Exception as e:
        print(f"Error deleting from Chroma: {str(e)}")
        return False
