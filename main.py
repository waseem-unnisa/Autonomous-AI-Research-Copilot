from langgraph.types import Command

from src.graph import graph

def start_research(topic: str, thread_id: str):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    initial_state = {
        "user_topic": topic,
        "plan":[],
        "web_results": [],
        "research_papers": [],
        "documents": [],
        "retrieved_chunk": [],
        "context": "",
        "analysis":None,
        "verified_analysis":None,
        "markdown_report": None,
        "approval_status":"pending",
        "feedback":None,
        "pdf_path":None,
        "error": None
    }

    return graph.invoke(initial_state, config=config)

def resume_research(
    approved: bool,
    feedback: str,
    thread_id: str,
):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    return graph.invoke(
        Command(
            resume={
                "approved": approved,
                "feedback": feedback,
            }
        ),
        config=config,
    )