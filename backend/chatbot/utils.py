"""
Chatbot utility functions for RAG integration and knowledge base management.
"""

import os
from pathlib import Path
from django.conf import settings


def get_db_path(tenant_id=None):
    """
    Get Chroma database path for a tenant.
    
    Args:
        tenant_id: ID of the tenant (optional)
    
    Returns:
        str: Path to the Chroma database
    """
    db_dir = Path(settings.BASE_DIR) / 'chroma_db'
    db_dir.mkdir(exist_ok=True)
    
    if tenant_id:
        return str(db_dir / f'tenant_{tenant_id}')
    return str(db_dir / 'default')


def initialize_knowledge_base(documents, tenant_id=None):
    """
    Initialize or rebuild the Chroma vector database with documents.
    
    Args:
        documents: List of document strings to embed
        tenant_id: ID of the tenant (optional)
    
    Returns:
        Chroma: Initialized vector store
    """
    try:
        from langchain_chroma import Chroma
        from langchain_community.embeddings import HuggingFaceInstructEmbeddings
    except ImportError:
        raise ImportError(
            "LangChain dependencies not installed. "
            "Run: pip install langchain langchain-chroma langchain-community"
        )
    
    # Initialize embeddings
    embedding_model = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-large",
        model_kwargs={'device': 'cpu'}
    )
    
    # Create Chroma vector store
    db_path = get_db_path(tenant_id)
    vectordb = Chroma.from_texts(
        texts=documents,
        embedding=embedding_model,
        persist_directory=db_path
    )
    
    return vectordb


def get_retriever(tenant_id=None, k=3):
    """
    Get a retriever from an existing Chroma database.
    
    Args:
        tenant_id: ID of the tenant (optional)
        k: Number of documents to retrieve
    
    Returns:
        Retriever: LangChain retriever object
    """
    try:
        from langchain_chroma import Chroma
        from langchain_community.embeddings import HuggingFaceInstructEmbeddings
    except ImportError:
        raise ImportError("LangChain dependencies not installed")
    
    db_path = get_db_path(tenant_id)
    
    # Load embeddings
    embedding_model = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-large",
        model_kwargs={'device': 'cpu'}
    )
    
    # Load Chroma database
    vectordb = Chroma(
        embedding_function=embedding_model,
        persist_directory=db_path
    )
    
    return vectordb.as_retriever(search_kwargs={"k": k})


def create_rag_chain(retriever, temperature=0.2):
    """
    Create a RAG chain with LangChain and Groq LLM.
    
    Args:
        retriever: LangChain retriever object
        temperature: LLM temperature for randomness
    
    Returns:
        Runnable: RAG chain
    """
    try:
        from langchain_groq import ChatGroq
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.runnables import RunnablePassthrough
        from langchain_core.output_parsers import StrOutputParser
    except ImportError:
        raise ImportError("LangChain dependencies not installed")
    
    if "GROQ_API_KEY" not in os.environ:
        raise ValueError("GROQ_API_KEY environment variable not set")
    
    # Initialize LLM
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=temperature
    )
    
    # Create prompt
    template = """You are the NUST Olympiad Assistant.
Analyze the context below to answer the user's question accurately and helpfully.

Guidelines:
- If the answer is in the context, provide a clear answer
- If the context is irrelevant, politely say you don't have information
- Be concise and helpful
- Use context to reason through complex questions

Context: {context}
Question: {question}
Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain
