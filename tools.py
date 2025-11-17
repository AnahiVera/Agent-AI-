from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from datetime import datetime


# Create the DuckDuckGo search instance
duckduckgo_search = DuckDuckGoSearchRun()

#create my own tool 

def save_to_txt(data:str, filename: str = "research_output.txt"):
    timestap = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatted_text = f"--- research Output ---\nTimestamp: {timestap}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data succesfully saved to {filename}"

@tool("save_to_txt")
def save_to_txt_tool(data:str, filename: str = "research_output.txt"):
    """Save data to a text file with a timestamp."""
    return save_to_txt(data, filename)


@tool("web_search")
def search_tool(query: str) -> str:
    """Search the web for information using DuckDuckGo."""
    return duckduckgo_search.run(query)

api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=200)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)