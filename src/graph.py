from typing import Literal
import os
from langgraph.graph import StateGraph, START, END

from src.state import ResearchState

from src.agents.planner import planner_agent
from src.agents.analyzer import analyzer_agent
from src.agents.fact_verification import fact_verification_agent
from src.agents.reporter import report_agent

from src.utils.tools import search_web, search_arxiv

from src.memory.rag_pipeline import add_documents, retrieve_documents
from langgraph.types import interrupt, Command

#Planner Node
def planner_node(state: ResearchState):
    print("PLANNER STATE user_topic:", repr(state.user_topic))
    plan = planner_agent(
        topic=state.user_topic,
        feedback=state.feedback or ""
    )
    return{
        "reserach_plan": plan
    }
                       
#Search Node
def search_node(state: ResearchState):
    print("SEARCH STATE user_topic:", repr(state.user_topic))
    tavily_results = search_web(state.user_topic)
    arxiv_results = search_arxiv(state.user_topic)

    return {
        "web_results": tavily_results,
        "research_papers": arxiv_results,
    }
#RAG Node
def rag_node(state: ResearchState):
    documents = [r["content"] for r in state.web_results] + [
        p.get("summary", "") for p in state.research_papers
    ]

    if documents:
        add_documents(documents)

    retrieved_docs = retrieve_documents(state.user_topic)
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    return {
        "retrieved_chunk": [doc.page_content for doc in retrieved_docs],
        "context": context,
    }
#Analyzer Node

def analyzer_node(state: ResearchState):
    print("ANALYZER CONTEXT:", state.context[:300])
    analysis = analyzer_agent(
        topic=state.user_topic,
        context=state.context,
    )

    return {
        "analysis": analysis
    }
#Fact Verification Node
def fact_verification_node(state: ResearchState):

    verified = fact_verification_agent(
        topic=state.user_topic,
        analysis=state.analysis,
        context=state.context,
    )

    return {
        "verified_analysis": verified
    }
#Report Node
def report_node(state: ResearchState):

    report = report_agent(
        topic=state.user_topic,
        analysis=state.verified_analysis,
    )

    return {
        "markdown_report": report
    }
#Human in the loop
def human_approval_node(state: ResearchState):

    response = interrupt(
        {
            "report": state.markdown_report,
            "message": "Review the report and choose Approve or Request Changes."
        }
    )

    status = "appoved" if response["approved"] else "revision_required"

    return {
        "apporoval_status": status,
        "feedback": response.get("feedback", "")
    }

#Pdf Node
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
def pdf_node(state: ResearchState):

    report = state.markdown_report

    pdf_path = "reports/research_report.pdf"

    doc = SimpleDocTemplate(pdf_path)
    
    os.makedirs("reports", exist_ok=True)

    styles = getSampleStyleSheet()

    story = []

    for line in report.split("\n"):

        if line.strip():
            story.append(
                Paragraph(
                    line,
                    styles["BodyText"],
                )
            )

    doc.build(story)

    return {
        "pdf_path": pdf_path
    }

#Approval Router
def approval_router(state: ResearchState) -> Literal["pdf", "planner"]:
    if state.apporoval_status == "appoved":
        return "pdf"
    return "planner"

#State Graph
research_graph = StateGraph(ResearchState)

research_graph.add_node("planner",planner_node)
research_graph.add_node("search",search_node)
research_graph.add_node("rag", rag_node)
research_graph.add_node("analyzer", analyzer_node)
research_graph.add_node("fact_verification", fact_verification_node)
research_graph.add_node("report", report_node)
research_graph.add_node("human_approval",human_approval_node)
research_graph.add_node("pdf", pdf_node)

research_graph.add_edge(START,"planner")
research_graph.add_edge("planner", "search")
research_graph.add_edge("search","rag")
research_graph.add_edge("rag","analyzer")
research_graph.add_edge("analyzer","fact_verification")
research_graph.add_edge("fact_verification", "report")
research_graph.add_edge("report","human_approval")
research_graph.add_conditional_edges(
    "human_approval",
    approval_router,
    {
        "pdf": "pdf",
        "planner": "planner",
    },
)
research_graph.add_edge("pdf", END)

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

graph = research_graph.compile(
    checkpointer=memory
)

