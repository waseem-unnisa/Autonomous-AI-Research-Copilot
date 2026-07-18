from tavily import TavilyClient
from src.utils.config import TAVILY_API_KEY
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
import arxiv
arxiv_client = arxiv.Client()
def search_web(query:str, max_results: int = 3) -> list:
    query = (query or "").strip()
    if not query:
        return []
    """
    Search the web using Tavily API and returns the results.
    """
    response = tavily_client.search(
        query = query,
        max_results= max_results,
        search_depth= "advanced"
    )
    return response.get("results",[])
#arxiv Tool
def search_arxiv(query:str, max_results:int = 3) -> list:
    query = (query or "").strip()
    if not query:
        return []
    """ 
    Search the reasherch papers from arxiv.
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    papers= []
    for paper in arxiv_client.results(search):
         papers.append(
            {
                "title": paper.title,
                "authors": [author.name for author in paper.authors],
                "summary": paper.summary,
                "published": str(paper.published.date()),
                "pdf_url": paper.pdf_url,
                "entry_id": paper.entry_id,
            }
        )
    return papers

