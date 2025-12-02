from flask import Flask, request, jsonify
from main import agent, parser, is_question_allowed

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("question", "")
    if not is_question_allowed(query):
        return jsonify({"answer": "No tengo información sobre ese tema. Solo puedo responder preguntas relacionadas con Anahi."})
    response = agent.invoke({"messages": [{"role": "user", "content": query}]})
    try:
        structured_response = parser.parse(response.get("messages")[-1].content)
        return jsonify({"answer": structured_response.summary})
    except Exception:
        return jsonify({"answer": "Hubo un error procesando la respuesta."})
    

@app.route("/chat", methods=["GET"])
def chat_get():
    return jsonify({"message": "API is running. Use POST method to chat."})
    

if __name__ == "__main__":
    app.run(port=5000, debug=True)