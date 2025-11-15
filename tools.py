from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from datetime import datetime


# Create the DuckDuckGo search instance
duckduckgo_search = DuckDuckGoSearchRun()

@tool("web_search")
def search_tool(query: str) -> str:
    """Search the web for information using DuckDuckGo."""
    return duckduckgo_search.run(query)

