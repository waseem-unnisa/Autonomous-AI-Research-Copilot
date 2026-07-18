from langchain_core.prompts import ChatPromptTemplate

from src.models.llm import llm
from src.prompts.fact_checker_prompt import FACT_VERIFICATION_PROMPT

fact_verification_prompt = ChatPromptTemplate.from_template(FACT_VERIFICATION_PROMPT)
fact_verification_chain = fact_verification_prompt | llm

def fact_verification_agent (
        topic:str, 
        analysis:str, 
        context:str,
):
    """
    Verify reasearch analysis using retrieved evidence."""

    response = fact_verification_chain.invoke(
        {
            "topic":topic,
            "analysis":analysis,
            "context":context,
        }
    )
    return response.content

