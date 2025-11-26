from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
from tools import save_to_txt_tool, read_cv_tool, read_personality_tool



load_dotenv() # Load .env variables 


#This is the model for the response
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize language models 
llm = ChatOpenAI(model = "gpt-4o-mini")
#llm = ChatAnthropic(model = "claude-3-5-sonnet-20241022")

#set uo the output parser to use the ResearchResponse model
parser= PydanticOutputParser(pydantic_object=ResearchResponse)

#Tools list
tools=[save_to_txt_tool, read_personality_tool, read_cv_tool]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=f"""
        You are a research assistant. You know the following about your creator: 
        - Name: Anahi Vera Rogel
        - Address: Pupetra s/n, Dalcahue, Chiloe, Chile
        - email: vera.anahi.93@gmail.com 


    Format your response as JSON with these fields:
    - topic: the main topic
    - summary: a concise summary
    - tools_used: list any tools used
    
    {parser.get_format_instructions()}
    """
   
)

#executes the agent / generates the response
query = input("What would you like to know about my creator?:")
response = agent.invoke(
   {"messages": [{"role": "user", "content": query}]}
)

try:
    structured_response = parser.parse(response.get("messages")[-1].content)
    print(structured_response)
except Exception as error:
    print("Error parsing response ", error, "Raw Response: - ", response)
