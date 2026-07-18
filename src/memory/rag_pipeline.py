from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Text Spiltter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)

 # Embedding Model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

 # Vector Store
vector_store = Chroma(
    collection_name="research_memory",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

 # Chunk Documents
def chunk_documents(documents: list[str]):
    docs = [Document(page_content=text) for text in documents]
    return text_splitter.split_documents(docs)


 # Store Documents
def add_documents(documents: list[str]):
    chunks = chunk_documents(documents)
    vector_store.add_documents(chunks)
    return chunks

 # Retrieve
def retrieve_documents(query: str, k: int = 3):
    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )
    return retriever.invoke(query)

 # Complete Pipeline
def rag_pipeline(documents: list[str], query: str, k: int = 3):
    add_documents(documents)
    return retrieve_documents(query, k)

 # Clear Database
def clear_database():
    vector_store.reset_collection()




