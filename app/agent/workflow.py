from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from app.agent.tools import hotel_tools
from app.llm import get_llm

# Systems -pŕompt - le dice al agente quién es y cómo comportarse

SYSTEM_PROMPT = """
Eres un asistente virtual del hotel. Ayudas a las huéspedes con:
- Consultar habitaciones disponibles
- Crear reservas
- Realizar check-in y check-out
- Consultar sus reservas existentes
- Responder preguntas sobre servicios, políticas y FAQ del hotel

Reglas:
- Siempre los datos antes de crear una reserva
- Si el usuario no da fecha, pregunta antes de proceder
- Sé amable y profesional en todo momento
- Si no puedes ayudar con algo, dilo claramente
"""

def create_agent():
    ## llmado al llm:openai-gpt-4o-mini.
    llm = get_llm()
    memory = MemorySaver() # memoria conversacional por sesion.

    agent = create_react_agent(
        model=llm,
        tools=hotel_tools,
        checkpointer=memory,
        prompt=SYSTEM_PROMPT
    )

    return agent

def run_agent(agent, user_massage: str, session_id: str='default'):
    """
    Ejecuta el agente con un mensaje del usuario.
    Session_id mantiene memoria separada por conversasion.
    """

    config = {"configurable": {"thread_id": session_id}}

    result = agent.invoke(
        {"messages": [{"role": "user", "content":user_massage}] },
        config=config,
    )

    return result["messages"][-1].content

if __name__ =='__main__':
    
    agent = create_agent()

    # simular una conversacion
    session = "test-session-001"

    # user_query = "Hola, quiero ver habitaciones disponibles"
    user_query = "Cuales son las politicas de cancelacion y si se puede llevar mascotas?"
    agent_answer = run_agent(agent, user_query, session)

    print(agent_answer)