from uuid import uuid4
import streamlit as st
from main import start_research, resume_research

st.set_page_config(
    page_title="Autonomus AI Research Copilot",
    page_icon="🤖",
    layout="wide",
)
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    div[data-testid="stSidebar"] {
        background-color: #161a23;
        border-right: 1px solid #262b36;
    }
    .stage-pending { color: #5c6370; padding: 4px 0; }
    .stage-active { color: #00d4ff; font-weight: 600; padding: 4px 0; }
    .stage-done { color: #3ddc84; padding: 4px 0; }
    div[data-testid="stButton"] button {
        border-radius: 8px;
        border: 1px solid #262b36;
    }
</style>
""", unsafe_allow_html=True)

st.title("Autonomus AI Research Copilot 🤖")
st.caption("Research . Analyze . Verify . Generate")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid4())

if "result" not in st.session_state:
    st.session_state.result = None

if"waiting_for_approval" not in st.session_state:
    st.session_state.waiting_for_approval = False

def render_pipeline_status():
    result = st.session_state.result
    stages = [
        ("Planner", True),
        ("Search (Tavily + ArXiv)", result and result.get("web_results")),
        ("RAG Retrieval", result and result.get("context")),
        ("Analyzer", result and result.get("analysis")),
        ("Fact Verification", result and result.get("verified_analysis")),
        ("Report Generation", result and result.get("markdown_report")),
        ("Human Approval", result and result.get("apporoval_status") == "appoved"),
        ("PDF Generation", result and result.get("pdf_path")),
    ]

    st.sidebar.subheader("Pipeline Status")
    for name, done in stages:
        if done:
            st.sidebar.markdown(f'<div class="stage-done">✅ {name}</div>', unsafe_allow_html=True)
        elif result:
            st.sidebar.markdown(f'<div class="stage-active">⏳ {name}</div>', unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f'<div class="stage-pending">◯ {name}</div>', unsafe_allow_html=True)    

render_pipeline_status()
    #Research Topic
topic = st.text_input(
    "Research Topic",
    placeholder= "e.g. Research on Healthcare & Biotechnology"
)

   #Generate Report
if st.button("Generate Research Report", use_container_width=True):
    with st.spinner("Researching..."):
        st.session_state.result = start_research(
        topic,
        st.session_state.thread_id,)
        st.session_state.waiting_for_approval = True

    #Dispaly Report

if st.session_state.result:
    st.divider()
    st.subheader("Research Report")
    st.markdown(st.session_state.result.get("markdown_report"))

    #Human in the Loop

if st.session_state.waiting_for_approval:
    st.subheader("Review Report")
    feedback = st.text_area(
        "request Changes(Optional)"
    )
    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Approve & Generate PDF",
            use_container_width=True,
        ):

            st.session_state.result = resume_research(
                approved=True,
                feedback="",
                thread_id=st.session_state.thread_id,
            )

            st.session_state.waiting_for_approval = False
            st.rerun()

    with col2:

        if st.button(
            "Request Changes",
            use_container_width=True,
        ):

            st.session_state.result = resume_research(
                approved=False,
                feedback=feedback,
                thread_id=st.session_state.thread_id,
            )
            st.rerun()
   # Download PDF  
if (
    st.session_state.result
    and st.session_state.result.get("pdf_path")
):

    with open(
        st.session_state.result.get("pdf_path"),
        "rb",
    ) as file:

        st.download_button(
            "📄 Download PDF Report",
            data=file,
            file_name="research_report.pdf",
            mime="application/pdf",
            use_container_width=True,
        )