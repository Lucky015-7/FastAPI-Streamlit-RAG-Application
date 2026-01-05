import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from api.chroma_utils import vectorstore

# Initialize retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Prompt to rephrase the question into a standalone version
rephrase_prompt = ChatPromptTemplate.from_messages([
    ("system", "Given the chat history and user question, rephrase it as a standalone question."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Prompt for the final Q&A answer
qa_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant. Use the following context to answer:\n\n{context}"),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


def get_rag_chain(model="llama-3.3-70b-versatile"):
    llm = ChatGroq(model=model, temperature=0)

    def rag_logic(input_data):
        # Step A: Rephrase if history exists
        if input_data.get("chat_history"):
            rephrase_chain = rephrase_prompt | llm | StrOutputParser()
            standalone_q = rephrase_chain.invoke(input_data)
        else:
            standalone_q = input_data["input"]

        # Step B: Retrieve relevant documents
        docs = retriever.invoke(standalone_q)
        context_text = "\n\n".join(d.page_content for d in docs)

        # Step C: Generate Answer
        final_chain = qa_prompt | llm | StrOutputParser()
        answer = final_chain.invoke({
            "context": context_text,
            "chat_history": input_data["chat_history"],
            "input": input_data["input"]
        })

        # CRITICAL UPDATE: Return a dictionary to match referencing project structure
        # This allows main.py to extract result['answer'] and metadata for sources
        return {
            "answer": answer,
            "context": docs  # Pass the original Doc objects so metadata can be extracted
        }

    return RunnableLambda(rag_logic)
