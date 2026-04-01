import os
from typing import List
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from backend.app.core.config import settings

class RAGEngine:
    def __init__(self):
        # We use Qwen embeddings via OpenAI compatible interface
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-v2",
            openai_api_key=settings.DASHSCOPE_API_KEY,
            openai_api_base=settings.DASHSCOPE_BASE_URL
        )
        self.llm = ChatOpenAI(
            model="qwen-plus",
            openai_api_key=settings.DASHSCOPE_API_KEY,
            openai_api_base=settings.DASHSCOPE_BASE_URL
        )
        self.persist_directory = settings.CHROMA_DB_DIR
        self.vector_db = None

    def ingest_text(self, text: str, collection_name: str = "default"):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(text)

        self.vector_db = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=collection_name
        )
        # self.vector_db.persist() # Chroma 0.4+ persists automatically

    def query(self, question: str, collection_name: str = "default") -> str:
        if not self.vector_db:
            self.vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=collection_name
            )

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever()
        )
        return qa_chain.invoke(question)["result"]

rag_engine = RAGEngine()
