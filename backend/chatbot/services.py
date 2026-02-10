"""
Chatbot Service Module
Handles RAG-powered chatbot using LangChain and Groq LLM
Integrates NUST Olympiad knowledge base with semantic search
"""

import os
import logging
from typing import List, Optional, Dict, Tuple

# Optional pandas import
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
logger = logging.getLogger(__name__)

# LangChain imports
try:
    from langchain_groq import ChatGroq
    from langchain_chroma import Chroma
    from langchain_community.embeddings import HuggingFaceInstructEmbeddings
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough
    from langchain_core.output_parsers import StrOutputParser
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("LangChain dependencies not installed. Chatbot service will be limited.")


class ChatbotService:
    """
    RAG-powered chatbot service for NUST Olympiad
    Uses Groq LLM with Chroma vector database for semantic search
    """
    
    def __init__(self):
        self.embedding_model = None
        self.llm = None
        self.vectordb = None
        self._initialize()
    
    def _initialize(self):
        """Initialize embeddings and LLM models"""
        if not LANGCHAIN_AVAILABLE:
            logger.error("LangChain not available")
            return False
        
        try:
            # Initialize embeddings with CPU if CUDA not available
            self.embedding_model = HuggingFaceInstructEmbeddings(
                model_name="hkunlp/instructor-large",
                model_kwargs={'device': 'cpu'}
            )
            
            # Initialize Groq LLM
            if "GROQ_API_KEY" not in os.environ:
                logger.warning("GROQ_API_KEY not set. Chatbot will not work properly.")
                return False
            
            self.llm = ChatGroq(
                model_name="llama-3.3-70b-versatile",
                temperature=0.2
            )
            
            logger.info("Chatbot service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize chatbot service: {str(e)}")
            return False
    
    def build_knowledge_base(self, documents: List[str], db_path: str = "./chroma_db"):
        """
        Build vector database from documents
        
        Args:
            documents: List of document strings to embed
            db_path: Path to persist Chroma database
        
        Returns:
            bool: Success status
        """
        if not LANGCHAIN_AVAILABLE or not self.embedding_model:
            logger.error("Cannot build knowledge base - dependencies not available")
            return False
        
        if not documents:
            logger.warning("No documents provided for knowledge base")
            return False
        
        try:
            self.vectordb = Chroma.from_texts(
                texts=documents,
                embedding=self.embedding_model,
                persist_directory=db_path
            )
            logger.info(f"Knowledge base created with {len(documents)} documents")
            return True
        except Exception as e:
            logger.error(f"Failed to build knowledge base: {str(e)}")
            return False
    
    def load_knowledge_base(self, db_path: str = "./chroma_db"):
        """
        Load existing Chroma vector database
        
        Args:
            db_path: Path to Chroma database
        
        Returns:
            bool: Success status
        """
        if not LANGCHAIN_AVAILABLE or not self.embedding_model:
            return False
        
        try:
            self.vectordb = Chroma(
                persist_directory=db_path,
                embedding_function=self.embedding_model
            )
            logger.info(f"Knowledge base loaded from {db_path}")
            return True
        except Exception as e:
            logger.warning(f"Could not load knowledge base: {str(e)}")
            return False
    
    def get_response(self, user_message: str, context_docs: int = 3) -> Tuple[str, List[str]]:
        """
        Get RAG response from chatbot
        
        Args:
            user_message: User's question
            context_docs: Number of context documents to retrieve
        
        Returns:
            Tuple of (response_text, retrieved_document_ids)
        """
        if not LANGCHAIN_AVAILABLE or not self.llm or not self.vectordb:
            return "Chatbot service is not available. Please check configuration.", []
        
        try:
            # Set up retriever
            retriever = self.vectordb.as_retriever(search_kwargs={"k": context_docs})
            
            # Create prompt template
            template = """You are the NUST Olympiad Assistant, helping attendees with event information.

Your responsibilities:
1. Answer questions about the olympiad, events, schedule, and logistics
2. Provide venue information and directions
3. Help with registration and ticket information
4. Answer FAQs about the event
5. Be helpful, accurate, and concise

Guidelines:
- If the answer is in the provided context, use it to answer accurately
- If the context doesn't have the information, politely say you don't have that information
- Provide clear, structured answers
- Use context to reason through complex questions
- Always be professional and helpful

Context from knowledge base:
{context}

User Question: {question}

Answer:"""
            
            prompt = ChatPromptTemplate.from_template(template)
            
            def format_docs(docs):
                """Format retrieved documents"""
                return "\n\n".join([
                    f"[Source {i+1}] {doc.page_content}"
                    for i, doc in enumerate(docs)
                ])
            
            # Build RAG chain
            rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            
            # Get response
            response = rag_chain.invoke(user_message)
            
            # Retrieve document IDs for reference
            retrieved_docs = retriever.invoke(user_message)
            doc_ids = [doc.metadata.get('source', 'unknown') for doc in retrieved_docs]
            
            return response, doc_ids
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            logger.error(error_msg)
            return error_msg, []
    
    def get_multi_query_response(self, user_message: str, context_docs: int = 3) -> str:
        """
        Get response using multi-query expansion for better retrieval
        
        Args:
            user_message: User's question
            context_docs: Number of context documents to retrieve
        
        Returns:
            Response string
        """
        if not LANGCHAIN_AVAILABLE or not self.llm or not self.vectordb:
            return "Chatbot service is not available."
        
        try:
            # Generate query variations
            query_variation_prompt = ChatPromptTemplate.from_template(
                """Generate 3 different versions of the following question that could be used 
to retrieve information from a knowledge base. Return only the 3 versions, one per line, 
without numbering or extra text.

Original question: {question}"""
            )
            
            # Generate variations
            query_generator = query_variation_prompt | self.llm | StrOutputParser()
            variations_text = query_generator.invoke({"question": user_message})
            variations = [q.strip() for q in variations_text.split('\n') if q.strip()][:3]
            
            # Add original question
            all_queries = [user_message] + variations
            
            # Retrieve documents for all queries
            retriever = self.vectordb.as_retriever(search_kwargs={"k": context_docs})
            all_docs = []
            for query in all_queries:
                try:
                    docs = retriever.invoke(query)
                    all_docs.extend(docs)
                except:
                    pass
            
            # Remove duplicates
            unique_docs = {doc.page_content: doc for doc in all_docs}.values()
            
            # Generate response using retrieved documents
            template = """You are the NUST Olympiad Assistant.

Context from knowledge base:
{context}

User Question: {question}

Provide a helpful and accurate answer:"""
            
            prompt = ChatPromptTemplate.from_template(template)
            context_text = "\n\n".join([doc.page_content for doc in unique_docs])
            
            response_chain = prompt | self.llm | StrOutputParser()
            response = response_chain.invoke({
                "context": context_text,
                "question": user_message
            })
            
            return response
            
        except Exception as e:
            logger.error(f"Multi-query response error: {str(e)}")
            return f"Error generating response: {str(e)}"


