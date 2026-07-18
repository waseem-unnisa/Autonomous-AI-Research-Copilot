from langchain_core.prompts import ChatPromptTemplate

from src.models.llm import llm
from src.prompts.report_prompt import REPORT_PROMPT

report_prompt = ChatPromptTemplate.from_template(REPORT_PROMPT)
report_chain = report_prompt | llm

def report_agent(
        topic:str,
        analysis:str,
):
    """
    Generate the final reaserach report.
    """

    response = report_chain.invoke(
        {
            "topic":topic,
            "analysis":analysis,
        }
    )
    return response.content