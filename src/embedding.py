import requests


from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredMarkdownLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import PGVector


from src.config import api_key, vector_db_connection_string, vector_db_collection_name



class SiliconFlowEmbedding(Embeddings):
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = "https://api.siliconflow.cn/v1/embeddings"

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        payload = {
            "model": self.model_name,
            "input": texts
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", self.api_url, json=payload, headers=headers)
        return [item["embedding"] for item in response.json()["data"]]



def load_and_chunk(file_path: str, 
                   separator: str = "\n\n", 
                   chunk_size: int = 1024, 
                   chunk_overlap: int = 80
                   ):
    ## load file
    if file_path.endswith(".pdf"):
        loader = PyMuPDFLoader(file_path=file_path)
    elif file_path.endswith(".md"):
        loader = UnstructuredMarkdownLoader(file_path=file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path=file_path, encoding="utf-8")
    else:
        raise ValueError("Unsupported file type")

    ## split file
    text_splitter = RecursiveCharacterTextSplitter(
        separators=[separator, ],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = text_splitter.split_documents(loader.load())

    
    ## embed and save
    embedding_model = SiliconFlowEmbedding(
        api_key = api_key,
        model_name = "BAAI/bge-m3"
    )

    db = PGVector.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=vector_db_collection_name,
        connection_string=vector_db_connection_string,
    )

    return db


