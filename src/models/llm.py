from langchain_groq import ChatGroq

from src.utils.config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="openai/gpt-oss-20b",
    temperature=0,
) 

