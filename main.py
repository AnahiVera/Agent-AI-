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

# Fail-safe para controlar qué preguntas están permitidas
def is_question_allowed(query: str) -> bool:
    q = query.lower()

    print("\n[DEBUG] ---- INICIO CHECKEO FAILSAFE ----")
    print(f"[DEBUG] Query recibida: {query}")

    # Palabras bloqueadas
    forbidden = [
        "sexual", "violencia", "hackear", "contraseña",
        "nudes", "desnudo", "contenido explicito"
    ]

    # Keywords relacionadas con Anahi (base del CV + personalidad)
    allowed_keywords = [
        # Identidad
        "anahi", "vera", "anahi vera", "anahi constanza",
        "perfil", "sobre ti", "sobre anahi",

        # CV / Datos
        "cv", "curriculum", "portafolio", "portfolio",
        "linkedin", "github", "contacto",

        # Skills
        "javascript", "react", "api", "api rest", "jwt", "cloudinary",
        "nestjs", "sql", "python", "flask", "html", "css", "tailwind",
        "postman", "node", "node.js", "express", "typescript",
        "git", "mongodb",

        # Educación
        "4geeks", "four gees", "full stack open", "helsinki",
        "universidad catolica", "profesora de ingles",
        "licenciada en educacion", "certificacion", "estudios",

        # Experiencia laboral
        "hoktus", "octopus", "ingeniera", "desarrolladora",
        "secretaria", "administrativa", "dayenu", "experiencia laboral",

        # Proyectos
        "proyecto", "proyectos", "flash jobs", "certificados",
        "repositorio",

        # Personalidad y gustos
        "personalidad", "caracter", "gustos", "hobbies",
        "jardin", "jardineria", "gaming", "juegos", "videojuegos",
        "dragon age", "d&d", "rol",
        "lectura", "libros", "tolkien", "lord of the rings",
        "100 años de soledad", "fantasmas del invierno",
        "chocolate amargo", "cafe", "lemon pie"
    ]

    # 1. Verificar palabras prohibidas
    forbidden_matches = [word for word in forbidden if word in q]
    print(f"[DEBUG] Coincidencias prohibidas: {forbidden_matches}")

    if forbidden_matches:
        print("[DEBUG] BLOQUEADO: Contiene palabra prohibida.")
        print("No puedo responder esa pregunta.")
        return False

    # 2. Verificar si es relevante a Anahi
    allowed_matches = [word for word in allowed_keywords if word in q]
    print(f"[DEBUG] Coincidencias permitidas: {allowed_matches}")

    if not allowed_matches:
        print("[DEBUG] BLOQUEADO: No contiene keywords sobre Anahi.")
        print("No tengo información sobre ese tema. Solo puedo responder preguntas relacionadas con Anahi.")
        return False

    print("[DEBUG] PASA FAILSAFE ✔")
    return True


# --------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# --------------------------------------------------------
# solo se ejecuta si se corre este archivo directamente de lo contrario se importa como módulo
if __name__ == "__main__":
    query = input("What would you like to know about my creator?: ")

    print("\n[DEBUG] Llamando failsafe...")
    if not is_question_allowed(query):
        print("[DEBUG] FAILSAFE BLOQUEÓ LA CONSULTA. NO LLAMAREMOS AL AGENTE")
        print("No tengo información sobre ese tema. Solo puedo responder preguntas relacionadas con Anahi.")
        exit()

    print("[DEBUG] FAILSAFE PERMITIÓ LA PREGUNTA. LLAMANDO AL AGENTE... ✔")

    # 2. SI PASA EL FILTRO, SE EJECUTA EL AGENTE NORMALMENTE
    response = agent.invoke(
       {"messages": [{"role": "user", "content": query}]}
    )

    print("[DEBUG] RESPUESTA DEL AGENTE RECIBIDA")

    # 3. Parseo normal
    try:
        structured_response = parser.parse(response.get("messages")[-1].content)
        print("[DEBUG] PARSEO EXITOSO ✔")
        print("[IA]:", structured_response.summary)
    except Exception as error:
        print("[DEBUG] ERROR PARSEANDO LA RESPUESTA")
        print("Error parsing response ", error, "Raw Response: - ", response)
