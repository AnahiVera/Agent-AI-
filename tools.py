from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from datetime import datetime
import json
import os

# Tool to read CV
@tool("read_cv")
def read_cv_tool() -> str:
    """Reads the cv.json file and returns its content as text so the AI can answer questions about your experience, education and skills."""
    try:
        with open("cv.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return json.dumps(data, ensure_ascii=False, indent=2)
    except FileNotFoundError:
        return "Error: cv.json file was not found."
    except json.JSONDecodeError:
        return "Error: cv.json file has invalid JSON format."

# Tool to read personality
@tool("read_personality")
def read_personality_tool() -> str:
    """Reads the personality.txt file and returns its content so the AI can understand your personality, interests and character."""
    try:
        with open("personality.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Error: personality.txt file was not found."

# Tool to save text
@tool("save_to_txt")
def save_to_txt_tool(data: str, filename: str = "research_output.txt") -> str:
    """Save data to a text file with a timestamp."""
    return save_to_txt(data, filename)

def save_to_txt(data: str, filename: str = "research_output.txt") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"

# Verify that files exist
def check_files():
    required_files = ["cv.json", "personality.txt"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"Warning: {file} not found in current directory")

# Check files on import
check_files()

# Wikipedia configuration
api_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=200)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)