from langchain_core.prompts import ChatPromptTemplate
from src.models.llm import llm
import json
from src.prompts.planner_prompt import PLANNER_PROMPT

# Create a ChatPromptTemplate from the planner prompt template
planner_prompt = ChatPromptTemplate.from_template(PLANNER_PROMPT)

planner_chain = planner_prompt | llm

def planner_agent(topic:str, feedback: str = ""):
    """
    Create a research plan from the user's topic.
    """
    response = planner_chain.invoke({
        "topic": topic,                     
        "feedback": feedback,
        }
    )
    plan = json.loads(response.content)
    return plan

