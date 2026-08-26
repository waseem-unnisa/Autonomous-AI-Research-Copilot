from langchain_groq import ChatGroq

from src.utils.config import GROQ_API_KEY

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0,
) 

response = llm.invoke("Whhat is the capital of The United Kingdom?")

print(response.content)