class ChatbotDataLoader:
    """
    Load predefined NUST Olympiad knowledge base
    """
    
    @staticmethod
    def get_default_knowledge_base() -> List[str]:
        """
        Return default NUST Olympiad FAQ and information
        
        Returns:
            List of knowledge base documents
        """
        data = [
            {
                "question": "What is the University Olympiad?",
                "answer": "The University Olympiad is a multi-day event consisting of technical, non-technical, and sports competitions organized by different university societies in collaboration with the central Olympiad society."
            },
            {
                "question": "Who organizes the Olympiad?",
                "answer": "The Olympiad is centrally governed by the Olympiad Society and individual modules are managed by respective university societies."
            },
            {
                "question": "What types of events are included in the Olympiad?",
                "answer": "The Olympiad includes technical modules, non-technical modules, and sports events."
            },
            {
                "question": "What is a module in the Olympiad?",
                "answer": "A module is a category of events such as a technical competition, non-technical contest, or sports event managed by a specific society."
            },
            {
                "question": "Who can create events in the system?",
                "answer": "Only Society Admins or authorized Event Heads can create and manage events."
            },
            {
                "question": "What is the role of the Olympiad Core Team?",
                "answer": "The Olympiad Core Team acts as Super Admin and oversees all societies, events, and platform configurations."
            },
            {
                "question": "How does participant registration work?",
                "answer": "Participants register online through dynamic forms, select tickets, and receive a QR code confirmation."
            },
            {
                "question": "What is early bird registration?",
                "answer": "Early bird registration offers discounted pricing for participants who register before a defined deadline."
            },
            {
                "question": "What happens if an event is full?",
                "answer": "If an event reaches capacity, new registrants are added to a waitlist automatically."
            },
            {
                "question": "How is entry managed at the venue?",
                "answer": "Entry is managed using QR code check-in which can work both online and offline."
            },
            {
                "question": "What is AI-based attendee matching?",
                "answer": "AI-based attendee matching recommends participants to connect based on interests, roles, and goals."
            },
            {
                "question": "What is the event chatbot used for?",
                "answer": "The chatbot answers questions related to schedule, venue, speakers, and general event logistics."
            },
            {
                "question": "Can attendees get a personalized agenda?",
                "answer": "Yes, the system generates a personalized agenda based on attendee interests and preferences."
            },
            {
                "question": "What is the venue floor plan feature?",
                "answer": "It is an interactive visual map showing seating, booths, and capacity information."
            },
            {
                "question": "How are badges generated?",
                "answer": "Badges are generated using a custom badge designer with dynamic fields and exported as PDFs."
            },
        ]
        
        # Convert to document strings
        documents = [
            f"Q: {item['question']}\nA: {item['answer']}"
            for item in data
        ]
        
        return documents
    
    @staticmethod
    def load_from_csv(csv_path: str) -> List[str]:
        """
        Load knowledge base from CSV file
        
        Args:
            csv_path: Path to CSV file with 'question' and 'answer' columns
        
        Returns:
            List of document strings
                if not PANDAS_AVAILABLE:
                    logger.error("Pandas not installed. Cannot load CSV files.")
                    return []
        
        """
        try:
            df = pd.read_csv(csv_path)
            documents = [
                f"Q: {row['question']}\nA: {row['answer']}"
                for _, row in df.iterrows()
            ]
            logger.info(f"Loaded {len(documents)} documents from {csv_path}")
            return documents
        except Exception as e:
            logger.error(f"Failed to load CSV: {str(e)}")
            return []


# Global chatbot instance
_chatbot_instance = None


def get_chatbot_service() -> ChatbotService:
    """
    Get or create global chatbot service instance
    
    Returns:
        ChatbotService instance
    """
    global _chatbot_instance
    if _chatbot_instance is None:
        _chatbot_instance = ChatbotService()
    return _chatbot_instance


def initialize_chatbot_with_defaults():
    """
    Initialize chatbot with default knowledge base
    """
    service = get_chatbot_service()
    docs = ChatbotDataLoader.get_default_knowledge_base()
    service.build_knowledge_base(docs, "./chroma_db_default")
    logger.info("Chatbot initialized with default knowledge base")
