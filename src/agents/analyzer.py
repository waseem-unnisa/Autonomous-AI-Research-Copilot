from langchain_core.prompts import ChatPromptTemplate

from src.models.llm import llm
from src.prompts.analyzer_prompt import ANALYZER_PROMPT

analyzer_prompt = ChatPromptTemplate.from_template(ANALYZER_PROMPT)

analyzer_chain = analyzer_prompt | llm

def analyzer_agent(topic: str, context: str):
    """ 
    Analyze retrieved reasearch documents.
    """
    response = analyzer_chain.invoke({
        "context": context,
        "topic": topic
    })
    return response.content