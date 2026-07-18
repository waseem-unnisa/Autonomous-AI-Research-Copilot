# 🤖 Autonomous AI Research Copilot

An autonomous, multi-agent research assistant built with **LangGraph**, capable of planning, searching, retrieving, analyzing, fact-checking, and generating a fully cited research report — with a human-in-the-loop approval step before final PDF generation.

> Give it a topic. It plans its own research strategy, searches the web and academic papers, grounds its findings in a retrieval-augmented memory, verifies its own claims, writes a polished report, waits for your approval, and exports a PDF.

---

## 🧠 How It Works

The system is orchestrated as a **stateful multi-agent graph**, where each node is a specialized agent operating on a shared, strongly-typed state object.

```
START
  │
  ▼
Planner Agent  ──────────► generates a structured research plan from the topic
  │
  ▼
Web + ArXiv Search  ─────► Tavily (web) + ArXiv (academic papers)
  │
  ▼
RAG Pipeline  ───────────► chunks + embeds + stores documents in ChromaDB, retrieves relevant context
  │
  ▼
Research Analyzer  ──────► synthesizes retrieved context into a deep analytical breakdown
  │
  ▼
Fact Verification  ──────► strips unverified claims, checks source grounding
  │
  ▼
Report Generation  ──────► writes a polished, cited Markdown report
  │
  ▼
Human Approval (interrupt) ── reviewer approves or requests changes
  │                    │
  ▼                    ▼
Generate PDF      Back to Planner (with feedback)
  │
  ▼
END
```

Each stage writes to a shared `ResearchState` (a Pydantic model), so every agent has access to everything discovered before it — while the graph itself handles branching, retries, and the human-in-the-loop pause/resume cycle via LangGraph's `interrupt()` and checkpointing.

---

## ⚙️ Tech Stack

| Layer | Tool |
|---|---|
| Agent orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM inference | [Groq](https://groq.com/) |
| Web search | [Tavily](https://tavily.com/) |
| Academic search | [ArXiv API](https://pypi.org/project/arxiv/) |
| Vector memory / RAG | [ChromaDB](https://www.trychroma.com/) |
| Frontend | [Streamlit](https://streamlit.io/) |
| PDF generation | [ReportLab](https://www.reportlab.com/) |
| State validation | [Pydantic](https://docs.pydantic.dev/) |

---

## ✨ Features

- 🧭 **Autonomous planning** — breaks a broad topic into targeted sub-queries
- 🔎 **Dual-source search** — combines real-time web results with academic papers
- 🧩 **Retrieval-augmented synthesis** — grounds analysis in retrieved context, not just LLM memory
- ✅ **Self-verification** — a dedicated fact-checking pass before the report is written
- 🧑‍⚖️ **Human-in-the-loop** — nothing gets finalized without explicit approval, with a feedback loop back to planning if changes are requested
- 📄 **One-click PDF export** — of the final, approved report
- 🖥️ **Live pipeline status sidebar** — see which stage of research is complete at a glance

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- API keys for [Groq](https://console.groq.com/) and [Tavily](https://tavily.com/)

### Installation

```bash
git clone https://github.com/waseem-unnisa/autonomous-ai-research-copilot.git
cd autonomous-ai-research-copilot

python -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run Locally

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
autonomous-ai-research-copilot/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── fact_verification.py
│   │   ├── planner.py
│   │   └── reporter.py
│   ├── memory/
│   │   ├── __init__.py
│   │   └── rag_pipeline.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── llm.py
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── analyzer_prompt.py
│   │   ├── fact_checker_prompt.py
│   │   ├── planner_prompt.py
│   │   └── report_prompt.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── tools.py
│   │  
│   │   
│   ├── graph.py
│   └── state.py
├── chroma_db/                 # local vector store (gitignored)
├── reports/                   # generated PDF output (gitignored)
├── .env                        # API keys (gitignored, never committed)
├── .gitignore
├── api.py                      # FastAPI wrapper for programmatic access
├── app.py                      # Streamlit frontend
├── main.py                     # start_research / resume_research entry points
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 🎥 Demo

*(Video walkthrough coming soon)*

---

## 🌐 Live Demo

https://autonomous-ai-research-copilot-wylhtkas3shrfnbl3j5oqm.streamlit.app/

---

## 🗺️ Roadmap

- [ ] Real-time pipeline streaming (currently status is inferred post-hoc)
- [ ] Hosted deployment (Streamlit Community Cloud)
- [ ] Support for additional academic sources beyond ArXiv
- [ ] Multi-topic comparative research mode

---

##  Acknowledgments

**Built with:**
- [LangGraph](https://github.com/langchain-ai/langgraph) — stateful multi-agent orchestration
- [LangChain](https://www.langchain.com/) — prompt templating and chain composition
- [Groq](https://groq.com/) — high-speed LLM inference
- [ChromaDB](https://www.trychroma.com/) — vector store for retrieval-augmented generation
- [Streamlit](https://streamlit.io/) — interactive frontend
- [ReportLab](https://www.reportlab.com/) — PDF report generation
- [Pydantic](https://docs.pydantic.dev/) — typed, validated state management

**Supports:**
- [Tavily](https://tavily.com/) — real-time web search
- [ArXiv API](https://pypi.org/project/arxiv/) — academic paper search
- [FastAPI](https://fastapi.tiangolo.com/) — optional programmatic API access

---

## 📬 Contact

- **GitHub:** [waseem-unnisa](https://github.com/waseem-unnisa)
- **LinkedIn:** [Waseem Unnisa](https://www.linkedin.com/in/waseem-unnisa-8a68293ba/)
- **Hugging Face:** [wazym](https://huggingface.co/wazym)
- **Email:** [waseem.unisa2184@gmail.com](mailto:waseem.unisa2184@gmail.com)
