# 🧠 Research Agent – LangChain + OpenAI/Anthropic

Este proyecto implementa un **agente de investigación** utilizando LangChain, capaz de responder consultas generando un resumen estructurado en formato JSON.  
El agente también usa herramientas externas como **DuckDuckGo Search** para obtener información actualizada.

---

## 🚀 Características

- Usa **ChatOpenAI** (o **ChatAnthropic**) como modelo LLM.
- Implementa **LangChain Agents** con herramientas externas.
- Respuestas estructuradas mediante **Pydantic** (`ResearchResponse`).
- Búsquedas reales con **DuckDuckGo**.
- Arquitectura modular: `main.py`, `tools.py`, `requirements.txt`.

---



## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone <url>
cd project
```
### 2. Crea un virtual environment
```bash
python -m venv venv
```

Si cierras la terminal o desactivas el environment, se activa con
```bash
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```


## 🔐 Configurar variables de entorno
Crea un archivo .env con:
```bash
OPENAI_API_KEY=tu_api_key
ANTHROPIC_API_KEY=tu_api_key
```

## ▶️ Ejecutar el proyecto 
```bash
python main.py
```

## 💬 Uso
```bash
What can I help you research?: What is the capital of Chile
```

### El agente devuelve la informacion estructurada
```
json
{
  "topic": "Research topic",

  "summary": "Concise summary of findings",

  "sources": ["Source 1", "Source 2", ...],

  "tools_used": ["web_search", ...]
}
```