from fastapi import FastAPI
from pydantic import BaseModel
from main import start_research, resume_research
app = FastAPI(
    title="Autonomous AI Research Copilot",
    version="1.0.0",
)
class ResearchRequest(BaseModel):
    topic: str
    thread_id: str

class ApprovalRequest(BaseModel):
    approved: bool
    feedback: str = ""
    thread_id: str

@app.get("/")
def home():
    return {
        "message": "Autonomous AI Research Copilot API"
    }

@app.post("/research")
def research(request: ResearchRequest):

    return start_research(
        topic=request.topic,
        thread_id=request.thread_id,
    )

@app.post("/resume")
def resume(request: ApprovalRequest):

    return resume_research(
        approved=request.approved,
        feedback=request.feedback,
        thread_id=request.thread_id,
    )
