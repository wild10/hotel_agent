import logging
import warnings

# Silenciar logs de httpx y openai
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

# Silenciar advertencia de deprecación de LangGraph
warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*create_react_agent has been moved to.*")

from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
# from langchain.agents import create_agent

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
- Siempre verifica los datos antes de crear una reserva (confirmar habitación y fechas).
- Si el usuario no da fecha, pregunta antes de proceder.
- Después de crear una reserva existosamente, puedes verificarla usando tool_get_reservations si el usuario lo solicita.
- Sé amable y profesional en todo momento.
- Si una herramienta devuelve un error, explícale al usuario qué pasó basándote en el mensaje de error.
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
    
    # agent = create_agent()

    # # simular una conversacion
    # session = "test-session-001"

    # # user_query = "Hola, quiero ver habitaciones disponibles"
    # user_query = "oka hast me una reservar no pidas confirmacion, es este mes: 2026, habitacion 101,mi nombre es: wilderd Mamani my id es 65478323, fecha de check in 15 fecha de checkout 17 de marzo de este mes: 2026"
    # agent_answer = run_agent(agent, user_query, session)

    # print(agent_answer)

    ## create new agent 
    agent = create_agent()
    session = "test-session-002"
    
    while True:
        user_query = input("Usuario: ")
        agent_answer = run_agent(agent, user_query, session)
        print("Agente: ", agent_answer)